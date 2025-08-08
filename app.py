import streamlit as st
from datetime import datetime
import re
from pyluach.dates import GregorianDate, HebrewDate

# Dicionário com valores numéricos das letras hebraicas
hebrew_values = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70,
    'פ': 80, 'ף': 80, 'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400
}

# Significados simbólicos das letras hebraicas
hebrew_letter_meanings = {
    'א': "Unidade, liderança, origem divina",
    'ב': "Dualidade, bênção, construção",
    'ג': "Generosidade, recompensa, movimento",
    'ד': "Porta, humildade, oportunidade",
    'ה': "Sopro, visão espiritual, revelação",
    'ו': "Conexão, continuidade, harmonia",
    'ז': "Espada, proteção, decisão",
    'ח': "Vida, graça, equilíbrio",
    'ט': "Serpente, transformação, purificação",
    'י': "Criação, potencial, mão divina",
    'כ': "Abertura, receptividade, poder",
    'ל': "Aprendizado, ensino, aspiração",
    'מ': "Água, sabedoria, fluxo",
    'נ': "Transformação, fidelidade, alma",
    'ס': "Apoio, proteção, estabilidade",
    'ע': "Visão, percepção, profundidade",
    'פ': "Boca, expressão, comunicação",
    'צ': "Justiça, retidão, propósito",
    'ק': "Sagrado, transcendência, elevação",
    'ר': "Cabeça, liderança, início",
    'ש': "Fogo, paixão, integração",
    'ת': "Completude, verdade, manifestação"
}

# Dicionário de transliteração simplificada (português para hebraico)
transliteration_map = {
    'a': 'א', 'b': 'ב', 'g': 'ג', 'd': 'ד', 'h': 'ה', 'v': 'ו', 'w': 'ו', 'z': 'ז',
    'ch': 'ח', 't': 'ט', 'i': 'י', 'y': 'י', 'k': 'כ', 'kh': 'כ', 'l': 'ל', 'm': 'מ',
    'n': 'נ', 's': 'ס', 'ss': 'ס', 'o': 'ע', 'p': 'פ', 'ph': 'פ', 'tz': 'צ', 'q': 'ק',
    'r': 'ר', 'sh': 'ש', 't': 'ת', 'e': 'א'
}

# Associações de números com sefirot, cores, características, pedras, elementos e letras
number_traits = {
    1: {"cores": ["Branco", "Vermelho"], "caracteristicas": "Liderança, independência, iniciativa",
        "sefira": "Keter (Coroa)", "letra": "Aleph (א)", "pedra": "Diamante", "elemento": "Fogo"},
    2: {"cores": ["Laranja", "Azul claro"], "caracteristicas": "Cooperação, sensibilidade, diplomacia",
        "sefira": "Chochmah (Sabedoria)", "letra": "Bet (ב)", "pedra": "Pérola", "elemento": "Água"},
    3: {"cores": ["Amarelo", "Rosa"], "caracteristicas": "Criatividade, expressão, otimismo",
        "sefira": "Chesed (Bondade)", "letra": "Gimel (ג)", "pedra": "Safira", "elemento": "Fogo"},
    4: {"cores": ["Verde escuro", "Marrom"], "caracteristicas": "Estabilidade, organização, trabalho árduo",
        "sefira": "Gevurah (Força)", "letra": "Dalet (ד)", "pedra": "Esmeralda", "elemento": "Terra"},
    5: {"cores": ["Vermelho", "Laranja"], "caracteristicas": "Liberdade, versatilidade, aventura",
        "sefira": "Hod (Esplendor)", "letra": "Heh (ה)", "pedra": "Turquesa", "elemento": "Ar"},
    6: {"cores": ["Verde", "Dourado"], "caracteristicas": "Harmonia, responsabilidade, cuidado",
        "sefira": "Tiferet (Beleza)", "letra": "Vav (ו)", "pedra": "Quartzo rosa", "elemento": "Ar"},
    7: {"cores": ["Roxo", "Azul escuro"], "caracteristicas": "Espiritualidade, introspecção, sabedoria",
        "sefira": "Netzach (Vitória)", "letra": "Zayin (ז)", "pedra": "Ametista", "elemento": "Água"},
    8: {"cores": ["Azul escuro", "Preto"], "caracteristicas": "Abundância, poder, realização",
        "sefira": "Binah (Compreensão)", "letra": "Chet (ח)", "pedra": "Ônix", "elemento": "Terra"},
    9: {"cores": ["Violeta", "Dourado"], "caracteristicas": "Humanitarismo, compaixão, idealismo",
        "sefira": "Yesod (Fundação)", "letra": "Tet (ט)", "pedra": "Topázio", "elemento": "Ar"}
}

