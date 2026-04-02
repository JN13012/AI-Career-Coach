import os
import gradio as gr
from dotenv import load_dotenv
from pypdf import PdfReader
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters

# Config
load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"), 
    api_key=os.getenv("WATSONX_APIKEY")
)
project_id = os.getenv("WATSONX_PROJECT_ID")

model = ModelInference(
    model_id="meta-llama/llama-3-2-11b-vision-instruct",
    credentials=credentials,
    project_id=project_id,
    params=TextChatParameters(temperature=0.7, max_tokens=1024)
)

# PDF Extraction
def extract_text_from_pdf(file):
    if file is None:
        return ""
    try:
        reader = PdfReader(file.name)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        return f"Erreur de lecture PDF : {e}"

# Send prompt
def ask_llm(prompt):
    messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
    response = model.chat(messages=messages)
    return response['choices'][0]['message']['content']

# Prompt Opti CV
def polish_resume(job, resume):
    if not job or not resume: return "Erreur : Poste et CV requis."
    prompt = f"Expert RH : Améliore ce CV pour le poste de '{job}'. CV : {resume}"
    return ask_llm(prompt)

# Prompt Lettre
def generate_cover_letter(company, job, resume):
    if not company or not job or not resume: return "Erreur : Champs manquants."
    prompt = f"Rédige une lettre de motivation pour '{company}' (Poste: '{job}') basée sur : {resume}"
    return ask_llm(prompt)

# Prompt Conseils
def get_career_advice(job, resume):
    if not job or not resume: return "Erreur : Poste et CV requis."
    prompt = f"Analyse ce CV pour le poste de '{job}'. Donne 3 conseils d'amélioration. CV : {resume}"
    return ask_llm(prompt)

# UI Gradio
with gr.Blocks(theme=gr.themes.Soft(), title="AI Career Coach") as demo:
    gr.Markdown("# 🎓 AI Career Coach Professional")
    
    with gr.Tabs():
        # Optimiseur de CV
        with gr.TabItem("📄 Optimiseur de CV"):
            with gr.Row():
                with gr.Column(scale=1):
                    job_input1 = gr.Textbox(label="Poste visé", placeholder="Ex: Développeur Fullstack")
                    file_input1 = gr.File(label="Upload CV (PDF)", file_types=[".pdf"])
                    resume_input1 = gr.Textbox(label="Texte extrait", lines=18, max_lines=20)
                    btn_polish = gr.Button("🚀 Optimiser", variant="primary")
                with gr.Column(scale=1):
                    output_polish = gr.Textbox(label="Résultat", lines=28, max_lines=35)
            
            file_input1.change(extract_text_from_pdf, inputs=[file_input1], outputs=[resume_input1])
            btn_polish.click(polish_resume, [job_input1, resume_input1], output_polish)

        # Lettre
        with gr.TabItem("✉️ Lettre de Motivation"):
            with gr.Row():
                with gr.Column(scale=1):
                    comp_input = gr.Textbox(label="Entreprise")
                    job_input2 = gr.Textbox(label="Poste")
                    file_input2 = gr.File(label="Upload CV (PDF)", file_types=[".pdf"])
                    resume_input2 = gr.Textbox(label="Texte extrait", lines=15, max_lines=18)
                    btn_letter = gr.Button("📝 Générer la lettre", variant="primary")
                with gr.Column(scale=1):
                    output_letter = gr.Textbox(label="Lettre générée", lines=28, max_lines=35)
            
            file_input2.change(extract_text_from_pdf, inputs=[file_input2], outputs=[resume_input2])
            btn_letter.click(generate_cover_letter, [comp_input, job_input2, resume_input2], output_letter)

        # Conseils
        with gr.TabItem("💡 Conseils Carrière"):
            with gr.Row():
                with gr.Column(scale=1):
                    job_input3 = gr.Textbox(label="Poste cible")
                    file_input3 = gr.File(label="Upload CV (PDF)", file_types=[".pdf"])
                    resume_input3 = gr.Textbox(label="Texte extrait", lines=18, max_lines=20)
                    btn_advice = gr.Button("🧠 Analyser", variant="primary")
                with gr.Column(scale=1):
                    output_advice = gr.Textbox(label="Analyse & Conseils", lines=28, max_lines=35)
            
            file_input3.change(extract_text_from_pdf, inputs=[file_input3], outputs=[resume_input3])
            btn_advice.click(get_career_advice, [job_input3, resume_input3], output_advice)

if __name__ == "__main__":
    demo.launch()