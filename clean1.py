#!/usr/bin/env python3
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import math


def update_outcome_with_edplans(row):
    if row['edplans'] == 2:
        return 'Still Looking (Continuing Education)'
    return row['outcome']
    
def update_job_function(row):
    x = row['job_function']
    if x == 1:
        return 'Artist/performer'
    elif x == 2:
        return 'Consultant'
    elif x == 3:
        return 'Designer'
    elif x == 4:
        return 'Engineer'
    elif x == 5:
        return 'Entrepreneur'
    elif x == 6:
        return 'Financial analyst or advisor'
    elif x == 7:
        return 'Manager or administrator'
    elif x == 8:
        return 'Military service'
    elif x == 9:
        return 'Paralegal or legal aide'
    elif x == 10:
        return 'Policy analyst or political aide'
    elif x == 11:
        return 'Researcher'
    elif x == 12:
        return 'Scientific/lab technician'
    elif x == 13:
        return 'Software developer or programmer'
    elif x == 14:
        return 'Teacher (or teacher-in-training)'
    elif x == 15:
        return 'Writer/journalist/editor'
    elif x == 16:
        return 'Other'
    elif x == 17:
        return 'Sales or marketing associate '
    elif x == 18:
        return 'Business or market analyst'
    elif x == 19:
        return 'Data analyst or data scientist'  
    elif x == 20:
        return 'Nurse'
    elif x == 21:
        return 'Organizer, activist, or politician'
    elif x==16: 
        return row['jobdesc1_16_TEXT']

def update_country_with_liveinout(row):
    if row['liveinout'] == 1:
        return 'United States'

def update_outcome_with_emp_classes(row):
    if row['emp_class_1'] == 1:
        return 'Fellowship'
    elif row['emp_class_2'] == 1:
        return 'Working (Part-Time/Internship)'
    
    return row['outcome']

def update_employment_category_with_emp_classes(row):
    if row['emp_class_1'] == 1:
        return 'Fellowship'
    elif row['emp_class_2'] == 1:
        return 'Internship'
    elif row['emp_class_3'] == 1:
        return 'Freelancer'
    elif row['emp_class_4'] == 1: 
        return 'Freelancer'
    elif row['emp_class_5'] == 1: 
        return 'Temporary/Contract Work Assignment'
    
    return row['employment_category']

def update_outcome_with_job_plans(row):
    if row['jobplans'] == 3 or row['jobplans'] == 4 or row['jobplans'] == 5 :
        return 'Still Looking (Employment)' 
    return row['outcome']

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

def update_employer_name_with_volunteer(row):
    
    if row['ngo_pick'] == 1:
        return 'Peace Corps'
    elif row['ngo_pick'] == 2:
        return 'Teach for America'
    elif row['ngo_pick'] == 3:
        return 'City Year'
    elif row['ngo_pick'] == 4:
        return 'AmeriCorps'
    elif row['ngo_pick'] == 5:
        return 'Citizen Schools'
    elif row['ngo_pick'] == 6:
        return 'Alliance for Catholic Education'
    elif row['ngo_pick'] == 8:
        return 'Teaching Assistant Program in France'
    elif row['ngo_pick'] == 7:
        return row['ngo_pick_7_TEXT']

    return row['employer_name']

def update_outcome_with_military_volunteer(row):

    if row['military'] !=1:
        return 'Military'
    if row['ngo'] == 1: 
        return 'Volunteering'
    return row['outcome']

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

    df['Finished'] = df['Finished'].replace(1, 'true')
    df['Finished'] = df['Finished'].replace(0, 'false')
    
    df = df.drop(['RecordedDate'], axis=1)

    df['rescind'] = df['rescind'].replace(1, 'true')
    df['rescind'] = df['rescind'].replace(2, 'false')

    df = df.rename(columns={'ResponseId': 'response_id', 'rescind':'had_rescinded_offer', 'fellow_text': 'fellowship_name', 'firmname':'employer_name', 'jobtitle':'job_title', 'emptype':'employment_category', 'liveus':'state', 'livenonus':'country', 'jobdesc1':'job_function', 'jobsect':'employer_industry'})
    
    df['outcome'] = getOutcome(df)

    df = df.drop(['fall_12_TEXT', 'fall_1', 'fall_2', 'fall_3', 'fall_4', 'fall_5', 'fall_6', 'fall_7', 'fall_10', 'fall_11', 'fall_12'], axis=1)

    df['outcome'] = df[['outcome','military', 'ngo']].apply(update_outcome_with_military_volunteer, axis=1)

    df['employer_name'] = df[['ngo_pick', 'employer_name', 'ngo_pick_7_TEXT']].apply(update_employer_name_with_volunteer, axis=1)
    df = df.drop(['ngo_pick_7_TEXT', 'ngo_pick', 'nxact_text', 'primary', 'primary_6_TEXT', 'ngo', 'military'], axis=1)

    df['employer_name'] = df[['employer_name', 'Intern_text']].apply(update_employer_name_with_Intern, axis=1)

    df['outcome'] = df[['outcome', 'jobplans']].apply(update_outcome_with_job_plans, axis=1)
    df = df.drop(['jobplans'], axis=1)

    df['employment_category'].map({ 1:'Freelancer', 2:'Organization', 3:'Organization', 4:'Organization' })

    df['outcome'] = df[['outcome', 'emp_class_1', 'emp_class_2', 'emp_class_3', 'emp_class_4', 'emp_class_5']].apply(update_outcome_with_emp_classes, axis=1)
    df['employment_category'] = df[['employment_category', 'emp_class_1', 'emp_class_2', 'emp_class_3', 'emp_class_4', 'emp_class_5']].apply(update_employment_category_with_emp_classes, axis=1)
    df = df.drop(['emp_class_1', 'emp_class_2', 'emp_class_3', 'emp_class_4', 'emp_class_5'], axis=1)

    df['country'] = df[['country', 'liveinout']].apply(update_country_with_liveinout, axis=1)
    df = df.drop(['liveinout', 'workdesc', 'jobsect_32_TEXT', 'Rescind2'], axis = 1)

    df['job_function'] = df[['job_function','jobdesc1_16_TEXT']].apply(update_job_function, axis=1)
    df = df.drop(['jobdesc1_16_TEXT'], axis = 1)


    df['outcome'] = df[['outcome', 'edplans']].apply(update_outcome_with_edplans, axis = 1)

    #df.to_excel("output1.xlsx")  


if __name__ == "__main__":
    main()
