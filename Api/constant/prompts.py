IMPROVING_ENGLISH_PROMPT = """
    Consider a variety of Indian government contract descriptions that come in different formats, styles, and languages. These often include regional slangs, informal expressions, mixed-language usage, or procedural jargon, and may also contain codewords. Your task is to parse these descriptions to extract the fundamental work being described, presenting it in clear, standardized English. Simplify and refine the essence of the work, excluding any non-essential terms, formalities, or codewords. The goal is to provide a concise, straightforward summary of the work required, ideally within 250 characters, to ensure clarity and accessibility for a wide audience. If the description does not contain any information about the actual contract work, reply with 'None'.

    Here's one such "{description}". Just reply with your improved version in STANDARDIZED ENGLISH.
    """
IMPROVING_ENGLISH_TENDER_INFORMATION =  """
Given the following details about a government contract, create a clear and concise description that includes all relevant information. If any information is missing or not applicable, simply exclude it from the summary. Ensure the final description is in standardized English and encapsulates the essence of the contract clearly.

- Description: {description}
- Work Type: {work_type}
- Organisation Chain: {organisation_chain}
- Locations: {locations}

Construct a summary that integrates these details coherently. For instance, describe the work in context of the work type, specifying who is responsible (organisation chain) and where it is taking place (locations). If any details are missing, adapt the summary to remain fluid and complete without those specifics.Write everything in a single paragraph capturing all the information from these 4 fields.Ensure that the entire summary is written in proper case, even if any of the fields are in uppercase.
"""
IMPROVING_ENGLISH_ORG_PROMPT ="""
    Translate and standardize the name of an organization from a regional Indian language into clear, standardized English
    here's onee such Organisation_Name: '{organisation_name}'. Just reply with your improved version in ENGLISH.
"""
IMPROVING_ENGLISH_QUERY_PROMPT="""
Translate and standardize the following user query from a regional Indian language to clear, standardized English for effective search and retrieval of government tenders.

here's the the query: "{query}". Just reply with your improved_version in ENGLISH. 
"""
