import streamlit as st
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
st.set_page_config(
    page_title="Estuda+",
    page_icon="📘",
    layout="wide"
)

# =========================================================
# STYLE
# =========================================================
st.markdown("""
<style>
    .main {
        background-color: #f7faff;
    }

    .stApp {
        background: linear-gradient(180deg, #f7faff 0%, #eef5ff 100%);
    }

    .title-box {
        background: linear-gradient(135deg, #0b4ea2, #1f6fe5);
        color: white;
        padding: 22px;
        border-radius: 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.10);
    }

    .gold-line {
        height: 4px;
        width: 80px;
        background: #d4af37;
        border-radius: 999px;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .info-card {
        background: white;
        border: 1px solid #dbe7ff;
        border-radius: 16px;
        padding: 16px;
        box-shadow: 0 6px 14px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }

    .small-muted {
        color: #5c6d88;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "step" not in st.session_state:
    st.session_state.step = "welcome"

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "student_grade" not in st.session_state:
    st.session_state.student_grade = ""

if "student_goal" not in st.session_state:
    st.session_state.student_goal = ""

if "diagnostic_answers" not in st.session_state:
    st.session_state.diagnostic_answers = []

if "diagnostic_index" not in st.session_state:
    st.session_state.diagnostic_index = 0

if "diagnostic_score" not in st.session_state:
    st.session_state.diagnostic_score = 0

if "diagnostic_level" not in st.session_state:
    st.session_state.diagnostic_level = None

if "study_plan" not in st.session_state:
    st.session_state.study_plan = []

if "started" not in st.session_state:
    st.session_state.started = False


# =========================================================
# DIAGNOSTIC QUESTIONS
# =========================================================
diagnostic_questions = [
    {
        "question": "Quanto é 7 + 8?",
        "answer": "15",
        "topic": "Adição"
    },
    {
        "question": "Quanto é 9 x 6?",
        "answer": "54",
        "topic": "Multiplicação"
    },
    {
        "question": "Quanto é 25% de 200?",
        "answer": "50",
        "topic": "Porcentagem"
    },
    {
        "question": "Resolva: 3x = 18",
        "answer": "6",
        "topic": "Equações"
    },
    {
        "question": "Um triângulo tem ângulos de 50° e 60°. Qual é o terceiro ângulo?",
        "answer": "70",
        "topic": "Geometria"
    }
]


# =========================================================
# HELPERS
# =========================================================
def add_bot_message(text: str) -> None:
    st.session_state.messages.append({"role": "assistant", "content": text})

def add_user_message(text: str) -> None:
    st.session_state.messages.append({"role": "user", "content": text})

def normalize_text(text: str) -> str:
    return text.strip().lower()

def get_diagnostic_level(score: int) -> str:
    if score <= 2:
        return "Iniciante"
    if score == 3 or score == 4:
        return "Intermediário"
    return "Avançado"

def generate_study_plan(level: str, goal: str):
    if level == "Iniciante":
        topics = [
            "Adição e subtração",
            "Multiplicação e divisão",
            "Frações básicas",
            "Problemas simples",
            "Porcentagem inicial"
        ]
    elif level == "Intermediário":
        topics = [
            "Porcentagem",
            "Frações e decimais",
            "Equações simples",
            "Geometria básica",
            "Expressões numéricas"
        ]
    else:
        topics = [
            "Álgebra",
            "Geometria",
            "Potências e raízes",
            "Expressões algébricas",
            "Problemas mais desafiadores"
        ]

    plan = []
    for i, topic in enumerate(topics, start=1):
        plan.append({
            "day": f"Dia {i}",
            "topic": topic,
            "task": f"Estudar {topic} por 25 minutos e resolver 5 exercícios.",
            "goal": goal
        })
    return plan

def tutor_reply(message: str) -> str:
    msg = normalize_text(message)

    if "fração" in msg or "fracao" in msg:
        return (
            "Frações representam partes de um todo. "
            "Por exemplo, 1/2 significa uma de duas partes iguais. "
            "Se quiser, eu também posso te mostrar como somar frações."
        )

    if "porcentagem" in msg:
        return (
            "Porcentagem é uma parte de 100. "
            "Exemplo: 25% de 200 = 200 × 0,25 = 50."
        )

    if "equação" in msg or "equacao" in msg:
        return (
            "Equação é como uma balança: os dois lados precisam ficar iguais. "
            "Exemplo: 3x = 18. Então x = 18 ÷ 3, ou seja, x = 6."
        )

    if "área" in msg or "area" in msg:
        return "Área é o espaço dentro de uma figura. No retângulo, fazemos base × altura."

    if "não entendi" in msg or "nao entendi" in msg:
        return "Tudo bem. Me fala exatamente qual conta ou tema te confundiu que eu explico mais devagar."

    if "oi" in msg or "olá" in msg or "ola" in msg:
        return "Oi! Eu sou o tutor da Estuda+. Posso te ajudar com matemática de um jeito simples."

    return (
        "Posso te ajudar com matemática, frações, porcentagem, equações e geometria. "
        "Pergunte algo como: 'explique frações' ou 'como fazer porcentagem?'."
    )

def show_plan():
    if not st.session_state.study_plan:
        return

    st.markdown("### Plano de estudos")
    for item in st.session_state.study_plan:
        st.markdown(
            f"""
            <div class="info-card">
                <strong>{item["day"]}</strong><br>
                <strong>Tema:</strong> {item["topic"]}<br>
                <strong>Atividade:</strong> {item["task"]}<br>
                <strong>Objetivo:</strong> {item["goal"]}
            </div>
            """,
            unsafe_allow_html=True
        )

def process_user_input(user_input: str) -> None:
    text = user_input.strip()
    normalized = normalize_text(text)

    add_user_message(text)

    # =====================================================
    # FLOW
    # =====================================================
    if st.session_state.step == "welcome":
        st.session_state.student_name = text
        st.session_state.step = "grade"
        add_bot_message(
            f"Prazer, {st.session_state.student_name}! Em que ano/série você está?"
        )
        return

    if st.session_state.step == "grade":
        st.session_state.student_grade = text
        st.session_state.step = "goal"
        add_bot_message(
            "Boa. E qual é seu principal objetivo em matemática agora? "
            "Exemplo: melhorar notas, aprender base, me preparar para prova."
        )
        return

    if st.session_state.step == "goal":
        st.session_state.student_goal = text
        st.session_state.step = "diagnostic"
        st.session_state.diagnostic_index = 0
        st.session_state.diagnostic_score = 0
        st.session_state.diagnostic_answers = []
        first_q = diagnostic_questions[0]["question"]
        add_bot_message(
            "Perfeito. Agora vamos fazer um diagnóstico rápido com 5 perguntas. "
            f"Primeira pergunta:\n\n**{first_q}**"
        )
        return

    if st.session_state.step == "diagnostic":
        idx = st.session_state.diagnostic_index
        current_q = diagnostic_questions[idx]
        correct_answer = normalize_text(current_q["answer"])

        st.session_state.diagnostic_answers.append(
            {
                "question": current_q["question"],
                "user_answer": text,
                "correct_answer": current_q["answer"],
                "topic": current_q["topic"]
            }
        )

        if normalized == correct_answer:
            st.session_state.diagnostic_score += 1

        st.session_state.diagnostic_index += 1

        if st.session_state.diagnostic_index < len(diagnostic_questions):
            next_q = diagnostic_questions[st.session_state.diagnostic_index]["question"]
            add_bot_message(f"Próxima pergunta:\n\n**{next_q}**")
        else:
            score = st.session_state.diagnostic_score
            level = get_diagnostic_level(score)
            st.session_state.diagnostic_level = level
            st.session_state.study_plan = generate_study_plan(
                level,
                st.session_state.student_goal
            )
            st.session_state.step = "main_chat"

            add_bot_message(
                f"Diagnóstico concluído, {st.session_state.student_name}!\n\n"
                f"Você acertou **{score} de {len(diagnostic_questions)}** perguntas.\n"
                f"Seu nível estimado é: **{level}**.\n\n"
                "Eu já gerei um plano de estudos para você. "
                "Agora você pode conversar comigo normalmente no chat e pedir coisas como:\n"
                "- explique frações\n"
                "- monte exercícios\n"
                "- revise porcentagem\n"
                "- o que eu preciso melhorar?"
            )
        return

    if st.session_state.step == "main_chat":
        if "o que eu preciso melhorar" in normalized or "melhorar" in normalized:
            weak_topics = []

            for item in st.session_state.diagnostic_answers:
                if normalize_text(item["user_answer"]) != normalize_text(item["correct_answer"]):
                    weak_topics.append(item["topic"])

            if weak_topics:
                topics_text = ", ".join(weak_topics)
                add_bot_message(
                    f"Pelos seus resultados, você precisa reforçar principalmente: **{topics_text}**."
                )
            else:
                add_bot_message(
                    "Você foi muito bem no diagnóstico. Seu foco agora pode ser aprofundar e praticar mais."
                )
            return

        if "plano" in normalized:
            add_bot_message("Seu plano de estudos está logo abaixo na tela.")
            return

        if "exercício" in normalized or "exercicio" in normalized:
            add_bot_message(
                "Claro. Aqui vai um exercício:\n\n"
                "**Quanto é 30% de 150?**\n\n"
                "Me mande sua resposta no chat que eu corrijo."
            )
            return

        if normalized in ["45", "quarenta e cinco"]:
            previous_bot = ""
            for msg in reversed(st.session_state.messages[:-1]):
                if msg["role"] == "assistant":
                    previous_bot = normalize_text(msg["content"])
                    break

            if "30% de 150" in previous_bot:
                add_bot_message("Correto! 30% de 150 = 45. Muito bem.")
                return

        add_bot_message(tutor_reply(text))
        return


# =========================================================
# INITIAL BOT MESSAGE
# =========================================================
if not st.session_state.started:
    add_bot_message(
        "Oi! Eu sou a **Estuda+** 📘\n\n"
        "**Aprendendo no seu ritmo**\n\n"
        "Vamos começar. Qual é o seu nome?"
    )
    st.session_state.started = True


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 📘 Estuda+")
    st.caption("Aprendendo no seu ritmo")

    st.markdown("---")
    st.markdown(
        f"""
        <div class="info-card">
            <strong>Aluno:</strong> {st.session_state.student_name or "-"}<br>
            <strong>Série:</strong> {st.session_state.student_grade or "-"}<br>
            <strong>Nível:</strong> {st.session_state.diagnostic_level or "-"}<br>
            <strong>Data:</strong> {datetime.now().strftime('%d/%m/%Y')}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Reiniciar conversa"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="title-box">
    <h1 style="margin-bottom:6px;">Estuda+</h1>
    <div style="font-size:20px;">Aprendendo no seu ritmo</div>
    <div class="gold-line"></div>
    <div>Chat com diagnóstico, plano de estudos e tutor de matemática.</div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MAIN LAYOUT
# =========================================================
col1, col2 = st.columns([2.1, 1.1])

with col1:
    st.markdown("### Chat")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Digite sua resposta ou sua dúvida em matemática...")
    if prompt:
        process_user_input(prompt)
        st.rerun()

with col2:
    st.markdown("### Resumo")

    st.markdown(
        """
        <div class="info-card">
            <strong>Como funciona</strong><br><br>
            1. O aluno responde no chat<br>
            2. Faz o diagnóstico<br>
            3. Recebe nível estimado<br>
            4. Ganha um plano de estudos<br>
            5. Continua tirando dúvidas no tutor
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.diagnostic_level:
        st.markdown(
            f"""
            <div class="info-card">
                <strong>Nível estimado:</strong><br>
                {st.session_state.diagnostic_level}
            </div>
            """,
            unsafe_allow_html=True
        )

    show_plan()
