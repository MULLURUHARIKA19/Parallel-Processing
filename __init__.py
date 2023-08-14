import os
import logging
import concurrent.futures
import PyPDF2
import azure.functions as func

def process_pdf(pdf_file):
    with open(pdf_file, 'rb') as pdf:
        pdf_reader = PyPDF2.PdfReader(pdf)
        num_pages = len(pdf_reader.pages)
        text = ''
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

        return pdf_file, num_pages, len(text)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        pdf_folder = "C:\\Users\\harikamu\\Desktop\\parallel processing\\Pdfs"  
        pdf_files = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith('.pdf')]

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(process_pdf, pdf_files[:10])) 
        
        end_time = time.time()
        elapsed_time = end_time - start_time

        response_text = "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.\n"
        for pdf_file, num_pages, text_length in results:
            response_text += f"Processed {pdf_file} - Pages: {num_pages}, Text Length: {text_length}\n"

        response_text += f"Total time taken: {elapsed_time:.2f} seconds"

        return func.HttpResponse(response_text, status_code=200)

# if __name__ == '__main__':
#     main()

