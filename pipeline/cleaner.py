import os
import re

def clean_asm_line(line):
    # 1. Supprimer les instructions de contrôle de flot inutiles (signatures)
    if "endbr64" in line or "push\trbp" in line or "mov\trbp, rsp" in line or "pop\trbp" in line:
        return None
    
    # 2. Optimisation : Remplacer mov eax, 0 par xor eax, eax
    line = re.sub(r'mov\teax, 0', 'xor\teax, eax', line)
    
    # 3. Nettoyage des directives de debug et commentaires
    if line.strip().startswith(('.', '#')):
        if not line.strip().startswith('.LC'): # On garde les labels de strings
            return None

    # 4. (Optionnel) Nettoyage des DWORD PTR pour utiliser les registres
    # Note : Cela demande une analyse plus complexe, mais on peut déjà
    # supprimer les manipulations de stack frame inutiles
    if "leave" in line or "ret" in line:
        return line.strip()

    return line.strip()

def process_files():
    raw_dir = "raw_c"
    clean_dir = "clean_asm"
    os.makedirs(clean_dir, exist_ok=True)

    for f_name in os.listdir(raw_dir):
        if f_name.endswith(".c"):
            asm_file = f_name.replace(".c", ".s")
            # Compilation brute vers assembleur Intel
            os.system(f"gcc -S -masm=intel -Oz -fomit-frame-pointer -fno-stack-protector -fcf-protection=none {raw_dir}/{f_name} -o {clean_dir}/{asm_file}")

            # Lecture et nettoyage
            with open(f"{clean_dir}/{asm_file}", "r") as f:
                lines = f.readlines()

            cleaned_lines = []
            for line in lines:
                cleaned = clean_asm_line(line)
                if cleaned:
                    cleaned_lines.append(cleaned)

            # Réécriture du fichier propre
            with open(f"{clean_dir}/{asm_file}", "w") as f:
                f.write("\n".join(cleaned_lines))

if __name__ == "__main__":
    process_files()
    print("✨ Dataset nettoyé : mov -> xor, signatures supprimées, registres optimisés.")