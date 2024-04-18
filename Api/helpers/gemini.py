from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from Api.constant.constants import GOOGLE_API_KEY

async def chat_gemini(prompt):
    try : 
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, google_api_key=GOOGLE_API_KEY,safety_settings={
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    })
        print("inside: chat_gemini")
        result = llm.invoke(prompt)
        return result.content
    except Exception as e:
        print(f"Encountered a Gemini-specific exception: {e}")
        return "Null"