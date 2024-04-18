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
from Api.helpers.PincodeToDistrictHelper import get_district_by_pincode
from Api.helpers.languageDetectHelper import safe_detect
from Api.config.db import db


async def improve_english_gemini(description):
    prompt = PromptTemplate(
        input_variables=["description"],
        template = IMPROVING_ENGLISH_PROMPT
    )
    formatted_prompt = prompt.format(description=description)
    return await chat_gemini(formatted_prompt)
    
    

async def contract_summary(description,work_type,organisation_chain,locations):
    prompt = PromptTemplate(
        input_variables=["description", "work_type", "organisation_chain", "locations"],
        template =IMPROVING_ENGLISH_TENDER_INFORMATION
    )
    formatted_prompt = prompt.format(description=description, work_type=work_type, organisation_chain=organisation_chain, locations=locations)

    # Invoke the language model with the prompt
    return await chat_gemini(formatted_prompt)
  

# def check_englsih_quality(title,description,work_type,organisation_chain,locations):
#     description_language = detect(description)
#     title_language = detect(title)
#     if ' ' in description:
#         if description_language == 'en':
#             return description
#         else :
#             return improve_english_gemini(description)
#     elif ' ' in title:
#         if title_language == 'en':
#             return title
#         else :
#             return improve_english_gemini(title)
#     else :
#         return contract_info(description,work_type,organisation_chain,locations)
    


async def tendersDataCleaningHelper(tender):
    # Use get method with a default value for each key to handle missing data
    tenderId = tender.get('Basic Details', {}).get('Tender ID', '')
    collection = db['processed-tenders']
    existing_tender = collection.find_one({'tenderId': tenderId})
    if existing_tender:
        print(f"Tender with Tender id Number: {tenderId} already exists.")
        return
    tenderOrgName = tender.get('Basic Details', {}).get('Organisation Chain', '')
    tenderRefNumber = tender.get('Basic Details', {}).get('Tender Reference Number', '')
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
    
    description_language = safe_detect(tenderDescription)
    title_language = safe_detect(tenderTitle)
    if ' ' in tenderDescription:
        if description_language == 'en':
            AIImprovedDescription = tenderDescription
        else :
            AIImprovedDescription = await improve_english_gemini(tenderDescription)
    elif ' ' in tenderTitle:
        if title_language == 'en':
            AIImprovedDescription = tenderTitle
        else :
            AIImprovedDescription = await improve_english_gemini(tenderTitle)
    else:
        AIImprovedDescription = "Null"
        
    LocationByPincode = await get_district_by_pincode(str(tenderBidLocation))
    AIContractSummary = await contract_summary(AIImprovedDescription, tenderProductCategory, tenderOrgName, LocationByPincode)
    tender_document = {
        'tenderOrgName': tenderOrgName,
        'tenderRefNumber': tenderRefNumber,
        'tenderId': tenderId,
        'tenderCategory': tenderCategory,
        'tenderCost': tenderCost,
        'tenderEMDCost': tenderEMDCost,
        'tenderTitle': tenderTitle,
        'tenderDescription': tenderDescription,
        'tenderProductCategory': tenderProductCategory,
        'tenderBidLocation': tenderBidLocation,
        'tenderBidStartDate': tenderBidStartDate,
        'tenderBidEndDate': tenderBidEndDate,
        'tenderUrl': tenderUrl,
        'AIImprovedDescription': AIImprovedDescription,
        'LocationByPincode':LocationByPincode,
        'AIContractSummary':AIContractSummary
    }
    print('tenderDescription',tenderDescription)
    print('AIContractSummary',AIContractSummary)
    processed_tenders = await insert_processed_tenders(tender_document)
    print(processed_tenders)


