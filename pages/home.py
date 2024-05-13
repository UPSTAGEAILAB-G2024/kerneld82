import json

import dash_bootstrap_components as dbc
from dash import html, ctx, Input, Output, State, clientside_callback, dcc, dash_table
import pandas as pd
import plotly.express as px
from sklearn import preprocessing
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolValidator

# 정부 정책 주석이 추가된 아파트매매실거래가격지수 그래프
def getAnnotatedSellPlot():
    # 아파트매매실거래가격지수
    dfSellIdx = pd.read_csv('data/Data.csv')
    dfSellIdx = dfSellIdx[dfSellIdx['기준년도'] >= 2018]

    # 정부 정책
    dfGov = pd.read_csv('data/정부_부동산_대책.csv')
    dfMerged = pd.merge(left = dfSellIdx, right = dfGov, on = ['기준년도', '기준월'], how = 'left')

    # 연도-월 컬럼 추가
    ymList = list(map(lambda x: '%d-%02d' % (int(dfMerged['기준년도'][x]), int(dfMerged['기준월'][x])), range(len(dfMerged))))
    dfMerged['ym'] = pd.DataFrame(ymList)

    #fig = px.scatter(dfMerged, x='ym', y='아파트매매실거래가격지수', text='약칭', line_shape='linear')
    #fig.update_traces(textposition='top center')

    #fig = go.Figure()
    #fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['아파트매매실거래가격지수'], mode='lines+markers+text', 
    #                         name='아파트매매실거래가격지수',
    #                         text=dfMerged['약칭'],
    #                         textposition="top center"))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dfMerged['ym'], y=dfMerged['아파트매매실거래가격지수'], mode='lines+markers+text', 
                            name='아파트매매실거래가격지수'))
    fig.update_layout(showlegend=True, height=600)

    dfForAnnotation = dfMerged
    dfForAnnotation.dropna(axis=0, inplace=True)

    # 정부 정책 주석 표시
    for i in range(len(dfForAnnotation)):
        fig.add_annotation(x=dfForAnnotation.iloc[i]['ym'], y=dfForAnnotation.iloc[i]['아파트매매실거래가격지수'], 
                        text=dfForAnnotation.iloc[i]['약칭'], showarrow=True,
                        font=dict(family='Courier New, monospace',
                                    size=13,
                                    color='blue'),
                        align='center',
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor='orange',
                        ax=dfForAnnotation.iloc[i]['annot_x'], ay=dfForAnnotation.iloc[i]['annot_y'],
                        bordercolor='red',
                        borderwidth=2,
                        borderpad=4,
                        bgcolor='yellow',
                        opacity=0.8)
    return fig

def get_sidebar(active_item=None):
    nav = html.Nav(id="sidebar", className="active", children=[
        html.Div(className="custom-menu", children=[
            html.Button([
                html.I(className="fa fa-bars"),
                html.Span("Toggle Menu", className="sr-only")
            ], type="button", id="sidebarCollapse", className="btn btn-primary")
        ]),
        html.Div(className="flex-column p-4 nav nav-pills", children=[
            html.A([
                html.Span("메뉴", className='fs-4'),
            ], className='d-flex align-items-center mb-3 mb-md-0 me-md-auto text-white text-decoration-none', href='/'),
            html.Hr(),
            dbc.NavItem(dbc.NavLink("홈", href="/", className='text-white', active=True if active_item=='pages.home' else False)),
            dbc.NavItem(dbc.NavLink("생활", href="/life", className='text-white', active=True if active_item=='pages.life' else False)),
            dbc.NavItem(dbc.NavLink("공급", href="/supply", className='text-white', active=True if active_item=='pages.supply' else False)),
            dbc.NavItem(dbc.NavLink("심리", href="/mind", className='text-white', active=True if active_item=='pages.mind' else False)),
            dbc.NavItem(dbc.NavLink("금리 및 물가", href="/interest", className='text-white', active=True if active_item=='pages.interest' else False)),
            dbc.NavItem(dbc.NavLink("통화 및 부채", href="/currency", className='text-white', active=True if active_item=='pages.currency' else False))
        ])
    ])
    return nav

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://cdn.cctoday.co.kr/news/photo/202311/2187993_626588_3232.jpg', alt='respiratory droplet', className="banner-image"),
                html.Div([
                    html.H1("서울 아파트 매매가 급등 및 급락에 영향을 주는 변수 탐색"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    layout_components = html.Div([
        #html.Div(children='My First App with Data and a Graph'),
        #dash_table.DataTable(data=dfMerged.to_dict('records'), page_size=10),
        dcc.Graph(figure=getAnnotatedSellPlot()),
    ])

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout

clientside_callback(
    """
    function(imageMapName) {
        const divElement = document.getElementById('genome_proteins_container');
        const originalMapElement = document.querySelector('map[name="image-map"]');
        const mapElement = originalMapElement.cloneNode(true);

        function updateCoords() {
            const imageRatio = 1200 / 909;
            const currentWidth = divElement.clientWidth - parseFloat(getComputedStyle(divElement).paddingLeft) - parseFloat(getComputedStyle(divElement).paddingRight);
            const currentHeight = currentWidth / imageRatio;

            const widthScale = currentWidth / 1200;
            const heightScale = currentHeight / 909;
            
            const originalAreas = originalMapElement.getElementsByTagName('area');
            const areas = mapElement.getElementsByTagName('area');
            for (let i = 0; i < areas.length; i++) {
                const originalCoords = areas[i].getAttribute('coords').split(',');
                const newCoords = originalCoords.map((coord, index) => {
                return index % 2 === 0 ? Math.round(coord * widthScale) : Math.round(coord * heightScale);
                });
                originalAreas[i].setAttribute('coords', newCoords.join(','));
            }
        }

        updateCoords();
        window.addEventListener('resize', updateCoords);
    }
    """,
    Output('image-map', 'style'),
    Input('image-map', 'name')
)

clientside_callback(
    """
    function(yes, name){
        if (name === 'active') {
            return '';
        } else if (name === '') {
            return 'active';
        }
    }
    """,
    Output('sidebar', 'className'),
    Input('sidebarCollapse', 'n_clicks'),
    State('sidebar', 'className')
)