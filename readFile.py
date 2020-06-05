"""" readFile.py
*   Author : Yvain RAYNAUD
*   Date : 05/06/2020
*   Object : file used to extract text from pdf and docx
"""


from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import docx2txt


#local version using pdfminer
def readPdfFile(input):
    """
    Return str containing input pdf converted to text
    :param input:
    :return str:
    """
    output_string = StringIO()
    with open(input , 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        text = output_string.getvalue()
    #print(text.isascii()) #not ascii ? but comprehensible 
    return text

def readDocxFile(input):
    text = docx2txt.process(input)
    return text
