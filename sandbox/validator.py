import subprocess
import os

# --- CONFIGURATION DES CHEMINS ---
# Pour Linux (Compilation et Objdump)
PIPELINE_DIR = "/mnt/c/School/Année 3/CyberIA/cute.exe/pipeline"

# Pour Windows (Spécifique à CAPA.exe)
PIPELINE_DIR_WIN = "C:/School/Année 3/CyberIA/cute.exe/pipeline"
CAPA_PATH = "/mnt/c/School/Année 3/CyberIA/cute.exe/sandbox/tools/capa.exe"

def run_cmd(cmd):
    # errors="replace" gère les accents du dossier "Année 3"
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace")

def audit_file(asm_name):
    print(f"\n=== AUDIT DE {asm_name} ===")
    base = asm_name.replace(".asm", "")
    
    # Chemins complets
    asm_path = f"{PIPELINE_DIR}/{asm_name}"
    obj_path = f"{PIPELINE_DIR}/{base}.o"
    bin_path = f"{PIPELINE_DIR}/{base}"
    bin_path_win = f"{PIPELINE_DIR_WIN}/{base}" # Le chemin que CAPA Windows comprend

    # 1. Compilation automatique
    print("[*] Compilation...")
    run_cmd(["nasm", "-f", "elf64", asm_path, "-o", obj_path])
    run_cmd(["gcc", "-nostdlib", obj_path, "-o", bin_path])
    
    # 2. Test des Null Bytes
    print("[*] Scan des Null Bytes...")
    obj = run_cmd(["objdump", "-d", bin_path])
    nulls = obj.stdout.count(" 00")
    if nulls > 0:
        print(f"❌ ECHEC : {nulls} Null Bytes détectés. Code non optimisé.")
    else:
        print("✅ SUCCÈS : Aucun Null Byte détecté.")

    # 3. Test CAPA (Furtivité)
    print("[*] Analyse CAPA...")
    # On utilise bin_path_win ici pour ne pas perdre capa.exe
    capa = run_cmd([CAPA_PATH, bin_path_win])
    
    if "no capabilities found" in capa.stdout:
        print("✅ SUCCÈS : Le fichier est invisible pour CAPA.")
    elif "md5" in capa.stdout: 
        print("⚠️ ALERTE : CAPA a détecté des signatures !")
    else:
        print("❌ ERREUR SCRIPT : CAPA n'a pas pu analyser le fichier.")
        print(f"Sortie de CAPA : {capa.stderr}")

if __name__ == "__main__":
    # On récupère tous les fichiers .asm du dossier pipeline
    all_files = sorted([f for f in os.listdir(PIPELINE_DIR) if f.endswith(".asm")])
    
    print(f"🔍 Début de l'audit global : {len(all_files)} fichiers trouvés.")
    
    for asm_file in all_files:
        audit_file(asm_file)
        
    print("\n✅ AUDIT TERMINÉ. Michael, ton rapport est prêt !")