import os
from dateutil.parser import parse
import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ctx, dcc, html, callback, dash_table

from .home import get_sidebar

# Incorporate data
DASHBOARD_DATA_SET_PATH = 'data/developzest/dashboard_data'
DASHBOARD_INCOME_DATA = 'income.csv'
DASHBOARD_UNEMPLOYMENT_DATA = 'unemployment.csv'
DASHBOARD_POPULATION_DATA = 'population.csv'
DASHBOARD_REAL_ESTATE_PRICE_ALL_DATA = 'realestate_price_all.csv'
DASHBOARD_REAL_ESTATE_PRICE_PARTIAL_DATA = 'realestate_price_partial.csv'

income_df = pd.read_csv(os.path.join(DASHBOARD_DATA_SET_PATH, DASHBOARD_INCOME_DATA))
unemployment_rate_df = pd.read_csv(os.path.join(DASHBOARD_DATA_SET_PATH, DASHBOARD_UNEMPLOYMENT_DATA))
population_df = pd.read_csv(os.path.join(DASHBOARD_DATA_SET_PATH, DASHBOARD_POPULATION_DATA))
real_estate_price_all_df = pd.read_csv(os.path.join(DASHBOARD_DATA_SET_PATH, DASHBOARD_REAL_ESTATE_PRICE_ALL_DATA))
real_estate_price_partial_df = pd.read_csv(os.path.join(DASHBOARD_DATA_SET_PATH, DASHBOARD_REAL_ESTATE_PRICE_PARTIAL_DATA))
income_df['기준년월'] = income_df['기준년월'].apply(lambda x: parse(x))
unemployment_rate_df['기준년월'] = unemployment_rate_df['기준년월'].apply(lambda x: parse(x))
population_df['기준일'] = population_df['기준일'].apply(lambda x: parse(x))
real_estate_price_all_df['기준년월'] = real_estate_price_all_df['기준년월'].apply(lambda x: parse(x))
real_estate_price_partial_df['기준년월'] = real_estate_price_partial_df['기준년월'].apply(lambda x: parse(x))

data_income_df = income_df.copy().loc[:, '식료품_지출_총금액':]
for column in data_income_df.columns:
  data_income_df[column] /= income_df['지출_총금액']
data_income_df = pd.concat([income_df.loc[:, ['시군구명', '행정동_코드_명']], data_income_df], axis=1)
data_income_df = pd.pivot_table(data=data_income_df, index=['시군구명', '행정동_코드_명'], values=data_income_df.columns[2:])
data_income_df.columns = ['교육', '교통', '기타', '생활용품', '식료품', '여가', '유흥', '음식', '의료비', '의류']
data_income_df.reset_index(inplace=True)

value_population_df = population_df.loc[:, population_df.columns[8:]]
for column in value_population_df.columns:
  value_population_df[column] /= population_df['총생활인구수']
data_population_df = pd.concat([population_df.loc[:, population_df.columns[0:7]], value_population_df], axis=1)
# 행정동별 생활인구 연령 비율
pop_per_dong_df = pd.pivot_table(data=data_population_df, index=['시군구명', '행정동명', '행정동코드'], values=population_df.columns[8:]).reset_index()

income_df_for_corr = pd.pivot_table(data=income_df, 
                                  index=['기준년월', '기준년도', '기준월', '시도명', '시군구명'], 
                                  values=['소득_구간_코드', '소득_총금액', '지출_총금액'], aggfunc='mean').reset_index()
income_realestate_df = pd.merge(left=income_df_for_corr, right=real_estate_price_all_df, how='left', left_on=['기준년도', '기준월', '시군구명'], right_on=['기준년도', '기준월', '자치구'])
income_realestate_df.drop(columns=['기준년월_y','자치구'], inplace=True)
income_realestate_df.columns = ['기준년월', '기준년도', '기준월', '시도명', '시군구명', '소득_구간_코드', '소득_총금액', '지출_총금액', '매매가', '전세가', '월세가']
income_realestate_partial_df = pd.merge(left=income_df.loc[:, '기준년월':'지출_총금액'], right=real_estate_price_partial_df, how='inner', 
                     left_on=['기준년도', '기준월', '시도명', '시군구명', '행정동_코드_명', '행정동_코드'], 
                     right_on=['기준년도', '기준월', '시도명', '시군구명', '행정동_코드_명', '행정동_코드'])
