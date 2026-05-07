import os
import json

def generate_jsonl():
    dataset = []
    c_dir = "raw_c"
    asm_dir = "clean_asm"
    output_file = "ares_dataset.jsonl"

    # On liste les fichiers C
    if not os.path.exists(c_dir):
        print(f"❌ Erreur : Le dossier {c_dir} n'existe pas.")
        return

    c_files = [f for f in os.listdir(c_dir) if f.endswith(".c")]

    for f_name in c_files:
        asm_name = f_name.replace(".c", ".s")
        c_path = os.path.join(c_dir, f_name)
        asm_path = os.path.join(asm_dir, asm_name)

        # On vérifie si on a bien la paire (C et Assembleur)
        if os.path.exists(asm_path):
            with open(c_path, "r") as f_c:
                c_code = f_c.read()
            with open(asm_path, "r") as f_asm:
                asm_code = f_asm.read()

            # Structure du JSONL pour l'entraînement (Instruction / Input / Output)
            entry = {
                "instruction": f"Translate this C function into clean x86_64 shellcode-ready assembly: {f_name}",
                "input": c_code.strip(),
                "output": asm_code.strip()
            }
            dataset.append(entry)

    # Écriture du fichier final
    with open(output_file, "w") as f_out:
        for entry in dataset:
            f_out.write(json.dumps(entry) + "\n")

    print(f"✨ Succès ! {len(dataset)} paires C/ASM ont été packagées dans {output_file}")

if __name__ == "__main__":
    generate_jsonl()