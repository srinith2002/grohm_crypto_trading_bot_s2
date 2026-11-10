
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
from pathlib import Path

# ==========================================
# PROJECT PATH CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

DATA_DIR = BASE_DIR / "data" / "candles"

# ==========================================
# PROJECT IMPORTS
# ==========================================

from genai.chat_assistant import ask_grohm_ai
from genai.config import check_configuration
from agentic_ai.orchestrator import GrohmAgenticOrchestrator

# ==========================================
# STREAMLIT CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="GROHM Markets",
    page_icon="📊",
    layout="wide"
)

st.title("📊 GROHM MARKETS")
st.caption(
    "Unified Trading | Machine Learning | "
    "Artificial Intelligence | Agentic AI | GenAI"
)

# ==========================================
# DATA FILES
# ==========================================

FILES = {

    # CORE
    "Market Data": "BTCUSD_30m.csv",
    "Data Validation": "BTCUSD_30m_validated.csv",
    "Technical Indicators": "BTCUSD_30m_indicators.csv",
    "Candlestick Analysis": "BTCUSD_30m_candlestick.csv",
    "Flexi Matrix": "BTCUSD_30m_flexi_matrix.csv",
    "Risk Management": "BTCUSD_30m_risk_results.csv",
    "Paper Trading": "BTCUSD_30m_paper_trades.csv",
    "Trade Monitoring": "BTCUSD_30m_trade_monitoring.csv",
    "Performance Analysis": "BTCUSD_30m_performance.csv",

    # ML
    "ML Dataset": "BTCUSD_30m_ml_dataset.csv",
    "Linear Regression": "BTCUSD_30m_linear_regression_results.csv",
    "Random Forest": "BTCUSD_30m_random_forest_results.csv",
    "XGBoost": "BTCUSD_30m_xgboost_results.csv",
    "Ensemble Learning": "BTCUSD_30m_ensemble_results.csv",
    "Model Comparison": "BTCUSD_30m_model_comparison.csv",

    # AI
    "AI Prediction": "BTCUSD_30m_ai_prediction.csv",
    "AI Signal": "BTCUSD_30m_ai_signal.csv",
    "Market Regime": "BTCUSD_30m_market_regime.csv",
    "Anomaly Detection": "BTCUSD_30m_anomalies.csv",
    "AI Explanation": "BTCUSD_30m_ai_explanation.csv",
    "LSTM Deep Learning": "BTCUSD_30m_lstm_prediction.csv",
    "Sentiment Analysis": "BTCUSD_30m_sentiment.csv",
    "Strategy Optimizer": "BTCUSD_30m_strategy_optimizer.csv",
}

# ==========================================
# LOAD DATA
# ==========================================

def load_data(category):

    filename = FILES.get(category)

    if filename is None:
        return None

    path = DATA_DIR / filename

    if not path.exists():
        return None

    try:
        return pd.read_csv(path)

    except Exception as error:
        st.error(f"Unable to read {filename}: {error}")
        return None


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("GROHM Navigation")

section = st.sidebar.radio(
    "Select Module",
    [
        "Overview",
        "Core Trading Agents",
        "Machine Learning",
        "Artificial Intelligence",
        "GROHM AI Assistant"
    ]
)

core_options = [
    "Market Data",
    "Data Validation",
    "Technical Indicators",
    "Candlestick Analysis",
    "Flexi Matrix",
    "Risk Management",
    "Paper Trading",
    "Trade Monitoring",
    "Performance Analysis"
]

ml_options = [
    "ML Dataset",
    "Linear Regression",
    "Random Forest",
    "XGBoost",
    "Ensemble Learning",
    "Model Comparison"
]

ai_options = [
    "AI Prediction",
    "AI Signal",
    "Market Regime",
    "Anomaly Detection",
    "AI Explanation",
    "LSTM Deep Learning",
    "Sentiment Analysis",
    "Strategy Optimizer"
]

# ==========================================
# REUSABLE DISPLAY FUNCTION
# ==========================================

def display_data(category):

    st.subheader(category)

    df = load_data(category)

    if df is None:
        st.warning(
            f"Data file not found or unreadable: "
            f"{FILES.get(category)}"
        )
        return

    if df.empty:
        st.warning("Dataset is empty.")
        return

    col1, col2 = st.columns(2)

    col1.metric("Total Records", len(df))
    col2.metric("Total Columns", len(df.columns))

    st.dataframe(
        df.tail(100),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=FILES[category],
        mime="text/csv"
    )


