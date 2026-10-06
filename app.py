# app.py

import streamlit as st

from interview_questions import INTERVIEW_QUESTIONS

from evaluator import evaluate_answer


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Interview Practice System",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .question-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #f2f5ff;
        border: 1px solid #d8def5;
        margin-bottom: 20px;
    }

    .score-box {
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #ddd;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "started" not in st.session_state:

    st.session_state.started = False


if "question_number" not in st.session_state:

    st.session_state.question_number = 0


if "questions" not in st.session_state:

    st.session_state.questions = []


if "results" not in st.session_state:

    st.session_state.results = []


if "student_name" not in st.session_state:

    st.session_state.student_name = ""


if "role" not in st.session_state:

    st.session_state.role = ""


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🎯 AI-Based Interview Practice System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Practice interviews and receive AI-based feedback</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.header("Interview Setup")

    student_name = st.text_input(
        "Enter your name",
        value=st.session_state.student_name
    )

    role = st.selectbox(
        "Select interview category",
        list(INTERVIEW_QUESTIONS.keys())
    )

    st.markdown("---")

    st.write("### How it works")

    st.write(
        "1. Select your interview category."
    )

    st.write(
        "2. Read the interview question."
    )

    st.write(
        "3. Write your answer."
    )

    st.write(
        "4. Submit your answer."
    )

    st.write(
        "5. Receive AI-based score and feedback."
    )


# --------------------------------------------------
# START INTERVIEW
# --------------------------------------------------

if not st.session_state.started:

    st.subheader("Start Your Interview")

    st.write(
        "Prepare yourself for technical and HR interviews."
    )

    if st.button(
        "🚀 Start Interview",
        type="primary"
    ):

        if student_name.strip() == "":

            st.warning(
                "Please enter your name first."
            )

        else:

            st.session_state.student_name = student_name

            st.session_state.role = role

            st.session_state.questions = INTERVIEW_QUESTIONS[role]

            st.session_state.question_number = 0

            st.session_state.results = []

            st.session_state.started = True

            st.rerun()


# --------------------------------------------------
# INTERVIEW SCREEN
# --------------------------------------------------

else:

    questions = st.session_state.questions

    current_number = st.session_state.question_number

    total_questions = len(questions)


    # ----------------------------------------------
    # HEADER
    # ----------------------------------------------

    st.subheader(
        f"Hello, {st.session_state.student_name}! 👋"
    )

    st.write(
        f"Interview Category: **{st.session_state.role}**"
    )

    st.progress(
        (current_number) / total_questions
    )

    st.write(
        f"Question {current_number + 1} of {total_questions}"
    )


    # ----------------------------------------------
    # QUESTION
    # ----------------------------------------------

    current_question = questions[current_number]

    st.markdown(
        f"""
        <div class="question-box">

        <h3>Question {current_number + 1}</h3>

        <p>{current_question["question"]}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ----------------------------------------------
    # ANSWER
    # ----------------------------------------------

    answer = st.text_area(
        "Write your answer here:",
        height=180,
        placeholder="Type your interview answer..."
    )


    # ----------------------------------------------
    # SUBMIT ANSWER
    # ----------------------------------------------

    if st.button(
        "📊 Evaluate Answer",
        type="primary"
    ):

        if answer.strip() == "":

            st.warning(
                "Please write an answer before submitting."
            )

        else:

            result = evaluate_answer(
                answer,
                current_question["answer"],
                current_question["keywords"]
            )

            st.session_state.results.append(
                result
            )

            st.session_state.last_result = result

            st.rerun()


    # ----------------------------------------------
    # DISPLAY RESULT
    # ----------------------------------------------

    if "last_result" in st.session_state:

        result = st.session_state.last_result

        st.markdown("---")

        st.subheader("🤖 AI Evaluation")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Score",
                f"{result['score']}/10"
            )

        with col2:

            st.metric(
                "Answer Similarity",
                f"{result['similarity']}%"
            )

        with col3:

            st.metric(
                "Keyword Match",
                f"{result['keyword_score']}%"
            )


        st.info(
            f"💡 **Feedback:** {result['feedback']}"
        )


        with st.expander(
            "📚 View Suggested Answer"
        ):

            st.write(
                current_question["answer"]
            )


        # ------------------------------------------
        # NEXT QUESTION
        # ------------------------------------------

        if current_number < total_questions - 1:

            if st.button(
                "➡️ Next Question"
            ):

                st.session_state.question_number += 1

                if "last_result" in st.session_state:

                    del st.session_state.last_result

                st.rerun()

        else:

            st.success(
                "🎉 Interview completed!"
            )

            # --------------------------------------
            # FINAL SCORE
            # --------------------------------------

            results = st.session_state.results

            if results:

                average_score = sum(
                    r["score"] for r in results
                ) / len(results)

                st.markdown(
                    f"""
                    <div class="score-box">

                    <h2>🏆 Final Interview Score</h2>

                    <h1>{average_score:.1f}/10</h1>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # --------------------------------------
            # RESULT TABLE
            # --------------------------------------

            st.subheader("📊 Interview Summary")

            for i, result in enumerate(
                results,
                start=1
            ):

                st.write(
                    f"**Question {i}:** "
                    f"{result['score']}/10"
                )

            st.markdown("---")


            # --------------------------------------
            # RESTART
            # --------------------------------------

            if st.button(
                "🔄 Start New Interview"
            ):

                st.session_state.started = False

                st.session_state.question_number = 0

                st.session_state.questions = []

                st.session_state.results = []

                if "last_result" in st.session_state:

                    del st.session_state.last_result

                st.rerun()