import io
import re
import pandas as pd
import numpy as np
from IPython.display import display , Markdown

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

 # read pdf file
def extract_text_from_pdf(pdf_path):
    '''
    read pdf file into string type
    '''
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text

def extract_text_from_txt(path):
    with open(path,'rt') as f :
        lines = f.readlines()
    return ','.join(lines).replace('\n','')

################################################################################
def find_page_idx(file_):
    page_ls = []
    page_idx = [re.search((re.findall('\x0c[\d]*',file_)[i]),file_).end() for i in range(len(re.findall('\x0c[\d]+',file_)))]
    for idx,val in enumerate(page_idx):
        if idx ==0 :
            page_ls.append(file_[:val])
        else : page_ls.append(file_[page_idx[idx-1]:page_idx[idx]])
    return page_ls

def find_start_page(file_):
    ls = ['references','References','REFERENCES','참고 문헌','참 고 문 헌','참  고  문  헌' , '참고문헌','<참 고 문 헌>','Reference','reference','REFERENCE']
    ref_page = [idx for idx,val in enumerate(find_page_idx(file_)) for i in ls if i in val]
    if ref_page != [] : return ref_page[0]
    else :
        display(Markdown('### you should find another constraint'))
        print(file_)

def find_end_page_ex(file_):
    page_file = ref1.find_page_idx(file_)
    start_page = ref1.find_start_page(file_)
    ls3 = ['“' , '”' , '19[0-9]{2}' , '20[0-9]{2}' , 'Journal' , '[0-9]+[-][0-9]+']
    if len(page_file[start_page:]) == 1 : return 1
    for idx,page in enumerate(reversed(page_file[start_page:])):
        if (len(page_file[start_page:])-idx-1) > start_page :
            for i in ls3 :
                if len(re.findall(i,page)) <2 : pass
                else : return  len(page_file[start_page:])-idx-1
        else : return -1

def find_end_page_ex(file_):
    page_file = find_page_idx(file_)
    start_page = find_start_page(file_)
    ls3 = ['“' , '”' , '19[0-9]{2}' , '20[0-9]{2}' , 'Journal' , '[0-9]+[-][0-9]+']
    if len(page_file[start_page:]) == 1 : return 1
    for idx,page in enumerate(reversed(page_file[start_page:])):
        for i in ls3 :
            if len(re.findall(i,page)) <2 : pass
            else : return  len(page_file[start_page:])-idx-1

def make_references_page(file_):
    page_file = find_page_idx(file_)
    start_page = find_start_page(file_)
    end_page = find_end_page(file_)
    return page_file[start_page:start_page+end_page]

################################################################################

def find_start_idx(file_) :
    #'references'
    ls = ['References','REFERENCES','reference','Reference','REFERENCE','참고 문헌','참 고 문 헌','참  고  문  헌' , '참고문헌','<참 고 문 헌>','Reference','reference','REFERENCE']
    start_idx = []
    start_idx = [re.search(str(i),file_).end() for i in ls if re.search(i,file_)]
    if (start_idx != []) and (start_idx[0] < len(file_)) : return start_idx[0]
    else :
        start_idx = [re.search(str(i),file_).end() for i in ls if re.search(i,file_)]
        if (start_idx != []) and (start_idx < len(file_)) : return start_idx[0]
        else :
            display(Markdown('you might find another constraint.'))

def find_end_idx(file_):
    references = file_[find_start_idx(file_):]
    # ls = ['표 1','테이블 1','테 이 블 1','table 1','Table 1','TABLE 1' ,'Appendix 1','appendix 1','APPENDIX 1','부록','부 록','Endnotes','Figure 1','FIGURE 1',\
    # '표 I','테이블 I','테 이 블 I','table I','Table I','TABLE I' ,'Appendix I','appendix I','APPENDIX I','부록','부 록','Endnotes','Figure I','FIGURE I']
    ls = ['표 1','테이블 1','테이블','테 이 블 1','테 이 블','table 1','Table','Table 1','TABLE 1','TABLE' ,'Appendix','Appendix 1','appendix 1','APPENDIX 1','부록','부 록','Endnotes','Figure 1','FIGURE 1',\
    '표 I','테이블 I','테 이 블 I','table I','Table I','TABLE I' ,'Appendix I','appendix I','APPENDIX I','부록','부 록','Endnotes','Figure I','Figure','FIGURE I']
    testing_ls = [re.search('[\S]*'+str(i)+'[\S]*',references) for i in ls]
    testing_val = [idx for idx,val in enumerate(testing_ls) if val != None]
    testing_idx = [val.start() for idx,val in enumerate(testing_ls) if val != None]
    if testing_idx != []:
        return find_start_idx(file_) +  int(np.min(testing_idx))
        # end_idx =[(m.start(0), m.end(0)) for m in re.finditer(ls[testing_val[np.argmax(testing_idx)]],references)][-1][0]
        # if end_idx > find_start_idx(file_) :
            # return end_idx + find_start_idx(file_)
    else :
        end_idx = [(m.start(0),m.end(0)) for m in re.finditer(re.findall('[0-9]+[-][0-9]+',file_)[-1],file_)][-1][1]
        if end_idx < find_start_idx(file_) :
            display(Markdown('you might find another constraint.'))
            print(file_)
        else : return end_idx


