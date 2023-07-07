import os
import pandas as pd
import re
from decouple import config

def get_email_addresses(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        email_addresses = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', content)
        return email_addresses

def get_email_subject(file_path):
    with open(file_path, 'r') as file:
            file_content = file.read()
            subject_list = []
            pre_start = 0
            start = 0

            while True:
                pre_start = file_content.find('|', start)
                if pre_start == -1:
                    break
                start = file_content.find('"', pre_start + 1)
                
                if start == -1:
                    break
                end = file_content.find('"', start + 1)
                if end == -1:
                    break

                text = file_content[start + 1: end]
                subject_list.append(text)
                start = end + 1

    return subject_list

# def content_extractor(directory_path, file_extension):
#     data = []
#     for file_name in os.listdir(directory_path):
#         if file_name.endswith(file_extension):
#             file_path = os.path.join(directory_path, file_name)
#             email_addresses = get_email_addresses(file_path)
#             email_subject = get_email_subject(file_path)
#             data.append({'File Name': file_name, 'Email Subject': email_subject, 'Email Addresses': ', '.join(email_addresses)})
#     df = pd.DataFrame(data)
#     return df

def content_extractor(directory_path, file_extension):
    file_data = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            if file_name.endswith(file_extension):
                file_path = os.path.join(root, file_name)
                email_addresses = get_email_addresses(file_path)
                email_subject = get_email_subject(file_path)
                file_data.append({'File Name': file_name, 'Email Subject': email_subject, 'Email Addresses': ', '.join(email_addresses)})
        for dir in dirs:
                dir_path = os.path.join(root, dir)
                file_data += content_extractor(dir_path, file_extension)  # Recursive call to process subfolders

    return file_data


# Need to replace 'directory_path' and 'file_extension' with the required values
directory_path = config('DIR_PATH')
file_extension = config('FILE_EXTENSION')
output_file_path = config('OUT_DIR_PATH')

file_date = content_extractor(directory_path, file_extension)


df = pd.DataFrame(file_date)
f_name = 'report_name_extraction.csv'
df.to_csv(os.path.join(output_file_path, f_name), sep='|', index=False)

# Exporting content in the same folder
# f_name = 'report_name_extraction.csv'
# df.to_csv(os.path.join(directory_path, f_name), sep='|' , index=False)

print(df)
