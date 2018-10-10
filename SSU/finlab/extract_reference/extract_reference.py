import io
import re
import pandas as pd
 
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
 
def __extract_text_from_pdf(pdf_path):
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
    
    
def __make_references(start,end,file_):
    references = file_[re.search(start,file_).end():re.search(end,file_).end()+1]
    return references

def __make_new_references(references):
    code_ls = re.findall('[0-9]+[-][0-9]+',references)
    
    start_idx , end_idx =[],[]
    for i,val in enumerate(code_ls):
        start_idx.append(references.find(code_ls[i]))
        end_idx.append(references.find(code_ls[i]) + len(val))
    
    new_references = []
    for idx,val in enumerate(end_idx):
        if idx == 0: new_references.append(references[:val])
        else : new_references.append(references[end_idx[idx-1]:val])
            
    return new_references

def __make_idx(new_references,references):
    person_idx = []
    for idx,val in enumerate(new_references):
        person_idx.append(val[:val.find('“')])
    
    journal_idx = []
    for idx,val in enumerate(new_references):
        journal_idx.append(val[val.find('”')+1:])
        
    year_ls = []
    for idx,val in enumerate(new_references):
        if re.findall('20[0-9]{2}',val) or re.findall('19[0-9]{2}',val) != []:
            year_ls.append((re.findall('20[0-9]{2}',val) or re.findall('19[0-9]{2}',val))[0])
        else : year_ls.append('0')
    
    code_ls = re.findall('[0-9]+[-][0-9]+',references)
    
    df = pd.DataFrame()
    df['person'] = person_idx
    df['journal'] = journal_idx
    df['year'] = year_ls
    df['code'] = code_ls
    
    return df

def total_sequence_func(file_path,start,end):
    file_ = __extract_text_from_pdf(file_path)
    references = __make_references(start,end,file_)
    new_references = __make_new_references(references)
    df = __make_idx(new_references,references)
    return df