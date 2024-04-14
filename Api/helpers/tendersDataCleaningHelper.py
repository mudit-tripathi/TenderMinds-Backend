import os
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from Api.constant.constants import OPENAI_API_KEY , GOOGLE_API_KEY
from Api.constant.prompts import IMPROVE_DESCRIPTION_FROM_GEN_AI
from langchain_google_vertexai import ChatVertexAI
from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI

async def improveDescriptionFromGenAi(tenderTitle, tenderDescription, tenderProductCategory):
    try:
        # Set the GOOGLE_API_KEY in the environment
        # os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
        # genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
        # Create a prompt template with the provided inputs
        prompt = PromptTemplate(
            input_variables=["title", "workType", "description"],
            template=IMPROVE_DESCRIPTION_FROM_GEN_AI
        )
        
        # Format the prompt with the provided title, workType, and description
        formatted_prompt = prompt.format(title=tenderTitle, workType=tenderProductCategory, description=tenderDescription)
        llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

        # Use the formatted prompt from the previous step
        result = llm.invoke(formatted_prompt)
        print(result)
        return result
        
    except Exception as e:
        # Handle any exceptions that occur during the function's execution
        print(f"An error occurred: {e}")
        # You can also choose to log the error or take other actions as needed
# async def improveDescriptionFromGenAi(tenderTitle, tenderDescription, tenderProductCategory):
#     try:
#         # Set the GOOGLE_API_KEY in the environment
#         os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
#         genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        
#         # Create a prompt template with the provided inputs
#         prompt = PromptTemplate(
#             input_variables=["title", "workType", "description"],
#             template=IMPROVE_DESCRIPTION_FROM_GEN_AI
#         )
        
#         # Format the prompt with the provided title, workType, and description
#         formatted_prompt = prompt.format(title=tenderTitle, workType=tenderProductCategory, description=tenderDescription)
        
#         llm = ChatVertexAI(model="gemini-pro", max_output_tokens=1000,)

#         # Use the formatted prompt from the previous step
#         result = llm.invoke(formatted_prompt)

#         print(result)
#         return result
        
#     except Exception as e:
#         # Handle any exceptions that occur during the function's execution
#         print(f"An error occurred: {e}")
#         # You can also choose to log the error or take other actions as needed

# Example usage
# improveDescriptionFromGenAi("Sample Title", "Sample Description", "Sample Product Category")

    
async def tendersDataCleaningHelper(tender):
    # Use get method with a default value for each key to handle missing data
    tenderOrgName = tender.get('Basic Details', {}).get('Organisation Chain', '')
    tenderRefNumber = tender.get('Basic Details', {}).get('Tender Reference Number', '')
    tenderId = tender.get('Basic Details', {}).get('Tender ID', '')
    tenderCategory = tender.get('Basic Details', {}).get('Tender Category', '')
    
    tenderCost = float(tender.get('Tender Fee Details', {}).get('Tender Fee in ₹', 0).replace(',', ''))
    tenderEMDCost = float(tender.get('EMD Fee Details', {}).get('EMD Amount in ₹', 0).replace(',', ''))
    
    tenderTitle = tender.get('Work Item Details', {}).get('Title', '')
    tenderDescription = tender.get('Work Item Details', {}).get('Work Description', '')
    tenderProductCategory = tender.get('Work Item Details', {}).get('Product Category', '')
    tenderBidLocation = tender.get('Work Item Details', {}).get('Pincode', '')
    
    tenderBidStartDate = tender.get('Critical Dates', {}).get('Bid Submission Start Date', '')
    tenderBidEndDate = tender.get('Critical Dates', {}).get('Bid Submission End Date', '')
    tenderUrl = tender.get('tender_url', '')
    return await improveDescriptionFromGenAi(tenderTitle,tenderDescription,tenderProductCategory)



