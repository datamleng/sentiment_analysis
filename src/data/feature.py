import nltk
import string
from time import time
from string import punctuation
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download(["stopwords"])
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

import spacy
try:
    import en_core_web_sm
    print("module en_core_web_sm is installed")
except ModuleNotFoundError:
    print("module en_core_web_sm is not installed")
    spacy.cli.download("en_core_web_sm")

from spacytextblob.spacytextblob import SpacyTextBlob


def get_nltk_sentiment_compound_score(df):
    sia = SentimentIntensityAnalyzer()

    start = time()
    df['nltk_sentiment_score'] = df['body'].apply(lambda body: sia.polarity_scores(body))
    df['nltk_compound'] = df['nltk_sentiment_score'].apply(lambda score_dict: score_dict['compound'])
    df['nltk_sentiment'] = df['nltk_compound'].apply(lambda c: 'pos' if c >= 0 else 'neg')
    df['nltk_sentiment_label'] = df['nltk_sentiment'].apply(lambda c: 1 if c == 'pos' else 0)
    end = time()
    print(f"NLTK - data preprocessing took {end - start}")
    return df


def get_spacy_sentiment_score(df):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')

    # Spacy has the limit of test length that can handle.
    MAX_TEXT_LENGTH = 10000
    spacy_polarity_score = []

    start = time()
    for i, row in df.iterrows():
        if MAX_TEXT_LENGTH > len(row['body']):
            doc = nlp(row["body"])
            spacy_polarity_score.append(doc._.blob.polarity)
        else:
            doc = nlp(row["body"][:MAX_TEXT_LENGTH])
            spacy_polarity_score.append(doc._.blob.polarity)

    df['spacy_polarity_score'] = spacy_polarity_score
    df['spacy_sentiment_label'] = df['spacy_polarity_score'].apply(lambda c: 1 if c > 0 else 0)
    end = time()
    print(f"Spacy - data preprocessing took {end - start}")
    return df


def clean_text_data(text: str) -> list:
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)

    # lemmatize tokens
    lemmatized_tokens = []
    for token in doc:
        if token.lemma_ == '-PRON-':
            word = token.lower_
        else:
            word = token.lemma_.lower().strip()
        lemmatized_tokens.append(word)

    # remove punctuation and stop words
    cleaned_tokens = []
    for token in lemmatized_tokens:
        if token not in stop_words and token not in string.punctuation:
            cleaned_tokens.append(token)

    return cleaned_tokens