def make_references(file_):
    start_idx = find_start_idx(file_)
    end_idx = find_end_idx(file_)
    return file_[start_idx:end_idx]

def make_new_references(file_):
    display(Markdown('make_references func is working on...'))
    references = make_references(file_)
    code_ls = re.findall('[0-9]+[-][0-9]+',references) + re.findall('[0-9]+[–][0-9]+',references) + re.findall('[0-9]+[~][0-9]+',references)
    start_idx = sorted([references.find(code) for code in code_ls])
    end_idx = [val+len(code_ls[idx]) for idx,val in enumerate(start_idx)]
    code_idx = list(zip(start_idx,end_idx))
    code_idx.insert(0,(0,0))
    new_references = []
    for idx in range(len(code_ls)):
        new_references.append(references[code_idx[idx][1]:code_idx[idx+1][1]])
    return new_references

def initial_split(file_):
    ls = ['OECD.','연구보고서','Publishing','Review','Institute','SSRN','대회','정기학술발표회','School','Prentice Hall','WorkingPaper' , 'Working Paper' , 'working paper' , 'Working paper' , 'University' , 'Uni' , 'university' , 'uni']
    references = ref1.make_references(file_)
    code_ls = [re.findall('[\S]*'+str(i)+'[\S]*',references) for i in ls]
    code_ls = list(set([j for i in code_ls for j in i]))
    start_idx = sorted([references.find(code) for code in code_ls])
    end_idx = [val+len(code_ls[idx]) for idx,val in enumerate(start_idx)]
    code_idx = list(zip(start_idx,end_idx))
    code_idx.insert(0,(0,0))
    new_references = []
    for idx in range(len(code_ls)):
        new_references.append(references[code_idx[idx][1]:code_idx[idx+1][1]])
    return new_references

def make_new_references_new_vers(file_,one_more_tuned=False):
    ls = ['[0-9]{4}년～[0-9]{4}년','[0-9]+[~][0-9]+','[0-9]+[–][0-9]+','[0-9]+[-][0-9]+','Elsevier','MIT','Press.','Forthcoming','forthcoming','WorkingPaper' , 'Working Paper' , 'working paper' , 'Working paper' , 'University' , 'Uni' , 'university' , 'uni',\
    'OECD.','연구보고서','연구원','한국은행','자원부','기술부','Publishing','Institute','SSRN','대회','정기학술발표회','School','Prentice Hall', 'national bureau','National Burea','National burea']
    references = make_references(file_)
    start_idx = [m.start(0) for m in re.finditer('[(]',references)]
    end_idx = [m.end(0) for m in re.finditer('[)]',references)]
    http_ls = [references[start_idx[idx]:end_idx[idx]] for idx in range(len(start_idx)) if 'http' in references[start_idx[idx]:end_idx[idx]]]
    for http in http_ls:
        references = re.sub(http,'',references)
    # new_references = make_new_references(file_)
    # new_references = [j for i in [ref.split('  ') for ref in new_references] for j in i]
    # code_ls = [re.findall(str(i),references) for i in ls]
    code_ls = [re.findall(i,references) for i in ls]
    code_ls = list(set([j for i in code_ls for j in i]))
    # start_idx = sorted([references.find(code) for code in code_ls])
    # end_idx = [val+len(code_ls[idx]) for idx,val in enumerate(start_idx)]
    testing_ls = sorted([(m.start(0),m.end(0))for i in ls for m in re.finditer(i,references)])
    testing_ls.insert(0,(0,0))
    new_references = [references[testing_ls[idx][1]:testing_ls[idx+1][1]] for idx in range(len(testing_ls)-1)]
    # code_idx = list(zip(start_idx,end_idx))
    # code_idx.insert(0,(0,0))
    # new_references = []
    # for idx in range(len(code_ls)):
    #     new_references.append(references[code_idx[idx][1]:code_idx[idx+1][1]])
    if one_more_tuned :
        new_references = [k for j in [i.split('  ') for i in new_references] for k in j]
    return new_references