# ==========================================
# OVERVIEW
# ==========================================

if section == "Overview":

    st.subheader("GROHM Project Overview")

    core_count = sum(
        1 for name in core_options
        if load_data(name) is not None
    )

    ml_count = sum(
        1 for name in ml_options
        if load_data(name) is not None
    )

    ai_count = sum(
        1 for name in ai_options
        if load_data(name) is not None
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Core Outputs",
        f"{core_count}/{len(core_options)}"
    )

    col2.metric(
        "ML Outputs",
        f"{ml_count}/{len(ml_options)}"
    )

    col3.metric(
        "AI Outputs",
        f"{ai_count}/{len(ai_options)}"
    )

    st.divider()

    st.subheader("Project Architecture")

    st.markdown("""
    **CORE TRADING**

    Market Data → Validation → Indicators → Candlesticks
    → Flexi Matrix → Risk Management → Paper Trading
    → Trade Monitoring → Performance Analysis

    **MACHINE LEARNING**

    ML Dataset → Linear Regression → Random Forest
    → XGBoost → Ensemble Learning → Model Comparison

    **ARTIFICIAL INTELLIGENCE**

    AI Prediction → AI Signal → Market Regime
    → Anomaly Detection → AI Explanation → LSTM
    → NLP Sentiment → Strategy Optimizer

    **AGENTIC AI**

    Market Data Agent → Technical Analysis Agent
    → Strategy Agent → Risk Analysis Agent
    → ML Prediction Agent → Decision Agent
    → AI Explanation Agent

    **GENERATIVE AI**

    GROHM AI Assistant → Google Gemini
    """)

    st.info(
        "GROHM is an educational historical analysis and "
        "paper-simulation project. Dashboard metrics do not "
        "guarantee future performance."
    )


# ==========================================
# CORE TRADING AGENTS
# ==========================================

elif section == "Core Trading Agents":

    selected = st.sidebar.selectbox(
        "Select Core Agent",
        core_options
    )

    display_data(selected)


# ==========================================
# MACHINE LEARNING
# ==========================================

elif section == "Machine Learning":

    selected = st.sidebar.selectbox(
        "Select ML Category",
        ml_options
    )

    display_data(selected)


# ==========================================
# ARTIFICIAL INTELLIGENCE
# ==========================================

elif section == "Artificial Intelligence":

    selected = st.sidebar.selectbox(
        "Select AI Category",
        ai_options
    )

    display_data(selected)


# ==========================================
# GROHM AI ASSISTANT
# AGENTIC AI + GEMINI GENAI
# ==========================================

