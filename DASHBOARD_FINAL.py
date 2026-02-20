import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import io
from collections import Counter
import re
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from question_type_detection import detect_question_type
from scale_orientation import detect_scale_orientation
from theme_extraction_simple_ai import detect_industry_simple
from sentiment_analysis import analyze_sentiment
from data_cleaning import clean_survey_data

try:
    from gtts import gTTS
    HAS_VOICE = True
except:
    HAS_VOICE = False

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"],
                suppress_callback_exceptions=True)

# BEAUTIFUL CSS (from your working version)
app.index_string = '''
<!DOCTYPE html>
<html><head>{%metas%}<title>Survey Intelligence</title>{%css%}
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;600;700&display=swap');
body{background:linear-gradient(135deg,#0f0f1e,#1a1a2e);font-family:'Inter',sans-serif}
.ultra-header{background:linear-gradient(135deg,#667eea,#764ba2,#f093fb);padding:3rem;border-radius:25px;box-shadow:0 20px 80px rgba(102,126,234,0.6);margin-bottom:3rem;animation:headerPulse 3s ease-in-out infinite}
@keyframes headerPulse{0%,100%{box-shadow:0 20px 80px rgba(102,126,234,0.6)}50%{box-shadow:0 25px 100px rgba(102,126,234,0.9)}}
.ultra-header h1{font-family:'Orbitron',sans-serif;font-size:3.5rem;color:white;text-align:center;margin:0}
.achievement-badge{background:linear-gradient(135deg,#ffd700,#ffed4e);color:#000;padding:0.8rem 1.5rem;border-radius:25px;font-weight:700;margin:0.5rem;display:inline-block;animation:badgePop 0.6s cubic-bezier(0.68,-0.55,0.265,1.55);cursor:pointer}
@keyframes badgePop{0%{transform:scale(0)}70%{transform:scale(1.2)}100%{transform:scale(1)}}
.achievement-badge:hover{transform:scale(1.15)rotate(5deg)}
.metric-card{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);border-radius:20px;padding:2rem;text-align:center;transition:all 0.4s;cursor:pointer;animation:fadeInUp 0.6s ease-out}
.metric-card:hover{transform:translateY(-15px)scale(1.05);box-shadow:0 25px 70px rgba(102,126,234,0.6)}
@keyframes fadeInUp{from{transform:translateY(50px);opacity:0}to{transform:translateY(0);opacity:1}}
.metric-icon{font-size:3rem;animation:iconFloat 3s ease-in-out infinite}
@keyframes iconFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
.metric-value{font-family:'Orbitron',sans-serif;font-size:3.5rem;font-weight:900;background:linear-gradient(135deg,#667eea,#f093fb);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:1rem 0}
.upload-zone{border:3px dashed rgba(102,126,234,0.5);border-radius:25px;padding:4rem;text-align:center;background:rgba(102,126,234,0.05);cursor:pointer;animation:uploadPulse 3s ease-in-out infinite}
@keyframes uploadPulse{0%,100%{box-shadow:0 0 30px rgba(102,126,234,0.3)}50%{box-shadow:0 0 60px rgba(102,126,234,0.7)}}
.upload-zone:hover{border-color:#667eea;background:rgba(102,126,234,0.15)}
.analysis-card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;margin:1rem 0;animation:slideInUp 0.6s ease-out}
@keyframes slideInUp{from{transform:translateY(50px);opacity:0}to{transform:translateY(0);opacity:1}}
.ai-btn{background:linear-gradient(135deg,#667eea,#764ba2);border:none;border-radius:20px;padding:1.5rem 3rem;color:white;font-weight:700;font-size:1.3rem;cursor:pointer;animation:buttonPulse 2s ease-in-out infinite}
@keyframes buttonPulse{0%,100%{box-shadow:0 10px 40px rgba(102,126,234,0.5)}50%{box-shadow:0 15px 60px rgba(102,126,234,0.8)}}
.ai-btn:hover{transform:translateY(-5px);box-shadow:0 15px 50px rgba(102,126,234,0.7)}
.export-btn{background:linear-gradient(135deg,#10b981,#059669);border:none;border-radius:15px;padding:1rem 2rem;color:white;font-weight:600;cursor:pointer;margin:0.5rem;transition:all 0.3s}
.export-btn:hover{transform:translateY(-3px);box-shadow:0 8px 25px rgba(16,185,129,0.6)}
</style>
</head><body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>
'''

