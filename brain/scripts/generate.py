import argparse
import os
import re
import subprocess
import sys

# Force UTF-8 sur stdout/stderr (sinon crash sur '→', 'é', etc. en console Windows cp1252).
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

# --- CONFIGURATION ---
OLLAMA_PATH = r"C:\Users\User\AppData\Local\Programs\Ollama\ollama.exe"
MODEL_NAME = "ares-v1"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "pipeline"))

# --- VALIDATION ---
REQUIRED_TOKENS = ["section .text", "global _start", "syscall"]
FORBIDDEN_TOKENS = [
    "@PLT", "@plt",
    "endbr64",
    "DWORD PTR", "QWORD PTR", "BYTE PTR",
    ".LC0", ".cfi_",
    "call printf", "call scanf", "call write", "call mmap",
    "call malloc", "call strlen", "call puts",
]

CODEBLOCK_RE = re.compile(
    r"```(?:nasm|asm|assembly|x86|x86_64)?\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)


def extract_code(raw_text: str) -> str:
    """Extrait le premier bloc markdown si présent, sinon retourne le texte brut nettoyé."""
    m = CODEBLOCK_RE.search(raw_text)
    if m:
        return m.group(1).strip()
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.lstrip("`").lstrip()
    return cleaned


def validate(code: str) -> list[str]:
    """Retourne la liste des problèmes détectés. Liste vide = code OK."""
    issues = []
    for tok in REQUIRED_TOKENS:
        if tok not in code:
            issues.append(f"manquant: '{tok}'")
    for tok in FORBIDDEN_TOKENS:
        if tok in code:
            issues.append(f"interdit présent: '{tok}'")
    return issues


def call_ollama(prompt: str) -> str:
    result = subprocess.run(
        [OLLAMA_PATH, "run", MODEL_NAME, prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Ollama exit {result.returncode}: {result.stderr}")
    return result.stdout


def build_prompt(task: str, prior_error: str | None = None) -> str:
    parts = [
        "Génère un payload NASM x86_64 Linux qui réalise la tâche suivante.",
        "Réponds UNIQUEMENT avec un bloc ```nasm ... ``` puis stop.",
        "",
        f"Tâche : {task}",
    ]
    if prior_error:
        parts += [
            "",
            "Ta tentative précédente était invalide pour ces raisons :",
            prior_error,
            "Corrige et regénère.",
        ]
    return "\n".join(parts)


def generate_payload(task: str, output_filename: str, retries: int = 2) -> bool:
    os.makedirs(PIPELINE_DIR, exist_ok=True)

    last_issues: list[str] = []
    last_code = ""

    for attempt in range(retries + 1):
        prior = "\n".join(f"- {i}" for i in last_issues) if last_issues else None
        prompt = build_prompt(task, prior)

        print(f"[*] ARES-LLM ({MODEL_NAME}) tentative {attempt + 1}/{retries + 1} : {output_filename}")
        try:
            raw = call_ollama(prompt)
        except Exception as e:
            print(f"[!] Erreur appel Ollama : {e}")
            return False

        code = extract_code(raw)
        last_code = code
        last_issues = validate(code)

        if not last_issues:
            full_path = os.path.join(PIPELINE_DIR, output_filename)
            with open(full_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(code + "\n")
            print(f"[+] OK → {full_path}")
            return True

        print(f"[~] Validation KO ({len(last_issues)} problème(s)) :")
        for issue in last_issues:
            print(f"    - {issue}")

    # Toutes les tentatives ont échoué : on sauvegarde quand même en .reject
    reject_path = os.path.join(PIPELINE_DIR, output_filename + ".reject")
    with open(reject_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(last_code + "\n")
    print(f"[!] Échec après {retries + 1} tentatives, code rejeté → {reject_path}")
    return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Génération de payload NASM via ARES-LLM")
    parser.add_argument("--task", help="Description de la tâche à réaliser")
    parser.add_argument("--name", help="Nom du fichier de sortie (sans extension)")
    parser.add_argument("--retries", type=int, default=2, help="Nombre de retry sur validation KO")
    args = parser.parse_args(argv)

    task = args.task or input("Tâche à générer : ").strip()
    name = args.name or input("Nom du payload (sans extension) : ").strip()

    if not task or not name:
        print("[!] Tâche et nom requis.")
        return 2

    ok = generate_payload(task, f"{name}.asm", retries=args.retries)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