# Caminhos da Árvore da Vida (todos os 22 caminhos, de 11 a 32)
paths = {
    11: {"letra": "Aleph (א)", "conexão": "Keter-Chochmah", "significado": "Respiração divina, início espiritual"},
    12: {"letra": "Bet (ב)", "conexão": "Keter-Binah", "significado": "Criação, estrutura inicial"},
    13: {"letra": "Gimel (ג)", "conexão": "Keter-Tiferet", "significado": "Generosidade, equilíbrio cósmico"},
    14: {"letra": "Dalet (ד)", "conexão": "Chochmah-Binah", "significado": "Porta da sabedoria, humildade"},
    15: {"letra": "Heh (ה)", "conexão": "Chochmah-Tiferet", "significado": "Visão espiritual, harmonia"},
    16: {"letra": "Vav (ו)", "conexão": "Chochmah-Chesed", "significado": "Conexão, amor universal"},
    17: {"letra": "Zayin (ז)", "conexão": "Binah-Tiferet", "significado": "Proteção, decisão espiritual"},
    18: {"letra": "Chet (ח)", "conexão": "Binah-Gevurah", "significado": "Vida, equilíbrio de forças"},
    19: {"letra": "Tet (ט)", "conexão": "Chesed-Gevurah", "significado": "Transformação, purificação"},
    20: {"letra": "Yud (י)", "conexão": "Chesed-Tiferet", "significado": "Criação, potencial divino"},
    21: {"letra": "Kaf (כ)", "conexão": "Chesed-Netzach", "significado": "Receptividade, poder espiritual"},
    22: {"letra": "Lamed (ל)", "conexão": "Gevurah-Tiferet", "significado": "Aprendizado, aspiração"},
    23: {"letra": "Mem (מ)", "conexão": "Gevurah-Hod", "significado": "Sabedoria fluida, introspecção"},
    24: {"letra": "Nun (נ)", "conexão": "Tiferet-Netzach", "significado": "Transformação, fidelidade"},
    25: {"letra": "Samech (ס)", "conexão": "Tiferet-Hod", "significado": "Apoio, estabilidade espiritual"},
    26: {"letra": "Ayin (ע)", "conexão": "Tiferet-Yesod", "significado": "Visão profunda, conexão com a alma"},
    27: {"letra": "Peh (פ)", "conexão": "Netzach-Hod", "significado": "Expressão, comunicação divina"},
    28: {"letra": "Tzadi (צ)", "conexão": "Netzach-Yesod", "significado": "Justiça, propósito elevado"},
    29: {"letra": "Kuf (ק)", "conexão": "Hod-Yesod", "significado": "Sagrado, transcendência"},
    30: {"letra": "Resh (ר)", "conexão": "Hod-Malkhut", "significado": "Liderança, manifestação inicial"},
    31: {"letra": "Shin (ש)", "conexão": "Netzach-Malkhut", "significado": "Paixão, integração espiritual"},
    32: {"letra": "Tav (ת)", "conexão": "Yesod-Malkhut", "significado": "Completude, verdade manifestada"}
}

# Signos hebraicos por mês hebraico
hebrew_signs = {
    1: {"signo": "Nisan (Áries)", "tribo": "Judá", "letra": "Heh (ה)", "qualidade": "Liderança"},
    2: {"signo": "Iyar (Touro)", "tribo": "Issacar", "letra": "Vav (ו)", "qualidade": "Estabilidade"},
    3: {"signo": "Sivan (Gêmeos)", "tribo": "Zebulom", "letra": "Zayin (ז)", "qualidade": "Comunicação"},
    4: {"signo": "Tammuz (Câncer)", "tribo": "Rúben", "letra": "Chet (ח)", "qualidade": "Sensibilidade"},
    5: {"signo": "Av (Leão)", "tribo": "Simeão", "letra": "Tet (ט)", "qualidade": "Coragem"},
    6: {"signo": "Elul (Virgem)", "tribo": "Gad", "letra": "Yud (י)", "qualidade": "Detalhismo"},
    7: {"signo": "Tishrei (Libra)", "tribo": "Efraim", "letra": "Lamed (ל)", "qualidade": "Equilíbrio"},
    8: {"signo": "Cheshvan (Escorpião)", "tribo": "Manassés", "letra": "Nun (נ)", "qualidade": "Transformação"},
    9: {"signo": "Kislev (Sagitário)", "tribo": "Benjamim", "letra": "Samech (ס)", "qualidade": "Otimismo"},
    10: {"signo": "Tevet (Capricórnio)", "tribo": "Dan", "letra": "Ayin (ע)", "qualidade": "Ambição"},
    11: {"signo": "Shevat (Aquário)", "tribo": "Asher", "letra": "Tzadi (צ)", "qualidade": "Inovação"},
    12: {"signo": "Adar I (Peixes)", "tribo": "Naftali", "letra": "Kuf (ק)", "qualidade": "Compaixão"},
    13: {"signo": "Adar II (Peixes)", "tribo": "Naftali", "letra": "Kuf (ק)", "qualidade": "Compaixão"}
}

