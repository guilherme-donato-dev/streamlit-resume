# app.py

import streamlit as st
import requests

# --- Configuração da Página ---
# Define o título que aparece na aba do navegador e um ícone
st.set_page_config(page_title="Resumidor de Artigos", page_icon="✂️")

# --- Título Principal ---
st.title("✂️ Resumidor de Artigos com IA")
st.write("Cole a URL de um artigo ou notícia abaixo e clique em 'Resumir' para obter um resumo feito por IA.")

# --- URL da nossa API Django ---
# Este é o "telefone" que o Streamlit vai usar para "ligar" para o seu back-end.
# IMPORTANTE: A API Django DEVE estar rodando para isso funcionar.
API_URL = "https://api-resume-znyg.onrender.com/api/summarize/"

# --- Interface do Usuário ---

# 1. Cria um campo de texto para o usuário colar a URL
url = st.text_input(
    "Cole a URL aqui:", 
    placeholder="https://leagueoflegends.com.br/lol/news/..."
)

# 2. Cria um botão "Resumir"
if st.button("Resumir"):
    # 3. Lógica que roda QUANDO o botão é clicado
    
    # Validação simples
    if not url or not (url.startswith("http://") or url.startswith("https://")):
        st.error("Por favor, insira uma URL válida (começando com http:// ou https://)")
    else:
        # Mostra um "spinner" de loading enquanto a API trabalha
        with st.spinner("Lendo o artigo, resumindo com IA... Isso pode levar alguns segundos..."):
            try:
                # 4. A "Ligação": Chama a API Django
                #    Envia o JSON {"url": url}
                payload = {"url": url}
                response = requests.post(API_URL, json=payload, timeout=30) # Timeout de 30s

                # 5. Verifica a resposta da API
                if response.status_code == 200:
                    # Sucesso! Pega o JSON da resposta
                    data = response.json()
                    resumo = data.get("summary")
                    
                    st.subheader("Aqui está seu resumo:")
                    st.success(resumo) # .success() mostra numa caixa verde
                
                else:
                    # Erro da API (ex: URL não encontrada, OpenAI falhou)
                    data = response.json()
                    erro_msg = data.get("error", "Erro desconhecido retornado pela API.")
                    st.error(f"Falha ao processar a URL: {erro_msg}")

            except requests.exceptions.ConnectionError:
                st.error("Erro de Conexão: Não foi possível se conectar à API.")
                st.warning("Verifique se o servidor Django (Fase 1 e 2) está rodando no terminal!")
            except requests.exceptions.Timeout:
                st.error("Erro: A requisição demorou muito (Timeout). A URL pode estar inacessível ou lenta.")
            except Exception as e:
                st.error(f"Ocorreu um erro inesperado: {e}")