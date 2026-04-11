import subprocess
import os

# --- CONFIGURATION ---
OLLAMA_PATH = r"C:\Users\User\AppData\Local\Programs\Ollama\ollama.exe" 
MODEL_NAME = "ares-v1"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "pipeline"))
# ---------------------

def generate_payload(prompt, output_filename):
    if not os.path.exists(PIPELINE_DIR):
        os.makedirs(PIPELINE_DIR)
        
    print(f"[*] ARES-LLM ({MODEL_NAME}) génère : {output_filename}...")
    
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", MODEL_NAME, prompt],
            capture_output=True,
            text=True,
            encoding='latin-1',
            errors='ignore',
            shell=False
        )
        
        if result.returncode == 0:
            raw_text = result.stdout
            
            # --- EXTRACTION DU CODE ---
            if "```" in raw_text:
                parts = raw_text.split("```")
                final_code = parts[1]
                
                lines = final_code.splitlines()
                if lines and lines[0].strip().lower() in ['nasm', 'assembly', 'asm']:
                    final_code = "\n".join(lines[1:])
            else:
                final_code = raw_text

            # --- SAUVEGARDE ---
            full_path = os.path.join(PIPELINE_DIR, output_filename)
            with open(full_path, "w", encoding='utf-8') as f:
                f.write(final_code.strip())
            
            print(f"[+] Succès ! Code ASM extrait dans : {full_path}")
        else:
            print(f"[!] Erreur Ollama : {result.stderr}")
            
    except Exception as e:
        print(f"[!] Erreur système : {e}")

if __name__ == "__main__":
    file_name = input("Nom du payload (sans extension) : ")
    prompt_instruct = (
        "Donne-moi UNIQUEMENT le code source NASM x86_64 pour afficher 'Connected' "
        "avec des syscalls. Utilise un bloc de code Markdown."
    )
    generate_payload(prompt_instruct, f"{file_name}.asm")