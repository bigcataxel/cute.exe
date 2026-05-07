# 🛠️ Project cute.exe | CyberIA Framework

**cute.exe** est un framework de génération automatisée de shellcodes spécialisés dans l’exfiltration de données via des **canaux détournés (Covert Channels)**. En exploitant la puissance d'une IA locale (ARES-v1), le projet transforme des intentions en langage naturel en binaire ASM optimisé, furtif et sans dépendances.

## 🚀 Vision du Projet
L'objectif est de s'affranchir de la standardisation des malwares. En générant du code **NASM x86_64 pur** à la volée, `cute.exe` garantit :
*   **Empreinte minimale** (Pas de libc).
*   **Furtivité accrue** (Contournement des signatures EDR/DLP).
*   **Adaptabilité** (Exfiltration via DNS/ICMP/IP Headers).

---

## 🏗️ Architecture Technique

Le framework repose sur trois piliers fondamentaux conçus pour l'évasion :

### 🧠 Pipeline IA (ARES-v1)
Le script `generate.py` agit comme chef d'orchestre. Il traduit les instructions stratégiques en logique assembleur.
*   **Gestion de la pile (RSP) :** Construction dynamique des structures (ex: `sockaddr_in`).
*   **Zéro-Data Section :** Aucune section `.data` n'est utilisée pour éviter la détection statique.
*   **Null-Byte Avoidance :** Algorithmes de filtrage pour garantir un code compatible avec les injections mémoires (pas de `0x00`).

### 📡 Modules d'Exfiltration (Covert Channels)
| Méthode | Vecteur | Description |
| :--- | :--- | :--- |
| **DNS Tunneling** | Port 53 UDP | Encodage Base64 des data dans les sous-domaines. |
| **Header Crafting** | Raw Sockets | Dissimulation dans les champs `TTL` ou `Fragment ID` de l'en-tête IP. |
| **ICMP Payload** | Ping | Injection de données dans le corps des requêtes echo. |

---

## 👥 L'Équipe & Workflow

Le projet suit un cycle de développement itératif impliquant quatre entités :

1.  **Axel (Architecte) :** Design des prompts et gestion du pipeline.
2.  **Clovis (Fine-Tuner) :** Optimisation du dataset d'entraînement pour réduire les *Segmentation Faults*.
3.  **Michael (Auditeur) :** Validation en environnement sandbox (Docker) et analyse de la reconstruction des données.



---