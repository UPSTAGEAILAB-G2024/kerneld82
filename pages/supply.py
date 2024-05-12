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

df1 = pd.read_csv('data/공급량_관련/전처리/전처리_주택건설_분양실적_공동주택(월별_순계)_호.csv')
df1 = df1.rename(columns={'분양':'분양_분양', '임대':'분양_임대', '조합':'분양_조합', '합계':'분양_합계'})

# 연도-월 컬럼 추가
ymList = list(map(lambda x: '%d-%02d' % (int(df1['기준년도'][x]), int(df1['기준월'][x])), range(len(df1))))
df1['ym'] = pd.DataFrame(ymList)

df2 = pd.read_csv('data/공급량_관련/전처리/전처리_주택유형별_주택건설_인허가실적(월별_순계)_호.csv')
df2 = df2.rename(columns={'아파트':'인허가_아파트', '비아파트':'인허가_비아파트', '합계':'인허가_합계'})

df3 = pd.read_csv('data/공급량_관련/전처리/전처리_주택유형별_주택건설_준공실적(월별_순계)_호.csv')
df3 = df3.rename(columns={'아파트':'준공_아파트', '비아파트':'준공_비아파트', '합계':'준공_합계'})

df4 = pd.read_csv('data/공급량_관련/전처리/전처리_주택유형별_주택건설_착공실적(월계_순계)_호.csv')
df4 = df4.rename(columns={'아파트':'착공_아파트', '비아파트':'착공_비아파트', '합계':'착공_합계'})

dfMerged = pd.merge(left = df1, right = df2, on=['기준년도', '기준월'], how='inner')
dfMerged = pd.merge(left = dfMerged, right = df3, on=['기준년도', '기준월'], how='inner')

dfMerged = dfMerged.drop(['지역_y', '지역_x'], axis=1)

dfMerged = pd.merge(left = dfMerged, right = df4, on=['기준년도', '기준월'], how='inner')

dfMerged = dfMerged.drop(['지역_y', '지역_x'], axis=1)

dfSellIdx = pd.read_csv('data/Data.csv')

dfMerged = pd.merge(left = dfMerged, right = dfSellIdx, on=['기준년도', '기준월'], how='inner')

dfMerged = dfMerged.drop(['분양_분양', '분양_임대', '분양_조합', '인허가_비아파트', '인허가_합계', '준공_비아파트', '준공_합계', '착공_비아파트', '착공_합계', 
               '지가변동률', 'KB주택매매가격지수', 'KB주택전세가격지수', '아파트매매가격지수', '아파트전세가격지수', '아파트월세통합가격지수', 
               '한국은행 기준금리', '정부대출금리', '국민주택채권1종(5년)', '현금통화량', '중앙은행 대 예금취급기관부채', '가계 통화량', '기업 통화량', 
               '금융기관 통화량', '기타 통화량', '  주택담보대출-예금취급기관', '    주택담보대출-예금은행', '    주택담보대출-비은행예금취급기관', 
               '주택담보대출 - 주택금융공사 및 주택도시기금', '뉴스심리지수', '경제심리지수(원계열)', '경제심리지수(순환변동치)', '소비자물가지수(총지수)', 
               '소비자물가지수(주택임차료)', '소비자물가지수(전세)', '소비자물가지수(월세)', '생산자물가지수', '수입물가지수', '수출물가지수', '기대인플레이션'], axis=1)

min_max_scaler = preprocessing.MinMaxScaler()
scale_columns = ['분양_합계', '인허가_아파트', '준공_아파트', '착공_아파트', '아파트매매실거래가격지수']
dfMerged[scale_columns] = min_max_scaler.fit_transform(dfMerged[scale_columns])

fig = go.Figure()
fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['아파트매매실거래가격지수'], mode='lines+markers', name='아파트매매실거래가격지수'))
fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['인허가_아파트'], mode='lines+markers', name='인허가(아파트)'))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['아파트매매실거래가격지수'], mode='lines+markers', name='아파트매매실거래가격지수'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['착공_아파트'], mode='lines+markers', name='착공(아파트)'))

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['아파트매매실거래가격지수'], mode='lines+markers', name='아파트매매실거래가격지수'))
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['분양_합계'], mode='lines+markers', name='분양'))

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['아파트매매실거래가격지수'], mode='lines+markers', name='아파트매매실거래가격지수'))
fig4.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['준공_아파트'], mode='lines+markers', name='준공(아파트)'))

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://cdn.cctoday.co.kr/news/photo/202311/2187993_626588_3232.jpg', alt='공급', className="banner-image"),
                html.Div([
                    html.H2("공급"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    layout_components = html.Div([
        #html.Div(children='My First App with Data and a Graph'),
        #dash_table.DataTable(data=dfMerged.to_dict('records'), page_size=10),
        dcc.Graph(figure=fig),
        html.P('매매가와 인허가는 어느정도 정비례 관계가 있어보임.'),
        dcc.Graph(figure=fig2),
        html.P('매매가와 착공은 어느정도 정비례 관계가 있어보임.'),
        dcc.Graph(figure=fig3),
        html.P('매매가와 분양은 관련이 없어보임.'),
        dcc.Graph(figure=fig4),
        html.P('매매가와 준공은 관련이 없어보임.'),
        html.H3('결론 : 2018년~2024년 동안 매매가와 공급은 큰 관련이 없어보임.'),
    ])

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout
