#!/usr/bin/env python3
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import math


def column_A_remapping(list):

    newCol=[]
    del list[0]

    for i in list:
        if i==1 :
            newCol.append('true')
        
        elif i==0 :
            newCol.append('false')
        

    jObject = {'Finished': newCol}
    return jObject

def colRename(newName, list):
    del list[0]
    JObject = {newName : list}

    return JObject

def column_D_remapping(list):
    
    newCol=[]
    del list[0]

    for i in list:
        if i==1 :
            newCol.append('true')
        
        elif i==2 :
            newCol.append('false')
        

    jObject = {'had_rescinded_offer': newCol}
    return jObject

def optionColumn(f1, f2, f3, f4, f5, f6, f7, f10, f11, f12):
    length = len(f1)
    #print(length)
    newList = []
    

    for i in range(length):
            
        if f1[i] == '1' and f4[i]== '1':
            newList.insert(i, 'Continuing Education')
        
        else:
            
            if f1[i] == '1' :
                newList.insert(i, 'Working (Full-Time)')
            elif f2[i] == '1': 
                newList.insert(i, 'Working (Part-Time/Internship)')
            elif f3[i] == '1': 
                newList.insert(i, 'Working (Full-Time)')
            elif f4[i] == '1': 
                newList.insert(i, 'Continuing Education')
            elif f5[i] == '1': 
                newList.insert(i, 'Continuing Education')
            elif f6[i] == '1': 
                newList.insert(i, 'Continuing Education')
            elif f7[i] == '1': 
                newList.insert(i, 'Other')
            elif f10[i] == '1': 
                newList.insert(i, 'Other')
            elif f11[i] == '1': 
                newList.insert(i, 'Other')
            elif f12[i] == '1': 
                newList.insert(i, 'Other')
            else:
                if i!= 0:
                    newList.insert(i-1, None)
    
    #print(len(newList))
    return newList   


def getOutcome(df):
    f1 = df['fall_1']
    f2 = df['fall_2']
    f3 = df['fall_3']
    f4 = df['fall_4']
    f5 = df['fall_5']
    f6 = df['fall_6']
    f7 = df['fall_7']
    f10 = df['fall_10']
    f11 = df['fall_11']
    f12 = df['fall_12']

    return optionColumn(f1, f2, f3, f4, f5, f6, f7, f10, f11, f10)

def updateOutcomeWithMilitaryData(outcomeList, militaryList):

    length = len(outcomeList)

    for i in range(length):

        if militaryList[i+1] !=1 :
            outcomeList[i]='Military'


def updateOutcomeWithVolunteerData(outcomeList, volunteerList):

    length = len(outcomeList)

    for i in range(length):

        if volunteerList[i+1] ==1 :
            #print(i+1)
            outcomeList[i]='Volunteering'



def volunteerEmployers(list, otherList):
    newList = [] 
    length = len(list) - 1

    for i in range(length):
        if list[i+1] == 1:
            newList.insert(i, 'Peace Corps')
        elif list[i+1] == 2:
            newList.insert(i, 'Teach for America')
        elif list[i+1] == 3:
            newList.insert(i, 'City Year')
        elif list[i+1] == 4:
            newList.insert(i, 'AmeriCorps')
        elif list[i+1] == 5:
            newList.insert(i, 'Citizen Schools')
        elif list[i+1] == 6:
            newList.insert(i, 'Alliance for Catholic Education')
        elif list[i+1] == 8:
            newList.insert(i, 'Teaching Assistant Program in France')
        elif list[i+1] == 7:
            newList.insert(i, otherList[i])
        else:
                newList.insert(i, None)

    return newList

def updateEmployerListWithIntern(employerList, colAA): 
    length = len(colAA) -1

    for i in range(length):
        
        if isfloat(colAA[i+1]) == False:
            #print(i+1)
            employerList[i] = colAA[i+1]
            

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def col_A_F_remapping(colAF, codeList, stateList):
    newList=[]
    length = len(colAF) - 1

    for i in range(length):
        x = float(colAF[i+1])
        if math.isnan(x) == False:

            code = colAF[i+1]
            #print('Code: ')
            #print(code)
            index = code -1
            if index < 62:
                state = stateList[index]
                newList.insert(i, state)
        else:
            newList.insert(i, None)

    return {'state': newList}

def  update_col_AG(colAG, colAE):
    newList =[]
    length = len(colAE) -1
    for i in range(length):
        if colAE[i+1] == 1:
            newList.insert(i, 'United States')
        else:
            newList.insert(i, colAG[i+1])
    
    return {'country': newList}

def updateOutcomeWithJopPlans(outcomeList, colAH):
    length = len(colAH) -1

    for i in range(length):
        x = colAH[i+1]
        if x == 3 or x == 4 or x == 5:
            print(i+1)
            outcomeList[i] = 'Still Looking (Employment)'

def main():
    print("Hello World")
    df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

    colA = df['Finished']
    newColA = column_A_remapping(colA)

    colC = df['ResponseId']
    newColC = colRename('response_id', colC)

    colD = df['rescind']
    newColD = column_D_remapping(colD)

    colOutcomeList = getOutcome(df)

    colP = df['military']
    updateOutcomeWithMilitaryData(colOutcomeList, colP)
    

    colQ = df['ngo']
    updateOutcomeWithVolunteerData(colOutcomeList, colQ)

    colR = df['ngo_pick']
    colS = df['ngo_pick_7_TEXT']
    employerList = volunteerEmployers(colR, colS)
    #print(employerList)

    colAA = df['Intern_text']
    updateEmployerListWithIntern(employerList, colAA)
    #print(employerList)

    colZ = df['fellow_text']
    newColZ = colRename('fellowship_name', colZ)

    colAF = df['liveus']
    df2 = pd.read_excel('data.xlsx', sheet_name='State codes')
    codeList = df2['Qualtrics code']
    stateList = df2['State']
    newColAF = col_A_F_remapping(colAF, codeList, stateList)

    colAG = df['livenonus']
    colAE = df['liveinout']
    newAG = update_col_AG(colAG, colAE)
    print(newAG)

    colAH = df['jobplans']
    updateOutcomeWithJopPlans(colOutcomeList, colAH)

    colAK = df['jontitle']
    newColAk = colRename('job_title', colAK)

    colBL = df['fallschool']
    newColBL = colRename('cont_ed_school', colBL)

    print(colOutcomeList)

    print("Done Processing")

if __name__ == "__main__":
    main()

