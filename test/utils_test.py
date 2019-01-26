from cvanalyse.dataStore import Store
from cvanalyse.utils import Converter, DataPreProcess


def testDocxToText(filePath = 'data/input/cv1.docx'):
    content = Converter.docxToText(filePath)
    assert "Duarte Alfredo Jairo " in content


def testPdfToText():
    content = Converter.pdfToText("data/input/cv5.pdf")

    assert "celiersophie@gmail.com" in content

def testDataProcess():
    content = Converter.pdfToText("data/input/cv6.pdf")
    lines, sentences = DataPreProcess.process(content)
    print("".format())
    
    assert sentences[0][0][0] in lines[0]


def testFormatNotSupported():
    try:
        lines, sentences = Store.getCV("data/input/cv5.doc")
        assert sentences[0][0][0] in lines[0]
    except:
        pass

if __name__ == '__main__':
    print("{}".format('hello'))
    testDataProcess()