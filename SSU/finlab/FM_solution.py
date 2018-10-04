import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.api import *
from IPython.display import display , Markdown
import matplotlib.pyplot as plt
import statsmodels as sm
from patsy import dmatrix
import scipy as sp
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF
from FM_solution import *

def first_OLS(individual_stock_df,df):
    display(Markdown('시간 소요가 걸리는 작업입니다. 잠시만 기다려주세요!'))
    model_ls = []
    for idx,value in enumerate(individual_stock_df.index):
        model_ls.append(OLS(individual_stock_df.loc[value][:400].T,df.loc['market'][:, np.newaxis][:400]))
        result_ls = [i.fit() for i in model_ls]
        beta_ls = [i.params.values[0] for i in result_ls]
        resid_ls = [np.std(i.resid) for i in result_ls]

    return beta_ls , resid_ls

def first_sorting_beta_resid(beta_bundles1,resid_bundles1,df):

    # beta, residual ,stock_index 를 포함하는 DataFrame을 만들어준다.
    rank_df1 = pd.DataFrame()
    rank_df1['beta'] = beta_bundles1
    rank_df1['resid'] = resid_bundles1
    rank_df1['stock'] = df[(df.index != 'market')&(df.index != 'bias')].index
    rank_df1.reset_index(inplace=True)

    # 해당 데이터 프레임을 베타 순으로 sorting
    sorted_rank_df1 = rank_df1.sort_values(by='beta',ascending=True)

    #index를 크기 순으로 20개씩 자른다.
    testing_ls = []
    ranked_idx_ls = []
    popped_ls = list(sorted_rank_df1['index'])
    for _ in range(20):
        testing_ls = []
        for _ in range(20):
            testing_ls.append(popped_ls.pop())
        ranked_idx_ls.append(testing_ls)

    #stock_code를 크기 순으로 20개씩 자른다.
    testing_ls = []
    ranked_stock_ls = []
    popped_ls = list(sorted_rank_df1['stock'])
    for _ in range(20):
        testing_ls = []
        for _ in range(20):
            testing_ls.append(popped_ls.pop())
        ranked_stock_ls.append(testing_ls)

    sorted_beta_bundles = sorted(beta_bundles1)

    #beta를 크기 순으로 20개씩 자른다.
    ranked_beta_ls = []
    for i in range(20):
        ls = []
        for _ in range(20):
            ls.append(sorted_beta_bundles.pop())
        ranked_beta_ls.append(ls)

    #resid를 크기 순으로 20개씩 자른다.
    ranked_resid_ls = []
    for i in range(20):
        ls = []
        for _ in range(20):
            ls.append(resid_bundles1.pop())
        ranked_resid_ls.append(ls)

    #하나의 포트폴리오에 N개의 개별 종목들이 있고, 그 개별 종목들의 베타의 평균을 내준다. 즉, 포트폴리오 베타를 생성해준다.
    beta_ls1 = []
    for i in range(len(ranked_beta_ls)):
        beta_ls1.append(np.mean(ranked_beta_ls[i]))

    #하나의 포트폴리오에 N개의 개별 종목들이 있고, 그 개별 종목들의 잔차의 평균을 내준다. 즉, 포트폴리오 잔차를 생성해준다.
    resid_ls1 = []
    for i in range(len(ranked_resid_ls)):
        resid_ls1.append(np.mean(ranked_resid_ls[i]))
    #testing_df 는 1단계에서 pre_ranking $\beta_P$ 를 $sorting$ 해주는 프로세스에서 나온 데이터 프레임이다.
    testing_df = pd.DataFrame()
    testing_df['beta'] = beta_ls1
    testing_df['resid'] = resid_ls1
    testing_df['valued_stock_idx'] = ranked_idx_ls
    testing_df['valued_stock'] = ranked_stock_ls

    return beta_ls1 , resid_ls1 , ranked_stock_ls , ranked_idx_ls , testing_df

###################################################################################

def second_OLS(individual_stock_df,df,term=10,i=0):
    '''
    term : window batch size
    i = how far to go amount of batch size
    '''
    display(Markdown('시간 소요가 걸리는 작업입니다. 잠시만 기다려주세요!'))
    model_ls = []
    for idx,value in enumerate(individual_stock_df.index):
        model_ls.append(\
        OLS(individual_stock_df.loc[value][400+(term*i):900+(term*i)].T,\
            df.loc['market'][:, np.newaxis][400+(term*i):900+(term*i)]))\

        result_ls = [i.fit() for i in model_ls]
        beta_ls = [i.params.values[0] for i in result_ls]
        resid_ls = [np.std(i.resid) for i in result_ls]

    return beta_ls , resid_ls

