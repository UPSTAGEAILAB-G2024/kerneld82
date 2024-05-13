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

df1 = pd.read_excel('data/통화 및 부채/통화증가율_과_인플레이션율.xlsx')
df1 = df1.rename(columns={'통화량':'통화량', '인플레이션':'인플레이션'})

# 연도-월 컬럼 추가
ymList = list(map(lambda x: '%d-%02d' % (int(df1['기준연도'][x]), int(df1['기준월'][x])), range(len(df1))))
df1['ym'] = pd.DataFrame(ymList)

df2 = pd.read_csv('data/통화 및 부채/월간주택가격동향.csv')
df2 = df2.rename(columns={'매매지수':'매매지수', '전세지수':'전세지수', '월세지수':'월세지수'})

df3 = pd.read_csv('data/통화 및 부채/전처리_서울시_가계대출규모.csv')
df3 = df3.rename(columns={'합계':'대출_합계', '예금취급기관':'예금취급기관', '비은행예금취급기관':'비은행예금취급기관'})


dfMerged = pd.merge(left = df1, right = df2, on=['기준연도', '기준월'], how='inner')
dfMerged = pd.merge(left = dfMerged, right = df3, on=['기준연도', '기준월'], how='inner')

min_max_scaler = preprocessing.MinMaxScaler()
scale_columns = ['통화량', '인플레이션', '매매지수', '전세지수', '월세지수', '대출_합계']
dfMerged[scale_columns] = min_max_scaler.fit_transform(dfMerged[scale_columns])


fig = go.Figure()
fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['대출_합계'], mode='lines+markers', name='대출_합계'))
fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['통화량'], mode='lines+markers', name='통화량'))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['대출_합계'], mode='lines+markers', name='대출_합계'))
fig2.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['인플레이션'], mode='lines+markers', name='인플레이션'))

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['대출_합계'], mode='lines+markers', name='대출_합계'))
fig3.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['매매지수'], mode='lines+markers', name='매매지수'))

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['대출_합계'], mode='lines+markers', name='대출_합계'))
fig4.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['전세지수'], mode='lines+markers', name='전세지수'))

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['통화량'], mode='lines+markers', name='통화량'))
fig5.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['매매지수'], mode='lines+markers', name='매매지수'))

fig6 = go.Figure()
fig6.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['통화량'], mode='lines+markers', name='통화량'))
fig6.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['전세지수'], mode='lines+markers', name='전세지수'))

fig7 = go.Figure()
fig7.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['통화량'], mode='lines+markers', name='통화량'))
fig7.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['인플레이션'], mode='lines+markers', name='인플레이션'))

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
        html.P('통화량과 대출합계는 어느정도 정비례 관계가 있어 보이나, 그 끝은 통화량이 줄어들어도 대출은 뒤늦게 줄어들려는 걸 볼수 있음.'),
        dcc.Graph(figure=fig2),
        html.P('대출합계와 인플레이션은 어느정도 정비례 관계가 있어보임.'),
        dcc.Graph(figure=fig3),
        html.P('대출합계와 매매지수는 통화량과 대출합계와 같은 모습을 보임.'),
        dcc.Graph(figure=fig4),
        html.P('대출합계와 전세지수는 통화량과 대출합계와 같은 모습을 보임.'),
        dcc.Graph(figure=fig5),
        html.P('통화량과 매매지수는 같은 흐름의 모습을 보임.'),
        dcc.Graph(figure=fig6),
        html.P('통화량과 전세지수는 같은 흐름의 모습을 보임.'),
        dcc.Graph(figure=fig7),
        html.P('통화량과 인플레이션은 같은 흐름의 모습을 보임.'),
        html.H3('결론 : 2018년~2024년 동안 모든 것은 통화량을 따라간다.'),
    ])

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout
