
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter,TextConverter,XMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import io
import re
import nltk
import json
import logging

def convert_json_to_spacy(filePath):
    try:
        training_data = []
        lines=[]
        with open(filePath, 'r') as f:
            lines = json.loads(f.read())
       
        for line in lines['train']:
            data = line
            text = data['content']
            entities = []
            for annotation in data['annotation']:
                #only a single point in text annotation.
                point = annotation['points'][0]
                labels = annotation['label']
                # handle both list of labels or a single label.
                if not isinstance(labels, list):
                    labels = [labels]

                for label in labels:
                    #dataturks indices are both inclusive [start, end] but spacy is not [start, end)
                    entities.append((point['start'], point['end'] + 1 ,label))
            training_data.append((text, {"entities" : entities}))

        return training_data
    except Exception as e:
        logging.exception("Unable to process " + filePath + "\n" + "error = " + str(e))
        return None

def preprocess( document):
    '''
    Information Extraction: Preprocess a document with the necessary POS tagging.
    Returns three lists, one with tokens, one with POS tagged lines, one with POS tagged sentences.
    Modules required: nltk
    '''
    try:
        # Try to get rid of special characters
        try:
           document.decode('ascii', 'ignore')
        except:
            document.encode('ascii', 'ignore')
        # Newlines are one element of structure in the data
        # Helps limit the context and breaks up the data as is intended in resumes - i.e., into points
        lines = [el.strip() for el in document.split("\n") if len(el) > 3]  # Splitting on the basis of newlines 
        lines = nltk.sent_tokenize(document)    # Tokenize the individual lines
        #lines = [nltk.pos_tag(el) for el in lines]  # Tag them
        # Below approach is slightly different because it splits sentences not just on the basis of newlines, but also full stops 
        # - (barring abbreviations etc.)
        # But it fails miserably at predicting names, so currently using it only for tokenization of the whole document
        sentences = nltk.sent_tokenize(document)    # Split/Tokenize into sentences (List of strings)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]    # Split/Tokenize sentences into words (List of lists of strings)
        tokens = sentences
        sentences = [nltk.pos_tag(sent) for sent in sentences]    # Tag the tokens - list of lists of tuples - each tuple is (<word>, <tag>)
        # Next 4 lines convert tokens from a list of list of strings to a list of strings; basically stitches them together
        dummy = []
        for el in tokens:
            dummy += el
        tokens = dummy
        # tokens - words extracted from the doc, lines - split only based on newlines (may have more than one sentence)
        # sentences - split on the basis of rules of grammar
        return tokens, lines, sentences
    except Exception as e:
        print('proc --')
        print(e)

def tokenize(inputString):
    try:
        tokens, lines, sentences = preprocess(inputString)
        return tokens, lines, sentences
    except Exception as e:
        print('tok')
        print(e)

def clean(content, char='<*=%>'):
    _content = str(content)
    clean = re.compile(char)
    content = (re.sub(clean, '',_content))
    #clean = re.compile('[-()\"#/;:<>{}`+=~|.!?,]')
    content = (re.sub(clean, '',content))
    clean = re.compile('(\w+=)')
    content = (re.sub(clean, '',content))
    content = content.replace('amp;','')
    content = content.replace('"','')
    content = content.replace('é','e')
    content = content.replace('ê','e')
    content = content.replace('è','e')
    content = content.replace('.*\n','')
    #p = [el.strip() for el in p.split(".*\n") if len(el) > 0]
    return content