def validate_date(birth_date):
    """Valida o formato da data DD/MM/YYYY."""
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    if not re.match(pattern, birth_date):
        raise ValueError("Data deve estar no formato DD/MM/YYYY")
    try:
        datetime.strptime(birth_date, '%d/%m/%Y')
    except ValueError:
        raise ValueError("Data inválida")
    return True

def transliterate_name(name):
    """Translitera um nome em português para letras hebraicas."""
    name = name.lower().replace(' ', '')
    hebrew_name = ""
    i = 0
    while i < len(name):
        if i + 1 < len(name) and name[i:i+2] in transliteration_map:
            hebrew_name += transliteration_map[name[i:i+2]]
            i += 2
        else:
            hebrew_name += transliteration_map.get(name[i], 'א')
            i += 1
    return hebrew_name

def analyze_hebrew_letters(hebrew_name):
    """Analisa as letras hebraicas predominantes no nome."""
    letter_count = {}
    for letter in hebrew_name:
        letter_count[letter] = letter_count.get(letter, 0) + 1
    if letter_count:
        dominant_letter = max(letter_count, key=letter_count.get)
        return f"Letra predominante: {dominant_letter} (valor: {hebrew_values[dominant_letter]}, " \
               f"aparece {letter_count[dominant_letter]} vezes, significado: {hebrew_letter_meanings[dominant_letter]})"
    return "Nenhuma letra predominante identificada"

def calculate_name_number(name):
    """Calcula o número do nome com base nos valores hebraicos."""
    hebrew_name = transliterate_name(name)
    total = sum(hebrew_values.get(letter, 0) for letter in hebrew_name)
    intermediate = total
    while total > 9 and total not in [11, 22]:
        total = sum(int(d) for d in str(total))
    return total, intermediate, hebrew_name

def calculate_birth_number(birth_date):
    """Calcula o número da data de nascimento."""
    digits = birth_date.replace('/', '')
    total = sum(int(d) for d in digits)
    intermediate = total
    while total > 9 and total not in [11, 22]:
        total = sum(int(d) for d in str(total))
    return total, intermediate

def map_high_number(number):
    """Reduz números altos para valores entre 1 e 9 (ou 11, 22) e mapeia para caminhos, se possível."""
    original = number
    while number > 9 and number not in [11, 22]:
        number = sum(int(d) for d in str(number))
    reduced = number
    path_number = original if 11 <= original <= 32 else None
    if path_number and path_number in paths:
        return f"Número reduzido: {reduced}, Mapeado ao Caminho {path_number}: {paths[path_number]['letra']} " \
               f"({paths[path_number]['conexão']}), Significado: {paths[path_number]['significado']}"
    return f"Número reduzido: {reduced} (associações: {number_traits.get(reduced, {'caracteristicas': 'Não mapeado'})['caracteristicas']})"

def get_lucky_numbers(name_number, birth_number, name_intermediate, birth_intermediate):
    """Determina os números da sorte."""
    primary = [name_number, birth_number]
    sum_numbers = name_number + birth_number
    intermediate_sum = sum_numbers
    while sum_numbers > 9 and sum_numbers not in [11, 22]:
        sum_numbers = sum(int(d) for d in str(sum_numbers))
    primary.append(sum_numbers)
    secondary = [name_intermediate, birth_intermediate, intermediate_sum]
    return list(set(primary)), list(set(secondary))

def get_colors_and_traits(numbers):
    """Retorna cores e características associadas aos números."""
    colors = []
    traits = []
    for num in numbers:
        if num in number_traits:
            colors.extend(number_traits[num]["cores"])
            traits.append({
                "numero": num,
                "caracteristicas": number_traits[num]["caracteristicas"],
                "sefira": number_traits[num]["sefira"],
                "letra": number_traits[num]["letra"],
                "pedra": number_traits[num]["pedra"],
                "elemento": number_traits[num]["elemento"]
            })
    return list(set(colors)), traits

def get_path_info(number):
    """Retorna informações sobre os caminhos da Árvore da Vida."""
    if number in paths:
        return f"Caminho {number}: {paths[number]['letra']} ({paths[number]['conexão']}), " \
               f"Significado: {paths[number]['significado']}"
    return None

