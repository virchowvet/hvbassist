from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def processar_texto(transcricao, tipo="consulta"):
    if tipo == "consulta":
        prompt = (
            "Você é um assistente médico-veterinário. A seguir está a transcrição de uma consulta.\n\n"
            "Gere um RELATÓRIO CLÍNICO COMPLETO em HTML com as seções:\n"
            "<h1>Relatório Clínico</h1>\n"
            "<h2>Anamnese</h2>\n"
            "<h2>Exame Físico</h2>\n"
            "<h2>Achados Laboratoriais</h2>\n"
            "<h2>Diagnóstico Provável</h2>\n"
            "<h2>Plano Terapêutico</h2>\n"
            "<h2>Orientações ao Tutor</h2>\n\n"
            "Utilize somente as informações que estiverem explicitamente descritas na transcrição.\n"
            "Não invente, não preencha com suposições, nem complete lacunas com base em contexto clínico.\n"
            "Se alguma seção não for abordada na transcrição, escreva: <p>Nenhuma informação fornecida.</p>\n\n"
            "Use apenas HTML sem CSS ou JavaScript, com estrutura limpa.\n"
            "Use <p> para parágrafos e <ul>/<li> para listas, quando necessário.\n\n"
            f"Aqui está a transcrição:\n\n{transcricao}"
        )
    elif tipo == "receita":
        prompt = (
            "Você é um assistente médico-veterinário. A seguir está a transcrição de uma prescrição.\n\n"
            "Gere uma RECEITA VETERINÁRIA em HTML com os seguintes critérios:\n"
            "- Agrupe os medicamentos por VIA DE ADMINISTRAÇÃO (ex: oral, subcutânea, etc.)\n"
            "- Antes da lista de cada via, adicione um título centralizado com <h3 style=\"text-align:center;\">Via oral</h3>\n"
            "- Para cada medicamento, use a estrutura:\n"
            "  <li><strong>Nome do medicamento</strong><br>Dê [quantidade], a cada [intervalo], por [duração].</li>\n"
            "- Após cada item <li>, adicione uma tag <p></p> para espaçamento\n"
            "- Liste os medicamentos com <ul><li>...\n"
            "- Não inclua dados do paciente, veterinário, cabeçalhos ou rodapés\n"
            "- Utilize apenas HTML puro e limpo, sem CSS externo ou JavaScript\n\n"
            f"Transcrição:\n\n{transcricao}"
        )
    elif tipo == "retorno":
        prompt = (
            "Você é um assistente médico-veterinário. A seguir está a transcrição de uma consulta de retorno.\n\n"
            "Gere um RELATÓRIO DE RETORNO estruturado em HTML com as seguintes seções:\n"
            "<h1>Relatório de Retorno</h1>\n"
            "<h2>Evolução Clínica</h2>\n"
            "<h2>Resposta ao Tratamento</h2>\n"
            "<h2>Conduta Atual</h2>\n"
            "<h2>Orientações ao Tutor</h2>\n\n"
            "Converta automaticamente quaisquer expressões informais ou populares em terminologia clínica adequada à medicina veterinária.\n"
            "Por exemplo, substitua palavras como 'bumbum', 'pomadinha', 'ouvidinho', 'machucadinho', etc., por equivalentes técnicos apropriados com base no contexto.\n"
            "Use linguagem formal e técnica, mas sem alterar o sentido clínico das informações descritas na transcrição.\n"
            "Mantenha fidelidade ao conteúdo mencionado, sem adicionar informações novas ou inventadas, não preencha com suposições, nem complete lacunas com base em contexto clínico.\n"
            "Utilize apenas HTML limpo, com <p> e <ul>/<li> conforme necessário. Não adicione CSS ou JavaScript.\n\n"
            f"Transcrição:\n\n{transcricao}"
        )
    else:
        prompt = f"Transcrição inválida. Tipo não reconhecido: {tipo}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um assistente médico-veterinário especializado em relatórios clínicos."},
            {"role": "user", "content": prompt}
        ]
    )

    conteudo = response.choices[0].message.content.strip()

    # remove blocos ```html ou '''html do início e fim
    if conteudo.startswith("```html"):
        conteudo = conteudo[7:].strip()
    elif conteudo.startswith("'''html"):
        conteudo = conteudo[7:].strip()

    if conteudo.endswith("```"):
        conteudo = conteudo[:-3].strip()
    elif conteudo.endswith("'''"):
        conteudo = conteudo[:-3].strip()

    return conteudo
