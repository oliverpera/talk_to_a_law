import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

pdf_path = "KWG.pdf"
fd = open(pdf_path, "rb")
viewer = SimplePDFViewer(fd)

print(viewer.metadata)
