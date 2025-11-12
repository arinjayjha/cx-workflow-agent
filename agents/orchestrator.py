
from .support_agent import SupportAgent
from .tech_agent import TechAgent
from .qa_agent import QAAgent

class Orchestrator:
    def __init__(self, docs, memory):
        self.support = SupportAgent('support', docs, memory)
        self.tech = TechAgent('tech', docs, memory)
        self.qa = QAAgent('qa', docs, memory)

    def handle_ticket(self, ticket_text):
        # Step 1: Support classification
        sup_out = self.support.act(ticket_text)
        category = sup_out.get('category') if isinstance(sup_out, dict) else 'Other'
        next_step = sup_out.get('next_step') if isinstance(sup_out, dict) else 'escalate_to_tech'

        # If support can resolve
        if next_step == 'resolve':
            # Let tech agent craft a resolution (for consistency)
            tech_out = self.tech.act(ticket_text)
            final = self.qa.act(tech_out, ticket_text)
            return final.get('final_message') if isinstance(final, dict) else str(final)

        # Escalate to tech
        tech_out = self.tech.act(ticket_text)
        qa_out = self.qa.act(tech_out, ticket_text)
        return qa_out.get('final_message') if isinstance(qa_out, dict) else str(qa_out)
