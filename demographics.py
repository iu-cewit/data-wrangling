# This script takes a list of email addresses from the CEWIT mailing list and
# cross-references it with demographic data to compile demographics for those
# on the mailing list

import csv
from def_split_email import *

fieldnames = ['Status', 'Program', 'Field', 'Last', 'First', 'Gender',
              'Email2', 'Email1', 'Ethnicity']

# Strip IU user IDs from email addresses and load into a list
with open('all_students_sep15.csv', 'r') as master:
    reader = csv.DictReader(master, fieldnames)
    next(reader, None)  # skip the header row
    student_list = []
    for student in reader:
        username = split_email(student.get('Email1'))[0]
        student_list.append(
            {
                'ID': username.lower(),
                'Status': student.get('Status'),
                'Program': student.get('Program'),
                'Field': student.get('Field'),
                'Last_Name': student.get('Last'),
                'First_Name': student.get('First'),
                'Gender': student.get('Gender'),
                'IU_Email': student.get('Email1'),
                'Alt_Email': student.get('Email2'),
                'Ethnicity': student.get('Ethnicity')
            }
        )

# set up for combining info from two files
fieldnames_in = ['last_name', 'first_name', 'email']
# The output file will include demographics for each person on mailing list.
# Copy the fields from the input file (mailing list) to the output file:
fieldnames_out = fieldnames_in.copy()
# Demographics to be added:
fields = ['Status', 'Program', 'Field', 'Gender', 'Ethnicity']
# Create list of fields for output file with mailing list and demographic
# fields included:
for item in fields:
    fieldnames_out.append(item)

with open('master_oct_15.csv', 'r', encoding='utf-8', errors='ignore') as \
        infile, open('demographics.csv', 'w') as outfile:
    reader = csv.DictReader(infile, fieldnames_in)
    next(reader, None)  # skip the header row
    writer = csv.DictWriter(outfile, fieldnames_out)
    writer.writeheader()
    for student in reader:
        temp = student.copy()  # first name, last name, and email
        email_acct = student.get('email')
        email_name = split_email(student.get('email'))[0]
        email_domain = split_email(student.get('email'))[1]
        student_info = [student for student in student_list if
                        student['ID'] == email_name.lower() or
                        student['Alt_Email'] == email_acct.lower()]
        if len(student_info) > 0:
            # if the student is matched, remove their demographic information
            # from the source list (student_list) so that if they are listed
            # in the mailing list more than once with the same IUID, they will
            # not also appear more than once in the final file.  This prevents
            # duplicates for IU addresses (e.g. nbrodnax@indiana.edu and
            # nbrodnax@umail.iu.edu are the same person but might both be
            # subscribed).  There still might be duplicates for people with
            # both IU and non-IU accounts but there is no way to verify a
            # match between a non-IU email and a particular student
            student_list.remove(student_info[0])
            for item in fields:
                temp[item] = student_info[0][item]
        else:
            for item in fields:
                temp[item] = 'N/A'
        writer.writerow(temp)
