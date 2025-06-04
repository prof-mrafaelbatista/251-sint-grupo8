# projeto_flask_python/app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import google.generativeai as genai
import os
from config import Config # Importa a classe de configurações

app = Flask(__name__)
app.config.from_object(Config) # Carrega as configurações do arquivo config.py
app.secret_key = 'supersecretkey' # Necessário para usar flash messages (mudar em produção)

# --- Configuração da API do Gemini ---
if Config.GEMINI_API_KEY:
    genai.configure(api_key=Config.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    print("ATENÇÃO: GEMINI_API_KEY não configurada em .env. A funcionalidade de dúvidas não estará disponível.")
    gemini_model = None

# --- Funções Auxiliares para o Dicionário ---
def ler_termos():
    termos = {}
    if not os.path.exists(Config.DICIONARIO_FILE):
        return termos
    with open(Config.DICIONARIO_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and ':' in line:
                termo, definicao = line.split(':', 1)
                termos[termo.strip().lower()] = {"termo": termo.strip(), "definicao": definicao.strip()}
    return termos

def salvar_termos(termos):
    with open(Config.DICIONARIO_FILE, 'w', encoding='utf-8') as f:
        for termo_key in sorted(termos.keys()): # Salva em ordem alfabética
            termo_obj = termos[termo_key]
            f.write(f"{termo_obj['termo']}:{termo_obj['definicao']}\n")

# --- Rotas da Aplicação ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    equipe = [
        {
            "nome": "Filipe Silva",
            "rede_social": "https://github.com/FilipeBcode",
            "descricao": "Desenvolvedor backend, apaixonado por Python e tecnológica.",
            "imagem": "img/filipe.jpg" 
        },
        {
            "nome": "Mauro Sergio",
            "rede_social": "https://github.com/devmauro107",
            "descricao": "Especialista em frontend e design de interfaces acessíveis.",
            "imagem": "img/mauro.jpg"
        },
        {
            "nome": "Carlos Guilherme",
            "rede_social": "https://github.com/GuilhermeSaldanha02",
            "descricao": "Responsável pela integração de IA e automação no projeto.",
            "imagem": "img/carlos_guilherme.jpg"
        },
        {
            "nome": "Bruna Oliveira",
            "rede_social": "https://github.com/brunamarllus",
            "descricao": "Gestora de conteúdo e revisora técnica.",
            "imagem": "img/bruna.jpg"
        }
    ]
    return render_template('sobre.html', equipe=equipe)

@app.route('/fundamentos')
def fundamentos_geral():
    return render_template('fundamentos_geral.html')

@app.route('/fundamentos/<tema>')
def fundamentos_tema(tema):
    # Dicionário mapeando temas para templates
    temas_validos = {
        'selecao': 'estruturas_selecao.html',
        'repeticao': 'estruturas_repeticao.html',
        'vetores_matrizes': 'vetores_matrizes.html',
        'funcoes_procedimentos': 'funcoes_procedimentos.html',
        'tratamento_excecao': 'tratamento_excecao.html',
    }
    template_name = temas_validos.get(tema)
    if template_name:
        return render_template(template_name)
    else:
        flash('Tema não encontrado.', 'error')
        return redirect(url_for('fundamentos_geral'))

@app.route('/duvidas', methods=['GET', 'POST'])
def duvidas():
    resposta_gemini = None
    pergunta_usuario = None
    if request.method == 'POST':
        pergunta_usuario = request.form['pergunta']
        if gemini_model:
            try:
                # O modelo Gemini pode ser sensível ao contexto.
                # Podemos adicionar um prompt inicial para direcioná-lo.
                prompt = f"Como especialista em Python, por favor, responda à seguinte pergunta de forma clara e concisa:\n\n{pergunta_usuario}"
                response = gemini_model.generate_content(prompt)
                resposta_gemini = response.text
            except Exception as e:
                resposta_gemini = f"Ocorreu um erro ao consultar o Gemini: {e}. Verifique sua chave da API ou tente novamente mais tarde."
                flash(resposta_gemini, 'error')
        else:
            resposta_gemini = "A funcionalidade de tirar dúvidas não está disponível. A chave da API do Gemini não foi configurada."
            flash(resposta_gemini, 'warning')
    return render_template('duvidas.html', resposta=resposta_gemini, pergunta=pergunta_usuario)

@app.route('/dicionario')
def dicionario():
    termos = ler_termos()
    # Converte para uma lista de dicionários para facilitar o Jinja
    lista_termos = sorted(termos.values(), key=lambda x: x['termo'].lower())
    return render_template('dicionario.html', termos=lista_termos)

@app.route('/dicionario/adicionar', methods=['GET', 'POST'])
def adicionar_termo():
    if request.method == 'POST':
        termo = request.form['termo'].strip()
        definicao = request.form['definicao'].strip()
        if termo and definicao:
            termos = ler_termos()
            if termo.lower() in termos:
                flash(f'O termo "{termo}" já existe no dicionário. Considere alterá-lo.', 'warning')
            else:
                termos[termo.lower()] = {"termo": termo, "definicao": definicao}
                salvar_termos(termos)
                flash(f'Termo "{termo}" adicionado com sucesso!', 'success')
                return redirect(url_for('dicionario'))
        else:
            flash('Termo e definição não podem ser vazios.', 'error')
    return render_template('adicionar_termo.html')

@app.route('/dicionario/alterar', methods=['GET', 'POST'])
def alterar_termo():
    termos = ler_termos()
    lista_termos_para_selecao = sorted([t['termo'] for t in termos.values()], key=lambda x: x.lower())
    
    termo_selecionado = request.args.get('termo') # Pre-seleciona da URL se houver
    definicao_existente = ''

    if request.method == 'POST':
        termo_original = request.form.get('termo_original')
        novo_termo = request.form.get('novo_termo', termo_original).strip()
        nova_definicao = request.form['nova_definicao'].strip()

        if termo_original and nova_definicao:
            if termo_original.lower() not in termos:
                flash('Termo original não encontrado para alteração.', 'error')
                return redirect(url_for('alterar_termo'))
            
            # Se o termo foi renomeado, deleta o antigo e adiciona o novo
            if novo_termo.lower() != termo_original.lower():
                # Verifica se o novo termo já existe (se for diferente do original)
                if novo_termo.lower() in termos and novo_termo.lower() != termo_original.lower():
                    flash(f'O novo termo "{novo_termo}" já existe.', 'error')
                    return render_template('alterar_termo.html', termos_existentes=lista_termos_para_selecao,
                                            termo_selecionado=termo_original,
                                            definicao_existente=termos[termo_original.lower()]['definicao'])

                del termos[termo_original.lower()] # Remove o termo antigo
                termos[novo_termo.lower()] = {"termo": novo_termo, "definicao": nova_definicao} # Adiciona o novo
                flash(f'Termo "{termo_original}" alterado para "{novo_termo}" com sucesso!', 'success')
            else: # Apenas a definição foi alterada
                termos[termo_original.lower()]['definicao'] = nova_definicao
                flash(f'Definição do termo "{termo_original}" atualizada com sucesso!', 'success')
            
            salvar_termos(termos)
            return redirect(url_for('dicionario'))
        else:
            flash('Selecione um termo e forneça a nova definição.', 'error')
    
    # Se for GET, ou POST com erro, carrega a definição do termo selecionado (se houver)
    if termo_selecionado and termo_selecionado.lower() in termos:
        definicao_existente = termos[termo_selecionado.lower()]['definicao']

    return render_template('alterar_termo.html', termos_existentes=lista_termos_para_selecao, 
                           termo_selecionado=termo_selecionado,
                           definicao_existente=definicao_existente)

@app.route('/dicionario/deletar', methods=['GET', 'POST'])
def deletar_termo():
    termos = ler_termos()
    lista_termos_para_selecao = sorted([t['termo'] for t in termos.values()], key=lambda x: x.lower())

    if request.method == 'POST':
        termo_a_deletar = request.form['termo_a_deletar'].strip()
        if termo_a_deletar.lower() in termos:
            del termos[termo_a_deletar.lower()]
            salvar_termos(termos)
            flash(f'Termo "{termo_a_deletar}" removido com sucesso!', 'success')
            return redirect(url_for('dicionario'))
        else:
            flash('Termo não encontrado para remoção.', 'error')
    return render_template('deletar_termo.html', termos_existentes=lista_termos_para_selecao)


if __name__ == '__main__':
    # Cria a pasta 'data' se não existir
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(debug=True)