import os
from pathlib import Path
import google.generativeai as genai
from PyPDF2 import PdfReader, PdfWriter
from load_dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from trim import trim_pdf

def process_chapter_content(chapter_data, pdf_page_for_book_page_1, full_pdf_path, mode="revise", 
                          previous_knowledge="", education_level="12th studying", language="english"):
    """
    Process chapter content from a PDF based on provided structure and learning parameters.
    
    Args:
        chapter_data: List containing chapter title and topics with page numbers
        pdf_page_for_book_page_1: PDF page number corresponding to book page 1
        full_pdf_path: Path to the complete PDF file
        mode: Learning mode - "deep dive", "revise", or "exam"
        previous_knowledge: User's existing knowledge of the topic
        education_level: User's education level (e.g. "10th pass", "12th studying")
        language: Preferred language for content (english/hindi/hinglish)
    
    Returns:
        Dictionary containing generated content for each topic
    """
    # Configure Gemini API
    genai.configure(api_key=os.getenv("GEMINI"))
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    # Extract chapter title and topics
    chapter_title = chapter_data[0]
    topics_dict = chapter_data[1]
    
    # Create output directory
    output_dir = Path(f"output/{chapter_title.replace(':', '_').replace(' ', '_')}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Define mode-specific prompts
    mode_prompts = {
        "deep dive": """
            Please provide an in-depth explanation of this topic. Include:
            - Detailed theoretical concepts with clear analogies and examples
            - Step-by-step solutions if numerical problems available
            - Real-world applications and significance
            - Interconnections with related concepts
            - Common misconceptions and how to avoid them
            - don't keep the content too long
        """,
        
        "last minute exam": """
            Please focus on exam preparation for this topic. Include:
            - Brief explanations of key concepts , real world applications, formulas
            - Common question patterns and how to approach them
            - Quick revision points for last-minute study
            - just give a small line overview for non important / theoretical topics
            - keep the content short
        """
    }
    
    # Get sorted topics with page numbers to determine page ranges
    sorted_topics = []
    for topic, page in topics_dict.items():
        try:
            book_page = int(page)
            pdf_page = book_page + pdf_page_for_book_page_1 - 1
            sorted_topics.append((topic, book_page, pdf_page))
        except ValueError:
            print(f"Warning: Invalid page number for topic '{topic}': {page}")
    
    # Sort topics by book page number
    # sorted_topics.sort(key=lambda x: x[1])
    print(sorted_topics)
    
    results = {}
    
    # Process each topic
    for i, (topic, book_page, pdf_page) in enumerate(sorted_topics):
        print(f"Processing: {topic} (Page {book_page})")
        
        # Determine end page for this topic
        if i < len(sorted_topics) - 1:
            next_pdf_page = sorted_topics[i + 1][2]
        else:
            # If it's the last topic, add a reasonable number of pages
            next_pdf_page = pdf_page + 1
        
        # Create trimmed PDF for this topic
        trimmed_pdf_path = trim_pdf(
            pdf_path=full_pdf_path,
            start_page=pdf_page,
            end_page=next_pdf_page ,
            output_path=str(output_dir / f"{topic.replace(':', '_').replace(' ', '_')}.pdf")
        )
        
        # Build the prompt for Gemini
        system_prompt = f"""
        You are an expert teacher explaining the topic: {topic} from {chapter_title}.
        
        Mode: {mode}
        {mode_prompts.get(mode.lower(), mode_prompts["last minute exam"])}
        
        Student's previous knowledge: {previous_knowledge}
        
        Education level: {education_level}
        
        Please explain in {language} language.
        
        Use the provided PDF content to create a comprehensive lesson. Focus on making the concepts clear,
        engaging, and appropriate for the student's level.
        """
        
        # Upload file to Gemini and generate content
        try:
            sample_file = genai.upload_file(path=trimmed_pdf_path, display_name=trimmed_pdf_path)
            response = model.generate_content([sample_file, system_prompt], safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            
        }).text
            
            # Save content to file
            output_file = output_dir / f"{topic.replace(':', '_').replace(' ', '_')}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(response)
            
            results[topic] = response
            print(f"✓ Generated content for '{topic}'")
            
        except Exception as e:
            print(f"Error generating content for '{topic}': {e}")
            results[topic] = f"Error: {str(e)}"
    
    return results








# Example usage:
if __name__ == "__main__":
    sample_chapter_data = [
        "Chapter 23: Heat and Temperature",
        {
            "23.1 Hot and Cold Bodies": "1",
            "23.2 Zeroth Law of Thermodynamics": "1",
            "23.3 Defining Scale of Temperature: Mercury and Resistance Thermometers": "1",
            "23.4 Constant Volume Gas Thermometer": "3",
            "23.5 Ideal Gas Temperature Scale": "5",
            "23.6 Celsius Temperature Scale": "5",
            "23.7 Ideal Gas Equation": "5",
            "23.8 Callender's Compensated Constant Pressure Thermometer": "5",
            "23.9 Adiabatic and Diathermic Walls": "6",
            "23.10 Thermal Expansion": "6",
            "Worked Out Examples": "7",
            "Questions for Short Answer": "11",
            "Objective I": "11",
            "Objective II": "12",
            "Exercises": "12"
        }
    ]
    
    # Set your PDF path and relevant page number here
    pdf_page_for_book_page_1 = 17  # Example value - adjust as needed
    full_pdf_path = "/home/aryan/deep-spark-mentor-ai/backend/Concepts_of_Physics_Vol_2_2023_Edition.pdf"  # Replace with actual path
    
    results = process_chapter_content(
        sample_chapter_data,
        pdf_page_for_book_page_1,
        full_pdf_path,
        mode="last minute exam",
        previous_knowledge="studied nothing in class 11th. just passed",
        education_level="12th studying",
        language="hinglish"
    )