from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from Api.constant.constants import GOOGLE_API_KEY

def chat_gemini(prompt):
    try : 
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, google_api_key=GOOGLE_API_KEY,transport='rest')
        result = llm.invoke(prompt)
        return result.content
    except Exception as e:
        print(f"Encountered a Gemini-specific exception: {e}")
        return "harm"