income_realestate_partial_df.drop(columns=['기준년월_y'], inplace=True)
income_realestate_partial_df.columns = ['기준년월', '기준년도', '기준월', '시도명', '시군구명', '행정동_코드_명', '행정동_코드', '소득_총금액',
       '소득_구간_코드', '지출_총금액', '아파트_단지_수', '아파트_평균_면적', '아파트_평균_시가']

unemployment_rate_df.loc[:, ['기준년월', '기준년도', '기준월', '15세이상인구_합계', '경제활동인구_합계', '경제활동인구_취업자_합계', '경제활동인구_실업자_합계', '비경제활동인구_합계']].columns
pd.pivot_table(data=real_estate_price_all_df, index=['기준년도', '기준월'], values=['매매가', '전세가', '월세가'], aggfunc='mean').reset_index().head()
unemployment_rate_realestate_df = pd.merge(left=unemployment_rate_df.loc[:, ['기준년월', '기준년도', '기준월', '15세이상인구_합계', '경제활동인구_합계', '경제활동인구_취업자_합계', '경제활동인구_실업자_합계', '비경제활동인구_합계']],
         right=pd.pivot_table(data=real_estate_price_all_df, index=['기준년도', '기준월'], values=['매매가', '전세가', '월세가'], aggfunc='mean').reset_index(),
         left_on=['기준년도', '기준월'],
         right_on=['기준년도', '기준월'],
         how='inner')

# 총생활인구
population_all_realestate_df = pd.merge(left=population_df.loc[:, :'총생활인구수'].pivot_table(index=['기준년도', '기준월', '시도명', '시군구명'], values='총생활인구수', aggfunc='mean').reset_index(),
         right=real_estate_price_all_df, 
         left_on=['기준년도', '기준월', '시군구명'], 
         right_on=['기준년도', '기준월', '자치구'], 
         how='inner')
population_all_realestate_df.drop(columns=['자치구'], inplace=True)
population_all_realestate_df = population_all_realestate_df.loc[:, ['기준년월', '기준년도', '기준월', '시도명', '시군구명', '총생활인구수', '매매가', '전세가', '월세가']]
# 연령별비율
population_age_realestate_df = pd.merge(left=pd.pivot_table(data=data_population_df, index=['기준년도', '기준월', '시도명', '시군구명'], values=population_df.columns[8:]).reset_index(), 
         right=real_estate_price_all_df, 
         left_on=['기준년도', '기준월', '시군구명'], 
         right_on=['기준년도', '기준월', '자치구'], 
         how='inner')
population_age_realestate_df.drop(columns=['자치구'], inplace=True)
population_age_realestate_df = population_age_realestate_df.loc[:, ['기준년월', '기준년도', '기준월', '시도명', '시군구명', '0 ~ 9세', '10 ~ 14세', '15 ~ 19세',
       '20 ~ 24세', '25 ~ 29세', '30 ~ 34세', '35 ~ 39세', '40 ~ 44세', '45 ~ 49세', '50 ~ 54세', '55 ~ 59세', 
       '60 ~ 64세', '65 ~ 69세', '70세이상', '매매가', '전세가', '월세가']]

# Add controls to build the interaction
# 각 구별 아파트 가격 변동 그래프 콜백
@callback(
    Output(component_id='fig_real_estate_gu_sale_price', component_property='figure'),
    Input(component_id='dropdown_gu_real_estate_price_all', component_property='value')
)
def update_real_estate_gu_sale_price_graph(chosen):
    fig = px.line(real_estate_price_all_df.loc[real_estate_price_all_df['자치구'].isin(chosen)], 
                  x="기준년월", y="매매가", color='자치구', title='자치구별 아파트 매매가 변동')
    return fig
@callback(
    Output(component_id='fig_real_estate_gu_yearly_rent', component_property='figure'),
    Input(component_id='dropdown_gu_real_estate_price_all', component_property='value')
)
def update_real_estate_gu_yearly_rent_graph(chosen):
    fig = px.line(real_estate_price_all_df.loc[real_estate_price_all_df['자치구'].isin(chosen)], 
                  x="기준년월", y="전세가", color='자치구', title='자치구별 아파트 전세가 변동')
    return fig
