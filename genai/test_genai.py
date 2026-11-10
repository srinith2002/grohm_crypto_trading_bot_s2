from genai.config import check_configuration
from genai.llm_client import generate_response
from genai.chat_assistant import ask_grohm_ai

print("================================")
print("       GROHM GENAI TEST")
print("================================")

print("\n1. Configuration Test")
print(check_configuration())

print("\n2. LLM Client Test")
print("Function available:", callable(generate_response))

print("\n3. Chat Assistant Test")
print("Function available:", callable(ask_grohm_ai))

print("\nGROHM GenAI Module Test Completed")