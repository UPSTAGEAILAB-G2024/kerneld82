import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, ctx, dcc, html

from .home import get_sidebar

def layout():
    banner = dbc.Row([
        dbc.Col([
            html.Div([
                html.Img(src='https://cdn.cctoday.co.kr/news/photo/202311/2187993_626588_3232.jpg', alt='금리 및 물가', className="banner-image"),
                html.Div([
                    html.H2("금리 및 물가"),
                ], className='overlay-text')
            ], className='banner-container')
        ]),
    ])

    layout_components = dbc.Row([
        dbc.Col([
            html.Div(html.P('You can zoom, rotate the virus model in the 3D Viewer to explore the virus.'), className='text-justify'),
            html.Div(html.P('You can zoom, rotate the virus model in the 3D Viewer to explore the virus.'), className='text-justify'),
            html.Div(html.P('You can zoom, rotate the virus model in the 3D Viewer to explore the virus.'), className='text-justify'),
            html.Div(html.P('You can zoom, rotate the virus model in the 3D Viewer to explore the virus.'), className='text-justify'),
        ]),
    ], className='mb-4 mt-2 align-items-end')

    layout = [
        get_sidebar(__name__),
        html.Div([
            dbc.Container(banner, fluid=True),
            dbc.Container(layout_components, fluid='md')
        ], className='content')
    ]

    return layout
