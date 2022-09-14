import pytest
import pandas as pd
import nltk
import string
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


@pytest.fixture
def df():
    sample_data = [[None, 'W2KMIG@ENRON_DEVELOPMENT', 'project.gem@enron.com', 'Project GEM', 'As you are probably aware, your department has been selected to participate \nin Project GEM (Global Enron Migration) for the rollout of Windows 2000.  In \npreparation for this rollout, it is imperative that we gather information \nabout your workstation and the applications you use.  To begin this data \ncollection, we have automated the process and your system has just been \ninventoried.   Once this information is received, we will be working with \nyour department co-ordinator, Sheri Cromwell, to consolidate this information \nto ensure this transition is as smooth as possible.\n\nThe GEM team would like to thank you for your participation.  If you have any \nquestions, please call Lee Steele at 713-345-8259.']]
    test_df = pd.DataFrame(sample_data, columns=['to', 'x-to', 'from', 'x-from', 'body'])
    return test_df


@pytest.fixture
def text():
    sample_text = 'As you are probably aware, your department has been selected to participate'
    return sample_text


def test_get_nltk_sentiment_compound_score(df):
    sia = SentimentIntensityAnalyzer()

    # get data from pytest fixture
    test_df = df

    test_df['nltk_sentiment_score'] = test_df['body'].apply(lambda body: sia.polarity_scores(body))
    test_df['nltk_compound'] = test_df['nltk_sentiment_score'].apply(lambda score_dict: score_dict['compound'])
    test_df['nltk_sentiment'] = test_df['nltk_compound'].apply(lambda c: 'pos' if c >= 0 else 'neg')
    test_df['nltk_sentiment_label'] = test_df['nltk_sentiment'].apply(lambda c: 1 if c == 'pos' else 0)

    expected_output = (1, 9)
    assert test_df.shape == expected_output


def test_get_spacy_sentiment_score(df):
    nlp = spacy.load('en_core_web_sm')
    nlp.add_pipe('spacytextblob')

    # get data from pytest fixture
    test_df = df

    test_df['spacy_polarity_score'] = test_df['body'].apply(lambda doc: nlp(doc)._.blob.polarity)
    test_df['spacy_sentiment_label'] = test_df['spacy_polarity_score'].apply(lambda c: 1 if c > 0 else 0)

    expected_output = (1, 7)
    assert test_df.shape == expected_output


def test_clean_text_data(text: str) -> list:
    test_text = text

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(test_text)

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

    print(cleaned_tokens)
    expected_output = ['probably', 'aware', 'department', 'select', 'participate']
    assert cleaned_tokens == expected_output