def fine_tuning_the_new_ref(new_references):
    ls = ['pp. [0-9]+[-][0-9]','[0-9]+[~][0-9]+','[0-9]+[–][0-9]+','[0-9]+[-][0-9]+','Elsevier','MIT','Press.','Forthcoming','forthcoming','WorkingPaper' , 'Working Paper' , 'working paper' , 'Working paper' , 'University' , 'Uni' , 'university' , 'uni',\
    'OECD.','연구보고서','연구원','한국은행','자원부','기술부','Publishing','Institute','SSRN','대회','정기학술발표회','School','Prentice Hall', 'national bureau','National Burea','National burea']
    new_references = [k for j in [i.split('\x0c') for i in new_references] for k in j]
    capture_ls = []
    for idx,val in enumerate(new_references):
        if re.search('19[0-9]{2}',new_references[idx]) or re.search('20[0-9]{2}',new_references[idx]) :
            capture_ls.append(1)
        else : capture_ls.append(0)
    capture_str = ','.join([str(i) for i in capture_ls]).replace(',','')
    capture_idx = [(m.start(0),m.end(0)) for m in re.finditer('1[0]*',capture_str)]
    new_references = [new_references[capture_idx[idx][0]:capture_idx[idx][1]] for idx,val in enumerate(capture_idx)]
    new_references = [','.join(ref).replace(',','') for ref in new_references]

    for i in range(len(new_references)):
        if i == 0 : pass
        else :
            if re.search('20[0-9]+',new_references[i][:5]) or re.search('19[0-9]+',new_references[i][:5]) :
                ls = [(m.start(0),m.end(0))for m in re.finditer('20[0-9]+',new_references[i][:5])] + [(m.start(0),m.end(0))for m in re.finditer('19[0-9]+',new_references[i][:5])]
                new_references[i-1] += new_references[i][ls[0][0]:ls[0][1]]
                new_references[i] = new_references[i][ls[0][1]:]
            else : pass
    new_references = [re.sub('- .+ -','',i) for i in new_references]
    # testing_ls = sorted([(m.start(0),m.end(0)) for ref in new_references for i in ls for m in re.finditer(i,ref)])
    # testing_ls.insert(0,(0,0))
    return new_references

def finer_tuning_new_references(new_references):
    '''
    new_references 를 보다보니, fine tuning 과정에서 코드가 누락된 경우가 있어서 다시 패턴 분석해주었다.
    또한, 링크로 인해서 분할이 잘 안되는 부분을 고려하여 링크 부분 (Available at: http:~~) 를 없애주었다.
    마지막 반환 과정에서 비어있는 요소들은 포함하지 않기 위해서 제외하는 코드를 삽입하였다.
    '''
    idx_ls = []
    for idx,ref in enumerate(new_references):
        if re.search('[0-9]+[-][0-9]+',new_references[idx]):
            if re.search('[0-9]+[-][0-9]+',new_references[idx]).end() / len(new_references[idx]) < 0.975 :
                idx_ls.append(idx)
        else : pass

    for idx in idx_ls:
        new_references += re.split('[0-9]+[-][0-9]',new_references[idx])
    for idx in idx_ls :
        del new_references[idx]

    # new_references = [val[:re.search('[(].*http.+[)]',new_references[idx]).start()] if re.search('[(].*http.+[)]',new_references[idx]) \
     # else val for idx,val in enumerate(new_references)]

    return [ref for ref in new_references if len(ref) > 5 and ref != ' ' and ref != '']

################################################################################
def make_paper_ls(new_references):
    paper_ls = []
    for idx in range(len(new_references)):
        try :
            paper_ls.append(new_references[idx][re.search('“',new_references[idx]).start():re.search('”',new_references[idx]).end()])
        except:paper_ls.append('0')
    return paper_ls

