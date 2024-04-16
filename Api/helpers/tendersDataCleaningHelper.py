import os
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from Api.helpers.gemini import chat_gemini
from Api.constant.prompts import IMPROVING_ENGLISH_PROMPT , IMPROVING_ENGLISH_TENDER_INFORMATION
from langchain.llms import OpenAI
from Api.helpers.mongoHelper import insert_processed_tenders
from langdetect import detect

def improve_english_gemini(description):
    try:
        prompt = PromptTemplate(
            input_variables=["description"],
            template = IMPROVING_ENGLISH_PROMPT
        )
        formatted_prompt = prompt.format(description=description)
        return chat_gemini(formatted_prompt)
    except Exception as e:
        print(f"Encountered a Gemini-specific exception: {e}")
        return "harm"
    

def contract_info(description,work_type,organisation_chain,locations):
    try:
        prompt = PromptTemplate(
            input_variables=["description", "work_type", "organisation_chain", "locations"],
            template =IMPROVING_ENGLISH_TENDER_INFORMATION
        )
        formatted_prompt = prompt.format(description=description, work_type=work_type, organisation_chain=organisation_chain, locations=locations)

        # Invoke the language model with the prompt
        return chat_gemini(formatted_prompt)
    except Exception as e:
        print(f"Encountered an exception: {e}")
        return "harm"  # Return "harm" if an exception is encountered
    

def check_englsih_quality(title,description,work_type,organisation_chain,locations):
    description_language = detect(description)
    title_language = detect(title)
    if ' ' in description:
        if description_language == 'en':
            return description
        else :
            return improve_english_gemini(description)
    elif ' ' in title:
        if title_language == 'en':
            return title
        else :
            return improve_english_gemini(title)
    else :
        return contract_info(description,work_type,organisation_chain,locations)
    

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
    AITenderDescription = improve_english_gemini(tenderDescription)
    document = {
        "tenderOrgName": tenderOrgName,
        "tenderRefNumber": tenderRefNumber,
        "tenderId": tenderId,
        "tenderCategory": tenderCategory,
        "tenderCost": tenderCost,
        "tenderEMDCost": tenderEMDCost,
        "tenderTitle": tenderTitle,
        "tenderDescription": tenderDescription,
        "tenderProductCategory": tenderProductCategory,
        "tenderBidLocation": tenderBidLocation,
        "tenderBidStartDate": tenderBidStartDate,
        "tenderBidEndDate": tenderBidEndDate,
        "tenderUrl": tenderUrl,
        "AITenderDescription": AITenderDescription
    }
    print('tenderDescription',tenderDescription)
    print('AITenderDescription',AITenderDescription)
    processed_tenders = await insert_processed_tenders(document)
    print(processed_tenders)


