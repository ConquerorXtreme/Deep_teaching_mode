import os
from PyPDF2 import PdfReader, PdfWriter

def trim_pdf(pdf_path, start_page, end_page, output_path=None):
    """
    Trims a PDF from start_page to end_page (inclusive) and saves it as a new file.

    Args:
        pdf_path (str): Path to the original PDF.
        start_page (int): Starting page index (0-based).
        end_page (int): Ending page index (0-based).
        output_path (str, optional): Path to save the trimmed PDF. 
                                     If None, saves as 'trimmed_<originalname>.pdf' in same directory.

    Returns:
        str: Path to the trimmed PDF file.
    """
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    total_pages = len(reader.pages)
    if start_page < 0 or end_page >= total_pages or start_page > end_page:
        raise ValueError("Invalid page range.")

    for i in range(start_page-1, end_page ):
        writer.add_page(reader.pages[i])

    if not output_path:
        base_name = os.path.basename(pdf_path)
        dir_name = os.path.dirname(pdf_path)
        trimmed_name = f"trimmed_{base_name}"
        output_path = os.path.join(dir_name, trimmed_name)

    with open(output_path, "wb") as f_out:
        writer.write(f_out)

    return output_path
if __name__ == "__main__":
    new_pdf = trim_pdf("/home/aryan/deep-spark-mentor-ai/backend/Concepts_of_Physics_Vol_2_2023_Edition.pdf", start_page=12, end_page=16)
    print("Trimmed PDF saved at:", new_pdf)