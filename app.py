import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Ler a chave da API do Google Gemini a partir de uma variável de ambiente
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

if GOOGLE_GEMINI_API_KEY is None:
    st.error("A chave da API do Google Gemini não está configurada. Defina a variável de ambiente 'GOOGLE_GEMINI_API_KEY'.")
else:
    genai.configure(api_key=GOOGLE_GEMINI_API_KEY)

    # Nome do modelo Gemini 1.5 Pro
    MODEL_NAME = "gemini-1.5-pro-latest"

    # Inicialização do modelo Gemini 1.5 Pro
    model = genai.GenerativeModel(MODEL_NAME)

    # Função para resumir texto com prompt específico
    def summarize_text(text):
        prompt = "Apenas resume isto, sem acrescentar novas informações.\n\n" + text
        response = model.generate_content(prompt)
        return response.text

    # Interface Streamlit para interação
    st.title("Aplicação de Resumo de Texto com Google Gemini")

    # Campo de entrada para o texto do usuário
    input_text = st.text_area("Digite o texto que deseja resumir:", height=200)

    # Botão para gerar resumo
    if st.button("Gerar Resumo"):
        if input_text:
            summary = summarize_text(input_text)
            st.subheader("Resumo Gerado:")
            st.write(summary)
        else:
            st.warning("Por favor, insira um texto para gerar o resumo.")
