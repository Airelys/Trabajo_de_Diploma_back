import pandas as pd

def read (path):
    df = pd.read_excel(path,sheet_name=['Suceptibles','Infectados','Recuperados','Latentes'],header=None)
    s,i,r,e = [],[],[],[]
    
    column_s, column_i, column_r, column_e = ['Suceptibles','Infectados','Recuperados','Latentes']
    for index, row in df.iterrows():
        s.append(row[column_s])
        i.append(row[column_i])
        r.append(row[column_r])
        e.append(row[column_e])

    return s[1:],i[1:],r[1:],e[1:]

def read2 (path,sheet,names):
    df = pd.read_excel(path,sheet_name=sheet,header=None)
    i,r,e = [],[],[]
    
    column_i, column_r, column_e = names
    for index, row in df.iterrows():
        i.append(row[column_i])
        r.append(row[column_r])
        e.append(row[column_e])

    s =[1000]*len(i)

    return s[1:101],i[1:101],r[1:101],e[1:101]

