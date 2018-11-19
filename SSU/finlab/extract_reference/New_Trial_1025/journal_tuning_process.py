import re
import pandas as pd

def journal_tuning(df):

    process_ls = []

    for idx,val in enumerate(df['journal_refer'].values) : 
        try : 
            if df['journal_refer'].notnull()[idx] :
                process_ls.append(','.join(re.findall('\D',val)).replace(",",'').split(' : ')[0])
            else : process_ls.append(val)
        except : print('{} data in columns of journal_refer has problem. Please check it'.format(val))
            
    for idx,val in enumerate(process_ls) : 
        try : 
            process_ls[idx] = val.replace('(','').replace(')','')
        except : pass
        
    process_ls = [i for i in process_ls if i != '']

    for idx,val in enumerate(process_ls) : 
        if type(val) != float : 
            if val[-1] == ' ' :
                process_ls[idx] = val[:-1]
        else : pass            

    return process_ls