# Sentiment Analysis

### Dataset
The input of the assignment is the emails in the Sent folder from the Enron dataset: https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz
More information on the Enron dataset: https://www.cs.cmu.edu/~enron/ The output of the assignment is a service that does the following:

### Inputs
- a single Email. 
- The email can be any email. 
- The model is trained on the Enron data, but the service can receive any email.

### Outputs
- the sentiment of the Email body.
- if the Email body is related to Enron's oil & gas business, then the output also lists each Person or Organization mentioned.

### Requirements
- Please use Python for the service.
- Please return the assignment in either a zip file or via a url to a public GIT repository.

### Additional Requirements
- Ensure you are following best software engineering practices.
- The code follows the SOLID coding principles. (SOLID: https://dev.to/ezzy1337/a-pythonic-guide-to-solid-design-principles-4c8i)

### Approach
- Given dataset (Enron dataset) is not labeled, so I used NLTK and Spacy to get sentiment labels such as polarity and compound values. 
- After labeling the original dataset, trains a model and store the trained model.

# --------------------------------------------------------------------  

## Environment
1. Python 3.9

### How to run
- It requires two parameters: input and mode

1. Train mode
   - python3 main.py --input [email file path] --mode train
2. Run mode
   - python3 main.py --input [email file path] --mode run
3. Example
   - python3 main.py --input /User/email/ --mode train
   - python3 main.py --input /User/email/ --mode run


### Libraries and Tools
1. NLTK
2. Spacy
   - tokenization
   - lemmatization
   - remove stopwords and punctuation
3. Sklearn
   - inearSVC
4. Pytest
