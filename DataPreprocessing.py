import pandas as pd
import numpy as  np

#Old Students
path     = '/Users/emadezzeldin/Dropbox/Networking/DEAN690_2018/SageConference/students/Alumni'
name     = '/FullRecords.csv'
OldFile  = path + name
Old      = pd.read_csv (OldFile)
#print (Old)

#New Students
name     = '/DAEN_emails.xlsx'
NewFile  = path + name
New      = pd.read_excel (NewFile)
#print (New)

Students = pd.DataFrame()
Students ['New'] = New ['mails']
#print (Students)
Students ['Old'] = Old ['Emails']
#print (Students)
Students ['First'] = Old ['First']
Students ['Last']  = Old ['Last']
#print (Students)

Students ['Alumni']             = Old.Emails [~Old.Emails.isin(New.mails)]
#print (Students)
#Students.to_csv("Students.csv")
Students ['ContinuingStudents'] = Old.Emails [Old.Emails.isin(New.mails)]
Students ['NewStudents']        = New.mails [~New.mails.isin(Old.Emails)]
#print (Students)
Students.to_csv("Students.csv")

#Appendix and Useful Code Snippits
#===============================================================================
def myunionmerge (df1,df2,df3):
    mydf = pd.merge (df1,df2, how ='outer',on= 'Country')
    mydf2= pd.merge (mydf,df3, how = 'outer',on= 'Country')
    return mydf2
def myintersectmerge (df1,df2,df3):
    mydf = pd.merge (df1,df2, how ='inner',on= 'Country')
    mydf2= pd.merge (mydf,df3, how = 'inner',on ='Country')
    return mydf2
def unionminusintersection (df1,df2,df3):
    #u_1  = pd.merge (df1,df2,how = 'outer') #union
    #u_2  = pd.merge (u_1,df3,how = 'outer',indicator = True) #union
    #umi= u_2 [u_2['_merge'] != 'both']
    #df1 : union
    #df2 : intersection
    u  = myunionmerge     (df1,df2,df3)
    i  = myintersectmerge (df1,df2,df3)
    u_c= u ['Country'].values.tolist()
    i_c= i ['Country'].values.tolist()
    umi= [c for c in u_c if c not in i_c]
    return [umi,u_c,i_c]
def myoutermerge (df1,df2,df3):
    #union        = (myunionmerge (df1,df2,df3).set_index ('Country'))
    #intersection = (myintersectmerge (df1,df2,df3).set_index ('Country'))
    #subtraction  = union.set_index('Country').subtract(intersection.set_index('Country'), fill_value=0,axis='index')
    #R = union[~union.index.isin(intersection.index)]
    umi  = unionminusintersection (df1,df2)
    del (umi['_merge'])
    umi_2= unionminusintersection ( umi,df3)
    return  umi_2
#===============================================================================
