import os
import email

# This global variable is to limit the data load counts
DATA_LIMIT_COUNT = 50000


def get_file_lists_from_local(data_local_path: str) -> list:
    data_list = []
    for path, subDirectories, files in os.walk(data_local_path):
        for name in files:
            data_list.append(os.path.join(path, name))
    return data_list


def read_email(file_path: str):
    msg = ''
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = f.read()
            msg = email.message_from_string(data)
    except Exception as e:
        print(f"Retrying to open the file with ISO-8859-1 encoding...")
        try:
            # if any input is encoded wrong, try opening with "ISO-8859-1"
            with open(file_path, "r", encoding="ISO-8859-1") as f1:
                data = f1.read()
                msg = email.message_from_string(data)
        except Exception as e:
            print(f"File path: {file_path}, Error: {e}")
    return msg


def read_file_lists_from_local(local_path_lists: list) -> list:
    each_parsed_data = []
    progress_index = 1
    total_emails = len(local_path_lists)

    for file_path in local_path_lists:
        print(f"{progress_index}/{total_emails}")
        parsed_email_msg = read_email(file_path)
        each_parsed_data.append([parsed_email_msg['to'], parsed_email_msg['x-to'], parsed_email_msg['from'], parsed_email_msg['x-from'], parsed_email_msg.get_payload()])
        progress_index += 1

        if progress_index >= DATA_LIMIT_COUNT:
            break

    return each_parsed_data


def read_one_file_from_local(file_path: str) -> list:
    each_parsed_data = []
    parsed_email_msg = read_email(file_path)
    each_parsed_data.append([parsed_email_msg['to'], parsed_email_msg['x-to'], parsed_email_msg['from'], parsed_email_msg['x-from'], parsed_email_msg.get_payload()])
    return each_parsed_data
