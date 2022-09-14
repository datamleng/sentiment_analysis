import re
import pytest


@pytest.fixture
def email_body_without_target_words():
    email_body_text = """Just a reminder we will have the initial meeting of the ENA/ AA Roundtable on 
        Friday at 9:00am in room EB30C1.  Again, the agenda is as follows:
        
        Discussion of PRC
        Immediate and future AA needs by business unit
        Skill shortages
        Campus and off-cycle recruitment
        Mottom 10% management
        Projecting AA needs from core schools for Summer 2001 intake
        Existing talent in specialist roles who should be in AA Program
        Ideas/suggestions on how we improve the Program/ENA retention
        
        Your groups need to be represented and if you can't attend please send 
        someone to represent you.  Those of you out of town need to call me if you 
        have any input.    Thanks again for all your support.  Ted"""
    return email_body_text


@pytest.fixture
def email_body_with_target_words():
    email_body_text = """Transwestern's average deliveries to California were 989 MMBtu/d (91%), with San Juan lateral throughput at 877 MMBtu/d.  Total East deliveries averaged 405 MMBtu/d.  
    El Paso's average deliveries to California were 2136 MMBtu/d (73%):
    - PG&ETop, capacity of 1140 MMBtu/d, deliveries of 615 MMBtu/d (54%)
    - SoCalEhr, capacity 1250 MMBtu/d, deliveries of 1011 MMBtu/d (81%)
    - SoCalTop, capacity 540 MMBtu/d, deliveries of 510 MMBtu/d (94%)
    
    Friday's posted Gas Daily prices:
        SoCal gas, large pkgs	  2.805 (+.08)
        PG&E, large pkgs	  2.81 (+.13)
        San Juan (non-Bondad)	  2.69 (+.125)   
        TW Permian		  2.64 (+.10)
    """
    return email_body_text


# Enron's oil & gas business test
def test_is_keyword_in_email_body(email_body_without_target_words, email_body_with_target_words):
    email_body_text = email_body_without_target_words
    search_result = re.findall(r'\b([a-z]*(Enron|oil|gas)[a-z]*)\b', email_body_text, re.I)
    assert search_result == []

    email_body_text = email_body_with_target_words
    search_result = re.findall(r'\b([a-z]*(Enron|oil|gas)[a-z]*)\b', email_body_text, re.I)
    assert search_result == [('Gas', 'Gas'), ('gas', 'gas')]

