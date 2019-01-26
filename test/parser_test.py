from cvanalyse.parser import Parser
from cvanalyse.dataStore import Store

def testGetEmail(filePath = 'data/input/cv1.docx'):
    lines,sentences = Store.getCV(filePath)

    parser = Parser(lines, sentences)
    emails = parser.getEmail()
    assert 'duartealfredoj@gmail.com' in emails

def testGetName(filePath = 'data/input/cv1.docx'):
    lines,sentences = Store.getCV(filePath)

    parser = Parser(lines, sentences)
    names = parser.getName()

    assert 'Duarte Alfredo Jairo' in names

def testGetFormations(filePath = 'data/input/cv2.docx'):
    lines,sentences = Store.getCV(filePath)

    parser = Parser(lines, sentences)
    formations = parser.getFormations()

    assert 'Ingénieur en informatique généraliste' in formations

def testGetCompetence(filePath = 'data/input/cv2.docx'):
    lines,sentences = Store.getCV(filePath)

    parser = Parser(lines, sentences)
    competences = parser.getCompetences()

    assert 'ANGLAIS' in competences

def testGetPhoneNumber(filePath = 'data/input/cv2.docx'):
    lines,sentences = Store.getCV(filePath)

    parser = Parser(lines, sentences)
    number = parser.getPhoneNumber()

    assert '0678415311' in number

if __name__ == '__main__':
    testGetFormations()