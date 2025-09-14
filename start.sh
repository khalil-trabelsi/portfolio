#!/bin/bash

# Créer le dossier instance s'il n'existe pas
mkdir -p instance

# Initialiser la base de données si nécessaire
echo "Initialisation de la base de données..."

# Vérifier si les migrations existent
if [ ! -d "migrations" ]; then
    echo "Dossier migrations non trouvé, initialisation..."
    flask db init
fi

# Créer une migration si aucune n'existe
if [ ! "$(ls -A migrations/versions 2>/dev/null)" ]; then
    echo "Aucune migration trouvée, création d'une migration initiale..."
    flask db migrate -m "Initial migration"
fi

# Appliquer les migrations
echo "Application des migrations..."
flask db upgrade

# Vérifier le succès de la migration
if [ $? -ne 0 ]; then
    echo "Erreur lors de l'application des migrations"
    exit 1
fi

echo "Base de données initialisée avec succès"

# Démarrer l'application
echo "Démarrage de l'application..."
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120