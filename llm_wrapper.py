from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Literal
import os

from dotenv import load_dotenv
load_dotenv()


# ---------- Message Schema ----------
print("OPENAI KEY LOADED:", bool(os.getenv("OPENAI_API_KEY")))
print("GEMINI KEY LOADED:", bool(os.getenv("GEMINI_API_KEY")))

Role = Literal["system", "user", "assistant"]

@dataclass
class Message:
    role: Role
    content: str


# ---------- Base Interface ----------

class LLMClient(ABC):
    @abstractmethod
    def chat(self, messages: List[Message]) -> str:
        pass


# ---------- OpenAI Client ----------

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model
        for model in client.models.list():
            if "generateContent" in model.supported_generation_methods:
                print(model.name)

    def chat(self, messages: List[Message]) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": m.role, "content": m.content}
                for m in messages
            ],
        )
        return response.choices[0].message.content


# ---------- Gemini Client ----------

from google import genai
from google.genai import types
import os

class GeminiGenAIClient(LLMClient):
    def __init__(self, model: str = "gemini-2.0-flash-001"):
        # Configure the client with your API key
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        # Use a stable model that your key has access to
        self.model = model

    def chat(self, messages):
        # Turn our message list into a single prompt
        system = []
        user = []
        for m in messages:
            if m.role == "system":
                system.append(m.content)
            elif m.role == "user":
                user.append(m.content)

        prompt = "SYSTEM INSTRUCTIONS:\n"
        prompt += "\n".join(system) + "\n\n"
        prompt += "USER:\n" + "\n".join(user)

        # Call the GenAI SDK
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

class DummyClient(LLMClient):
    """Ein einfacher LLM-Ersatz für lokale Tests."""
    def chat(self, messages):
        user_msg = [m.content for m in messages if m.role == "user"][-1]
        return f"[Dummy Response] You said: {user_msg}"
# ---------- Factory ----------
from ollama import chat, ChatResponse
from llm_wrapper import LLMClient, Message

class OllamaClient(LLMClient):
    """
    Ollama client using the official Ollama Python library's chat interface.
    Supports system, user, and assistant messages.
    """
    def __init__(self, model="ministral-3:3b-cloud"):
        self.model = model

    def chat(self, messages):
        """
        messages: List[Message] with roles "system", "user", "assistant"
        """
        # Convert llm_wrapper.Message to Ollama chat message dicts
        chat_messages = []
        for m in messages:
            if m.role not in ("system", "user", "assistant"):
                continue
            chat_messages.append({"role": m.role, "content": m.content})

        if not chat_messages:
            return "[ERROR]: No valid messages provided."

        try:
            # Call the Ollama chat function
            response: ChatResponse = chat(model=self.model, messages=chat_messages)
            
            # Access the content safely
            return response.message.content.strip()
        except Exception as e:
            return f"[ERROR]: {e}"

def get_llm(provider: str) -> LLMClient:
    provider = provider.lower()
    if provider == "ministral":
        return OllamaClient()
    if provider == "gemini":
        return GeminiGenAIClient()
    if provider == "kimi-k2":
        return OllamaClient("kimi-k2-thinking:cloud")
    if provider == "glm-5":
        return OllamaClient("glm-5:cloud")
    raise ValueError(f"Unknown provider: {provider}")
