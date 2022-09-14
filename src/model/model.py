import pickle

from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from data.feature import clean_text_data


def train_sentimental_analysis_model(df, text_column_name='body',
                                     label_column_name='nltk_sentiment_label',
                                     model_name='model/pipe.pickle') -> None:

    tfidf = TfidfVectorizer(tokenizer=clean_text_data)
    classifier = LinearSVC()

    X = df[text_column_name]
    Y = df[label_column_name]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=25)
    clf_pipe = Pipeline([('tfidf', tfidf), ('clf', classifier)], verbose=True)
    clf_pipe.fit(X_train, y_train)

    # store the trained model
    with open(model_name, 'wb') as pickle_file:
        pickle.dump(clf_pipe, pickle_file)


def predict_sentimental_analysis(df, text_column_name='body', model_name='model/pipe.pickle', text=''):
    # load the trained model
    with open(model_name, 'rb') as pickle_file:
        stored_pipe = pickle.load(pickle_file)

    if text == '':
        text = df[text_column_name]
        prediction = stored_pipe.predict(text)
    else:
        prediction = stored_pipe.predict(text)

    return prediction
