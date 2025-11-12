
from .base_agent import BaseAgent
from azure_client import call_azure_chat

class SupportAgent(BaseAgent):
    def act(self, ticket_text):
        prompt = f"""You are a Customer Support agent. Read the ticket and:
1) Classify the ticket into one of: Billing, Technical, Policy, Other.
2) Provide a short summary (1 line) and recommended next step: either 'resolve' or 'escalate_to_tech'.
Ticket: {ticket_text}
Output JSON with keys: category, summary, next_step
"""
        resp = call_azure_chat(prompt)
        # Try to parse JSON from LLM, fallback to heuristic
        content = resp.get('content','').strip()
        try:
            import json
            parsed = json.loads(content)
            return parsed
        except:
            # Very simple heuristic fallback
            category = 'Billing' if 'charge' in ticket_text.lower() or 'refund' in ticket_text.lower() else 'Technical'
            summary = ticket_text[:120]
            next_step = 'resolve' if category == 'Billing' else 'escalate_to_tech'
            return {'category': category, 'summary': summary, 'next_step': next_step}
