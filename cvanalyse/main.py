
import sys
from cvanalyse.dataStore import Store
from cvanalyse.parser import Parser

def main():

    if len(sys.argv) < 3:
        print("format: python cvanalyse/main.py data/input/cv2.docx data/cv.json".format())
        exit(0)

    fileinput = sys.argv[1]
    output = sys.argv[2]

    lines, sentences = Store.getCV(fileinput)
    parser = Parser(lines=lines, sentences=sentences)

    cv = {
        "name": parser.getName(),
        "contact": {"telephone":parser.getPhoneNumber(), "email": parser.getEmail()},
        "competences": parser.getCompetences(),
        "formations": parser.getFormations()
    }
    res = Store.saveCV(output,cv)
    if res:
        print("Operation terminée")


if __name__ == "__main__":
    main()