#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# training data
TRAIN_DATA = [
    ("ALFREDO JAIRO DUARTE\nCasablanca-Marrocos\n212622333820\nduartealfredoj@gmail.com linkedin.com/in/alfredo-jairo-duarte   jairoduarte.github.io Master Degree Student in Big Data and Cloud Computing Resumo Formation 2017 - 2019 Master en Big data et Cloud Computing Faculte des Sciences Ibn Tofaïl Kenitra Licence Professionnelle en Genie Logiciel et Administration Avancee de Systemes et Reseaux Informatiques Universite Hassan II de Casablanca EST Diplôme Universitaire de Technicien Informatique specialite Administration de base de donnees Universite Sidi Mohamed Ben Abdellah  EST  - Fes 2010 - 2012 Baccalaureat Technique en Informatique de gestion Instituto Medio Industrial de Luanda Angola EXPÉRIENCE 3/2017 - 7/2017 Stage de fin d etudes Licence CGI Morocco Sidi Marouf Casablanca Maintenance et support applicatif des systemes mainframe cobol pacbase pour les societes de commerce en detail Carrefour Walmart. Developpement et conception de systemes en .NET et JEE comme un systeme de gestion de plans de travail.  Stage de fin detudes DUT C.H.U Hassan II Narjiss Fes Stage d initiation CompetenceCenter Centre ville Fes Developpement dun site web vitrine Technologies utilisees Joomla PHP  MySQL COMPÉTENCES Systeme dexplotation Notions avancees en Programmation Developpement Web Full-Stack Maitrise d administration de bases des donnees relationnelle BI  Big Data Machine Leaning  Deep Learning Linux MacOSX Windows Java Python JavaScript C PL/SQL SQL Prolog Nodejs ASPNET  Django Flask Vuejs JEE Oracle 11g Microsoft SQL Server PostgresSQL MySQL Microsof Data Integration Talend Studio Pentaho Integration SAP Business Object Apache Hadoop Apache Spark NoSQL Pandas TensorFlow Scikitlearn OpenCV NLP Outils de Travail  Gestion de Projet  Cloud Computing   Git Docker SSH Bash Scrum R Studio GitHub Microsoft Team Foundation BitBucket Kanban Microsoft Azure Kubernete Microsoft Office Slack Trello XP Google Cloud Computing FRANÇAIS ENGLISH PORTUGUESE", {"entities": [(1, 20, "NOM"),(22,41,"ADRESSE"),(43,55,"TELEPHONE"),(57,81,"duartealfredoj@gmail.com")]}),
    
]
TRAIN_DATA1 = [
    ("ALFREDO JAIRO DUARTE\nCasablanca-Marrocos\n212622333820  duartealfredoj@gmail.com jairoduarte.github.io", {"entities": [(0, 19, "NOM"),(23,43,"ADRESSE"),(45,57,"TELEPHONE"),(57,81,"duartealfredoj@gmail.com")]}),
    ("Govardhana K\nSenior Software Engineer\n\nBengaluru, Karnataka, Karnataka - Email me on Indeed: indeed.com/r/Govardhana-K/\nb2de315d95905b68\n\nTotal IT experience 5 Years 6 Months\n", {"entities": [(13, 37, "Designation"), (18, 24, "LOC")]}),
    ("I like London and Berlin.", {"entities": [(7, 13, "LOC"), (18, 24, "LOC")]}),
    ("Je aime manger la viande. dans la avenue hassan 2 à casa.", {"entities": [(33, 52, "ADRESSE"), (18, 23, "NOM")]}),
    ("Horses are too tall and they pretend to care about your feelings", {'entities': [(0, 6, 'ANIMAL')]}),
]

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model='fr_core_news_sm', output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("fr")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA1:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA1)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA1, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in TRAIN_DATA1:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        #print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            #print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == "__main__":
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]
