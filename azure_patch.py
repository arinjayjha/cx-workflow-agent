# azure_patch.py
# ============================================================
# Global patch: remove deprecated 'proxies' argument from AzureOpenAI
# ============================================================
import sys
import openai
from openai import AzureOpenAI

class PatchedAzureOpenAI(AzureOpenAI):
    def __init__(self, *args, **kwargs):
        if "proxies" in kwargs:
            kwargs.pop("proxies")
        super().__init__(*args, **kwargs)

# Apply patch before anything else loads
openai.AzureOpenAI = PatchedAzureOpenAI
openai.OpenAI = PatchedAzureOpenAI
sys.modules["openai"].AzureOpenAI = PatchedAzureOpenAI

print("[Patch Applied EARLY] AzureOpenAI proxies arg globally removed.")
