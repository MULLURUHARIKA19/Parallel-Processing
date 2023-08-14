import os
import concurrent.futures
import PyPDF2
import time

def process_pdf(pdf_file):
    with open(pdf_file, 'rb') as pdf:
        pdf_reader = PyPDF2.PdfReader(pdf)
        num_pages = len(pdf_reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return pdf_file, num_pages, len(text)

if __name__ == '__main__':
    pdf_folder = "C:\\Users\\harikamu\\Desktop\\parallel processing\\Pdfs"  
    pdf_files = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith('.pdf')]

    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(process_pdf, pdf_files[:10])) 
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    for pdf_file, num_pages, text_length in results:
        print(f"Processed {pdf_file} - Pages: {num_pages}, Text Length: {text_length}")

    print(f"Total time taken: {elapsed_time:.2f} seconds")

