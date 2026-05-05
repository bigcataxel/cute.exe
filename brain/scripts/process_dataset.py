import json
import os
import re

from generate import generate_payload

# --- CONFIGURATION ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "..", "pipeline", "ares_dataset.jsonl")
)

FILENAME_RE = re.compile(r":\s*([\w\d_-]+)\.c", re.IGNORECASE)


def build_task(instruction: str, c_code: str) -> str:
    """Reformule l'item du dataset en consigne NASM/syscalls anti-GAS."""
    return (
        "Reproduis en NASM x86_64 Linux la logique du code C ci-dessous.\n"
        "Utilise UNIQUEMENT des syscalls. Pas de libc, pas de @PLT, pas de DWORD PTR.\n\n"
        f"Consigne d'origine : {instruction}\n\n"
        "Code C de référence :\n"
        "```c\n"
        f"{c_code}\n"
        "```\n\n"
        "RAPPEL : ignore le style GAS/AT&T que tu as pu voir en entraînement. "
        "Sortie = un seul bloc ```nasm ... ``` avec section .text, global _start, syscall, "
        "et exit (rax=60) en fin."
    )


def process_all() -> None:
    if not os.path.exists(DATASET_PATH):
        print(f"[!] Dataset introuvable : {DATASET_PATH}")
        return

    print(f"[*] Génération de masse depuis {DATASET_PATH}")
    ok = ko = 0

    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"[!] Ligne {i} malformée, sautée.")
                ko += 1
                continue

            instruction = data.get("instruction", "")
            c_code = data.get("input", "")

            m = FILENAME_RE.search(instruction)
            base_name = f"{m.group(1)}.asm" if m else f"payload_{i}.asm"

            task = build_task(instruction, c_code)
            success = generate_payload(task, base_name, retries=2)
            ok += int(success)
            ko += int(not success)

    total = ok + ko
    print(f"\n[=] Génération terminée : {ok}/{total} OK ({ko} rejets)")


if __name__ == "__main__":
    process_all()
