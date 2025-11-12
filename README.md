
# 🤖 CX Workflow — Multi-Agent System (CrewAI + LangGraph + Streamlit)

A **professional, animated customer experience (CX) automation system** that demonstrates how multiple AI agents (Support → Technical → QA) collaborate to resolve customer issues seamlessly.  
This project integrates **CrewAI**, **LangGraph**, and **Streamlit** into a single orchestrated multi-agent environment for real-world simulation and visualization.

---

## 🧠 Overview

Customer support operations often involve multiple teams — **Support Representatives**, **Technical Specialists**, and **Quality Assurance (QA) Reviewers**.  
This project automates that exact workflow using multi-agent coordination logic, visualized through an elegant Streamlit interface.

It combines:

- 🧩 **CrewAI** for agent collaboration and reasoning
- 🔗 **LangGraph** for graph-based flow visualization
- 🖥️ **Streamlit** for professional, interactive UI with real-time animation
- ☁️ **Azure OpenAI** or **OpenAI** models for reasoning, empathy, and conversation handling

---

## 🚀 Features

✅ Multi-agent workflow simulation (Support → Tech → QA)  
✅ Animated **LangGraph** visualization with dynamic agent highlighting  
✅ Professional **black-themed Streamlit UI** with glowing buttons  
✅ CrewAI-based orchestration with Azure/OpenAI backend  
✅ Modular architecture (easy to extend with more agents)  
✅ Built-in error handling and customizable reasoning chains  

---

## 🏗️ Architecture

```
+--------------------------------------------------------------+
|                        CX WORKFLOW SYSTEM                    |
|                                                              |
|   ┌──────────────┐      ┌────────────────┐      ┌──────────┐  |
|   │ Support      │  →   │ Technical      │  →   │ QA       │  |
|   │ Agent        │      │ Expert Agent   │      │ Reviewer │  |
|   └──────────────┘      └────────────────┘      └──────────┘  |
|                                                              |
|      CrewAI Agents orchestrate via LangGraph state flow.     |
|      Streamlit provides visualization & user interface.      |
+--------------------------------------------------------------+
```

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/arinjayjha/cx-workflow-agent.git
cd cx-workflow-agent
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
# OR
source .venv/bin/activate     # macOS/Linux
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Create a `.env` file in the project root:

```
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
# OR (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key
```

---

## 🧩 Project Structure

```
cx-workflow-agent/
│
├── streamlit_app.py         # Streamlit UI (main entry)
├── crew_workflow.py         # CrewAI logic and agents
├── workflow_graph.py        # LangGraph visualization + animation
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore list
├── .env                     # Environment variables (ignored in Git)
└── README.md                # Documentation (this file)
```

---

## 🎬 Running the App

Start the Streamlit server:

```bash
streamlit run streamlit_app.py
```

Once running, open your browser at:

> 🌐 http://localhost:8501

You’ll see:
- Animated **Agent Flow Visualization**
- Text input for new customer issues
- Real-time workflow simulation

---

## 🎨 UI Design Philosophy

The interface uses a **sleek black theme** with glowing blue and cyan highlights, inspired by modern SaaS dashboards.  
Typography and gradients are chosen to enhance professional presentation while keeping readability high.

**UI Highlights:**
- Black background (#000000)
- Blue action buttons (#0078ff → #00a2ff gradient)
- Cyan glow for active agents
- Smooth transitions and readable contrast

---

## 🧠 Example Workflow

### Input:
> “My order was cancelled but I was charged ₹899. Please help.”

### Step-by-Step Flow:
1. 🧩 **Customer Support Agent**
   - Reads and classifies the customer issue.
   - Decides whether escalation to Technical Expert is needed.

2. ⚙️ **Technical Expert**
   - Investigates technical cause (refund logic, system error, etc.)
   - Suggests solution or system fix.

3. 🧾 **QA Reviewer**
   - Refines the final response tone and grammar.
   - Ensures empathy, professionalism, and customer reassurance.

### Output:
> “Dear Customer, thank you for reporting this issue. We’ve verified the ₹899 charge and initiated your refund, which will be credited within 5–7 business days. We sincerely apologize for the inconvenience.”

---

## 🧮 Tech Stack

| Layer | Technology |
|-------|-------------|
| **Frontend** | Streamlit |
| **Agents** | CrewAI |
| **Flow Orchestration** | LangGraph |
| **Reasoning Engine** | Azure OpenAI / OpenAI GPT |
| **Visualization** | Matplotlib + NetworkX |
| **Environment** | Python 3.10+ |

---

## 📦 Requirements

```
streamlit
crewai
langgraph
matplotlib
networkx
openai
python-dotenv
```
(Use `pip install -r requirements.txt` to auto-install.)

---

## 🧰 Customization Tips

- You can **add more agents** by editing `crew_workflow.py`
- Adjust **animation timing** in `workflow_graph.py` (default 1.2s)
- Modify **themes** via CSS in `streamlit_app.py` (`st.markdown(<style>...</style>)`)

---

## 🔒 Security Best Practices

- Never commit your `.env` file
- Always use `.gitignore` to exclude secrets
- Use Azure role-based credentials if deploying to cloud

---

## 🌍 Deployment (Optional)

### Deploy to Streamlit Cloud:

```bash
# In your project root
git push origin main
```

Then visit [https://share.streamlit.io](https://share.streamlit.io), connect your GitHub repo, and deploy.

### Or via Docker (Advanced):

```bash
docker build -t cx-workflow-agent .
docker run -p 8501:8501 cx-workflow-agent
```

---

## 🧾 Example Outputs

### 🧠 Agent Logs (JSON format)
```json
{
  "Customer Support": "Classified and summarized the customer issue.",
  "Technical Expert": "Suggested corrective steps and technical diagnosis.",
  "QA Reviewer": "Refined final message tone and ensured empathy."
}
```

---

## 🧑‍💻 Contributors

| Name | Role | Contribution |
|------|------|---------------|
| **Arinjay Jha** | Creator / Developer | Design, architecture, and implementation |

---

## 🧷 License

This project is open-sourced under the **MIT License**.  
You are free to use, modify, and distribute with attribution.

---

## 💬 Contact

For collaboration or feedback:  
📧 [arinjayjha@gmail.com](mailto:arinjayjha@gmail.com)  
🌐 [https://github.com/arinjayjha](https://github.com/arinjayjha)

---

⭐ If you like this project, consider starring the repository on GitHub!
