
from .base_agent import BaseAgent
from azure_client import call_azure_chat

class TechAgent(BaseAgent):
    def act(self, ticket_text):
        # Tech agent tries to find steps in knowledge base (self.docs) and craft a resolution
        kb = self.docs.search(ticket_text) if self.docs else 'No KB available.'
        prompt = f"""You are a Technical Support agent. Given the ticket and KB, propose a step-by-step resolution.
Ticket: {ticket_text}
KB summary: {kb}
Output JSON: {{'resolution_steps': [..], 'confidence': 'high/medium/low'}}
"""
        resp = call_azure_chat(prompt, temperature=0.1)
        content = resp.get('content','').strip()
        try:
            import json
            parsed = json.loads(content)
            return parsed
        except:
            # fallback: simple resolution template
            return {'resolution_steps': ['Verify order and payment', 'Initiate refund if applicable', 'Notify customer'], 'confidence': 'medium'}