@callback(
    Output(component_id='fig_real_estate_gu_monthly_rent', component_property='figure'),
    Input(component_id='dropdown_gu_real_estate_price_all', component_property='value')
)
def update_real_estate_gu_monthly_rent_graph(chosen):
    fig = px.line(real_estate_price_all_df.loc[real_estate_price_all_df['자치구'].isin(chosen)], 
                  x="기준년월", y="월세가", color='자치구', title='자치구별 아파트 월세가 변동')
    return fig
@callback(
    Output(component_id='fig_line_real_estate_dong_price', component_property='figure'),
    Input(component_id='dropdown_gu_real_estate_price_all', component_property='value')
)
def update_real_estate_dong_price_graph(chosen):
    fig = px.line(real_estate_price_partial_df.loc[real_estate_price_partial_df['시군구명'].isin(chosen)], 
                  x="기준년월", y="아파트_평균_시가", color="시군구명", line_group="행정동_코드_명", title='자치구별 아파트 평균 시가')
    return fig
@callback(
    Output(component_id='fig_scatter_real_estate_dong_price', component_property='figure'),
    Input(component_id='dropdown_gu_real_estate_price_all', component_property='value')
)
def update_real_estate_dong_price_graph(chosen):
    fig = px.scatter(real_estate_price_partial_df.loc[real_estate_price_partial_df['시군구명'].isin(chosen)], 
                     x="아파트_평균_면적", y="아파트_평균_시가", color="시군구명", size='아파트_단지_수', title='자치구별 아파트 평균 시가에 따른 평균 면적과 단지수의 분포')
    return fig

# 각 행정동별 소득소비 그래프 콜백
@callback(
  Output(component_id='dropdown_dong_income', component_property='options'),
  Input(component_id='dropdown_gu_income', component_property='value')
)
def set_dong_dropdown_options(selected_gu):
  return [{'label': i, 'value': i} for i in income_df.loc[income_df['시군구명'].str.contains(selected_gu)]['행정동_코드_명'].unique()]
@callback(
  Output(component_id='dropdown_dong_income', component_property='value'),
  Input(component_id='dropdown_dong_income', component_property='options')
)
def set_dong_dropdown_value(available_options):
  return available_options[0]['value']
@callback(
    Output(component_id='fig_bar_income', component_property='figure'),
    Input(component_id='dropdown_gu_income', component_property='value'),
    Input(component_id='dropdown_dong_income', component_property='value')
)
def update_income_bar_graph(selected_gu, selected_dong):
  df = data_income_df.loc[data_income_df['시군구명'].str.contains(selected_gu) & data_income_df['행정동_코드_명'].str.contains(selected_dong)].loc[:, '교육':].T.reset_index()
  df.columns = ['지출항목', '비율']
  fig = px.bar(df, x='지출항목', y='비율', title=f'{selected_gu} {selected_dong}의 월평균 총소득액 대비 지출항목 비중', color='지출항목')
  return fig
@callback(
    Output(component_id='fig_pie_income', component_property='figure'),
    Input(component_id='dropdown_gu_income', component_property='value'),
    Input(component_id='dropdown_dong_income', component_property='value')
)
def update_income_pie_graph(selected_gu, selected_dong):
  df = data_income_df.loc[data_income_df['시군구명'].str.contains(selected_gu) & data_income_df['행정동_코드_명'].str.contains(selected_dong)].loc[:, '교육':].T.reset_index()
  df.columns = ['지출항목', '비율']
  fig = px.pie(df, names='지출항목', values='비율', title=f'{selected_gu} {selected_dong}의 월평균 총소득액 대비 지출항목 비중', color='지출항목')
  return fig

# 서울시 경제활동인구 통계 그래프 콜백
@callback(
    Output(component_id='fig_line_unemployment_rate', component_property='figure'),
    Input(component_id='radio_unemployment_rate', component_property='value')
)
def update_unemployment_rate_item_graph(col_chosen):
    fig = px.line(unemployment_rate_df[['기준년월', col_chosen]], x="기준년월", y=col_chosen, title=f'{col_chosen} 추이')
    return fig

