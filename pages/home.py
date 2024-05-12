import json

import dash_bootstrap_components as dbc
from dash import html, ctx, Input, Output, State, clientside_callback, dcc

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