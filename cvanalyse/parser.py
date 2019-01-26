import re

import json
from cvanalyse.utils import Combinations, PHONE_REGEX
import logging

class Parser():
    """"""

    def __init__(self, lines = None, sentences = None):
        """Constructor for Parser"""
        self.lines = lines
        self.sentences = sentences
        pass

    def getEmail(self):
        pattern = re.compile(r'\S*@\S*')
        email = []

        try:
            for  line in self.lines:
                email_ = pattern.findall(line)
                email += [el for el in email_ if len(el) >5 and el not in email]
        except Exception as e:
            logging.error(e)
            pass

        return email

    def getName(self):
        namesList = DataSet.getNames()
        names = []
        try:
            for line in self.sentences:
                for sentence,_ in line:
                    for name in namesList:
                        sent = sentence.upper()
                        if name == sent and len(sentence) > 2 and sent not  in names:
                            names.append(sent)

            combinations = Combinations(names)
            fullnames =[]
            while combinations.next():
                res = combinations.array
                fullnames.append(' '.join(el for el in combinations.array))
                combinations.next()
            for fullname in fullnames:
                for line in self.lines:
                    sizeline = len(line)
                    if fullname[:sizeline] in line.upper():
                        t = ' '.join(el for el in line.split() if el.upper() in namesList)
                        return t
            return 'N\'est pas trouvé'

        except Exception as e:
            logging.error(e)
            pass

    def getCompetences(self):
        competencesList = DataSet.getCompetences()
        competences = []
        try:
            for line in self.sentences:
                for sentence,_ in line:
                    for competence in competencesList:
                        if competence in sentence.upper() and competence not in competences:
                            competences.append(competence)

            return competences
        except Exception as e:
            logging.error(e)
            pass

    def getPhoneNumber(self):

        number = []
        try:
            pattern = re.compile(PHONE_REGEX)

            for line in self.lines:
                match = pattern.findall(line)
                number += match

        except:
            pass

        return number


    def getFormations(self):

        formationsList = DataSet.getFormations()

        formations = []

        try:
            for formation in formationsList:
                for line in self.lines:
                    if len(line) > 8 and formation.upper() in line.upper() and line not in formations:
                        formations.append(line)
            return formations

        except Exception as e:
            logging.error(e)
            pass

        return formations


class DataSet():

    @staticmethod
    def getNames():

        names = json.loads(open('data/dataset/dataset.json', 'r').read())

        return names['names']

    @staticmethod
    def getCompetences():
        data = json.loads(open('data/dataset/dataset.json', 'r').read())

        return data['competences']

    @staticmethod
    def getFormations():
        data = json.loads(open('data/dataset/dataset.json', 'r').read())

        return data['formations']

def main():
    na = DataSet.getNames()
    f = open("competences.txt","w")
    [f.write('"{}",'.format(t)) for t in na if len(t)]


if __name__ == "__main__":
    main()