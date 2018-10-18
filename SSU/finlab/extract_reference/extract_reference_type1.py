import io
import re
import pandas as pd

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

def find_start_idx(file_) :
    ls = ['references','References','REFERENCES','참 고 문 헌' , '참고문헌','<참 고 문 헌>']
    start_idx = []
    start_idx = [re.search(i,file_).end() for i in ls if re.search(i,file_)][0]
    return start_idx

def find_end_idx(file_):
    end_idx = re.search(re.findall('[0-9]+[-][0-9]+',file_)[-1],file_).end()
    return end_idx

def make_references(file_):
    start_idx = find_start_idx(file_)
    end_idx = find_end_idx(file_)
    return file_[start_idx:end_idx]

def make_new_references(references):
    code_ls = re.findall('[0-9]+[-][0-9]+',references) + re.findall('[0-9]+[–][0-9]+',references)
    start_idx = sorted([references.find(code) for code in code_ls])
    end_idx = [val+len(code_ls[idx]) for idx,val in enumerate(start_idx)]
    code_idx = list(zip(start_idx,end_idx))
    code_idx.insert(0,(0,0))
    new_references = []
    for idx in range(len(code_ls)):
        new_references.append(references[code_idx[idx][1]:code_idx[idx+1][1]])
    return new_references

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
