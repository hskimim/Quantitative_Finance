# THREE FACTOR MODEL
##### Brief presentation
> FAMA AND FRENCH (1992)
<br/>
> every image slide is from document for education authorized by
<br/>
Oren Hovemann,Yutong Jiang,Erhard Rathsack,Jon Tyler
<br/>
CSV file is from http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html
<!-- --- -->
--------------------------------------------------------------------

### Contents

1. FF 3 factor 모델 살펴보기

2. β 를 추정하기 위한 데이터와 접근법

3. β 산출 기준

3. `평균수익률`과 `베타`, `평균수익률`과 `사이즈`의 관계

5. `평균수익률`과  `E/P` , `Leverage` , `BE/ME`의 관계

6. 포트폴리오 접근법과 선형회귀분석의 차이와 장단점

7. Fama-Macbeth 와 Fama-French 3 factor model 의 차이점

--------------------------------------------------------------------

# 1. FF 3 factor 모델 살펴보기

### This model was proposed in 1993 by Eugene Fama and Kenneth French to describe stock returns.

<img src="FF3.jpg">


- `(K_m - R_f)` 는 시장의 초과수익률입니다. 이는 미국에 있는 NYSE, AMEX 또는 NASDAQ 거래소에서 1 개월 재무부 채권 수익률을 뺀 모든 CRSP 기업의 가중 평균 수익률입니다.

  - `(K_m - R_f)` is the excess return of the market. It's the value-weighted return of all CRSP firms incorporated in the US and listed on the NYSE, AMEX, or NASDAQ minus the 1-month Treasury Bill rate.

- `SMB` (Small Minus Big)은 `시가 총액`이 즉, `규모` 큰 주식에 비해 시가 총액이 작은 주식의 초과 수익을 측정합니다.

  - `SMB` (Small Minus Big) measures the excess return of stocks with small market cap over those with larger market cap.

- `HML` (High-Minus Low)은 `성장주`에 대한 `가치주`의 초과 수익을 측정합니다.

  - `HML` (High Minus Low) measures the excess return of value stocks over growth stocks. Value stocks have high book to price ratio (B/P) than growth stocks.

--------------------------------------------------------------------
# 2. β 를 추정하기 위한 데이터와 접근법

> 논문의 1장은 예비 절차(Preliminaries)로 분석에 있어서 사용되는 데이터와 시장 베타의 측정 기준이 정리되어 있다.

 0. Fama-French 3 factor model 의 데이터 관측 시기는 `1963-1990년` 간이다.

 1. 데이터 분석은 `비금융회사`만을 포함하고 있다.(Data analysis includes only `non-financial companies`.)

- why ? :
    - 비금융회사에서 높은 레버레지는 재정적으로 불안정하다는 것을 의미하지만, 금융회사의 경우 정상적인 경우일 수 있다.
    - A high leverage in a non-financial company means financially unstable, but it may be normal for a financial company.

 2. `회계 변수`들은 그것이 설명하는 `수익률`보다 먼저 확인 가능하다.(`Accounting variables` can be checked before `profit rate` which it explains.)

- So what did they do :
    - t-1 년 (1962-1989) 에 있는 모든 회계연도 말의 회계 자료를, t 년 7월부터 t+1 년 6월까지의 수익률과 대응시킨다.
    - 회계년도 말과 수익률 테스트 간에 최소 6개월의 차이를 둔다.

- `WHICH` data they used and `WHEN` did they take them :

  - BE/ME , LEVERAGE , E/P , A : `t-1년의 12월 말` 시가총액(ME)을 사용

  - ME : `t 년의 6월` 시가총액을 사용

  - pre-ranking beta : t 년 7월 이전의 60개월 중 최소 24개월에 대한 데이터 즉, 최대 5년 최소 2년의 historical Data

--------------------------------------------------------------------

# 2. β 산출 기준

- 각각의 베타들을 추정하기 위해서는, 회귀분석 작업이 필요하다. 즉, 모든 베타들에 대해서 회귀 분석 작업이 들어간다.
    - 베타 : `ME , E/P , A/ME , A/BE , β_m`
    - 주식별 베타 수치는 별도의 계산을 통해서 만들어져야 한다  

#### Calculating Post - ranking beta

1. NYSE 주식을 시가총액 순으로 10분위 기준점을 잡는다. `(10*1)`
    - NASDAQ이 표본에 추가되면, 대부분의 포트폴리오에 small_cap 만 포함된다.
2. 사이즈 포트폴리오 내에서, NYSE 주식을 pre-ranking beta 순으로 정렬해 10분위 기준점을 잡는다. `(10*10)`
    - 사이즈-베타 포트폴리오는 7월~6월동안의 데이터로 만들어지고, 6월말에 리밸런싱된다.
3. 베타를 측정하는 방법 :
      - 시장의 당월 수익률, 전월 수익률 기준 기울기 합을 쓴다.
      - 비동시적으로 일어나는 거래를 조정하기 위함이다.


- return_p,t = beta_0 + `beta_1` * r_m,t_1 + `beta_2` * r_m,t + resid_p
- beta_p = beta_1 + beta_2


<img src="table_1.jpg">

##### 위의 표를 보고 베타에 대해 알 수 있는 2 가지 사실
- 각 사이즈 분위 안에서 post-ranking 베타는 pre-ranking 베타의 순서를 매우 유사하게 재현한다.
    - pre-ranking 베타가 실제 post-ranking 베타를 유사하게 재현한다. (재현력 , 예측력)

- `베타의 순서를 변형된 사이즈 순서가 아니다.
    -모든 사이즈 분위 내에서 ,ln(ME) 의 평균값은 베타로 정렬도니 세부 포트폴리오들 간에 유사한 값을 지닌다.`
--------------------------------------------------------------------
# 3. 평균수익률과 베타, 평균수익률과 사이즈의 관계
> (Banz(1981))에 의하면, 사이즈와 R 은 Negative , 베타와 R은 Positive 한 상관성이 있다고 했다.

<img src="table2_1.jpg">
<img src="table2_2.jpg">

표를 보게 되면, 평균수익률과 사이즈는 역상관성, 베타는 상관성을 띄는 것으로 보인다.

- `사이즈 포트폴리오 내에서 사이즈와 베타 간의 상관 관계에 의한 왜곡된 결과이다.`

- Panel B : Portfolios Formed on Pre-Ranking β
    - β 의 10분위 수가 1A(최소극단치)일때와 10B(최대극단치)일 때의 차이가 미비하다.
    - 1969년 이후로 시장 베타와 수익률의 관계가 사라졌다!! (Reinganum(1981), Lakonishok-Shapario(1986))

    - Table I 에서 사이즈 분위 내의 post-ranking 베타의 변화에 따른 평균 수익률의 변화를 보자!

### 사이즈와 연동된 베타는 평균수익률과 연관이 있다. 하지만, 무관한 베타는 상관관계가 없다.
- 사이즈 <-> 베타 (Negative) , 사이즈 <-> 평균수익률(Negative) , 베타 <-> 평균수익률(Positive)
--------------------------------------------------------------------
# 4. Fama-Macbeth Cross_sectional Regression
- 모든 베타 선정에 대한 근거 자료

<img src="table3.jpg">

--------------------------------------------------------------------
~~~
- 평균 수익률(R)과 사이즈(ME) 간에는 강한 상관관계가 있다.
- 평균 수익률(R)과 베타(β) 간에는 상관성이 없다.
~~~
--------------------------------------------------------------------
# 5. 평균수익률과  E/P , Leverage , BE/ME의 관계

<img src="table4_1.jpg">
<img src="table4_2.jpg">

- 평균수익률(R)과 E/P 의 관계는 U자형이다.
- 평균수익률(R)과 BE/ME 의 관계는 정상관성을 띈다.
    - 음수 BE/ME는 제외하였다.(50개 기업에 불과함.)
    - 음수, 양수 BE/ME 모두 기업의 부정적 전망(negative prospective)를 드러낸다.
- 베타(β)와 BE/ME 의 관계는 상관성은 보이지 않는다.
--------------------------------------------------------------------
~~~
- BE / ME 가 사이즈와는 다른(distinctive) 중요한 설명변수이다.
- BE / ME 가 레버리지 변수의 역할을 대체하고 , E / P 의 역할을 대체한다.
~~~
--------------------------------------------------------------------

1. BE / ME :
    - BE / ME 와 ME 가 Cross_sectional Regression 시에 대체되지 않고, 두 베타 모두 유의미하다.

2. Leverage :
    - 장부 레버리지(A/BE) , 시장 레버리지 (A/ME) 두 가지 변수 사용.
    - 로그함수가 평균수익률에서 레버리지 효과 포착이 용이하다.즉, ln(A/BE) , ln(A/ME) 을 사용한다.

    - `장부 레버리지는 Negative , 시장 레버리지는 Positive`
    - `장부 레버리지와 시장 레버리지의 절대값은 유사하다.`

    - (시장 레버리지) - (장부 레버리지) 변수가 유의미해진다. `ln(A/ME) - ln(A/BE) = ln(BE/ME)` 가 된다. 즉, BE/ME 와 leverage는 강한 연관성이 존재한다.

    - StoryLine :
        - BE/ME 가 높을 경우는,
        1. low ME  -> Negative prospect
        2. high BE -> Implicitly leveraged(impose by Market)

 3. E / P :
     - 기대수익률(R) 에서 누락된 위험 요인들을 포괄하는 변수라고 규정한다.(Ball(1978))
     - `BUT`
     - 사이즈와 BE/ME를 더하면 , E / P 더미(dummies)의 영향력이 사라진다.
     - `E/P와 BE/ME의 정상관성 때문이다.`

--------------------------------------------------------------------
### 아래의 표는 사이즈와 BM/ME 를 기준으로 10X10 포트폴리오를 만들고, 평균수익률(R)을 표시한 것이다.
<img src="table5.jpg">

- 사이즈를 통제하면 BM/ME 가 평균 수익률의 강한 변동을 포착하게 되고,BM/ME 를 통제하면, 수익률에 사이즈 효과가 남는다.

~~~
1. 사이즈와 관련 없는 베타는 평균 수익률과의 연관성이 존재하지 않는다.

2. 평균 수익률에 있어 시장 레버리지(A/ME)와 장부 레버리지(A/BE) 간의 반대되는 역할은, BE/ME에 의해 포착된다.

3. E/P와 평균 수익률 간의 반상관성은(Negative) BM/ME 에 의해 흡수된다.
~~~

### 사이즈(ME)와 BE/ME 간의 상관성

- 반상관성을 띈다.(Negative correlation(-0.26))
- StoryLine :
    1. 사이즈가 작으면(low ME)
    2. 시가총액이 낮다.
    3. 회사의 전망이 부정적이다.
    4. high BE/ME
    5. High Risk
