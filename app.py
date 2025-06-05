import streamlit as st
from datetime import datetime
import re

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

# Signos hebraicos por mês hebraico (aproximação manual)
  #  """Converte a data gregoriana para o calendário hebraico e retorna a data e o signo (aproximação manual)."""
    month = int(birth_date.split('/')[1])
    hebrew_date = f"Aproximado: {birth_date} (baseado no mês gregoriano)"
    return hebrew_date, hebrew_signs.get(month, {"signo": "Desconhecido", "tribo": "", "letra": "", "qualidade": ""})

        "https://raw.githubusercontent.com/cesarvalentimjr/kabbalah/main/Kabbalah/lifetree.png",
        caption="Ilustração da Árvore da Vida Cabalística",
        use_column_width=True
    )

    # Layout com duas colunas
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Insira seus dados")
        name = st.text_input("Nome completo", placeholder="Ex.: Maylan Passos Oliveira")
        birth_date = st.text_input("Data de nascimento (DD/MM/YYYY)", placeholder="Ex.: 02/03/1982")
        if st.button("Gerar Relatório"):
            if name and birth_date:
                report = generate_report(name, birth_date)
                st.session_state['report'] = report
            else:
                st.error("Por favor, preencha todos os campos.")

    with col2:
        st.subheader("Relatório Numerológico")
        if 'report' in st.session_state:
            st.markdown(st.session_state['report'], unsafe_allow_html=True)
        else:
            st.info("Preencha os dados à esquerda e clique em 'Gerar Relatório' para visualizar o resultado.")

if __name__ == "__main__":
    main()