def make_code_ls(new_references):
    code_ls = []
    for idx,val in enumerate(new_references):
        if re.findall('[0-9]+[-][0-9]+',val):
            code_ls.append(re.findall('[0-9]+[-][0-9]*',val))
        else:
            code_ls.append(re.findall('[0-9]+[–]+[0-9]*',val))
    return [j for i in code_ls for j in i]

def make_year_ls(new_references):
    year_ls = []
    for i in range(len(new_references)):
        if re.findall('19[0-9]{2}',new_references[i]):
            year_ls.append(re.findall('19[0-9]{2}',new_references[i]))
        else : year_ls.append(re.findall('20[0-9]{2}',new_references[i]))
    return [j for i in year_ls for j in i]

def make_person_ls(new_references):
    person_idx = []
    for i in range(len(new_references)):
        try :
            person_idx.append(new_references[i][:re.search('“',new_references[i]).start()])
        except :
            person_idx.append('0')

    for idx,val in enumerate(person_idx) :
        if ('---' in val) or ('___' in val):
            person_idx[idx] = person_idx[idx-1]
    return [i.replace(' ','') for i in person_idx]

def make_journal_ls(new_references):
    paper_ls = make_paper_ls(new_references)
    year_ls = make_year_ls(new_references)
    journal_idx = [new_references[idx]\
    [new_references[idx].find(paper_ls[idx])+len(paper_ls[idx]) : new_references[idx].find(year_ls[idx])]\
    for idx in range(len(new_references))]
    return journal_idx

def make_df(new_references):
    person_ls = make_person_ls(new_references)
    paper_ls = make_paper_ls(new_references)
    year_ls = make_year_ls(new_references)
    journal_ls = make_journal_ls(new_references)

    df = pd.DataFrame()
    df['person'] = person_ls
    df['journal'] = journal_ls
    df['year'] = year_ls

    return df
######################################################################
def sorting_name(i,new_references):
    '''
    대부분의 paper 에는 저자 다음에 년도가 나오기 마련이다.(most common case)
    해당 패턴을 이용해서 이름을 추출하는 함수이다.
    idx : 이름이 끝나는 시점이다.
    '''
    sorted_ls = sorted([(m.start(0) , m.end(0)) for m in re.finditer('20[0-9]{2}',new_references[i])] + \
    [(m.start(0) , m.end(0)) for m in re.finditer('19[0-9]{2}',new_references[i])])
    return sorted_ls[0][0],new_references[i][:sorted_ls[0][0]]

def sorting_year(i,new_references):
    '''
    해당 함수는 년도가 어디에 있건 찾을 수 있는 함수이다. 다만 년도 형태가 두 개일 경우 앞에 있는 것을 추출한다.
    idx : 년도의 패턴이 끝나는 시점이다.
    '''
    sorted_ls = sorted([(m.start(0) , m.end(0)) for m in re.finditer('20[0-9]{2}',new_references[i])] + \
        [(m.start(0) , m.end(0)) for m in re.finditer('19[0-9]{2}',new_references[i])])
    return sorted_ls[0][1],new_references[i][sorted_ls[0][0]:sorted_ls[0][1]]

# 논문 제목이 쌍따옴표로 갇혀 있는 경우
def paper_ls(references,new_references):
    if len(re.findall('“',references) + re.findall('”',references)) :
        idx_ls = [re.search('“.+”',ref) for ref in new_references]
        idx_ls = [(idx.start(),idx.end()) if idx else 0 for idx in idx_ls]
        paper_ls = [new_references[idx][idx_ls[idx][0]:idx_ls[idx][1]] if idx_ls[idx]!=0 else 0 for idx,ref in enumerate(new_references)]
    else :return -1
    return paper_ls

######################################################################3
def total_sequence_func(file_path):
    file_ = extract_text_from_pdf(file_path)
    references = make_references(file_)
    new_references = make_new_references(references)
    paper_ls = make_paper_ls(new_references)
    code_ls = make_code_ls(new_references)
    year_ls = make_year_ls(new_references)
    person_ls = make_person_ls(new_references)
    journal_ls = make_journal_ls(new_references)
    print(len(paper_ls) == len(year_ls) == len(person_ls) == len(journal_ls))
    df = make_df(new_references)

    return df
