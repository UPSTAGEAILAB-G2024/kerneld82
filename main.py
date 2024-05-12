import dash
from dash import Dash
from flask import Flask
from pages import home, life, supply, mind, interest, currency

index_str = """<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-LCWNJQRXQH"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-LCWNJQRXQH');
        </script>
        <!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "0ded497d3a654a6daab165aabc396559"}'></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

app = Flask(__name__, instance_relative_config=True)
dash_app = Dash(__name__,
        server=app,
        use_pages=True,
        assets_folder='static',
        index_string=index_str,
        external_scripts=[{
            'src': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/js/bootstrap.bundle.min.js',
            'integrity': 'sha384-HwwvtgBNo3bZJJLYd8oVXjrBZt8cqVSpeBNS5n7C8IVInixGAoxmnlMuBnhbgrkm',
            'crossorigin': 'anonymous'
        }],
        external_stylesheets=[{
            'href': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css',
            'integrity': 'sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9',
            'crossorigin': 'anonymous',
            'rel': 'stylesheet'
        },
        {
            'href': 'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
            'rel': 'stylesheet'
        }]
    )
dash.register_page('pages.homepage',
    path='/',
    title='홈',
    name='홈',
    layout=home.layout)

dash.register_page('pages.life',
    path='/life',
    title='생활',
    name='생활',
    layout=life.layout)

dash.register_page('pages.supply',
    path='/supply',
    title='공급',
    name='공급',
    layout=supply.layout)

dash.register_page('pages.mind',
    path='/mind',
    title='심리',
    name='심리',
    layout=mind.layout)

dash.register_page('pages.interest',
    path='/interest',
    title='금리 및 물가',
    name='금리 및 물가',
    layout=interest.layout)

dash.register_page('pages.currency',
    path='/currency',
    title='통화 및 부채',
    name='통화 및 부채',
    layout=currency.layout)

with app.app_context():
    dash_app.layout = dash.page_container

if __name__ == "__main__":
    app.run(debug=True)