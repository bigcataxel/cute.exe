# cute.exe

Projet **CyberIA — A3 Semestre 2**.

Générateur automatisé de payloads **NASM x86_64 Linux** dont le rôle est de transmettre des données vers un **serveur de sauvegarde secondaire** quand les canaux classiques (HTTP, FTP, TCP direct) ne sont pas disponibles ou pas fiables. La transmission se fait en **canaux détournés** : découpage et envoi des données sous forme de **requêtes DNS** ou de **paquets IP fragmentés**, directement implémentés en assembleur via syscalls Linux purs (p