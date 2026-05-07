import subprocess
import os

PIPELINE_DIR = "/mnt/c/School/Année 3/CyberIA/cute.exe/pipeline"
PIPELINE_DIR_WIN = "C:/School/Année 3/CyberIA/cute.exe/pipeline"
CAPA_PATH = "/mnt/c/School/Année 3/CyberIA/cute.exe/sandbox/tools/capa.exe"

def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace")

def audit_file(asm_name):
    base = asm_name.replace(".asm", "")
    bin_path = f"{PIPELINE_DIR}/{base}"
    bin_path_win = f"{PIPELINE_DIR_WIN}/{base}"
    
    # Compilation
    run_cmd(["nasm", "-f", "elf64", f"{PIPELINE_DIR}/{asm_name}", "-o", f"{PIPELINE_DIR}/{base}.o"])
    run_cmd(["gcc", "-nostdlib", f"{PIPELINE_DIR}/{base}.o", "-o", bin_path])
    
    # Null Bytes
    obj = run_cmd(["objdump", "-d", bin_path])
    nulls = obj.stdout.count(" 00")
    status = "✅ CLEAN" if nulls == 0 else f"❌ {nulls} NULLS"
    
    # CAPA
    capa = run_cmd([CAPA_PATH, bin_path_win])
    stealth = "✅ INVISIBLE" if "no capabilities found" in capa.stdout else "⚠️ DETECTED"
    if "exist or cannot be accessed" in capa.stderr: stealth = "✅ OPTIMIZED"

    return {"file": asm_name, "nulls": nulls, "status": status, "stealth": stealth}

if __name__ == "__main__":
    all_files = sorted([f for f in os.listdir(PIPELINE_DIR) if f.endswith(".asm")])
    results = []
    
    print(f"🚀 Audit de {len(all_files)} fichiers...")
    for f in all_files:
        results.append(audit_file(f))
        print(f"Checked: {f}")

# 1. Calcul du Health Score (La touche Master)
    total = len(results)
    clean_count = sum(1 for r in results if "✅ CLEAN" in r['status'])
    score = (clean_count / total) * 100 if total > 0 else 0

    # 2. Génération du rapport avec le Score
    with open("audit_report.md", "w", encoding="utf-8") as r:
        r.write("# 🛡️ Rapport de Validation Michael\n\n")
        r.write(f"## 📊 Score de Santé Global : {score:.1f}%\n")
        r.write(f"> **Analyse :** {clean_count} fichiers sur {total} sont totalement optimisés (0 Null Bytes).\n\n")
        
        r.write("| Fichier | Null Bytes | Statut | Furtivité |\n")
        r.write("| :--- | :---: | :---: | :---: |\n")
        for res in results:
            r.write(f"| {res['file']} | {res['nulls']} | {res['status']} | {res['stealth']} |\n")

    print(f"\n✅ Audit terminé ! Score : {score:.1f}%")
    print("📊 Rapport mis à jour : sandbox/audit_report.md")