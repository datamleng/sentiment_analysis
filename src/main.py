import argparse
import pandas as pd

from data.load_data import get_file_lists_from_local,\
                                read_file_lists_from_local,\
                                read_one_file_from_local
from data.feature import get_nltk_sentiment_compound_score,\
                            get_spacy_sentiment_score
from model.model import train_sentimental_analysis_model,\
                            predict_sentimental_analysis
from algorithm.detect_relationship import is_keyword_in_email_body


def data_processing_for_sentimental_analysis(data_path):
    original_df = pd.DataFrame(data_path, columns=['to', 'x-to', 'from', 'x-from', 'body'])
    nltk_df = get_nltk_sentiment_compound_score(original_df)
    # We can also use Spacy to get the polarity score but in this exercise I use NLTK compound score
    # preprocessed_df = get_spacy_sentiment_score(nltk_df)
    return nltk_df


def display_sentiment_analysis_output(prediction_output, preprocessed_df, is_related_to_keywords=False):
    POSITIVE = [1]
    keywords = "Enron's oil & gas business"

    email_body = preprocessed_df['body'].item()
    email_body = email_body.replace("\n", "")
    email_body = email_body.replace("\t", "")

    email_to = preprocessed_df['to'].item()
    email_from = preprocessed_df['from'].item()

    output_string = ""
    if prediction_output == POSITIVE:
        output_string += f"Result: Positive.\n"
    else:
        output_string += f"Result: Negative.\n"

    if is_related_to_keywords:
        output_string += f"This email is related to {keywords}\n"
        output_string += f"Sender: {email_from}\n"
        output_string += f"Receiver: {email_to}\n"

    output_string += f"Email body: {str(email_body)}\n"
    print(f"{output_string}")


def main():
    input_parser = argparse.ArgumentParser(description='List the content of a folder', epilog='Enjoy the program! :)')
    input_parser.add_argument('--input',
                              action='store',
                              type=str,
                              required=True,
                              help='email file path')
    input_parser.add_argument('--mode',
                              action='store',
                              choices=['train', 'run'],
                              required=True,
                              help='service mode')

    args = input_parser.parse_args()

    data_path = "/Users/harrison/PycharmProjects/GlobalRelay/maildir"

    if args.mode == 'train':
        args.input = data_path
        data_path_list = get_file_lists_from_local(args.input)
        parsed_data_list = read_file_lists_from_local(data_path_list)

        preprocessed_df = data_processing_for_sentimental_analysis(parsed_data_list)
        train_sentimental_analysis_model(preprocessed_df)
    elif args.mode == 'run':
        data_path = "/Users/harrison/PycharmProjects/GlobalRelay/maildir/allen-p/_sent_mail/1."
        args.input = data_path

        # read an email data
        parsed_data_list = read_one_file_from_local(args.input)

        # data pre-processing
        preprocessed_df = data_processing_for_sentimental_analysis(parsed_data_list)

        # get a prediction output if it is positive or negative
        prediction = predict_sentimental_analysis(preprocessed_df)

        email_body = preprocessed_df['body'].item()
        email_body = email_body.replace("\n", "")
        email_body = email_body.replace("\t", "")

        # Check if the email body is related to Enron's oil & gas business
        is_found = is_keyword_in_email_body(email_body)

        # display the output
        display_sentiment_analysis_output(prediction, preprocessed_df, is_found)

    else:
        print(f"not supported")


if __name__ == "__main__":
    main()
