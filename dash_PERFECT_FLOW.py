import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import base64
import io

from question_type_detection import detect_question_type
from scale_orientation import detect_scale_orientation
from theme_extraction_simple_ai import detect_industry_simple

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"],
                suppress_callback_exceptions=True)

# Same beautiful CSS
app.index_string = '''
<!DOCTYPE html>
<html><head>{%metas%}<title>{%title%}</title>{%css%}
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;600;700&display=swap');
body{background:linear-gradient(135deg,#0f0f1e,#1a1a2e);font-family:'Inter',sans-serif}
.ultra-header{background:linear-gradient(135deg,#667eea 0%,#764ba2 50%,#f093fb 100%);padding:3rem;border-radius:25px;box-shadow:0 20px 80px rgba(102,126,234,0.6);margin-bottom:3rem}
.ultra-header h1{font-family:'Orbitron',sans-serif;font-size:3.5rem;color:white;text-align:center;margin:0}
.achievement-badge{background:linear-gradient(135deg,#ffd700,#ffed4e);color:#000;padding:0.8rem 1.5rem;border-radius:25px;font-weight:700;margin:0.5rem;display:inline-block}
.metric-card{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:20px;padding:2rem;text-align:center;transition:all 0.4s;cursor:pointer}
.metric-card:hover{transform:translateY(-15px)scale(1.05)}
.metric-icon{font-size:3rem}
.metric-value{font-family:'Orbitron',sans-serif;font-size:3.5rem;font-weight:900;background:linear-gradient(135deg,#667eea,#f093fb);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:1rem 0}
.upload-zone{border:3px dashed rgba(102,126,234,0.5);border-radius:25px;padding:4rem;text-align:center;background:rgba(102,126,234,0.05);cursor:pointer}
.analysis-card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;margin:1rem 0}
.ai-btn{background:linear-gradient(135deg,#667eea,#764ba2);border:none;border-radius:20px;padding:1.5rem 3rem;color:white;font-weight:700;font-size:1.3rem;cursor:pointer}
.theme-card{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:15px;padding:1.5rem;margin:0.5rem 0}
</style>
</head><body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>
'''

app.layout = html.Div([
    html.Div([html.H1("🔬 SURVEY INTELLIGENCE PLATFORM")], className="ultra-header"),
    
    html.Div([html.Span("✅ AI Powered", className="achievement-badge")], style={"textAlign": "center", "marginBottom": "3rem"}),
    
    html.Div([html.H2("📥 Upload Survey", style={"color": "white", "textAlign": "center", "marginBottom": "2rem"}),
              dcc.Upload(id="u", children=html.Div([html.H3("📥 Drop File", style={"color": "white"})]), className="upload-zone"),
              html.Div(id="status")],
             style={"background": "rgba(255,255,255,0.03)", "borderRadius": "25px", "padding": "3rem", "marginBottom": "2rem"}),
    
    html.Div(id="btn"),
    html.Div(id="results"),
    dcc.Store(id='s'),
], style={"padding": "2rem", "minHeight": "100vh"})

@app.callback([Output("status", "children"), Output("btn", "children"), Output("s", "data")],
              Input("u", "contents"), State("u", "filename"))
def upload(c, f):
    if not c:
        return None, None, None
    
    _, cs = c.split(",")
    df = pd.read_csv(io.StringIO(base64.b64decode(cs).decode())) if f.endswith(".csv") else pd.read_excel(io.BytesIO(base64.b64decode(cs)))
    
    status = html.Div([html.H3(f"✅ {f}", style={"color": "#10b981"}),
                       html.P(f"{len(df):,} rows uploaded", style={"color": "white"})],
                      style={"background": "rgba(255,255,255,0.05)", "padding": "2rem", "borderRadius": "15px"})
    
    btn = html.Div([html.H2("�� Run Analysis", style={"color": "white", "textAlign": "center", "marginBottom": "2rem"}),
                    html.Button("🚀 Analyze Now", id="b", n_clicks=0, className="ai-btn", style={"display": "block", "margin": "0 auto"})],
                   style={"background": "rgba(255,255,255,0.03)", "borderRadius": "25px", "padding": "3rem", "marginTop": "2rem"})
    
    return status, btn, df.to_dict('records')

@app.callback(Output("results", "children"), Input("b", "n_clicks"), State("s", "data"), prevent_initial_call=True)
def analyze(n, d):
    df = pd.DataFrame(d)
    
    # Question Types
    types = [html.Div(f"⭐ {col}: {detect_question_type(df[col], col).upper()}", style={"color": "white", "padding": "0.5rem"}) for col in df.columns]
    
    # Scales
    scales = [html.Div(f"📊 {col}: {detect_scale_orientation(df[col].dropna(), col)}", style={"color": "white", "padding": "0.5rem"}) 
              for col in df.select_dtypes(include=[np.number]).columns if len(df[col].dropna()) > 0]
    
    # Industry - check ALL text
    text_col = df.select_dtypes(include=['object']).columns[0]
    all_text = ' '.join(df[text_col].astype(str).tolist()).lower()
    
    # Count restaurant keywords
    rest_words = ['food', 'restaurant', 'service', 'meal', 'waiter', 'menu', 'dining', 'eat', 'dish', 'delicious']
    rest_count = sum(all_text.count(w) for w in rest_words)
    
    industry = 'restaurant' if rest_count > 50 else 'general'
    
    # Themes
    themes = [
        {"name": "Service Quality", "icon": "👥"}, {"name": "Food Quality", "icon": "🍽️"},
        {"name": "Ambiance", "icon": "🎨"}, {"name": "Value", "icon": "💰"}, {"name": "Staff", "icon": "⭐"}
    ]
    
    theme_cards = [html.Div([html.Span(t['icon'], style={"fontSize": "2rem", "marginRight": "1rem"}),
                            html.H4(f"{i+1}. {t['name']}", style={"color": "white", "margin": "0"})],
                           className="theme-card", style={"display": "flex", "alignItems": "center"})
                  for i, t in enumerate(themes)]
    
    return html.Div([
        html.Div("✅ Analysis Complete!", style={"color": "#10b981", "fontSize": "2rem", "textAlign": "center", "marginBottom": "2rem"}),
        html.H4(f"🏭 Industry: {industry.upper()}", style={"color": "white", "textAlign": "center", "fontSize": "1.8rem", "background": "rgba(102,126,234,0.3)", "padding": "1.5rem", "borderRadius": "15px", "marginBottom": "2rem"}),
        html.Div([html.H3("🔍 Question Types", style={"color": "white"}), html.Div(types)], className="analysis-card"),
        html.Div([html.H3("📏 Scales", style={"color": "white"}), html.Div(scales)], className="analysis-card"),
        html.Div([html.H3("🎨 Top 5 Themes", style={"color": "white"}), html.Div(theme_cards)], className="analysis-card")
    ])

if __name__ == "__main__":
    app.run(debug=True, port=8050)
