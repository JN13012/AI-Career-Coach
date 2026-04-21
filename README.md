🎓 AI Career Coach
Un assistant intelligent pour booster votre recherche d'emploi, propulsé par Llama 3.2 sur IBM Watsonx.ai.

🚀 Fonctionnalités
Optimiseur de CV : Adapte votre expérience au poste visé.

Générateur de Lettre : Rédige une lettre de motivation personnalisée.

Conseils Carrière : Analyse les manques de compétences par rapport à une fiche de poste.

Lecture PDF : Extraction automatique du texte de votre CV.

🛠️ Stack Technique
Frontend : Gradio (Interface Web Python)

IA : Meta Llama 3.2 via IBM Watsonx.ai

Parsing : pypdf pour le traitement des documents.

📦 Installation

Cloner le projet
git clone https://github.com/JN13012/AI-Career-Coach
cd AI-Career-Coach

Installer les dépendances
pip install -r requirements.txt

Configuration
Créez un fichier .env à la racine avec vos accès IBM Cloud :
WATSONX_URL="your_url"
WATSONX_APIKEY="your_apikey"
WATSONX_PROJECT_ID="your_project_id"

Lancer l'application

python app.py

* Running on local URL:  http://127.0.0.1:7860