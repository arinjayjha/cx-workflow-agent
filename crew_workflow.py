import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew

# ===============================================================
# Load environment variables
# ===============================================================
load_dotenv()

# ===============================================================
# Azure Client Helper
# ===============================================================

def call_azure_chat(prompt: str):
    """
    This function sends a prompt to Azure OpenAI and returns the response.
    It uses your configured Azure OpenAI environment variables.
    """
    import openai

    try:
        client = openai.AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-02-01",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )

        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[AzureAgent Error] {e}")
        return "[AzureAgent] No response from Azure"


# ===============================================================
# AzureAgent Class (CrewAI-Compatible Wrapper)
# ===============================================================

class AzureAgent(Agent):
    """
    A subclass of CrewAI's Agent that uses Azure OpenAI for responses.
    It overrides CrewAI's LLM binding logic to prevent crashes when llm=None.
    """

    def __init__(self, **kwargs):
        # Disable CrewAI’s LLM binding (we’ll use Azure manually)
        kwargs["llm"] = None
        super().__init__(**kwargs)

    def execute_task(self, task, context=None, tools=None):
        """
        This replaces CrewAI's native execution logic with an Azure API call.
        """
        prompt = f"""
You are acting as: {self.role}
Your mission: {self.goal}
Backstory: {self.backstory}

Task:
{task}

Context:
{context or 'No additional context provided.'}
"""
        result = call_azure_chat(prompt)
        return result or "[AzureAgent] No response."

    # Override to bypass CrewAI’s internal LLM executor setup
    def create_agent_executor(self):
        """Prevent CrewAI from trying to call llm.bind()."""
        self.agent_executor = None


# ===============================================================
# Initialize Multi-Agent Workflow
# ===============================================================

def run_cx_workflow(ticket_text: str):
    """
    Simulates a multi-agent customer support workflow using CrewAI orchestration.
    """
    # Create agents
    support_agent = AzureAgent(
        role="Customer Support",
        goal="Understand and classify the customer issue, decide if escalation is required.",
        backstory="Empathetic CX representative skilled at understanding customer sentiment and classifying tickets."
    )

    tech_agent = AzureAgent(
        role="Technical Expert",
        goal="Diagnose the technical cause and propose a resolution plan.",
        backstory="Highly skilled technical engineer who resolves backend and infrastructure issues quickly."
    )

    qa_agent = AzureAgent(
        role="QA Reviewer",
        goal="Review the final response to ensure clarity, tone, and completeness.",
        backstory="Detail-oriented QA agent ensuring the message is professional and reassuring."
    )

    # Create tasks
    support_task = Task(
        description=f"Classify and summarize the customer ticket:\n\n{ticket_text}",
        expected_output="A brief summary of the issue and the relevant category.",
        agent=support_agent,
    )

    tech_task = Task(
        description="Provide detailed resolution steps or potential causes for the issue.",
        expected_output="Actionable technical resolution instructions.",
        agent=tech_agent,
    )

    qa_task = Task(
        description="Review and polish the final message for tone and professionalism.",
        expected_output="Final, polished customer-facing response.",
        agent=qa_agent,
    )

    # Create crew and orchestrate
    crew = Crew(
        agents=[support_agent, tech_agent, qa_agent],
        tasks=[support_task, tech_task, qa_task],
        verbose=True,
    )

    results = crew.kickoff()

    return {
        "Customer Support": support_task.output,
        "Technical Expert": tech_task.output,
        "QA Reviewer": qa_task.output,
        "Final": results,
    }