elif section == "GROHM AI Assistant":

    st.title("🤖 GROHM AI Assistant")

    agentic_tab, gemini_tab = st.tabs([
        "Agentic AI Workflow",
        "Gemini AI Assistant"
    ])

    # ======================================
    # TAB 1: AGENTIC AI WORKFLOW
    # ======================================

    with agentic_tab:

        st.subheader("GROHM Agentic AI System")

        st.caption(
            "Seven-agent workflow using existing GROHM "
            "market data, technical analysis, strategy, "
            "risk and ML outputs."
        )

        st.markdown("### Agent Architecture")

        agent_names = [
            "1. Market Data Agent",
            "2. Technical Analysis Agent",
            "3. Strategy Agent",
            "4. Risk Analysis Agent",
            "5. ML Prediction Agent",
            "6. Decision Agent",
            "7. AI Explanation Agent"
        ]

        for agent in agent_names:
            st.write(f"✅ {agent}")

        st.divider()

        st.subheader("Run Agentic AI Analysis")

        question = st.text_input(
            "Enter your analysis question",
            value="Analyze BTCUSD"
        )

        if st.button(
            "🚀 Run Agentic AI Workflow",
            type="primary",
            use_container_width=True
        ):

            if not question.strip():

                st.warning("Please enter a question.")

            else:

                try:

                    with st.spinner(
                        "GROHM agents are analyzing the market..."
                    ):

                        orchestrator = GrohmAgenticOrchestrator()

                        result = orchestrator.run_workflow(question)

                        st.session_state[
                            "grohm_agentic_result"
                        ] = result

                    st.success(
                        "All seven agents executed successfully!"
                    )

                except Exception as error:

                    st.error(
                        f"Agentic AI Workflow Error: {error}"
                    )

        # ==================================
        # DISPLAY WORKFLOW RESULTS
        # ==================================

        if "grohm_agentic_result" in st.session_state:

            result = st.session_state[
                "grohm_agentic_result"
            ]

            st.divider()

            st.subheader("Workflow Results")

            decision = result.get("decision", {})
            market = result.get("market_data", {})
            strategy = result.get("strategy_analysis", {})
            risk = result.get("risk_analysis", {})
            technical = result.get("technical_analysis", {})
            ml = result.get("ml_prediction", {})
            explanation = result.get("ai_explanation", {})

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Workflow Status",
                result.get("workflow_status", "UNKNOWN")
            )

            col2.metric(
                "Final Decision",
                decision.get("decision", "UNKNOWN")
            )

            col3.metric(
                "Market Price",
                f"{market.get('latest_close', 0):,.2f}"
            )

            col4.metric(
                "Strategy Score",
                strategy.get("total_score", 0)
            )

            st.divider()

            # Decision summary
            st.subheader("Final Decision")

            if decision.get("decision") == "HOLD":

                st.warning("GROHM Decision: HOLD")

            elif decision.get("decision") == "PAPER_REVIEW_REQUIRED":

                st.info(
                    "Paper review required. "
                    "No orders are placed."
                )

            else:

                st.info(
                    f"Decision: {decision.get('decision')}"
                )

            st.write(
                explanation.get(
                    "summary",
                    "No explanation available."
                )
            )

            st.caption(
                "Execution enabled: "
                f"{decision.get('execution_enabled', False)}"
            )

            st.divider()

            # Technical Analysis
            with st.expander("Technical Analysis Agent"):

                st.json(technical)

            # Strategy
            with st.expander("Strategy Agent"):

                st.json(strategy)

            # Risk
            with st.expander("Risk Analysis Agent"):

                st.json(risk)

            # ML Prediction
            with st.expander("ML Prediction Agent"):

                st.json(ml)

            # Decision
            with st.expander("Decision Agent"):

                st.json(decision)

            # AI Explanation
            with st.expander("AI Explanation Agent"):

                st.write(explanation.get("summary", ""))

                for reason in explanation.get(
                    "explanation", []
                ):

                    st.write(f"• {reason}")

            # Complete results
            with st.expander("Complete Agentic AI Output"):

                st.json(result)

            st.caption(
                "Agentic AI currently uses rule-based Python "
                "agents and existing CSV outputs. It is not "
                "a live Gemini-powered workflow."
            )

    # ======================================
    # TAB 2: GEMINI AI ASSISTANT
    # ======================================

    with gemini_tab:

        st.subheader("GROHM Gemini AI Assistant")

        st.caption("Google Gemini integration")

        config = check_configuration()

        col1, col2 = st.columns(2)

        col1.metric(
            "Provider",
            config["provider"]
        )

        col2.metric(
            "Model",
            config["model"]
        )

        if config["api_key_configured"]:

            st.success("Gemini credential detected.")

        else:

            st.warning(
                "Gemini authentication is pending."
            )

        st.divider()

        st.subheader("Chat with GROHM AI")

        st.write(
            "Ask questions about cryptocurrency concepts, "
            "technical indicators, Flexi Matrix, machine learning "
            "and your GROHM project."
        )

        # Initialize chat history
        if "grohm_chat_history" not in st.session_state:

            st.session_state.grohm_chat_history = []

        # Display previous conversations
        for chat in st.session_state.grohm_chat_history:

            with st.chat_message(chat["role"]):

                st.write(chat["content"])

        # Chat input
        gemini_question = st.chat_input(
            "Ask GROHM AI anything..."
        )

        if gemini_question:

            st.session_state.grohm_chat_history.append({
                "role": "user",
                "content": gemini_question
            })

            with st.chat_message("user"):

                st.write(gemini_question)

            with st.chat_message("assistant"):

                with st.spinner("GROHM AI is thinking..."):

                    try:

                        answer = ask_grohm_ai(gemini_question)

                        st.write(answer)

                        st.session_state.grohm_chat_history.append({
                            "role": "assistant",
                            "content": answer
                        })

                    except Exception as error:

                        st.error(
                            f"Gemini Connection Error: {error}"
                        )

        if st.button("Clear Chat"):

            st.session_state.grohm_chat_history = []

            st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "GROHM MARKETS | Core + ML + AI + "
    "Agentic AI + Gemini GenAI Dashboard"
)

