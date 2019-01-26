import io

import nltk
from docx2txt import docx2txt
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
import re

EMAIL_REGEX = r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}"
PHONE_REGEX = r"\(?(\d{3})?\)?[\s\.-]{0,2}?(\d{3})[\s\.-]{0,2}(\d{4})"

class DataPreProcess():
    """
    Transformation, nettoyage et extraction des informations
    return: trois listes, une avec des jetons, une avec des lignes étiquetées POS, une avec des phrases étiquetées POS.
    """
    
    def __init__(self, ):
        """Constructor for """

    @staticmethod
    def process(document):
        """
        Args:
        Returns:

        """
        try:
            lines = [el.strip() for el in document.split("\n") if len(el) > 2]

            sentences = nltk.sent_tokenize(document)
            sentences = [nltk.word_tokenize(sent) for sent in sentences]
            sentences = [nltk.pos_tag(sent) for sent in sentences]

            lines = [DataPreProcess.clean(line) for  line in lines]
            return lines, sentences
        except Exception as e:
            print(e)
            pass

    @staticmethod
    def clean(content, char='<*=%>'):
        _content = str(content)

        clean = re.compile(char)
        content = (re.sub(clean, '', _content))
        content = content.replace('\n', ' ')

        return content
            

class Converter():
    
    @staticmethod
    def docxToText(filePath):
        """
        fait la conversion de du format word vers text
        :param filePath:
        :return: le text
        """
        text = ''
        try:
            text = docx2txt.process(filePath, "data/test/output")
        except Exception as e:
            print(e)
            pass

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