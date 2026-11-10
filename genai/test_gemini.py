
from genai.config import check_configuration
from genai.chat_assistant import ask_grohm_ai

print("================================")
print("       GROHM GEMINI TEST")
print("================================")

print("\n1. Configuration:")
print(check_configuration())

print("\n2. Gemini Response Test:")

try:
    answer = ask_grohm_ai(
        "Explain the Flexi Matrix Analyzer in simple words."
    )

    print("\nGROHM AI:")
    print(answer)

except Exception as error:
    print("\nGEMINI ERROR:")
    print(error)
