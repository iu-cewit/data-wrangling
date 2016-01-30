import csv

# read master list into a dictionary and load all the email addresses from the
# master list into a list
fieldnames = ["subscriber key", "last", "first", "email", "student",
              "undergrad", "masters", "professional", "phd", "faculty",
              "staff", "alum", "other", "appdes", "dighum", "game", "leader",
              "coding", "researchtech", "socialmed", "teachtech", "jobs",
              "service", "webdes"]

with open('mailing_list.csv', 'r') as master:
    reader = csv.DictReader(master, fieldnames)
    next(reader, None)  # skip the header row
    student_list = []
    for student in reader:
        student_list.append(student.get('email'))

# make a copy of the new admit list with a new column for whether the student's
# email is already in the master list
fieldnames_in = ['PRSN_PREF_LAST_NM',
                 'PRSN_PREF_1ST_NM',
                 'PRSN_PREF_MID_NM',
                 'PRSN_FERPA_RSTRCT_PRF_NM_IND',
                 'PRSN_PRM_LAST_NM',
                 'PRSN_PRM_1ST_NM',
                 'PRSN_PRM_MID_NM',
                 'PRSN_FERPA_RSTRCT_PRM_NM_IND',
                 'PRSN_GNDR_CD',
                 'STU_ADMT_TERM_CD',
                 'STU_LAST_ATND_TERM_CD',
                 'ACAD_PRM_PLAN_1_CD',
                 'ACAD_PRM_PLAN_1_DESC',
                 'ACAD_PRM_PLAN_2_CD',
                 'ACAD_PRM_PLAN_2_DESC',
                 'ACAD_PRM_PLAN_3_CD',
                 'ACAD_PRM_PLAN_3_DESC',
                 'ACAD_CAREER_CD',
                 'ACAD_DRVD_EXPND_LVL_NM',
                 'PRSN_CMP_EMAIL_ID',
                 'PRSN_FERPA_RSTRCT_C_EMAIL_IND']

fieldnames_out = fieldnames_in.copy()
fieldnames_out.append('IN_MASTER_LIST')
with open('new_admits.csv', 'r', encoding='utf-8', errors='ignore') as infile, \
        open('new_admits_clean.csv', 'w') as outfile:
    reader = csv.DictReader(infile, fieldnames_in)
    next(reader, None)  # skip the header row
    writer = csv.DictWriter(outfile, fieldnames_out)
    writer.writeheader()
    for student in reader:
        temp = student.copy()
        if student['PRSN_CMP_EMAIL_ID'] in student_list:
            temp['IN_MASTER_LIST'] = 'Yes'
        else:
            temp['IN_MASTER_LIST'] = 'No'
        writer.writerow(temp)
