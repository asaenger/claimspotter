import nltk
import spacy
from pycontractions import Contractions

nlp = None
spacy_to_nl = {
    "PERSON": "person",
    "NORP": "nationality",
    "FAC": "infrastructure",
    "ORG": "organization",
    "GPE": "country",
    "LOC": "location",
    "PRODUCT": "product",
    "EVENT": "event",
    "WORK_OF_ART": "art",
    "LAW": "law",
    "LANGUAGE": "language",
    "DATE": "date",
    "TIME": "time",
    "PERCENT": "percentage",
    "MONEY": "money",
    "QUANTITY": "quantity",
    "ORDINAL": "first",
    "CARDINAL": "number"
}


def list_to_string(list):
    ret = ""
    for f in list:
        ret = ret + f + " "
    return ret.rstrip()


def char_list_to_string(list):
    ret = ""
    for f in list:
        ret = ret + f
    return ret


def get_tags(sentence):
    text = nltk.tokenize.word_tokenize(sentence)
    res = nltk.pos_tag(text)
    return res


def process_sentence_noun_rep(sentence):
    prc_res = get_tags(sentence)
    ret = []
    for p in prc_res:
        if p[1] == "POS":
            continue
        elif "NN" in p[1]:
            ret.append("noun")
        else:
            ret.append(p[0])
    return list_to_string(ret)


def process_sentence_full_tags(sentence):
    prc_res = get_tags(sentence)
    ret = []
    for f in prc_res:
        ret.append(f[1])
    return list_to_string(ret)


def process_sentence_ner_spacy(sentence):
    doc = nlp(sentence)
    ret = list(sentence)
    print(doc.ents)
    print(ret)
    adj = 0
    for ent in doc.ents:
        newlab = spacy_to_nl[ent.label_]
        print(ent.text, newlab, ent.text)
        del ret[ent.start_char - adj:ent.end_char - adj]
        temp = list(newlab)
        ret[ent.start_char - adj:ent.start_char - adj] = temp
        adj = adj + len(ent.text) - len(newlab)
    return char_list_to_string(ret)


def load_dependencies(args):
    global nlp

    # Load NLTK deps
    if args.noun_rep or args.full_tags or args.ner_spacy:
        print("Loading NLTK Dependencies...")
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('tagsets')
        if args.ner_spacy:
            print("Loading Spacy NER Tagger...")
            nlp = spacy.load("en_core_web_lg")
            print("Tagger loaded.")
        print("NLTK dependencies Loaded.")

    # Load word2vec model for contraction expansion
    print("Loading model from " + args.w2v_loc)
    cont = Contractions(args.w2v_loc)

    try:
        cont.load_models()
        print("Model Loaded.")
    except:
        raise Exception("Error: Model does not exist")


def load_deps_dummy():
    global nlp

    print("Loading NLTK Dependencies...")
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('tagsets')
    print("Loading Spacy NER Tagger...")
    nlp = spacy.load("en_core_web_lg")
    print("Tagger loaded.")
    print("NLTK dependencies Loaded.")


if __name__ == '__main__':
    load_deps_dummy()
    print(process_sentence_ner_spacy('I like Kevin Meng because he has lots of $50 million.'))
