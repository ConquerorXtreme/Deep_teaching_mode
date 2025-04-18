import fitz  # PyMuPDF
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import google.generativeai as genai 
from load_dotenv import load_dotenv
import os
from trim import trim_pdf 
import json  
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI"))
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_toc_and_parse(pdf_path, toc_start_pdf_pg, toc_end_pdf_pg):

    final_result = []
    last_chapter = None

    for page_num in range(toc_start_pdf_pg, toc_end_pdf_pg + 1):
        # Extract single page as a PDF
        single_page_pdf_path = trim_pdf(pdf_path, start_page=page_num, end_page=page_num)
        sample_file = genai.upload_file(path=single_page_pdf_path, display_name=f"page_{page_num}")

        # Build the prompt with context from the last chapter
        prompt = f"""Please extract the Table of Contents from the PDF file provided.

If the content starts with subtopics, i.e. the chapter name is missing, then use the last chapter from the previous page for context:
Last Chapter name: {last_chapter if last_chapter else "None"}

Please extract the content into this format. please do not change the format . the format contains a list of tuples. each tuple contains a chapter name and a dictionary of topics with their page numbers. :
[
  ("Chapter X: Chapter Title", {{
      "Topic x : Topic Title" : "Page Number",
      "Topic y : Topic Title" : "Page Number",
      ...
      "Topic z : Topic Title" : "Page Number"
  }}),
  ...
]

"""
        try:

            response = model.generate_content([sample_file, prompt], safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            
        }).text
        except:
            response = model.generate_content([sample_file, prompt], safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            
        }).text
            

        print(f"Gemini response for page {page_num}:", response)
        if response[0] == "`":
            response = response.replace("```json", "").replace("```", "")
        print(f"Gemini response after trimming for page {page_num}:", response)

        try:
            parsed_json = eval(response)  # Changed from eval to json.loads for safety
            if parsed_json:
                # Extract the last chapter for context in the next iteration
                last_chapter = parsed_json[-1][0] if parsed_json else last_chapter
                final_result.extend(parsed_json)
        except Exception as e:
            print(f"JSON decoding error for page {page_num}:", e)
            return None
    with open("save.json", "w") as outfile:
        json.dump(final_result, outfile, indent=4)
    return final_result







if __name__ == "__main__":


    parsed_toc = extract_toc_and_parse("/home/aryan/deep-spark-mentor-ai/backend/Concepts_of_Physics_Vol_2_2023_Edition.pdf", toc_start_pdf_pg=12, toc_end_pdf_pg=16)
    
    if parsed_toc:
        print("Parsed Table of Contents:", parsed_toc)
    else:
        print("Failed to parse Table of Contents.")
