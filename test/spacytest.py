import spacy
nlp_fr = spacy.load("fr")

# We create a text with several sentences in french
text_fr = "Ceci est 1 première phrase. Puis j'en écris une seconde. pour finir en voilà une troisième sans mettre de majuscule"

# We process the text through the pipeline
doc_fr = nlp_fr(text_fr)
print("Entities", [(ent.text, ent.label_) for ent in doc_fr.ents])
print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc_fr])
# We print the sentences
for sent in doc_fr.sents:
    print(sent)

doc_fr = nlp_fr('Je aime manger la viande dans la avenue hassan 2 à casa.')
print("Entities", [(ent.text, ent.label_) for ent in doc_fr.ents])
print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc_fr])
# We print the sentences
for sent in doc_fr.sents:
    print(sent)

doc_fr = nlp_fr(u"Ceci est 1 première phrase. Puis j'en écris une seconde. pour finir en voilà une troisième sans mettre de majuscule")
print("Entities", [(ent.text, ent.label_) for ent in doc_fr.ents])
print("Tokens", [(t.text, t.pos_, t.ent_iob) for t in doc_fr])