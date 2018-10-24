import nltk
from nltk.corpus import stopwords
import string
import re
import pandas as pd
import numpy as np

def divide_kor_eng(new_references):
    korean_paper_list = [ref for ref in new_references if re.findall('[가-힣]+',ref)]
    korean_paper_list = [kor[re.search('[가-힣]+',kor).start():] for kor in korean_paper_list ]
    english_paper_list = [ref for ref in new_references if not re.findall('[가-힣]+',ref)]
    english_paper_list = [eng[re.search('[a-zA-Z]+',eng).start():] for eng in english_paper_list ]
    return korean_paper_list , english_paper_list

def latent_name_kor_eng(paper_list,kor=True):

    except_ls = list(string.printable[62:]) + ['“','”','``']

    if kor :
        i = 3
        latent_name_list = [(nltk.word_tokenize(word)[:i]) for word in paper_list]
        latent_name_list = [[val for idx,val in  enumerate(latent_name_list[i]) if not re.search('\d',val)] \
     for i in range(len(paper_list))]
        latent_name_list = [[val for val in latent_name_list[i] if val not in except_ls] for i in range(len(latent_name_list))]
    else :
        i = 8
        stop_words = set(stopwords.words('english'))
        latent_name_list = [(nltk.word_tokenize(word)[:i]) for word in paper_list]
        latent_name_list = [[val for idx,val in  enumerate(latent_name_list[i]) if not re.search('\d',val)] \
         for i in range(len(paper_list))]
        latent_name_list = [[val for val in latent_name_list[i] if val\
 not in stop_words] for i in range(len(latent_name_list))]
        latent_name_list = [[val for val in latent_name_list[i] if val not in except_ls]\
                            for i in range(len(latent_name_list))]

    return latent_name_list

def make_nltk_df(paper_list,kor=True):
    latent_name_list = ref2.latent_name_kor_eng(paper_list,kor=True)
    name_ls = [kor for kor in latent_name_list]
    year_ls = [re.findall('19[0-9]{2}|20[0-9]{2}',ref)[0] if re.findall('19[0-9]{2}|20[0-9]{2}',ref) else 0\
     for idx,ref in enumerate(paper_list)]
    double_quote_ls = [re.findall('“.+”',ref)[0] if re.findall('“.+”',ref) else 0\
     for idx,ref in enumerate(paper_list)]

    capture_df = pd.DataFrame(columns=['paper_list','year','quote'])
    capture_df['paper_list'] = paper_list
    capture_df['year'] = year_ls
    capture_df['quote'] = double_quote_ls
    capture_df['latent_name'] = latent_name_list
    return capture_df
