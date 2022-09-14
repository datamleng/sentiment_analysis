import pytest
import pickle
import pandas as pd

from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from data.feature import clean_text_data


@pytest.fixture
def df():
    sample_data = [[None, 'W2KMIG@ENRON_DEVELOPMENT', 'project.gem@enron.com', 'Project GEM', 'As you are probably aware, your department has been selected to participate \nin Project GEM (Global Enron Migration) for the rollout of Windows 2000.  In \npreparation for this rollout, it is imperative that we gather information \nabout your workstation and the applications you use.  To begin this data \ncollection, we have automated the process and your system has just been \ninventoried.   Once this information is received, we will be working with \nyour department co-ordinator, Sheri Cromwell, to consolidate this information \nto ensure this transition is as smooth as possible.\n\nThe GEM team would like to thank you for your participation.  If you have any \nquestions, please call Lee Steele at 713-345-8259.']]
    test_df = pd.DataFrame(sample_data, columns=['to', 'x-to', 'from', 'x-from', 'body'])
    return test_df


def test_train_sentimental_analysis_model(df, text_column_name='body',
                                     label_column_name='nltk_sentiment_label',
                                     model_name='model/pipe.pickle') -> None:
    test_df = df

    tfidf = TfidfVectorizer(tokenizer=clean_text_data)
    classifier = LinearSVC()

    X = test_df[text_column_name]
    Y = test_df[label_column_name]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=25)
    clf_pipe = Pipeline([('tfidf', tfidf), ('clf', classifier)], verbose=True)
    clf_pipe.fit(X_train, y_train)

    assert True


def test_predict_sentimental_analysis(df, text_column_name='body', model_name='model/pipe.pickle', text=''):
    test_df = df

    # load the trained model
    with open(model_name, 'rb') as pickle_file:
        stored_pipe = pickle.load(pickle_file)

    if text == '':
        text = test_df[text_column_name]
        prediction = stored_pipe.predict(text)
    else:
        prediction = stored_pipe.predict(text)

    print(f"prediction: {prediction}")
    assert prediction == [0]
