#!/usr/bin/env python3
"""
generator_v2.py - Shellcode PIC Generator
"""

import argparse, json, os, re, subprocess, sys, tempfile, shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

try:
    import yaml
except ImportError:
    print("[!] Missing: pip3 install pyyaml")
    sys.exit(1)

from templates_v2 import get_template, list_templates

SCRIPT_DIR = Path(__file__).parent
CATEGORIES_FILE = SCRIPT_DIR / "categories_v2.yaml"
PIPELINE_DIR = SCRIPT_DIR.parent.parent / "pipeline"

NASM_PATH = shutil.which("nasm")
OBJCOPY_PATH = shutil.which("objcopy")

if not NASM_PATH:
    print("[!] nasm not found")
    sys.exit(1)

def load_categories() -> Dict:
    if not CATEGORIES_FILE.exists():
        print(f"[!] {CATEGORIES_FILE} not found")
        sys.exit(1)
    with open(CATEGORIES_FILE) as f:
        return yaml.safe_load(f)

CATEGORIES = load_categories()

def log_info(msg: str):
    print(f"[*] {msg}")

def log_ok(msg: str):
    print(f"[+] {msg}")

def log_error(msg: str):
    print(f"[!] {msg}")

def log_warning(msg: str):
    print(f"[~] {msg}")

def tokenize_asm(code: str) -> List[str]:
    tokens = []
    for line in code.split("\n"):
        if ";" in line:
            line = line.split(";")[0]
        line = re.sub(r'"[^"]*"', '', line)
        parts = line.split()
        for part in parts:
            part = part.rstrip(':').strip()
            if part:
                tokens.append(part)
    return tokens

def validate_tokens(code: str, category: str) -> List[str]:
    issues = []
    config = CATEGORIES.get(category, {})
    tokens = tokenize_asm(code)
    tokens_str = " ".join(tokens).lower()
    
    forbidden = config.get("forbidden_tokens", [])
    for tok in forbidden:
        if re.search(rf'\b{re.escape(tok.lower())}\b', tokens_str):
            issues.append(f"forbidden token present: '{tok}'")
    
    return issues

def assemble_nasm(code: str, output_dir: Path) -> Tuple[bool, Optional[str], Optional[bytes]]:
    try:
        asm_file = output_dir / "temp.asm"
        obj_file = output_dir / "temp.o"
        bin_file = output_dir / "temp.bin"
        
        asm_file.write_text(code, encoding="utf-8")
        
        result = subprocess.run(
            [NASM_PATH, "-f", "elf64", "-o", str(obj_file), str(asm_file)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            error = result.stderr or "Unknown NASM error"
            return False, error, None
        
        if OBJCOPY_PATH:
            subprocess.run([OBJCOPY_PATH, "-O", "binary", str(obj_file), str(bin_file)], 
                          capture_output=True, timeout=10)
            if bin_file.exists():
                return True, None, bin_file.read_bytes()
        
        if obj_file.exists():
            return True, None, obj_file.read_bytes()
        
        return False, "Failed to extract binary", None
        
    except subprocess.TimeoutExpired:
        return False, "NASM timeout", None
    except Exception as e:
        return False, str(e), None
    finally:
        for f in [asm_file, obj_file, bin_file]:
            if f and f.exists():
                try:
                    f.unlink()
                except:
                    pass

def scan_null_bytes(binary: bytes) -> Tuple[bool, Optional[str]]:
    null_positions = [i for i, byte in enumerate(binary) if byte == 0x00]
    if null_positions:
        reported = null_positions[:5]
        positions_str = ", ".join(f"0x{pos:02x}" for pos in reported)
        error = f"Null bytes at: {positions_str}"
        if len(null_positions) > 5:
            error += f" (... +{len(null_positions) - 5} more)"
        return False, error
    return True, None

def validate_asm(code: str, category: str) -> Tuple[bool, List[str]]:
    issues = []
    tmpdir = Path(tempfile.mkdtemp())
    
    try:
        token_issues = validate_tokens(code, category)
        issues.extend(token_issues)
        
        if issues:
            return False, issues
        
        success, error, binary = assemble_nasm(code, tmpdir)
        if not success:
            issues.append(f"NASM: {error}")
            return False, issues
        
        config = CATEGORIES.get(category, {})
        if config.get("null_byte_free", False):
            clean, error = scan_null_bytes(binary)
            if not clean:
                issues.append(f"Null-bytes: {error}")
                return False, issues
        
        return True, []
        
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

def assemble_from_template(template_type: str) -> Optional[str]:
    """Assemble shellcode from template."""
    template = get_template(template_type)
    if not template:
        log_error(f"Template '{template_type}' not found")
        return None
    return template

def generate_payload(category: str, output_filename: str) -> bool:
    """V2 Pipeline: Template → Assemble → Validate."""
    PIPELINE_DIR.mkdir(parents=True, exist_ok=True)
    
    if category not in CATEGORIES or category == "syscall_reference":
        log_error(f"Invalid category: {category}")
        return False
    
    log_info(f"Generating shellcode for: {category}")
    
    # Assemble from template
    code = assemble_from_template(category)
    if not code:
        log_error("Failed to assemble template")
        return False
    
    # Validate
    valid, issues = validate_asm(code, category)
    
    if valid:
        output_path = PIPELINE_DIR / output_filename
        output_path.write_text(code, encoding="utf-8")
        log_ok(f"Generated → {output_path}")
        return True
    
    log_warning(f"Validation failed ({len(issues)} issues):")
    for issue in issues:
        log_warning(f"  - {issue}")
    
    reject_path = PIPELINE_DIR / (output_filename + ".reject")
    reject_path.write_text(code, encoding="utf-8")
    log_error(f"Validation failed")
    return False

def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="cute.exe V2 - Shellcode Generator")
    parser.add_argument("--type", choices=[c for c in CATEGORIES.keys() if c != "syscall_reference"], 
                        help="Shellcode type (required)")
    parser.add_argument("--name", help="Output filename (no .asm)")
    parser.add_argument("--list-types", action="store_true", help="List categories")
    parser.add_argument("--list-templates", action="store_true", help="List templates")
    
    args = parser.parse_args(argv)
    
    if args.list_types:
        print("V2 Shellcode Categories:")
        for cat in CATEGORIES.keys():
            if cat != "syscall_reference":
                desc = CATEGORIES[cat].get("description", "N/A")
                fmt = CATEGORIES[cat].get("format", "N/A")
                print(f"  {cat} [{fmt}]: {desc}")
        return 0
    
    if args.list_templates:
        print("Shellcode Templates:")
        for tpl in list_templates():
            print(f"  {tpl}")
        return 0
    
    category = args.type
    name = args.name or input("Filename (no .asm): ").strip()
    
    if not all([category, name]):
        log_error("Type and filename are required")
        return 2
    
    ok = generate_payload(category, f"{name}.asm")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
