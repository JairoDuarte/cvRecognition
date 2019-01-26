import re

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
            print(e)
            pass

        return email

        