import io

from docx2txt import docx2txt
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class Converter():
    
    @staticmethod
    def docxToText(filePath):
        text = docx2txt.process(filePath, "data/test/output")

        return text


    @staticmethod
    def pdfToText(filePath):
        """
        fait la conversion des fichiers pdf vers text
        """
        manager = PDFResourceManager()
        codec = 'utf-8'
        caching = True
        output = io.StringIO()
        converter = TextConverter(manager, output, codec=codec, laparams=LAParams())     
        interpreter = PDFPageInterpreter(manager, converter)   
        infile = open(filePath, 'rb')

        pagenums = set()
        for page in PDFPage.get_pages(infile, pagenums,caching=caching, check_extractable=True):
            interpreter.process_page(page)

        convertedPDF = output.getvalue()  

        infile.close() 
        converter.close()
        output.close()
        return convertedPDF

if __name__ == '__main__':
    content = Converter.docxToText('data/test/input/cvdoc.doc')
    print("{0}".format(content))