# crew_workflow.py
# ===============================================================
#  PATCH: disable CrewAI's OpenAI LLM bootstrap before import
# ===============================================================
import sys, types

# Fake the create_llm function *before* CrewAI loads it
fake_llm_utils = types.SimpleNamespace()
fake_llm_utils.create_llm = lambda *a, **kw: None
sys.modules["crewai.utilities.llm_utils"] = fake_llm_utils

# ===============================================================
#  Now import CrewAI safely (it will use the patched llm_utils)
# ===============================================================
from crewai import Agent, Task, Crew
from azure_client import call_azure_chat
# ===============================================================

class AzureAgent(Agent):
    """Azure OpenAI–powered CrewAI agent."""
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        kwargs["llm"] = None  # explicit safety
        super().__init__(**kwargs)

    def execute_task(self, task, context=None, tools=None):
        prompt = f"""
        Role: {self.role}
        Goal: {self.goal}
        Task: {task.description}
        Context: {context}
        """
        result = call_azure_chat(prompt)
        return result.get("content", "[AzureAgent] No response from Azure.")
# -----------------------------------------------------------------

support_agent = AzureAgent(
    role="Customer Support",
    goal="Understand and classify the customer issue, decide if escalation is needed.",
    backstory="Empathetic CX rep skilled at understanding user sentiment."
)

tech_agent = AzureAgent(
    role="Technical Expert",
    goal="Provide detailed steps to resolve technical or billing issues using documentation.",
    backstory="Experienced support engineer who writes concise, accurate solutions."
)

qa_agent = AzureAgent(
    role="QA Reviewer",
    goal="Check correctness, empathy, and tone of the final response.",
    backstory="Ensures clarity and customer satisfaction."
)

task_support = Task(
    description="Classify and summarize the customer issue.",
    expected_output="JSON with keys: category, summary, next_step",
    agent=support_agent,
)

task_tech = Task(
    description="Generate resolution steps based on ticket and knowledge base.",
    expected_output="Resolution plan or customer message.",
    agent=tech_agent,
)

task_qa = Task(
    description="Review and finalize the message to send back to the customer.",
    expected_output="Final, polished customer message.",
    agent=qa_agent,
)

crew = Crew(
    name="CX Workflow Crew (Azure-based)",
    description="Customer support ticket handled via multi-agent collaboration.",
    agents=[support_agent, tech_agent, qa_agent],
    tasks=[task_support, task_tech, task_qa],
)

def run_cx_workflow(ticket_text):
    try:
        result = crew.kickoff(inputs={"ticket": ticket_text})
        return result
    except Exception as e:
        return f"[ERROR in run_cx_workflow] {e}"
