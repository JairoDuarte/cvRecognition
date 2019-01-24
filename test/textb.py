train = [
    ('ALFREDO JAIRO DUARTE', 'nom'),
    ('Casablanca-Marrocos', 'adresse'),
    ('n212622333820', 'telephone'),
    ('laurence-langlois@hotmail.fr', 'email'),
    ('duartealfredoj@gmail.com', 'email'),
    ('laurence-langlois@hotmail.fr', 'email'),
    ('duartealfredoj@gmail.com', 'email'),
    ('linkedin.com/in/alfredo-jairo-duarte', 'rsocial'),
    ('12 Rue du Port  56000 VANNES.', 'adresse'),
    ('Master AES GRH Faculte de Droit de Nice 2012', 'formation'),
    ('jairoduarte.github.io', 'rsocial'),
    ('Master Degree Student in Big Data and Cloud Computing ','formation'),
    ('Master en Big data et Cloud Computing Faculte des Sciences Ibn Tofaïl','formation'),
    ('Master Degree Student in Big Data and Cloud Computing ','formation'),
    ('Master en Big data et Cloud Computing Faculte des Sciences Ibn Tofaïl','formation'),
    ('Master Degree Student in Big Data and Cloud Computing ','formation'),
    ('Master en Big data et Cloud Computing Faculte des Sciences Ibn Tofaïl','formation'),
    ('Licence Professionnelle en Genie Logiciel et Administration Avancee de Systemes et Reseaux Informatiques Universite Hassan II de Casablanca','formation'),
    ('Django','competence'),
    ('Vuejs','competence'),
    ('Flask','competence'),
    ('Big Data','competence'),
    ('Machine Leaning ','competence'),
    ('Caisse Nationale RSI Centre Informatique de Valbonne','RIEN'),
    ('Organisation et planification des seances daccompagnement et de formation ISO 9001','RIEN'),
    ('Optimiste impliquee et curieuse','PROFIL'),
    ('06 58 64 60 22','telephone'),
    ('Anglais','langue'),
    ('Espagnol','langue'),
    ('Maîtrise de Sciences Gestion en alternance ','formation'),
    ('Machine Leaning ','competence'),
]
test = [
    ('Master AES GRH Faculte de Droit de Nice', 'formation'),
    ('12 Rue du Port  56000 VANNES.', 'adresse'),
    ('laurence-langlois@hotmail.fr', 'email'),
    ('Master en Big data et Cloud Computing Faculte des Sciences Ibn Tofaïl','formation'),
]
from textblob.classifiers import NaiveBayesClassifier, DecisionTreeClassifier
from textblob import TextBlob

def getfile():
    f = open('cv4.pdfoutput.txt').read()
    content = [el for el in f.split("\n") if len(el) > 3] 
    return content

def getsum(content):
    cl = DecisionTreeClassifier(train)
    
    for line in content:
        blob = TextBlob(line, classifier=cl)
        print("{0} - {1}".format(line,blob.classify()))
    blob = TextBlob("laurence-langlois@hotmail.fr",classifier=cl)
    print(blob.classify())
    cl.classifier.most_informative_features(10)

content = getfile()
getsum(content)
"""
prob_dist = cl.prob_classify("laurence-langlois@hotmail.fr")

print( prob_dist.max())
print(round(prob_dist.prob("formation"), 2))
print(round(prob_dist.prob("email"), 2))
print(round(prob_dist.prob("formation"), 2))
print(round(prob_dist.prob("email"), 2))
"""

