# projeto_flask_python/config.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    DICIONARIO_FILE = 'data/dicionario.txt' # Caminho para o arquivo do dicionário
    # Adicione outras configurações aqui se necessário

# Instala a biblioteca google-generativeai
os.system('pip install google-generativeai')

if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash:generateContent')
else:
    print("ATENÇÃO: GEMINI_API_KEY não configurada em .env. A funcionalidade de dúvidas não estará disponível.")
    gemini_model = None