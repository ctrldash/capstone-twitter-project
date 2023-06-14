import sys, os
from translate import Translator
import pandas as pd


if __name__ == "__main__":
    translator = Translator(to_lang="de")
    df = pd.read_csv("tweets.csv")
    df.loc[:10, 'text'] = df.loc[:10, 'text'].apply(lambda x: translator.translate(x))
    translator = Translator(to_lang="uk")
    df.loc[10:20, 'text'] = df.loc[10:20, 'text'].apply(lambda x: translator.translate(x))
    translator = Translator(to_lang="es")
    df.loc[20:30, 'text'] = df.loc[20:30, 'text'].apply(lambda x: translator.translate(x))
    print(df.head(30))

    df.to_csv("lang_tweets.csv")