import re

# Enron's oil & gas business


def is_keyword_in_email_body(email_body: str) -> bool:
    # search_result = re.findall(r'\b([a-z]*(Enron|oil|gas)[a-z]*)\b', email_body, re.I)
    search_result = re.findall(r'\b([a-z]*(cast)[a-z]*)\b', email_body, re.I)
    if len(search_result) >= 1:
        return True
    else:
        return False
