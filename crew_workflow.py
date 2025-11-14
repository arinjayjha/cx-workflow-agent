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
    """Safe Azure OpenAI call that avoids 'proxies' errors."""
    from openai import AzureOpenAI

    try:
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

        print(f"[Azure Debug] Endpoint: {endpoint}")
        print(f"[Azure Debug] Deployment: {deployment}")
        print(f"[Azure Debug] API key exists: {bool(api_key)}")

        client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
        )

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful AI support assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )

        if not response or not response.choices:
            return "[AzureAgent] No response or empty choices from Azure."

        output = response.choices[0].message.content.strip()
        print(f"[AzureAgent Response] {output[:200]}...")
        return output

    except Exception as e:
        print(f"[AzureAgent Error] {e}")
        return f"[AzureAgent] Azure error: {e}"


# ===============================================================
# AzureAgent Class (CrewAI-Compatible Wrapper)
# ===============================================================
class AzureAgent(Agent):
    """A CrewAI Agent subclass using Azure OpenAI directly."""

    def __init__(self, **kwargs):
        # Disable CrewAI’s built-in llm binding (we’ll handle manually)
        kwargs["llm"] = None
        super().__init__(**kwargs)

    def execute_task(self, task, context=None, tools=None):
        """Use Azure API for executing CrewAI task."""
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

    # Prevent CrewAI from trying to call llm.bind()
    def create_agent_executor(self):
        self.agent_executor = None


# ===============================================================
# Initialize Multi-Agent Workflow
# ===============================================================
def run_cx_workflow(ticket_text: str):
    """Simulates a multi-agent customer support workflow."""
    # Agents
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

    # Tasks
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

    # Crew Orchestration
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
