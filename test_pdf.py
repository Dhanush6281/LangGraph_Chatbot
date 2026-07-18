from app.document_loader import loader

pdf_path = "sample.pdf"

text = loader.load_pdf(pdf_path)

print("=" * 50)

print(text[:1000])

print("=" * 50)

chunks = loader.split_text(text)

print("Chunks:", len(chunks))