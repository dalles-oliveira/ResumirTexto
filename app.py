import streamlit as st
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import nltk
from collections import Counter
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import fitz  # PyMuPDF para processamento de PDF
import docx  # python-docx para processamento de documentos Word
import requests

# Baixar recursos necessários do NLTK
nltk.download('stopwords')

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Interface Streamlit para interação
st.title("Análise de Texto e uso do Google GEMINI para resumi-lo")

# Ler a chave da API do Google Gemini a partir de uma variável de ambiente
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")

if GOOGLE_GEMINI_API_KEY is None:
    st.error("A chave da API do Google Gemini não está configurada. Defina a variável de ambiente 'GOOGLE_GEMINI_API_KEY'.")
else:
    # Configurar API do Google Gemini
    st.write("API do Google Gemini configurada.")

    # Nome do modelo Gemini 1.5 Pro
    MODEL_NAME = "gemini-1.5-pro-latest"

    # Inicialização do modelo Gemini 1.5 Pro
    st.write(f"Inicializando modelo {MODEL_NAME}...")

    # Simulação de modelo para exemplo
    class GenerativeModel:
        def generate_content(self, prompt):
            return f"Resumo do texto: {prompt}"

    model = GenerativeModel()

    # Função para resumir texto com prompt específico
    def summarize_text(text):
        prompt = "Apenas resume isto, sem acrescentar novas informações.\n\n" + text
        response = model.generate_content(prompt)
        return response

    # Função para extrair texto de um arquivo PDF usando PyMuPDF (fitz)
    def extract_text_from_pdf(uploaded_file):
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
        return text

    # Função para extrair texto de um arquivo Word usando python-docx
    def extract_text_from_word(uploaded_file):
        doc = docx.Document(uploaded_file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    # Função para extrair texto de uma URL usando requests e BeautifulSoup
    def extract_text_from_url(url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            paragraphs = soup.find_all('p')
            text = '\n'.join([paragraph.get_text() for paragraph in paragraphs])
            return text
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao acessar a URL: {e}")
            return ""

    # Função para criar nuvem de palavras
    def create_wordcloud(text):
        stop_words = set(stopwords.words('portuguese'))
        words = [word for word in text.split() if word.lower() not in stop_words and word.isalpha()]
        word_freq = Counter(words)
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)

    # Função para exibir as top 20 palavras mais frequentes
    def display_top_20_words(text):
        stop_words = set(stopwords.words('portuguese'))
        words = [word for word in text.split() if word.lower() not in stop_words and word.isalpha()]
        word_freq = Counter(words)
        top_20 = word_freq.most_common(20)
        result = ""
        for word, freq in top_20:
            result += f"{word}: {freq}\n"
        return result

    # Opção de entrada do texto
    input_option = st.selectbox("Escolha uma opção para enviar o texto:", ("Digite ou cole o texto", "Upload de PDF", "Upload de Word", "URL de uma página web"))

    input_text = ""

    if input_option == "Digite ou cole o texto":
        input_text = st.text_area("Digite ou cole o texto aqui:", height=200)
    elif input_option == "Upload de PDF":
        uploaded_file = st.file_uploader("Envie o arquivo PDF", type="pdf")
        if uploaded_file is not None:
            input_text = extract_text_from_pdf(uploaded_file)
    elif input_option == "Upload de Word":
        uploaded_file = st.file_uploader("Envie o arquivo Word", type="docx")
        if uploaded_file is not None:
            input_text = extract_text_from_word(uploaded_file)
    elif input_option == "URL de uma página web":
        url = st.text_input("Digite a URL da página web:")
        if url:
            input_text = extract_text_from_url(url)

    # Botão ENVIAR
    if st.button("ENVIAR"):
        if not input_text:
            st.warning("Por favor, insira ou envie um texto para análise.")
        else:
            # Exibir Resumo
            with st.spinner("Gerando Resumo..."):
                summary = summarize_text(input_text)
            st.write("Resumo Gerado:")
            st.write(summary)

            # Criar Nuvem de Palavras
            with st.spinner("Gerando Nuvem de Palavras..."):
                st.subheader("Nuvem de Palavras:")
                create_wordcloud(input_text)

            # Exibir Top 20 Palavras Mais Frequentes
            with st.spinner("Gerando Top 20 Palavras Mais Frequentes..."):
                st.subheader("Top 20 Palavras Mais Frequentes:")
                top_20_words = display_top_20_words(input_text)
                st.text_area("Top 20 Palavras Mais Frequentes:", value=top_20_words, height=300)
