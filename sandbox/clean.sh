#!/bin/bash
# Script de nettoyage Michael
rm -f ../pipeline/*.o
find ../pipeline/ -type f ! -name "*.*" -delete
echo "✅ Nettoyage terminé : Les binaires et artefacts ont été supprimés."