def convert(fname, pages=None):
    if not pages: pagenums = set();
    else:         pagenums = set(pages);      
    manager = PDFResourceManager() 
    codec = 'utf-8'
    caching = True
    output = io.StringIO()
    converter = TextConverter(manager, output, codec=codec, laparams=LAParams())     
    interpreter = PDFPageInterpreter(manager, converter)   
    infile = open(fname, 'rb')

    for page in PDFPage.get_pages(infile, pagenums,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    convertedPDF = output.getvalue()  

    infile.close() 
    converter.close()
    output.close()
    return convertedPDF

def getCV(sentences):
    content =''
    for sent in sentences:
        for text,tag in sent:
            text = clean(text)
            if len(text) > 5:
                text = text.replace('-','dash')
                text = text.replace('@','commail')
            
            content+= ''.join(e for e in text if e.isalnum())
            content = content.replace('dash','-')
            content = content.replace('commail','@')
            content+=' '
        content+=" \n"
   
    arrayContent = [el.strip() for el in content.split('\n') if len(el) > 3]
    #[print(el) for el in arrayContent]
    return content, arrayContent
    #print(content.encode('utf-8'))

def getCVLines(sentences):
    content =''
    for lines in sentences:
        text = clean(lines)
        if len(text) > 5:
            text = text.replace('-','dash')
            text = text.replace('@','commail')
            text = text.replace('.','dotp')
            text = text.replace('/','slash')
        
        content+= ''.join(e for e in text if e.isalnum() or e == ' ' or e == '\n')
        content+=" \n"

    content = content.replace('dash','-')
    content = content.replace('commail','@')
    content = content.replace('dotp','.')
    content = content.replace('slash','/')
    arrayContent = [el.strip() for el in content.split('\n') if len(el) > 3]
    #[print(el) for el in arrayContent]
    return content, arrayContent
    #print(content.encode('utf-8'))
    

filename = "cv6.pdf"

def trainModel(model=None, output_dir=None, n_iter=10, data = None):
    """Load the model, set up the pipeline and train the entity recognizer."""
    import spacy
    from spacy.lang.fr.examples import sentences
    from spacy.lang.fr import French
    from sklearn.metrics import classification_report
    from sklearn.metrics import precision_recall_fscore_support
    from spacy.gold import GoldParse
    from spacy.scorer import Scorer
    from sklearn.metrics import accuracy_score
    import plac
    import random
    from pathlib import Path
    from spacy.util import minibatch, compounding
    
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("fr")  # create blank Language class
        print("Created blank 'fr' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")
    TRAIN_DATA = convert_json_to_spacy(filePath='data/traindata.json')
    # add labels
    for _, annotations in TRAIN_DATA:
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
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.2,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    """
    tp=0
    tr=0
    tf=0

    ta=0
    c=0 
    for text,annot in TRAIN_DATA:

        f=open("resume"+str(c)+".txt","w")
        doc_to_test=nlp(text)
        d={}
        for ent in doc_to_test.ents:
            d[ent.label_]=[]
        for ent in doc_to_test.ents:
            d[ent.label_].append(ent.text)

        for i in set(d.keys()):

            f.write("\n\n")
            f.write(i +":"+"\n")
            for j in set(d[i]):
                f.write(j.replace('\n','')+"\n")
        d={}
        for ent in doc_to_test.ents:
            d[ent.label_]=[0,0,0,0,0,0]
        for ent in doc_to_test.ents:
            doc_gold_text= nlp.make_doc(text)
            gold = GoldParse(doc_gold_text, entities=annot.get("entities"))
            y_true = [ent.label_ if ent.label_ in x else 'Not '+ent.label_ for x in gold.ner]
            y_pred = [x.ent_type_ if x.ent_type_ ==ent.label_ else 'Not '+ent.label_ for x in doc_to_test]  
            if(d[ent.label_][0]==0):
                
                (p,r,f,s)= precision_recall_fscore_support(y_true,y_pred,average='weighted')
                a=accuracy_score(y_true,y_pred)
                d[ent.label_][0]=1
                d[ent.label_][1]+=p
                d[ent.label_][2]+=r
                d[ent.label_][3]+=f
                d[ent.label_][4]+=a
                d[ent.label_][5]+=1
        c+=1
    for i in d:
        print("\n For Entity "+i+"\n")
        print("Accuracy : "+str((d[i][4]/d[i][5])*100)+"%")
        print("Precision : "+str(d[i][1]/d[i][5]))
        print("Recall : "+str(d[i][2]/d[i][5]))
        print("F-score : "+str(d[i][3]/d[i][5]))
    """
    if data is not None:
        doc = nlp(data)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
    else:
        for text, _ in TRAIN_DATA:
            doc = nlp(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


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
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

def main():
    
    #out.write(cv.encode('utf-8'))
    cv = convert(fname=filename)
   
    tokens, lines, sentences = tokenize(cv)
    trainModel(data=cv)
    #cv, arrayCV = getCV(sentences)
    cv_, arrayCV_ = getCVLines(lines)
    out = open(filename+"output.txt","w")
    [out.write(el) for el in cv_]
    
    out.close()
    return cv_
    """
    

    nlp = spacy.load('fr_core_news_sm')
    tokenizer = French().Defaults.create_tokenizer(nlp)

    texts = [u'One document.', u'...', u'Lots of documents']
    for doc in tokenizer.pipe(texts, batch_size=50):
        print(doc)

  
    doc = nlp(cv_)
    print(doc.text)
    for token in doc:
        print(token.text, token.pos_, token.dep_)
    """

if __name__ == "__main__":
   #trainModel(n_iter=50)
   main()
   #convert_json_to_spacy('data/traindata.json')
   