def get_hebrew_date_and_sign(birth_date):
    """Converte a data gregoriana para o calendário hebraico e retorna a data e o signo."""
    try:
        date = datetime.strptime(birth_date, '%d/%m/%Y')
        hdate = GregorianDate(date.year, date.month, date.day).to_heb()
        hebrew_month_name = hdate.month_name(hebrew=True)
        hebrew_date = f"{hdate.day} de {hebrew_month_name} de {hdate.year}"
        return hebrew_date, hebrew_signs.get(hdate.month, {"signo": "Desconhecido", "tribo": "", "letra": "", "qualidade": ""})
    except AttributeError as e:
        return f"Erro na conversão: Problema com o módulo pyluach ({str(e)})", {"signo": "Desconhecido", "tribo": "", "letra": "", "qualidade": ""}
    except Exception as e:
        return f"Erro na conversão: {str(e)}", {"signo": "Desconhecido", "tribo": "", "letra": "", "qualidade": ""}

def generate_report(name, birth_date):
    """Gera um relatório numerológico cabalístico completo."""
    try:
        validate_date(birth_date)
        name_number, name_intermediate, hebrew_name = calculate_name_number(name)
        birth_number, birth_intermediate = calculate_birth_number(birth_date)
        lucky_numbers, secondary_numbers = get_lucky_numbers(name_number, birth_number, name_intermediate, birth_intermediate)
        colors, traits = get_colors_and_traits(lucky_numbers)
        hebrew_date, hebrew_sign = get_hebrew_date_and_sign(birth_date)
        dominant_letter = analyze_hebrew_letters(hebrew_name)

        report = f"**Relatório Numerológico Cabalístico**\n"
        report += f"Nome: {name}\n"
        report += f"Data de Nascimento (Gregoriana): {birth_date}\n"
        report += f"Data de Nascimento (Hebraica): {hebrew_date}\n"
        report += f"\n**Números da Sorte**:\n"
        report += f" - Primários: {', '.join(map(str, lucky_numbers))}\n"
        report += f" - Secundários: {', '.join(map(str, secondary_numbers))}\n"
        report += f"\n**Cores Associadas**: {', '.join(colors)}\n"
        report += f"\n**Signo Hebraico**: {hebrew_sign['signo']}\n"
        report += f" - Tribo: {hebrew_sign['tribo']}\n"
        report += f" - Letra: {hebrew_sign['letra']}\n"
        report += f" - Qualidade: {hebrew_sign['qualidade']}\n"
        report += f"\n**Análise do Nome**:\n"
        report += f" - Nome em Hebraico: {hebrew_name}\n"
        report += f" - {dominant_letter}\n"
        report += f"\n**Características e Associações Cabalísticas**:\n"
        for trait in traits:
            report += f"\nNúmero {trait['numero']}:\n"
            report += f" - Características: {trait['caracteristicas']}\n"
            report += f" - Sefirá: {trait['sefira']}\n"
            report += f" - Letra Hebraica: {trait['letra']}\n"
            report += f" - Pedra Preciosa: {trait['pedra']}\n"
            report += f" - Elemento: {trait['elemento']}\n"
        report += f"\n**Caminhos da Árvore da Vida e Análise de Números Secundários**:\n"
        for num in secondary_numbers:
            path_info = get_path_info(num)
            if path_info:
                report += f" - {path_info}\n"
            else:
                report += f" - Número {num}: {map_high_number(num)}\n"
        return report
    except ValueError as e:
        return f"Erro: {str(e)}"

# Interface Streamlit
def main():
    st.set_page_config(page_title="Numerologia Cabalística", page_icon="✡️", layout="wide")

    # Título e descrição
    st.markdown("""
        <h1 style='text-align: center; color: #4B0082;'>Numerologia Cabalística</h1>
        <p style='text-align: center; font-size: 18px;'>Descubra os segredos do seu nome e data de nascimento com base na Cabala e no calendário hebraico.</p>
    """, unsafe_allow_html=True)

    # Exibir a imagem da Árvore da Vida
   st.image(
    "https://raw.githubusercontent.com/cesarvalentimjr/Kabbalah/main/lifetree.png",
    caption="Ilustração da Árvore da Vida Cabalística",
    use_container_width=True
    )

    # Layout com duas colunas
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Insira seus dados")
        name = st.text_input("Nome completo", placeholder="Ex.: Maria Santos")
        birth_date = st.text_input("Data de nascimento (DD/MM/YYYY)", placeholder="Ex.: 02/07/1975")
        if st.button("Gerar Relatório"):
            if name and birth_date:
                report = generate_report(name, birth_date)
                st.session_state['report'] = report
            else:
                st.error("Por favor, preencha todos os campos.")

    with col2:
        st.subheader("Relatório Numerológico")
        if 'report' in st.session_state:
            st.markdown(st.session_state['report'])
        else:
            st.info("Preencha os dados à esquerda e clique em 'Gerar Relatório' para visualizar o resultado.")

if __name__ == "__main__":
    main()

