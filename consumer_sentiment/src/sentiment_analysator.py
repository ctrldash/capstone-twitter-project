import spacy
from spacytextblob.spacytextblob import SpacyTextBlob


class SentimentAnalysator:
    def __init__(self):
        self._nlp = spacy.load('en_core_web_sm')
        self._nlp.add_pipe('spacytextblob')

    def run(self, text):
        doc = self._nlp(text)
        sentiment = doc._.blob.polarity
        sentiment = round(sentiment, 2)

        print(sentiment)
        if sentiment > 0:
            sent_label = "Positive"
        else:
            sent_label = "Negative"

        return sent_label


if __name__ == '__main__':
    sample_text = [
        "@VirginAmerica I &lt;3 досить графіки. набагато краще, ніж мінімальна іконографія. :D",
        "@VirginAmerica son of the bitch, go fuck yourself, my flight 2/27 "
    ]
    an = SentimentAnalysator()
    for t in sample_text:
        print(an.run(t))