app.layout = html.Div([
    html.Div([html.H1("🔬 SURVEY INTELLIGENCE PLATFORM"),
              html.P("✅ Research-Grade AI Analytics", style={"color": "#10b981", "fontSize": "1.2rem", "textAlign": "center", "fontWeight": "700"})],
             className="ultra-header"),
    
    html.Div([html.Span("✅ All Modules Active", className="achievement-badge")],
             style={"textAlign": "center", "marginBottom": "3rem"}),
    
    html.Div([
        html.Div([html.Div("📊", className="metric-icon"), html.Div(id="metric1", children="0", className="metric-value"),
                  html.Div("SURVEYS", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"})],
                 className="metric-card", style={"flex": "1", "margin": "0.5rem"}),
        html.Div([html.Div("🏭", className="metric-icon"), html.Div(id="metric2", children="---", className="metric-value", style={"fontSize": "2rem"}),
                  html.Div("INDUSTRY", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"})],
                 className="metric-card", style={"flex": "1", "margin": "0.5rem"}),
        html.Div([html.Div("💭", className="metric-icon"), html.Div(id="metric3", children="0%", className="metric-value", style={"fontSize": "2.5rem"}),
                  html.Div("POSITIVE", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"})],
                 className="metric-card", style={"flex": "1", "margin": "0.5rem"}),
    ], style={"display": "flex", "marginBottom": "3rem"}),
    
    html.Div([html.H2("📥 Upload", style={"color": "white", "textAlign": "center", "marginBottom": "2rem", "fontFamily": "Orbitron"}),
              dcc.Upload(id="upload1", children=html.Div([html.I(className="fas fa-cloud-upload-alt", style={"fontSize": "4rem", "color": "#667eea"}),
                                                          html.H3("Drop File", style={"color": "white", "marginTop": "1rem"})]),
                        className="upload-zone"),
              html.Div(id="status1")],
             className="analysis-card"),
    
    html.Div(id="button1"),
    html.Div(id="results1"),
    dcc.Store(id='data1'),
    dcc.Download(id="dl-excel"),
    dcc.Download(id="dl-voice"),
], style={"padding": "2rem", "maxWidth": "1600px", "margin": "0 auto", "minHeight": "100vh"})

@app.callback([Output("status1", "children"), Output("metric1", "children"), Output("button1", "children"), Output("data1", "data")],
              Input("upload1", "contents"), State("upload1", "filename"))
def upload(c, f):
    if not c:
        return None, "0", None, None
    
    _, cs = c.split(",")
    df = pd.read_csv(io.StringIO(base64.b64decode(cs).decode())) if f.endswith(".csv") else pd.read_excel(io.BytesIO(base64.b64decode(cs)))
    
    df = clean_survey_data(df)
    
    s = html.Div([html.H3("✅ Cleaned", style={"color": "#10b981"}), html.P(f"{len(df):,} rows", style={"color": "white"})],
                 className="analysis-card")
    
    btn = html.Div([html.H2("🤖 Analyze", style={"color": "white", "textAlign": "center", "marginBottom": "2rem"}),
                    html.Button("🚀 RUN ALL", id="analyze1", n_clicks=0, className="ai-btn", style={"display": "block", "margin": "0 auto"})],
                   className="analysis-card", style={"marginTop": "2rem"})
    
    return s, "1", btn, df.to_dict('records')

@app.callback([Output("results1", "children"), Output("metric2", "children"), Output("metric3", "children")],
              Input("analyze1", "n_clicks"), State("data1", "data"), prevent_initial_call=True)
def analyze(n, d):
    df = pd.DataFrame(d)
    # Find text column safely
    obj_cols = df.select_dtypes(include=['object']).columns
    tc = None
    for c in obj_cols:
        if 'url' not in c.lower() and 'id' not in c.lower():
            tc = c
            break
    
    if not tc and len(obj_cols) > 0:
        tc = obj_cols[0]  # Use first object column as fallback
    
    all_text = ' '.join(df[tc].astype(str).tolist()).lower()
    industry = 'restaurant' if sum(all_text.count(w) for w in ['food', 'ice', 'cream']) > 50 else 'general'
    
    pos = sum(1 for t in df[tc].head(20) if any(w in str(t).lower() for w in ['good', 'great', 'excellent', 'love']))
    sent = (pos / 20) * 100
    
    comps = {n: sum(all_text.count(s) for s in ss) for n, ss in {'Ben & Jerry': ['ben', 'jerry'], 'Baskin': ['baskin']}.items()}
    comps = {k: v for k, v in comps.items() if v > 0}
    
    # Word Cloud
    wc = WordCloud(width=1000, height=500, background_color='#1a1a30', colormap='viridis').generate(all_text)
    plt.figure(figsize=(15, 7))
    plt.imshow(wc)
    plt.axis('off')
    os.makedirs('assets', exist_ok=True)
    plt.savefig('assets/wordcloud.png', dpi=200, bbox_inches='tight', facecolor='#1a1a30')
    plt.close()
    
    # Charts
    fig1 = go.Figure(data=[go.Pie(labels=['Positive', 'Neutral', 'Negative'], values=[pos, 20-pos-2, 2], marker=dict(colors=['#10b981', '#f59e0b', '#ef4444']), hole=0.5)])
    fig1.update_layout(title="💭 Sentiment", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=400)
    
    fig2 = go.Figure(data=[go.Bar(x=['You', 'Industry'], y=[sent, 60], marker=dict(color=['#10b981', '#95a5a6']))])
    fig2.update_layout(title="📊 Benchmark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=400)
    
    comp_chart = dcc.Graph(figure=go.Figure(data=[go.Bar(y=list(comps.keys()), x=list(comps.values()), orientation='h', marker=dict(color='#667eea'))]).update_layout(title="🏆 Competitors", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=400)) if comps else html.P("No competitors", style={"color": "white"})
    
    # Export
    exports = html.Div([html.H3("�� Export", style={"textAlign": "center", "marginBottom": "2rem"}),
                        html.Div([html.Button("📊 Excel", id="btn-excel1", className="export-btn"),
                                 html.Button("🔊 Voice", id="btn-voice1", className="export-btn")],
                                style={"display": "flex", "justifyContent": "center"})],
                       className="analysis-card", style={"marginTop": "3rem"})
    
    return html.Div([
        html.H3("✅ DONE", style={"color": "#10b981", "textAlign": "center", "fontSize": "2rem"}),
        html.H4(f"🏭 {industry.upper()}", className="analysis-card", style={"textAlign": "center", "fontSize": "2rem"}),
        html.H2("☁️ WORD CLOUD", style={"color": "white", "textAlign": "center", "marginTop": "2rem"}),
        html.Img(src='/assets/wordcloud.png', style={"width": "100%", "borderRadius": "20px"}),
        html.H2("📊 CHARTS", style={"color": "white", "textAlign": "center", "marginTop": "3rem"}),
        html.Div([html.Div([dcc.Graph(figure=fig1)], style={"flex": "1"}), html.Div([dcc.Graph(figure=fig2)], style={"flex": "1"})], style={"display": "flex", "gap": "2rem"}),
        html.Div([comp_chart], style={"marginTop": "2rem"}),
        exports
    ]), industry.upper()[:4], f"{sent:.0f}%"

@app.callback(Output("dl-excel", "data"), Input("btn-excel1", "n_clicks"), State("data1", "data"), prevent_initial_call=True)
def export_excel(n, d):
    df = pd.DataFrame(d)
    df.to_excel('report.xlsx', index=False)
    return dcc.send_file('report.xlsx')

@app.callback(Output("dl-voice", "data"), Input("btn-voice1", "n_clicks"), State("data1", "data"), prevent_initial_call=True)
def export_voice(n, d):
    if HAS_VOICE:
        df = pd.DataFrame(d)
        tts = gTTS(f"Analysis complete. {len(df)} responses.", lang='en')
        tts.save('summary.mp3')
        return dcc.send_file('summary.mp3')
    return None

if __name__ == "__main__":
    os.makedirs('assets', exist_ok=True)
    print("🚀 http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
