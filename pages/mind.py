import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ctx, dcc, html, dash_table
import pandas as pd
import plotly.express as px
from sklearn import preprocessing
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator

from .home import get_sidebar

dfSellIdx = pd.read_csv('data/Data.csv')

# KB부동산 -> 서울 매수우위지수 읽기
dfSellSuperiorityIdx = pd.read_csv('data/매수우위지수.csv')

dfMerged = pd.merge(left = dfSellIdx, right = dfSellSuperiorityIdx, on = ['기준년도', '기준월'], how = 'inner')

# 연도-월 컬럼 추가
ymList = list(map(lambda x: '%d-%02d' % (int(dfMerged['기준년도'][x]), int(dfMerged['기준월'][x])), range(len(dfMerged))))
dfMerged['ym'] = pd.DataFrame(ymList)

dfMerged['한국은행 기준금리 * 50'] = dfMerged['한국은행 기준금리'] * 50
dfMerged['지가변동률 * 50'] = dfMerged['지가변동률'] * 50
dfMerged['현금통화량 / 1000'] = dfMerged['현금통화량'] / 1000
dfMerged['가계 통화량 / 10000'] = dfMerged['가계 통화량'] / 10000
dfMerged['기대인플레이션 * 50'] = dfMerged['기대인플레이션'] * 50

dfNoJob = pd.read_csv('data/temp/실업률.csv')
dfNoJob['경제활동인구_취업자_합계 / 50'] = dfNoJob['경제활동인구_취업자_합계'] / 50
dfMerged = pd.merge(left = dfMerged, right = dfNoJob, on = ['기준년도', '기준월'], how = 'inner')

dfEarnConsume = pd.read_csv('data/서울시_1인당_지역내총생산_지역총소득_개인소득/전처리/전처리_개인소득소비.csv')
dfEarnConsume['가상? 가처분소득 / 20'] = dfEarnConsume['가상? 가처분소득'] / 20
dfMerged = pd.merge(left = dfMerged, right = dfEarnConsume, on = ['기준년도'], how = 'left')

dfDebt = pd.read_csv('data/서울시_가계대출규모/전처리/전처리_서울시_가계대출규모.csv')
dfDebt['서울시 가계대출규모 합계 / 5000'] = dfDebt['합계'] / 5000
dfMerged = pd.merge(left = dfMerged, right = dfDebt, on = ['기준년도', '기준월'], how = 'left')

dfMerged = dfMerged.drop(['Unnamed: 0_x', '지역_x', 'Unnamed: 0_y', '합계', '지역_y', '15세이상인구_합계', '15세이상인구_남자', '15세이상인구_여자', '경제활동인구_합계', '경제활동인구_남자',
       '경제활동인구_여자', '경제활동인구_취업자_남자', '경제활동인구_취업자_여자',
       '경제활동인구_실업자_합계', '경제활동인구_실업자_남자', '경제활동인구_실업자_여자', '비경제활동인구_합계',
       '비경제활동인구_남자', '비경제활동인구_여자', 'Unnamed: 0_y', 'Unnamed: 0', '예금취급기관', '예금은행',
       '비은행예금취급기관', '합계', '지역_y'], axis=1)

