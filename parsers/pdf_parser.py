import fitz

from parsers.text_parser import find_ioc, CollectedData


def process_pdf(pdf_path: str) -> CollectedData:
    """
        Processes the text from the PDF file

    Args:
        pdf_path (str): Path to the PDF file
    """
    doc = fitz.open(pdf_path)
    collected_data = CollectedData()
    for page in doc.pages():
        current_page_collected_data = find_ioc(page.get_text().lower())
        collected_data.hashes.update(current_page_collected_data.hashes)
        collected_data.ips.update(current_page_collected_data.ips)
        collected_data.urls.update(current_page_collected_data.urls)
    return collected_data