def second_sorting_beta_resid(beta_bundles2 , resid_bundles2 , df , testing_df):

    # beta, residual ,stock_index 를 포함하는 DataFrame을 만들어준다.
    rank_df2 = pd.DataFrame()
    rank_df2['beta'] = beta_bundles2
    rank_df2['resid'] = resid_bundles2
    rank_df2['stock'] = df[(df.index != 'market')&(df.index != 'bias')].index
    rank_df2.reset_index(inplace=True)

    beta_ls2 = []
    for i in range(len(testing_df['valued_stock_idx'])):
        beta_ls2.append(np.mean(rank_df2.iloc[testing_df['valued_stock_idx'][i]]['beta']))

    resid_ls2 = []
    for i in range(len(testing_df['valued_stock_idx'])):
        resid_ls2.append(np.mean(rank_df2.iloc[testing_df['valued_stock_idx'][i]]['resid']))

    final_df = pd.DataFrame()
    final_df['beta'] = beta_ls2
    final_df['resid'] = resid_ls2
    final_df['stock_idx'] = testing_df['valued_stock_idx']
    final_df['stock'] = testing_df['valued_stock']

    return beta_ls2 , resid_ls2 , final_df
###################################################################################

def real_df(individual_stock_df,final_df,T=0,nth_term=1):
    '''
    gamma_1 : constant
    gamma_2 : market_beta
    gamma_3 : market_beta_square
    gamma_4 : standard_error
    '''
    gamma_1 , gamma_2 , gamma_3 , gamma_4 = [],[],[],[]
    real_df = pd.DataFrame()
    ls = []

    #final_df 에 있는 beta coefficient를 20개씩 배정해주는 반복문입니다.
    for i in final_df['beta']:
        for _ in range(20):
            ls.append(i)
    real_df['beta'] = ls

    ls = []

    #final_df 에 있는 residual coefficient를 20개씩 배정해주는 반복문입니다.
    for i in final_df['resid']:
        for _ in range(20):
            ls.append(i)
    real_df['resid'] = ls

    #testing_stock_df 는 전체 데이터프레임에서 market과 bias를 뺀 나머지 데이터 프레임인
    #individual_stock_df 중에서 기간 제약이 된 데이터 프레임 형태입니다.
    # [:,900+(10*(nth_term-1)):900+(10*nth_term)] 이 과정은 window shift 과정입니다.
    testing_stock_df = individual_stock_df.iloc[:,900+(10*(nth_term)):900+(10*(nth_term+1))]
    # cross_section regression에서 output variable 은 개별 종목의 수익률입니다.
    real_df['y'] = [testing_stock_df.iat[int(k),-1] for k in [j for i in final_df['stock_idx'].values for j in i]]

    model = OLS.from_formula('y ~ beta + I(beta ** 2) + resid',real_df)
    result = model.fit()

    gamma_1.append(result.params[0])
    gamma_2.append(result.params[1])
    gamma_3.append(result.params[2])
    gamma_4.append(result.params[3])

    return gamma_1 , gamma_2 , gamma_3 , gamma_4


def cross_sectional_func(individual_stock_df,final_df,T=0,nth_term=1):
    '''
    gamma_1 : constant
    gamma_2 : market_beta
    gamma_3 : market_beta_square
    gamma_4 : standard_error
    '''
    gamma_1 , gamma_2 , gamma_3 , gamma_4 = [],[],[],[]
    real_df = pd.DataFrame()
    ls = []

    #final_df 에 있는 beta coefficient를 20개씩 배정해주는 반복문입니다.
    for i in final_df['beta']:
        for _ in range(20):
            ls.append(i)
    real_df['beta'] = ls

    ls = []

    #final_df 에 있는 residual coefficient를 20개씩 배정해주는 반복문입니다.
    for i in final_df['resid']:
        for _ in range(20):
            ls.append(i)
    real_df['resid'] = ls

    #testing_stock_df 는 전체 데이터프레임에서 market과 bias를 뺀 나머지 데이터 프레임인
    #individual_stock_df 중에서 기간 제약이 된 데이터 프레임 형태입니다.
    # [:,900+(10*(nth_term-1)):900+(10*nth_term)] 이 과정은 window shift 과정입니다.

    for z in range(10):
        testing_stock_df = individual_stock_df.iloc[:,900+(10*(nth_term)):900+(10*(nth_term+1))]
        # cross_section regression에서 output variable 은 개별 종목의 수익률입니다.
        real_df['y'] = [testing_stock_df.iat[int(k),z] for k in [j for i in final_df['stock_idx'].values for j in i]]

        for i in range(20):
            testing_real_df = real_df.iloc[20*(i):20*(i+1)]
            model = OLS.from_formula('y ~ beta + I(beta ** 2) + resid',testing_real_df)
            result = model.fit()

            gamma_1.append(result.params[0])
            gamma_2.append(result.params[1])
            gamma_3.append(result.params[2])
            gamma_4.append(result.params[3])

    return gamma_1 , gamma_2 , gamma_3 , gamma_4