fig = go.Figure()
fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['KB매수우위지수'], mode='lines+markers', name='KB매수우위지수'))
fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['아파트매매실거래가격지수'], mode='lines+markers', name='아파트매매실거래가격지수'))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['KB매수우위지수'], mode='lines+markers', name='KB매수우위지수'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['한국은행 기준금리 * 50'], mode='lines+markers', name='한국은행 기준금리 * 50'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['지가변동률 * 50'], mode='lines+markers', name='지가변동률 * 50'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['현금통화량 / 1000'], mode='lines+markers', name='현금통화량 / 1000'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['가계 통화량 / 10000'], mode='lines+markers', name='가계 통화량 / 10000'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['소비자물가지수(총지수)'], mode='lines+markers', name='소비자물가지수(총지수)'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['생산자물가지수'], mode='lines+markers', name='생산자물가지수'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['수입물가지수'], mode='lines+markers', name='수입물가지수'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['수출물가지수'], mode='lines+markers', name='수출물가지수'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['기대인플레이션 * 50'], mode='lines+markers', name='기대인플레이션 * 50'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['서울시 가계대출규모 합계 / 5000'], mode='lines+markers', name='서울시 가계대출규모 합계 / 5000'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['경제활동인구_취업자_합계 / 50'], mode='lines+markers', name='경제활동인구 취업자 합계 / 50'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['가상? 가처분소득 / 20'], mode='lines+markers', name='(소득-소비) / 20'))
fig2.update_layout(width=1200, height=800)

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['KB매수우위지수'], mode='lines+markers', name='KB매수우위지수'))
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['한국은행 기준금리 * 50'], mode='lines+markers', name='한국은행 기준금리 * 50'))
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['지가변동률 * 50'], mode='lines+markers', name='지가변동률 * 50'))
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['기대인플레이션 * 50'], mode='lines+markers', name='기대인플레이션 * 50'))
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['서울시 가계대출규모 합계 / 5000'], mode='lines+markers', name='서울시 가계대출규모 합계 / 5000'))
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['가상? 가처분소득 / 20'], mode='lines+markers', name='(소득-소비) / 20'))
fig3.update_layout(width=1200, height=800)

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['KB매수우위지수'], mode='lines+markers', name='KB매수우위지수'))
fig4.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['한국은행 기준금리 * 50'], mode='lines+markers', name='한국은행 기준금리 * 50'))
fig4.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['기대인플레이션 * 50'], mode='lines+markers', name='기대인플레이션 * 50'))
fig4.update_layout(width=1200, height=800)

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['KB매수우위지수'], mode='lines+markers', name='KB매수우위지수'))
fig5.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['뉴스심리지수'], mode='lines+markers', name='뉴스심리지수'))



def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://cdn.cctoday.co.kr/news/photo/202311/2187993_626588_3232.jpg', alt='심리', className="banner-image"),
                html.Div([
                    html.H2("심리"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])
    
    kbBuyMindIdxStr = '''
KB매수우위지수 : 본 통계는 표본 공인중개사무소를 대상으로 표본 설문조사로 집계된 통계입니다.

조사항목은 매수자많음, 비슷함, 매도자많음 3개중 택1 입니다.

매수우위지수 = 100 + "매수자 많음" 비중 - "매도자 많음" 비중

매수우위지수가 100을 초과할수록 매수자가 많음을, 100 미만일수록 매도자가 많음을 의미합니다.
    '''
    
    layout_components = html.Div([
        #html.Div(children='My First App with Data and a Graph'),
        #dash_table.DataTable(data=dfMerged.to_dict('records'), page_size=10),
        dcc.Graph(figure=fig),
        html.P('매매가와 KB매수우위지수는 매우 관계가 있어보임.'),
        html.P(kbBuyMindIdxStr),
        dcc.Graph(figure=fig2),
        html.P('KB매수우위지수와 관련 있을것으로 예상되는 항목들을 그려봄.'),
        dcc.Graph(figure=fig3),
        html.P('KB매수우위지수와 관련 있어보이는 항목들을 추림. 특히, 기대인플레이션과 기준금리가 매우 관계가 있어보임.'),
        dcc.Graph(figure=fig4),
        html.P('기대인플레이션이 기준금리보다 선행하는 것으로 보임. 기대인플레이션이 높아지면 기준금리가 올라가고, 기대인플레이션이 낮아지면 기준금리가 내려감.'),
        dcc.Graph(figure=fig5),
        html.P('KB매수우위지수와 뉴스심리 지수는 관련이 있어보임. 특히 2019년 9월 ~ 2021년 2월은 매우 관계가 있어보임.'),
        html.H3('결론 : 2018년~2024년 동안 매매가와 심리는 매우 관련이 있어보임.'),
        html.H5('참고로 KB매수우위지수가 뾰족한 2018년 8월~10월 사이의 기사를 검색해보면, 상승 원인으로 개발 사업(GTX, 여의도 용산 개발), 공급 부족, 상대적으로 저렴한 아파트의 인기 상승이 있고, 하락 원인으로 9.13대책, 금리 인상 예측이 있다.'),
        html.H5('또한 2021년 7월~11월 사이의 기사를 검색해보면, 상승 원인으로 매물 부족, 영영 못 살것 같은 불안한 심리(영끌)가 있고, 하락 원인으로 무거워진 양도세, 기준금리 상승(8월 27일부터), 대출 규제(10월 26일 가계부채 관리 강화방안)가 있다.'),
    ])

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout
