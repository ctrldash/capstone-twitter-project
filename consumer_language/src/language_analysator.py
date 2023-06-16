import spacy
from spacy.language import Language

from spacy_language_detection import LanguageDetector

class LanguageAnalysator:

    def __init__(self):

        def get_lang_detector(nlp, name):
            return LanguageDetector(seed=42)  # We use the seed 42
        
        self._nlp = spacy.load('en_core_web_sm')
        Language.factory("language_detector", func=get_lang_detector)
        self._nlp.add_pipe('language_detector', last=True)

    def run(self, text):
        doc = self._nlp(text)
        language = doc._.language['language']

        return language