# 서울시 생활인구 그래프 콜백
@callback(
    Output(component_id='fig_bar_dong_per_gu_population', component_property='figure'),
    Input(component_id='dropdown_gu_population', component_property='value')
)
def update_population_dong_per_gu_graph(selected_gu):
  df = pd.pivot_table(data=population_df, index=['시도명', '시군구명', '행정동명', '행정동코드'], values='총생활인구수', aggfunc='mean').reset_index()
  fig = px.bar(df[df['시군구명'].str.contains(selected_gu)], x='행정동명', y='총생활인구수', color='행정동명', title=f'{selected_gu}의 행정동별 월평균 총생활인구수')
  return fig
@callback(
  Output(component_id='dropdown_dong_population', component_property='options'),
  Input(component_id='dropdown_gu_population', component_property='value')
)
def set_dong_dropdown_options(selected_gu):
  return [{'label': i, 'value': i} for i in population_df.loc[population_df['시군구명'].str.contains(selected_gu)]['행정동명'].unique()]
@callback(
  Output(component_id='dropdown_dong_population', component_property='value'),
  Input(component_id='dropdown_dong_population', component_property='options')
)
def set_dong_dropdown_value(available_options):
  return available_options[0]['value']
@callback(
    Output(component_id='fig_pie_dong_population', component_property='figure'),
    Input(component_id='dropdown_gu_population', component_property='value'),
    Input(component_id='dropdown_dong_population', component_property='value')
)
def update_population_dong_pie_graph(selected_gu, selected_dong):  
  df = pop_per_dong_df.loc[pop_per_dong_df['시군구명'].str.contains(selected_gu) & pop_per_dong_df['행정동명'].str.contains(selected_dong)].loc[:, '0 ~ 9세':].T.reset_index()
  df.columns = ['연령', '비율']
  fig = px.pie(df, names='연령', values='비율', title=f'{selected_gu} {selected_dong}의 월평균 생활인구 연령 비중', color='연령')
  return fig

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://cdn.cctoday.co.kr/news/photo/202311/2187993_626588_3232.jpg', alt='생활', className="banner-image"),
                html.Div([
                    html.H2("생활"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    layout_components = html.Div([
        # 각 구별 아파트 가격 변동 그래프
        html.Div(className='row', children=[
            html.H1(children='서울시 아파트 가격', style={'textAlign':'center', 'fontSize': 30}),
            html.Label('자치구 선택', style={'textAlign': 'center', 'fontSize': 25}),
            dcc.Dropdown(id='dropdown_gu_real_estate_price_all', options=real_estate_price_all_df['자치구'].unique(), value=real_estate_price_all_df['자치구'].unique(), multi=True)
        ]),
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
            dcc.Graph(figure={}, id='fig_real_estate_gu_sale_price')
            ]),
            html.Div(className='four columns', children=[
            dcc.Graph(figure={}, id='fig_real_estate_gu_yearly_rent')
            ]),
            html.Div(className='four columns', children=[
            dcc.Graph(figure={}, id='fig_real_estate_gu_monthly_rent')
            ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='fig_line_real_estate_dong_price')
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='fig_scatter_real_estate_dong_price')
            ])
        ]),
        
        html.Hr(),
        
        # 각 행정동별 소득소비 그래프
        html.Div(className='row', children=[
            html.H1(children='서울시 내국인 소득소비', style={'textAlign':'center', 'fontSize': 30})
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dcc.Graph(figure=px.line(income_df, x="기준년월", y="소득_총금액", color="시군구명", line_group="행정동_코드_명", title='자치구별 월평균 총소득금액 추이'))
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(
                figure=px.scatter(
                    pd.pivot_table(data=income_df, index=['시군구명', '행정동_코드_명', '소득_구간_코드'], values='소득_총금액').sort_values(by='소득_총금액').reset_index(), 
                    x="소득_구간_코드", 
                    y='소득_총금액',
                    marginal_x='histogram', title='소득구간코드와 총소득금액의 관계')
                )
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                html.Label('자치구 선택', style={'textAlign': 'center', 'fontSize': 25}),
                dcc.Dropdown(id='dropdown_gu_income', options=income_df['시군구명'].unique(), value='강남구')
            ]),
            html.Div(className='six columns', children=[
                html.Label('행정동 선택', style={'textAlign': 'center', 'fontSize': 25}),
                dcc.Dropdown(id='dropdown_dong_income')
            ])
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='fig_bar_income')
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(figure={}, id='fig_pie_income')
            ])
        ]),
        
        html.Hr(),
        
        # 서울시 경제활동인구 통계 그래프
        html.Div(className='row', children=[
            html.H1(children='서울시 경제활동인구', style={'textAlign':'center', 'fontSize': 30}),
            dcc.Graph(
                figure=px.line(unemployment_rate_df[['기준년월', '15세이상인구_합계', '경제활동인구_합계', '경제활동인구_취업자_합계', '경제활동인구_실업자_합계', '비경제활동인구_합계']], 
                            x="기준년월", 
                            y=['15세이상인구_합계', '경제활동인구_합계', '경제활동인구_취업자_합계', '경제활동인구_실업자_합계', '비경제활동인구_합계'], 
                            title='경제활동인구 합계 추이'))
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
                dcc.Graph(
                figure=px.line(unemployment_rate_df[['기준년월'] + [col_name for col_name in unemployment_rate_df.columns if '남자' in col_name]], 
                            x="기준년월", 
                            y=[col_name for col_name in unemployment_rate_df.columns if '남자' in col_name], 
                            title='남성 경제활동인구 합계 추이'))
            ]),
            html.Div(className='six columns', children=[
                dcc.Graph(
                figure=px.line(unemployment_rate_df[['기준년월'] + [col_name for col_name in unemployment_rate_df.columns if '여자' in col_name]], 
                            x="기준년월", 
                            y=[col_name for col_name in unemployment_rate_df.columns if '여자' in col_name], 
                            title='여성 경제활동인구 합계 추이'))
            ])
        ]),
        html.Div(className='row', children=[
            dcc.RadioItems(options=unemployment_rate_df.columns[3:], value=unemployment_rate_df.columns[3], id='radio_unemployment_rate'),
            dcc.Graph(figure={}, id='fig_line_unemployment_rate')
        ]),
        
        html.Hr(),
        
        # 서울시 생활인구 그래프
        html.Div(className='row', children=[
            html.H1(children='서울시 생활인구', style={'textAlign':'center', 'fontSize': 30})
        ]),  
        
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
            dcc.Graph(
                figure=px.line(pd.pivot_table(data=population_df, index=['기준일', '시군구명'], values='총생활인구수', aggfunc='mean').reset_index(), 
                            x='기준일', y='총생활인구수', line_group='시군구명', color='시군구명', title='총생활인구수 추이'))
            ]),
            html.Div(className='six columns', children=[
            dcc.Graph(
                figure=px.bar(pd.pivot_table(data=population_df, index=['시도명', '시군구명'], values='총생활인구수', aggfunc='mean').reset_index(), 
                            x='시군구명', y='총생활인구수', color='시군구명', title='자치구별 월평균 총생활인구수'))
            ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
            html.Label('자치구 선택', style={'textAlign': 'center', 'fontSize': 25}),
            dcc.Dropdown(id='dropdown_gu_population', options=population_df['시군구명'].unique(), value='강남구'),
            dcc.Graph(figure={}, id='fig_bar_dong_per_gu_population')
            ]),
            html.Div(className='six columns', children=[
            html.Label('행정동 선택', style={'textAlign': 'center', 'fontSize': 25}),      
            dcc.Dropdown(id='dropdown_dong_population'),
            dcc.Graph(figure={}, id='fig_pie_dong_population')
            ])    
        ]),
            
        html.Hr(),
        
        # 아파트 가격과 소득소비의 상관관계분석 그래프
        html.Div(className='row', children=[
            html.H1(children='서울시 아파트 가격과 소득소비의 상관관계분석', style={'textAlign':'center', 'fontSize': 30})
        ]),
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
            dcc.Graph(figure=px.scatter(income_realestate_df, x='소득_총금액', y='매매가', title='총소득금액과 아파트 매매가의 상관관계', color='시군구명'))
            ]),
            html.Div(className='four columns', children=[
            dcc.Graph(figure=px.scatter(income_realestate_df, x='소득_총금액', y='전세가', title='총소득금액과 아파트 매매가의 상관관계', color='시군구명'))
            ]),
            html.Div(className='four columns', children=[
            dcc.Graph(figure=px.scatter(income_realestate_df, x='소득_총금액', y='월세가', title='총소득금액과 아파트 매매가의 상관관계', color='시군구명'))
            ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
            dcc.Graph(figure=px.scatter(income_realestate_partial_df, x='소득_총금액', y='아파트_평균_시가', title='총소득금액과 아파트 평균시가의 상관관계', color='시군구명'))
            ]),
            html.Div(className='six columns', children=[
            dcc.Graph(figure=px.scatter(income_realestate_partial_df, x='소득_총금액', y='아파트_평균_면적', title='총소득금액과 아파트 평균면적의 상관관계', color='시군구명'))
            ]),
        ]),  
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
            dcc.Graph(figure=px.imshow(income_realestate_df.drop(columns=income_realestate_df.columns[0:5]).corr().round(2), 
                        title='소득과 아파트 매매/전세/월세가 데이터의 Correlation heatmap',
                        text_auto=True, 
                        color_continuous_scale="Reds"))
            ]),
            html.Div(className='six columns', children=[
            dcc.Graph(figure=px.imshow(income_realestate_partial_df.drop(columns=income_realestate_partial_df.columns[0:7]).corr().round(2), 
                        title='소득과 아파트 평균 면적/시가 데이터의 Correlation heatmap',
                        text_auto=True, 
                        color_continuous_scale="Blues"))
            ]),
        ]),  
        
        html.Hr(),
        
        # 아파트 가격과 경제활동인구의 상관관계분석 그래프
        html.Div(className='row', children=[
            html.H1(children='서울시 아파트 가격과 경제활동인구의 상관관계분석', style={'textAlign':'center', 'fontSize': 30}),
            dcc.Graph(figure=px.imshow(unemployment_rate_realestate_df.drop(columns=unemployment_rate_realestate_df.columns[0:3]).corr().round(2), 
                        title='경제활동인구와 아파트 매매/전세/월세가 데이터의 Correlation heatmap',
                        text_auto=True, 
                        color_continuous_scale="Greens"))
        ]),
        
        html.Hr(),
        
        # 아파트 가격과 생활인구의 상관관계분석 그래프
        html.Div(className='row', children=[
            html.H1(children='서울시 아파트 가격과 생활인구의 상관관계분석', style={'textAlign':'center', 'fontSize': 30}),
        ]),
        html.Div(className='row', children=[
            html.Div(className='four columns', children=[
            dcc.Graph(figure=px.scatter(population_all_realestate_df, x='총생활인구수', y='매매가', title='총생활인구수와 아파트 매매가의 상관관계', color='시군구명'))
            ]),
            html.Div(className='four columns', children=[
            dcc.Graph(figure=px.scatter(population_all_realestate_df, x='총생활인구수', y='전세가', title='총생활인구수와 아파트 매매가의 상관관계', color='시군구명'))
            ]),
            html.Div(className='four columns', children=[
            dcc.Graph(figure=px.scatter(population_all_realestate_df, x='총생활인구수', y='월세가', title='총생활인구수와 아파트 매매가의 상관관계', color='시군구명'))
            ]),
        ]),
        html.Div(className='row', children=[
            html.Div(className='six columns', children=[
            dcc.Graph(figure=px.imshow(population_all_realestate_df.drop(columns=population_all_realestate_df.columns[0:5]).corr().round(2), 
                    title='총생활인구와 아파트 매매/전세/월세가 데이터의 Correlation heatmap',
                    text_auto=True, 
                    color_continuous_scale="Magenta"))
            ]),
            html.Div(className='six columns', children=[
            dcc.Graph(figure=px.imshow(population_age_realestate_df.drop(columns=population_age_realestate_df.columns[0:5]).corr().round(2), 
                    title='연령별 생활인구와 아파트 매매/전세/월세가 데이터의 Correlation heatmap',
                    text_auto=True, 
                    color_continuous_scale="Reds"))
            ])
        ]),
        
        html.Hr(),
        
    ])

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout
