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
from Api.helpers.PincodeToLocationsHelper import get_locations_by_pincode
from Api.helpers.languageDetectHelper import safe_detect
from Api.helpers.mongoHelper import tender_exists
from Api.config.db import db

from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)


async def improve_english_gemini(description):
    logger.info("Entered improve_english_gemini function")
    prompt = PromptTemplate(
        input_variables=["description"],
        template = IMPROVING_ENGLISH_PROMPT
    )
    formatted_prompt = prompt.format(description=description)
    return await chat_gemini(formatted_prompt)
    
    

# async def contract_summary(description,work_type,organisation_chain,locations):
#     prompt = PromptTemplate(
#         input_variables=["description", "work_type", "organisation_chain", "locations"],
#         template =IMPROVING_ENGLISH_TENDER_INFORMATION
#     )
#     formatted_prompt = prompt.format(description=description, work_type=work_type, organisation_chain=organisation_chain, locations=locations)

#     # Invoke the language model with the prompt
#     return await chat_gemini(formatted_prompt)
  

async def improved_description(title,description):
    logger.info("iEntered improved_description function")
    if ' ' in description:
        description_language = safe_detect(description)
        if description_language == 'en':
            return description
        else :
            return  await improve_english_gemini(description)
    elif ' ' in title:
        title_language = safe_detect(title)
        if title_language == 'en':
            return title
        else :
            return await improve_english_gemini(title)
    else:
        return "None"
    


async def tendersDataCleaningHelper(tender):
    logger.info("Entered tendersDataCleaningHelper")
    # Use get method with a default value for each key to handle missing data
    tenderId = tender.get('Basic Details', {}).get('Tender ID', '')
    if tender_exists(tenderId):
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
    tenderBidLocation = tender.get('Work Item Details', {}).get('Location', '')
    tenderBidPincode = tender.get('Work Item Details', {}).get('Pincode', '')
    tenderBidStartDate = tender.get('Critical Dates', {}).get('Bid Submission Start Date', '')
    tenderBidEndDate = tender.get('Critical Dates', {}).get('Bid Submission End Date', '')
    tenderUrl = tender.get('tender_url', '')
    AIImprovedDescription=await improved_description(tenderTitle, tenderDescription)
    AreasByPincode, DistrictsByPincode, StateByPincode= await get_locations_by_pincode(tenderBidPincode, tenderBidLocation)
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
        'AreasByPincode':AreasByPincode,
        'DistrictsByPincode':DistrictsByPincode,
        'StateByPincode':StateByPincode
    }
    logger.info(f'tenderDescription: {tenderDescription}')

    logger.info(f"AIImprovedDescription: {AIImprovedDescription}")
    await insert_processed_tenders(tender_document)
    


