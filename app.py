import streamlit as st
import random
from datetime import datetime

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Estuda+",
    page_icon="📘",
    layout="wide"
)

# =========================================================
# ESTILO
# =========================================================
st.markdown("""
<style>
    .main {
        background-color: #f7faff;
    }

    .hero-box {
        background: linear-gradient(135deg, #0b4ea2, #1f6fe5);
        padding: 28px;
        border-radius: 20px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.10);
    }

    .gold-line {
        height: 4px;
        width: 90px;
        background-color: #d4af37;
        border-radius: 999px;
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .card {
        background-color: white;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #dbe7ff;
        box-shadow: 0 6px 16px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }

    .section-title {
        color: #0b4ea2;
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .small-note {
        color: #4a5a75;
        font-size: 14px;
    }

    .metric-box {
        background-color: #eef5ff;
        padding: 16px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #d3e4ff;
    }

    .footer-text {
        text-align: center;
        color: #5d6b82;
        font-size: 14px;
        margin-top: 25px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# ESTADO
# =========================================================
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0

if "quiz_total" not in st.session_state:
    st.session_state.quiz_total = 0

if "diagnostic_level" not in st.session_state:
    st.session_state.diagnostic_level = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "study_plan" not in st.session_state:
    st.session_state.study_plan = []

# =========================================================
# BANCO SIMPLES DE QUESTÕES
# =========================================================
questions_easy = [
    {
        "question": "Quanto é 7 + 5?",
        "options": ["10", "11", "12", "13"],
        "answer": "12",
        "topic": "Adição"
    },
    {
        "question": "Quanto é 9 x 3?",
        "options": ["18", "21", "27", "36"],
        "answer": "27",
        "topic": "Multiplicação"
    },
    {
        "question": "Quanto é 20 - 8?",
        "options": ["10", "11", "12", "13"],
        "answer": "12",
        "topic": "Subtração"
    },
    {
        "question": "Quanto é 16 ÷ 4?",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "topic": "Divisão"
    }
]

questions_medium = [
    {
        "question": "Resolva: 3x = 18. Qual é o valor de x?",
        "options": ["3", "6", "9", "12"],
        "answer": "6",
        "topic": "Equações"
    },
    {
        "question": "Quanto é 25% de 200?",
        "options": ["25", "40", "50", "75"],
        "answer": "50",
        "topic": "Porcentagem"
    },
    {
        "question": "Um triângulo tem ângulos de 50° e 60°. Qual é o terceiro ângulo?",
        "options": ["60°", "70°", "80°", "90°"],
        "answer": "70°",
        "topic": "Geometria"
    },
    {
        "question": "Quanto é 2² + 3²?",
        "options": ["10", "11", "12", "13"],
        "answer": "13",
        "topic": "Potências"
    }
]

questions_hard = [
    {
        "question": "Resolva: 2x + 5 = 17",
        "options": ["5", "6", "7", "8"],
        "answer": "6",
        "topic": "Equações"
    },
    {
        "question": "Qual é a área de um retângulo de base 8 e altura 5?",
        "options": ["13", "20", "35", "40"],
        "answer": "40",
        "topic": "Geometria"
    },
    {
        "question": "Quanto é a raiz quadrada de 144?",
        "options": ["10", "11", "12", "13"],
        "answer": "12",
        "topic": "Raiz quadrada"
    },
    {
        "question": "Se y = 3x e x = 4, quanto vale y?",
        "options": ["7", "10", "12", "14"],
        "answer": "12",
        "topic": "Álgebra"
    }
]

# =========================================================
# FUNÇÕES
# =========================================================
def generate_study_plan(level, days_per_week, minutes_per_day):
    plan = []

    if level == "Iniciante":
        topics = [
            "Adição e subtração",
            "Multiplicação e divisão",
            "Problemas simples",
            "Frações básicas"
        ]
    elif level == "Intermediário":
        topics = [
            "Equações simples",
            "Porcentagem",
            "Frações e decimais",
            "Geometria básica"
        ]
    else:
        topics = [
            "Álgebra",
            "Geometria",
            "Expressões numéricas",
            "Potências e raízes"
        ]

    for i in range(days_per_week):
        topic = topics[i % len(topics)]
        plan.append({
            "dia": f"Dia {i + 1}",
            "tema": topic,
            "tempo": f"{minutes_per_day} minutos",
            "atividade": f"Estudar {topic} + resolver 5 exercícios."
        })

    return plan


def tutor_response(user_message):
    msg = user_message.lower()

    if "fração" in msg or "fracao" in msg:
        return (
            "Frações representam partes de um todo. "
            "Exemplo: 1/2 significa uma de duas partes iguais. "
            "Se quiser, eu posso te explicar soma de frações também."
        )

    if "porcentagem" in msg:
        return (
            "Porcentagem é uma forma de representar partes de 100. "
            "Exemplo: 25% de 200 = 200 × 0,25 = 50."
        )

    if "equação" in msg or "equacao" in msg:
        return (
            "Uma equação é como uma balança: os dois lados precisam ficar iguais. "
            "Exemplo: 3x = 12. Para descobrir x, dividimos os dois lados por 3. "
            "Então x = 4."
        )

    if "área" in msg or "area" in msg:
        return (
            "Área é o espaço dentro de uma figura. "
            "No retângulo, fazemos base × altura."
        )

    if "oi" in msg or "olá" in msg or "ola" in msg:
        return (
            "Oi! Eu sou o tutor da Estuda+. "
            "Posso te ajudar com matemática de um jeito mais simples."
        )

    if "não entendi" in msg or "nao entendi" in msg:
        return (
            "Sem problema. Vamos mais devagar: me diga exatamente qual conta, tema "
            "ou tipo de exercício te confundiu."
        )

    return (
        "Posso te ajudar com matemática básica, frações, porcentagem, equações, "
        "geometria e revisão. Tente me perguntar algo como: "
        "'explique frações' ou 'como fazer porcentagem?'."
    )


def calculate_diagnostic(score):
    if score <= 2:
        return "Iniciante"
    elif score == 3:
        return "Intermediário"
    return "Avançado"


def show_home():
    st.markdown("""
    <div class="hero-box">
        <h1 style="margin-bottom:6px;">Estuda+</h1>
        <div style="font-size:22px; font-weight:500;">Aprendendo no seu ritmo</div>
        <div class="gold-line"></div>
        <div style="font-size:16px; max-width:850px;">
            Uma plataforma simples para ajudar estudantes a evoluírem em matemática
            com diagnóstico, plano de estudo, exercícios e apoio estilo tutor de IA.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color:#0b4ea2;">Diagnóstico</h3>
            <p>Descubra seu nível atual.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color:#0b4ea2;">Plano de estudo</h3>
            <p>Organize seus dias com clareza.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-box">
            <h3 style="color:#0b4ea2;">Tutor IA</h3>
            <p>Tire dúvidas de forma simples.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Como funciona")
    st.write(
        "1. Faça um mini diagnóstico.\n"
        "2. Receba um plano de estudos.\n"
        "3. Pratique com exercícios.\n"
        "4. Use o tutor para revisar dúvidas."
    )

    st.markdown("### Público inicial")
    st.write("Estudantes que querem melhorar em matemática de forma leve, prática e personalizada.")


def show_diagnostic():
    st.markdown('<div class="section-title">Diagnóstico inicial</div>', unsafe_allow_html=True)
    st.write("Responda 4 perguntas para estimar seu nível atual em matemática.")

    diagnostic_questions = random.sample(
        questions_easy + questions_medium + questions_hard, 4
    )

    user_answers = []
    for idx, q in enumerate(diagnostic_questions):
        answer = st.radio(
            f"{idx + 1}. {q['question']}",
            q["options"],
            key=f"diag_{idx}"
        )
        user_answers.append((q, answer))

    if st.button("Ver meu nível"):
        score = 0
        for q, ans in user_answers:
            if ans == q["answer"]:
                score += 1

        level = calculate_diagnostic(score)
        st.session_state.diagnostic_level = level

        st.success(f"Você acertou {score} de 4. Seu nível estimado é: **{level}**")

        if level == "Iniciante":
            st.info("Sugestão: reforçar operações básicas, frações e interpretação de problemas.")
        elif level == "Intermediário":
            st.info("Sugestão: avançar em porcentagem, equações e geometria básica.")
        else:
            st.info("Sugestão: manter ritmo e aprofundar álgebra, geometria e resolução de problemas.")


def show_study_plan():
    st.markdown('<div class="section-title">Plano de estudos</div>', unsafe_allow_html=True)

    if st.session_state.diagnostic_level is None:
        st.warning("Faça primeiro o diagnóstico para gerar um plano mais personalizado.")
        default_level = "Iniciante"
    else:
        default_level = st.session_state.diagnostic_level

    col1, col2, col3 = st.columns(3)

    with col1:
        level = st.selectbox(
            "Nível",
            ["Iniciante", "Intermediário", "Avançado"],
            index=["Iniciante", "Intermediário", "Avançado"].index(default_level)
        )

    with col2:
        days_per_week = st.slider("Dias por semana", 2, 7, 4)

    with col3:
        minutes_per_day = st.slider("Minutos por dia", 15, 90, 30, 5)

    if st.button("Gerar plano"):
        plan = generate_study_plan(level, days_per_week, minutes_per_day)
        st.session_state.study_plan = plan

    if st.session_state.study_plan:
        st.markdown("### Seu plano")
        for item in st.session_state.study_plan:
            st.markdown(f"""
            <div class="card">
                <h4 style="color:#0b4ea2; margin-bottom:8px;">{item['dia']}</h4>
                <p><strong>Tema:</strong> {item['tema']}</p>
                <p><strong>Tempo:</strong> {item['tempo']}</p>
                <p><strong>Atividade:</strong> {item['atividade']}</p>
            </div>
            """, unsafe_allow_html=True)


def show_practice():
    st.markdown('<div class="section-title">Exercícios</div>', unsafe_allow_html=True)

    difficulty = st.selectbox(
        "Escolha a dificuldade",
        ["Fácil", "Média", "Difícil"]
    )

    if difficulty == "Fácil":
        current_bank = questions_easy
    elif difficulty == "Média":
        current_bank = questions_medium
    else:
        current_bank = questions_hard

    q = random.choice(current_bank)

    st.markdown(f"""
    <div class="card">
        <h4 style="color:#0b4ea2;">Tema: {q['topic']}</h4>
        <p style="font-size:18px;">{q['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    user_answer = st.radio("Escolha sua resposta", q["options"], key=f"practice_{q['question']}")

    if st.button("Corrigir exercício"):
        st.session_state.quiz_total += 1

        if user_answer == q["answer"]:
            st.session_state.quiz_score += 1
            st.success("Correto! Muito bem.")
        else:
            st.error(f"Não foi dessa vez. Resposta correta: {q['answer']}")

    if st.session_state.quiz_total > 0:
        accuracy = round((st.session_state.quiz_score / st.session_state.quiz_total) * 100, 1)
        st.info(
            f"Seu desempenho atual: {st.session_state.quiz_score}/{st.session_state.quiz_total} "
            f"acertos ({accuracy}%)."
        )


def show_tutor():
    st.markdown('<div class="section-title">Tutor Estuda+</div>', unsafe_allow_html=True)
    st.write("Faça uma pergunta de matemática e receba uma explicação simples.")

    user_input = st.text_input("Digite sua dúvida", placeholder="Ex: como fazer porcentagem?")

    if st.button("Perguntar ao tutor"):
        if user_input.strip():
            response = tutor_response(user_input)
            st.session_state.chat_history.append(("Você", user_input))
            st.session_state.chat_history.append(("Tutor", response))

    if st.session_state.chat_history:
        st.markdown("### Conversa")
        for sender, message in st.session_state.chat_history:
            if sender == "Você":
                st.markdown(f"""
                <div class="card" style="border-left: 6px solid #1f6fe5;">
                    <strong>{sender}:</strong> {message}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card" style="border-left: 6px solid #d4af37;">
                    <strong>{sender}:</strong> {message}
                </div>
                """, unsafe_allow_html=True)


def show_admin_vision():
    st.markdown('<div class="section-title">Visão do MVP</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h4 style="color:#0b4ea2;">O que este MVP já entrega</h4>
        <p>• Página inicial clara para apresentar o produto</p>
        <p>• Diagnóstico rápido de matemática</p>
        <p>• Plano de estudos com base no nível do aluno</p>
        <p>• Exercícios com correção imediata</p>
        <p>• Tutor estilo IA para dúvidas simples</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <h4 style="color:#0b4ea2;">Próximas evoluções</h4>
        <p>• Login de aluno</p>
        <p>• Histórico de desempenho</p>
        <p>• Mais matérias além de matemática</p>
        <p>• Integração com IA real via API</p>
        <p>• Área para pais e professores</p>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 📘 Estuda+")
    st.caption("Aprendendo no seu ritmo")
    page = st.radio(
        "Navegação",
        [
            "Início",
            "Diagnóstico",
            "Plano de estudos",
            "Exercícios",
            "Tutor IA",
            "Visão do MVP"
        ]
    )

    st.markdown("---")
    st.markdown("### Resumo")
    if st.session_state.diagnostic_level:
        st.write(f"**Nível atual:** {st.session_state.diagnostic_level}")
    else:
        st.write("**Nível atual:** ainda não definido")

    st.write(f"**Data:** {datetime.now().strftime('%d/%m/%Y')}")

# =========================================================
# ROTEAMENTO
# =========================================================
if page == "Início":
    show_home()
elif page == "Diagnóstico":
    show_diagnostic()
elif page == "Plano de estudos":
    show_study_plan()
elif page == "Exercícios":
    show_practice()
elif page == "Tutor IA":
    show_tutor()
elif page == "Visão do MVP":
    show_admin_vision()

# =========================================================
# RODAPÉ
# =========================================================
st.markdown(
    '<div class="footer-text">Estuda+ • MVP em Python • foco inicial em matemática</div>',
    unsafe_allow_html=True
)
