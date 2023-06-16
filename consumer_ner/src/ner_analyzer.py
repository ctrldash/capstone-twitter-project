import logging
import json
import spacy
from langdetect import detect


logger = logging.getLogger('NER_ANALYZER')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)


class NerParser:
    def __init__(self) -> None:
        self.all_lang = ["en", "de", "es", "uk"]
        self.nlp = {lang: spacy.load(lang + "_core_news_sm") for lang in self.all_lang[1:]}
        self.nlp["en"] = spacy.load("en_core_web_sm")
        self.all_entities = ('CARDINAL', 'DATE', 'EVENT', 'FAC', 'GPE', 'LANGUAGE', 'LAW', 'LOC', 'MONEY', 'NORP', 'ORDINAL', 'ORG', 'PERCENT', 'PERSON', 'PRODUCT', 'QUANTITY', 'TIME', 'WORK_OF_ART')
        self.filter_out = ('CARDINAL', 'MONEY', 'ORDINAL', 'PERCENT', 'QUANTITY', 'CARDINAL')


    def find(self, text):
        lang = detect(text)
        if lang not in self.all_lang:
            lang = "en"
        
        doc = self.nlp[lang](text)
        result = [str(w.text) for w in doc.ents if w.label_ not in self.filter_out]
        if result:
            return {"entities": result}
        return {"entities": []}


if __name__ == "__main__":
    # test of functions:
    NER = NerParser()
    test_uk = """@VirginAmerica знаєте, що було б дивовижно дивовижно? Flight BOS-FLL, БУДЬ ЛАСКА!!!!!!!  10 днів! Я хочу літати тільки з вами."""
    test_en = """"@VirginAmerica And now the flight Flight Booking Problems site is totally down. Folks, what is the problem? I have to be there tomorrow/ Phone 911. 5 days I'm waiting."""
    test_de = """@VirginAmerica würde ernsthaft 30 $ für einen Flug für Sitze zahlen, die dieses Spiel nicht haben. es ist wirklich die einzige schlechte Sache am Fliegen VA"""
    test_es = """@VirginAmerica ¿Harás que BOS>LAS no se detenga permanentemente en el corto plazo?,,2015-02-24 08:27:52 -0800, Boston, MA """

    print(NER.nlp['en'].get_pipe('ner').labels)
    for text in [test_en, test_de, test_es, test_uk]:
        print(NER.find(text), "\n")