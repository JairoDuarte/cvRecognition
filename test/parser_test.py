from cvanalyse.parser import Parser
from cvanalyse.dataStore import Store

def testGetEmail(filePath = 'data/test/input/cv1.docx'):
    lines,sentences = Store.getCV(filePath)

    parser = Parser(lines, sentences)
    emails = parser.getEmail()
    assert "'amaury@balmer.fr'" in emails


if __name__ == '__main__':
    testGetEmail()