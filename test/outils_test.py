import sys
from cvanalyse.outils import Converter
import sys, os

def testDocxToText(filePath = 'data/test/input/cv1.docx'):
    content = Converter.docxToText(filePath)
    assert "Duarte Alfredo Jairo " in content


def testPdfToText():
    content = Converter.pdfToText("data/test/input/cv5.pdf")

    assert "celiersophie@gmail.com" in content



if __name__ == '__main__':
    print("{}".format('hello'))

    testDocxToText()