# Site de Fundamentos de Programação em Python com Flask e Gemini

## Visão Geral do Projeto

Este é um projeto de aplicação web interativa desenvolvido com o framework Flask em Python. O objetivo é criar um site informativo sobre os fundamentos da programação em Python, oferecendo recursos educacionais e ferramentas interativas, como uma seção de perguntas e respostas integrada com a API do Google Gemini e um dicionário de termos de programação com persistência em arquivo de texto.

## Funcionalidades

* **Página Inicial:** Boas-vindas e navegação principal do site.
* **Sobre a Equipe:** Informações sobre os desenvolvedores do projeto.
* **Fundamentos de Python:** Seções detalhadas sobre os principais tópicos de programação em Python:
    * Estruturas de Seleção (`if`, `elif`, `else`)
    * Estruturas de Repetição (`for`, `while`)
    * Vetores e Matrizes (Listas e Listas Aninhadas)
    * Funções e Procedimentos
    * Tratamento de Exceções (`try`, `except`, `finally`)
    Cada seção inclui conceito, aplicação e exemplos de código.
* **Tirar Dúvidas (API Gemini):** Uma interface para o usuário enviar perguntas sobre Python e receber respostas geradas pela API do Google Gemini.
* **Dicionário de Termos de Programação:** Um dicionário interativo com funcionalidades CRUD (Create, Read, Update, Delete) para termos e suas definições, armazenados em um arquivo de texto.
    * Visualização de todos os termos.
    * Adição de novos termos.
    * Alteração de termos existentes (nome e/ou definição).
    * Exclusão de termos.

## Tecnologias Utilizadas

* **Backend:** Python 3.x, Flask (framework web)
* **Integração de IA:** Google Gemini API (`google-generativeai` library)
* **Frontend:** HTML5, CSS3, JavaScript (opcional para futuras interações)
* **Gerenciamento de Ambiente:** `venv` (ambiente virtual Python)
* **Variáveis de Ambiente:** `python-dotenv`

## Estrutura do Projeto