#!/usr/bin/env python3
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import math


def update_job_function(df):

    list = ['Artist/performer','Consultant','Designer','Engineer','Financial analyst or advisor','Manager or administrator','Military service','Paralegal or legal aide', 'Policy analyst or political aide', 
    'Researcher', 'Scientific/lab technician', 'Software developer or programmer','Teacher (or teacher-in-training)',  'Writer/journalist/editor', 'Other', 'Sales or marketing associate', 'Business or market analyst', 'Data analyst or data scientist', 'Nurse', 'Organizer, activist, or politician']

    for i in range(len(list)):
        df.loc[df['job_function'] == (i+1), 'outcome'] = list[i]

    #need to edit other with jobdesc1_16_text
    df = df.drop(['jobdesc1_16_TEXT'], axis = 1)


def update_outcome_with_emp_classes(df):

    df.loc[df['emp_class_1'] == 1, 'outcome'] = 'Fellowship'
    df.loc[df['emp_class_1'] == 1, 'outcome'] = 'Working (Part-Time/Internship)'

def update_employment_category_with_emp_classes(df):

    df.loc[df['emp_class_1'] == 1, 'employment_category'] = 'Fellowship'
    df.loc[df['emp_class_2'] == 1, 'employment_category'] = 'Internship'
    df.loc[df['emp_class_3'] == 1, 'employment_category'] = 'Freelancer'
    df.loc[df['emp_class_4'] == 1, 'employment_category'] = 'Temporary/Contract Work Assignment'

    df = df.drop(['emp_class_1', 'emp_class_2', 'emp_class_3', 'emp_class_4', 'emp_class_5'], axis=1)


def update_employer_name_with_Intern(row):
    if isfloat(row['Intern_text']) == False:
        return row['Intern_text']
    return row['employer_name']

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def update_employer_name_with_volunteer(df):

    list = ['Peace Corps','Teach for America','City Year','AmeriCorps','Citizen Schools','Alliance for Catholic Education','other','Teaching Assistant Program in France']
    for i in range(len(list)):
        df.loc[df['ngo_pick'] == (i+1), 'employer_name'] = list[i]

    #need to edit other with ngo_pick_7_Text

def combine_fall_rows(row):

    if row['fall_1'] == 1 and row['fall_4']== 1:
        return 'Continuing Education'
    
    else:
        
        if row['fall_1'] == 1:
            return 'Working (Full-Time)'
        elif row['fall_2'] == 1: 
            return 'Working (Part-Time/Internship)'
        elif row['fall_3'] == 1: 
            return 'Working (Full-Time)'
        elif row['fall_4'] == 1: 
            return 'Continuing Education'
        elif row['fall_5'] == 1: 
            return 'Continuing Education'
        elif row['fall_6'] == 1: 
            return 'Continuing Education'
        elif row['fall_7'] == 1: 
            return 'Other'
        elif row['fall_10'] == 1: 
            return 'Other'
        elif row['fall_11'] == 1: 
            return 'Other'
        elif row['fall_12'] == 1: 
            return 'Other'

    return "None"

def getOutcome(df):

    lockedRows = df[['fall_1', 'fall_2','fall_3', 'fall_4','fall_5', 'fall_6','fall_7', 'fall_10','fall_11', 'fall_12' ]]
    return lockedRows.apply(combine_fall_rows, axis=1)

def main():
    print("Data Cleaning")
    df = pd.read_excel('data.xlsx', sheet_name='Sheet1', skiprows = [1])

    df['Finished'] = df['Finished'].replace({1:'true', 0:'false'})
    
    df = df.drop(['RecordedDate'], axis=1)

    df['rescind'] = df['rescind'].replace({1:'true', 2:'false'})


    df = df.rename(columns={'ResponseId': 'response_id', 'rescind':'had_rescinded_offer', 'fellow_text': 'fellowship_name', 'firmname':'employer_name', 'jobtitle':'job_title', 'emptype':'employment_category', 'liveus':'state', 'livenonus':'country', 'jobdesc1':'job_function', 'jobsect':'employer_industry'})
    
    df['outcome'] = getOutcome(df)

    df = df.drop(['fall_12_TEXT', 'fall_1', 'fall_2', 'fall_3', 'fall_4', 'fall_5', 'fall_6', 'fall_7', 'fall_10', 'fall_11', 'fall_12'], axis=1)

    df.loc[df['military'] != 1, 'outcome'] = 'Military'
    df.loc[df['ngo'] != 1, 'outcome'] = 'Volunteering'

    update_employer_name_with_volunteer(df)
    df = df.drop(['ngo_pick_7_TEXT', 'ngo_pick', 'nxact_text', 'primary', 'primary_6_TEXT', 'ngo', 'military'], axis=1)

    df['employer_name'] = df[['employer_name', 'Intern_text']].apply(update_employer_name_with_Intern, axis=1)

    
    df.loc[(df['jobplans'] == 3 ) | (df['jobplans'] == 4 ) | (df['jobplans'] == 5 ) , 'country'] = 'Still Looking (Employment)' 
    df = df.drop(['jobplans'], axis=1)

    df['employment_category'].map({ 1:'Freelancer', 2:'Organization', 3:'Organization', 4:'Organization' })

    update_outcome_with_emp_classes(df)    

    update_employment_category_with_emp_classes(df)

    df.loc[df['liveinout'] == 1, 'country'] = 'United States'
    df = df.drop(['liveinout', 'workdesc', 'jobsect_32_TEXT', 'Rescind2'], axis = 1)

    update_job_function(df)
    
    df.loc[df['edplans'] == 2, 'outcome'] = 'Still Looking (Continuing Education)'
    
    print(df.head(4))
    #print(df['outcome'])
    #df.to_excel("output1.xlsx")  


if __name__ == "__main__":
    main()
