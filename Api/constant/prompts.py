IMPROVING_ENGLISH_PROMPT = '''Consider a variety of project descriptions that come in different formats, styles, and languages, often containing regional slangs, informal expressions, mixed-language usage, or procedural jargon. These descriptions aim to outline specific work or activities but may not do so clearly or consistently. Your task is to parse these descriptions to extract the fundamental work being described, presenting it in clear, standardized English. Simplify and refine the essence of the work, excluding any non-essential terms or formalities. The goal is to provide a concise, straightforward summary of the work required, ideally within 250 characters, to ensure clarity and accessibility for a wide audience.

    here's one such "{description}". just reply with your improved version in STANDARDISED ENGLISH.'''

IMPROVING_ENGLISH_TENDER_INFORMATION = '''Given the following details about a government contract, create a clear and concise description that includes all relevant information. If any information is missing or not applicable, simply exclude it from the summary. Ensure the final description is in standardized English and encapsulates the essence of the contract clearly.

- Description: {description}
- Work Type: {work_type}
- Organisation Chain: {organisation_chain}
- Locations: {locations}

Construct a summary that integrates these details coherently. For instance, describe the work in context of the work type, specifying who is responsible (organisation chain) and where it is taking place (locations). If any details are missing, adapt the summary to remain fluid and complete without those specifics. Write everything in a single paragraph capturing all the information from these 4 fields.'''