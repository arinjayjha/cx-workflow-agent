# azure_patch.py
"""
This module patches the OpenAI Azure client globally
before CrewAI imports it, to remove deprecated arguments like 'proxies'.
"""

import sys
import openai
from openai import AzureOpenAI

class PatchedAzureOpenAI(AzureOpenAI):
    def __init__(self, *args, **kwargs):
        # CrewAI passes proxies even when not needed
        if "proxies" in kwargs:
            kwargs.pop("proxies")
        super().__init__(*args, **kwargs)

# Inject into module system early
openai.AzureOpenAI = PatchedAzureOpenAI
openai.OpenAI = PatchedAzureOpenAI
sys.modules["openai"].AzureOpenAI = PatchedAzureOpenAI
sys.modules["openai"].OpenAI = PatchedAzureOpenAI

print("[✅ Patch Loaded] AzureOpenAI 'proxies' arg removed globally.")
