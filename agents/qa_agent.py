from .base_agent import BaseAgent
from azure_client import call_azure_chat
import json

class QAAgent(BaseAgent):
    def act(self, proposed_resolution, original_ticket):
        prompt = f"""
        You are a QA reviewer in a customer support workflow.
        Review the proposed resolution below for correctness, empathy, tone, and clarity.
        If it’s not suitable, rewrite it to be clear and helpful.
        Return a JSON with keys:
        - approved: true/false
        - feedback: a one-line comment on the quality
        - final_message: what should be sent to the customer

        Proposed resolution: {proposed_resolution}
        Original ticket: {original_ticket}
        """
        resp = call_azure_chat(prompt, temperature=0.4)
        content = resp.get("content", "").strip()

        # Try to parse the JSON LLM output
        try:
            parsed = json.loads(content)
            return parsed
        except:
            # Dynamic fallback if JSON parsing fails
            base_msg = f"I understand your concern regarding: '{original_ticket}'."
            if "refund" in original_ticket.lower() or "charged" in original_ticket.lower():
                msg = base_msg + " We have initiated a refund process. You will receive confirmation soon."
            elif "app" in original_ticket.lower() or "crash" in original_ticket.lower():
                msg = base_msg + " Please reinstall the app and ensure it’s updated to the latest version."
            elif "subscription" in original_ticket.lower():
                msg = base_msg + " You can change your subscription by visiting your account settings under 'Billing'."
            else:
                msg = base_msg + " Our team is reviewing your request and will get back shortly."
            
            return {
                "approved": True,
                "feedback": "Generated custom fallback message",
                "final_message": msg
            }
