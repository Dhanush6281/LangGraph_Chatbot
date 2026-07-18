from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentLoader:

    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def load_pdf(self, pdf_file):

        reader = PdfReader(pdf_file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    def split_text(self, text):

        return self.splitter.split_text(text)


loader = DocumentLoader()