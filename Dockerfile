# Utilise une image Python officielle
FROM python:3.10

# Crée un dossier de travail
WORKDIR /app

# Copie les dépendances et installe-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste des fichiers
COPY . .

# Lance le serveur FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
