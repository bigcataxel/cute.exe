import os
import subprocess
import re

def clean_asm():
    if not os.path.exists("clean_asm"):
        os.makedirs("clean_asm")
    
    c_files = [f for f in os.listdir("raw_c") if f.endswith(".c")]
    
    for f in c_files:
        input_path = f"raw_c/{f}"
        output_path = f"clean_asm/{f.replace('.c', '.s')}"
        
        # Commande GCC pour générer l'assembleur pur (Syntaxe Intel, pas de protections)
        cmd = f"gcc -S -masm=intel -fno-asynchronous-unwind-tables -fno-stack-protector {input_path} -o {output_path}"
        subprocess.run(cmd, shell=True)
        
        # Nettoyage des directives de debug (.file, .ident, etc.)
        if os.path.exists(output_path):
            with open(output_path, "r") as asm_f:
                lines = asm_f.readlines()
            
            clean_lines = []
            for line in lines:
                # On ignore les lignes qui commencent par un point (directives) 
                # SAUF les labels de fonctions et de sauts (.L)
                if line.strip().startswith(".") and not line.strip().startswith(".L") and "intel_syntax" not in line:
                    continue
                if "endbr64" in line: # On vire la protection Intel CET
                    continue
                clean_lines.append(line)
            
            with open(output_path, "w") as asm_f:
                asm_f.writelines(clean_lines)
            print(f"✔ Nettoyé : {f}")

if __name__ == "__main__":
    clean_asm()