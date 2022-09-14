import os
import email
import pytest


from data.load_data import read_email


@pytest.fixture
def data_local_path():
    test_data_path = "test/email"
    return test_data_path


@pytest.fixture
def file_path():
    test_file_path = "test/email/1."
    return test_file_path


@pytest.fixture
def local_path_lists():
    test_local_path_lists = ['test/email/3.', 'test/email/1.', 'test/email/2.']
    return test_local_path_lists


def test_get_file_lists_from_local(data_local_path: str):
    data_path = data_local_path
    data_list = []
    for path, subDirectories, files in os.walk(data_path):
        for name in files:
            data_list.append(os.path.join(path, name))
    assert data_list == ['test/email/3.', 'test/email/1.', 'test/email/2.']


def test_read_email(file_path: str):
    test_file_path = file_path
    msg = ''
    try:
        with open(test_file_path, "r", encoding="utf-8") as f:
            data = f.read()
            msg = email.message_from_string(data)
    except Exception as e:
        print(f"Retrying to open the file with ISO-8859-1 encoding...")
        try:
            # if any input is encoded wrong, try opening with "ISO-8859-1"
            with open(test_file_path, "r", encoding="ISO-8859-1") as f1:
                data = f1.read()
                msg = email.message_from_string(data)
        except Exception as e:
            print(f"File path: {test_file_path}, Error: {e}")
    print(msg)
    assert msg != []


def test_read_file_lists_from_local(local_path_lists: list):
    test_local_path_lists = local_path_lists
    each_parsed_data = []
    progress_index = 1

    for file_path in test_local_path_lists:
        parsed_email_msg = read_email(file_path)
        each_parsed_data.append([parsed_email_msg['to'], parsed_email_msg['x-to'], parsed_email_msg['from'], parsed_email_msg['x-from'], parsed_email_msg.get_payload()])
        progress_index += 1

    expected_output = [[None, '', 'taffy.milligan@enron.com', 'Taffy Milligan', 'The Credit Support Annex and Paragraph 13 (continued)'], [None, 'W2KMIG@ENRON_DEVELOPMENT', 'project.gem@enron.com', 'Project GEM', 'As you are probably aware, your department has been selected to participate \nin Project GEM (Global Enron Migration) for the rollout of Windows 2000.  In \npreparation for this rollout, it is imperative that we gather information \nabout your workstation and the applications you use.  To begin this data \ncollection, we have automated the process and your system has just been \ninventoried.   Once this information is received, we will be working with \nyour department co-ordinator, Sheri Cromwell, to consolidate this information \nto ensure this transition is as smooth as possible.\n\nThe GEM team would like to thank you for your participation.  If you have any \nquestions, please call Lee Steele at 713-345-8259.'], [None, '', 'taffy.milligan@enron.com', 'Taffy Milligan', 'Credit Support Annex and Paragraph 13']]
    assert each_parsed_data == expected_output


def test_read_one_file_from_local(file_path: str):
    test_file_path = file_path
    each_parsed_data = []
    parsed_email_msg = read_email(test_file_path)
    each_parsed_data.append([parsed_email_msg['to'], parsed_email_msg['x-to'], parsed_email_msg['from'], parsed_email_msg['x-from'], parsed_email_msg.get_payload()])
    print(each_parsed_data)

    expected_output = [[None, 'W2KMIG@ENRON_DEVELOPMENT', 'project.gem@enron.com', 'Project GEM', 'As you are probably aware, your department has been selected to participate \nin Project GEM (Global Enron Migration) for the rollout of Windows 2000.  In \npreparation for this rollout, it is imperative that we gather information \nabout your workstation and the applications you use.  To begin this data \ncollection, we have automated the process and your system has just been \ninventoried.   Once this information is received, we will be working with \nyour department co-ordinator, Sheri Cromwell, to consolidate this information \nto ensure this transition is as smooth as possible.\n\nThe GEM team would like to thank you for your participation.  If you have any \nquestions, please call Lee Steele at 713-345-8259.']]
    assert each_parsed_data == expected_output
