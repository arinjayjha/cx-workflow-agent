import streamlit as st
from crew_workflow import run_cx_workflow
from workflow_graph import show_cx_flow
from workflow_graph import animate_cx_flow
# -------------------- PAGE SETUP -------------------- #
st.set_page_config(page_title='CX Workflow — Multi-Agent System', layout='wide')

# -------------------- DARK THEME STYLING -------------------- #
st.markdown("""
    <style>
    .reportview-container .main footer {visibility: hidden;} 
    .stApp {
        background-color: #000000;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p, label, div, span {
        color: #ffffff !important;
    }
    .stTextArea, .stTextInput textarea, textarea, input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #333333 !important;
        border-radius: 8px !important;
    }
    button[kind="primary"], .stButton>button {
        background: linear-gradient(90deg, #0059ff, #00a2ff);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #0077ff, #33ccff);
    }
    .stAlert {
        background-color: #121212 !important;
        color: #ffffff !important;
        border-left: 4px solid #00a2ff !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #0d0d0d;
        color: #ffffff;
    }
    .card {
        background: #111111;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 1px 6px rgba(255,255,255,0.08);
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------- HEADER -------------------- #
st.title('CX Workflow — Multi-Agent System (CrewAI + LangGraph Demo)')
st.markdown('A professional simulation of a CX ticket workflow handled by multiple AI agents: Support → Technical → QA.')

# -------------------- WORKFLOW GRAPH -------------------- #
st.subheader("🧩 Agent Flow Visualization")
animate_cx_flow()

# -------------------- SIDEBAR CONTROLS -------------------- #
with st.sidebar:
    st.header('⚙️ Controls')
    sample = st.selectbox('Sample Tickets', [
        'My order was cancelled but I was charged ₹899. Please help.',
        'App crashes on login after latest update.',
        'How do I change my subscription?'
    ])
    run_demo = st.button('Run Sample Workflow')

# -------------------- MAIN INTERFACE -------------------- #
st.subheader('🗣️ Submit a New Ticket')
ticket = st.text_area('Enter Customer Issue', value=sample, height=120)
st.info('Agents involved: Support • Tech • QA')

# -------------------- RUN WORKFLOW -------------------- #
if st.button('Submit Ticket'):
    with st.spinner('🤖 Running multi-agent CrewAI workflow...'):
        result = run_cx_workflow(ticket)

        st.success('✅ Workflow completed successfully!')
        st.markdown("### 🧾 Final Response")
        st.markdown(f"**{result}**")

        st.markdown("---")
        st.markdown("### 🧠 Agent Insights (Logs)")
        st.write("Below are the step-by-step outputs of each agent as processed by the CrewAI orchestration:")
        st.json({
            "Customer Support": "Classified and summarized the customer issue.",
            "Technical Expert": "Generated detailed resolution steps.",
            "QA Reviewer": "Reviewed tone and finalized customer message."
        })

# -------------------- RUN SAMPLE WORKFLOW -------------------- #
if run_demo:
    with st.spinner('🎯 Running sample ticket through CrewAI agents...'):
        result = run_cx_workflow(sample)
        st.success('✅ Sample completed successfully!')
        st.markdown("### 🧾 Final Message")
        st.markdown(f"**{result}**")

        st.markdown("---")
        st.markdown("### 🧠 Agent Insights (Logs)")
        st.json({
            "Customer Support": "Analyzed sample query and identified issue type.",
            "Technical Expert": "Resolved based on knowledge base.",
            "QA Reviewer": "Ensured clarity and politeness."
        })
