from Api.constant.constants import GOOGLE_API_KEY
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

def improve_english_gemini(tender):
    try:
        # Access the work description from the tender
        description = tender['Work Item Details']['Work Description']
        # Define the prompt template
        prompt = PromptTemplate(
            input_variables=["description"],
            template = """
    Consider a variety of project descriptions that come in different formats, styles, and languages, often containing regional slangs, informal expressions, mixed-language usage, or procedural jargon. These descriptions aim to outline specific work or activities but may not do so clearly or consistently. Your task is to parse these descriptions to extract the fundamental work being described, presenting it in clear, standardized English. Simplify and refine the essence of the work, excluding any non-essential terms or formalities. The goal is to provide a concise, straightforward summary of the work required, ideally within 250 characters, to ensure clarity and accessibility for a wide audience.

    here's one such "{description}". just reply with your improved version in STANDARDISED ENGLISH.
    """

        )

        # Initialize the language model
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, google_api_key=GOOGLE_API_KEY)

        # Generate the formatted prompt
        formatted_prompt = prompt.format(description=description)

        # Invoke the language model with the prompt
        result = llm.invoke(formatted_prompt)

        # Return the improved description
        return result.content
    except Exception as e:
        print(f"Encountered a Gemini-specific exception: {e}")
        # Return "harm" if there's a Gemini-specific exception indicating problematic content
        return "harm"

def contract_info(tender):
    try:
        # Extract the required information from the tender object
        description = tender['Work Item Details']['Improved Work Description']
        work_type = tender['Work Item Details']['Product Category']
        organisation_chain = tender['Basic Details']['Organisation Chain']
        locations = tender['Work Item Details']['District']
        
        # Define the prompt template
        prompt = PromptTemplate(
            input_variables=["description", "work_type", "organisation_chain", "locations"],
            template = """
Given the following details about a government contract, create a clear and concise description that includes all relevant information. If any information is missing or not applicable, simply exclude it from the summary. Ensure the final description is in standardized English and encapsulates the essence of the contract clearly.

- Description: {description}
- Work Type: {work_type}
- Organisation Chain: {organisation_chain}
- Locations: {locations}

Construct a summary that integrates these details coherently. For instance, describe the work in context of the work type, specifying who is responsible (organisation chain) and where it is taking place (locations). If any details are missing, adapt the summary to remain fluid and complete without those specifics. Write everything in a single paragraph capturing all the information from these 4 fields.
"""
        )

        # Initialize the language model
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0, google_api_key=GOOGLE_API_KEY)

        # Generate the formatted prompt
        formatted_prompt = prompt.format(description=description, work_type=work_type, organisation_chain=organisation_chain, locations=locations)

        # Invoke the language model with the prompt
        result = llm.invoke(formatted_prompt)

        # Return the summary description
        return result.content
    except Exception as e:
        print(f"Encountered an exception: {e}")
        return "harm"  # Return "harm" if an exception is encountered

def tendersDataCleaningHelper(tender):
    print(tender)