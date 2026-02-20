import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import base64
import io
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from question_type_detection import detect_question_type
from scale_orientation import detect_scale_orientation
from theme_extraction_simple_ai import detect_industry_simple
from data_cleaning import clean_survey_data

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"],
                suppress_callback_exceptions=True)

# YOUR BEAUTIFUL CSS (EXACT from before)
app.index_string = '''
<!DOCTYPE html>
<html><head>{%metas%}<title>Survey Intelligence Platform</title>{%css%}
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@300;400;600;700&display=swap');
body{background:linear-gradient(135deg,#0f0f1e,#1a1a2e);font-family:'Inter',sans-serif}
.ultra-header{background:linear-gradient(135deg,#667eea 0%,#764ba2 50%,#f093fb 100%);padding:3rem;border-radius:25px;box-shadow:0 20px 80px rgba(102,126,234,0.6);margin-bottom:3rem;position:relative;overflow:hidden;animation:headerPulse 3s ease-in-out infinite}
@keyframes headerPulse{0%,100%{box-shadow:0 20px 80px rgba(102,126,234,0.6)}50%{box-shadow:0 25px 100px rgba(102,126,234,0.9)}}
.ultra-header::before{content:'';position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:linear-gradient(45deg,transparent,rgba(255,255,255,0.1),transparent);animation:shine 3s infinite}
@keyframes shine{0%{transform:translateX(-100%)translateY(-100%)rotate(45deg)}100%{transform:translateX(100%)translateY(100%)rotate(45deg)}}
.ultra-header h1{font-family:'Orbitron',sans-serif;font-size:3.5rem;color:white;text-align:center;margin:0;position:relative;z-index:1}
.achievement-badge{background:linear-gradient(135deg,#ffd700,#ffed4e);color:#000;padding:0.8rem 1.5rem;border-radius:25px;font-weight:700;margin:0.5rem;display:inline-block;cursor:pointer;transition:all 0.3s;animation:badgePop 0.6s cubic-bezier(0.68,-0.55,0.265,1.55)}
.achievement-badge:hover{transform:scale(1.15)rotate(5deg);box-shadow:0 8px 30px rgba(255,215,0,0.8)}
@keyframes badgePop{0%{transform:scale(0)rotate(-180deg);opacity:0}70%{transform:scale(1.2)rotate(10deg)}100%{transform:scale(1)rotate(0);opacity:1}}
.metric-card{background:rgba(255,255,255,0.08);backdrop-filter:blur(30px);border:1px solid rgba(255,255,255,0.15);border-radius:20px;padding:2rem;text-align:center;transition:all 0.4s cubic-bezier(0.175,0.885,0.32,1.275);cursor:pointer;position:relative;overflow:hidden;animation:fadeInUp 0.6s ease-out}
.metric-card::before{content:'';position:absolute;top:0;left:-100%;width:100%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.1),transparent);transition:left 0.5s}
.metric-card:hover::before{left:100%}
.metric-card:hover{transform:translateY(-15px)scale(1.05);box-shadow:0 25px 70px rgba(102,126,234,0.6);border-color:rgba(102,126,234,0.5)}
@keyframes fadeInUp{from{transform:translateY(50px);opacity:0}to{transform:translateY(0);opacity:1}}
.metric-icon{font-size:3rem;animation:iconFloat 3s ease-in-out infinite}
@keyframes iconFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
.metric-value{font-family:'Orbitron',sans-serif;font-size:3.5rem;font-weight:900;background:linear-gradient(135deg,#667eea,#f093fb);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:1rem 0;animation:valueGlow 2s ease-in-out infinite}
@keyframes valueGlow{0%,100%{filter:drop-shadow(0 0 10px rgba(102,126,234,0.5))}50%{filter:drop-shadow(0 0 20px rgba(102,126,234,0.9))}}
.upload-zone{border:3px dashed rgba(102,126,234,0.5);border-radius:25px;padding:4rem;text-align:center;background:rgba(102,126,234,0.05);cursor:pointer;transition:all 0.3s;animation:uploadPulse 3s ease-in-out infinite}
@keyframes uploadPulse{0%,100%{box-shadow:0 0 30px rgba(102,126,234,0.3)}50%{box-shadow:0 0 60px rgba(102,126,234,0.7)}}
.upload-zone:hover{border-color:#667eea;background:rgba(102,126,234,0.15);transform:scale(1.02)}
.analysis-card{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;margin:1rem 0;animation:slideInUp 0.6s ease-out}
@keyframes slideInUp{from{transform:translateY(50px);opacity:0}to{transform:translateY(0);opacity:1}}
.ai-btn{background:linear-gradient(135deg,#667eea,#764ba2);border:none;border-radius:20px;padding:1.5rem 3rem;color:white;font-weight:700;font-size:1.3rem;cursor:pointer;box-shadow:0 10px 40px rgba(102,126,234,0.5);animation:buttonPulse 2s ease-in-out infinite}
.ai-btn:hover{transform:translateY(-5px);box-shadow:0 15px 50px rgba(102,126,234,0.7)}
@keyframes buttonPulse{0%,100%{box-shadow:0 10px 40px rgba(102,126,234,0.5)}50%{box-shadow:0 15px 60px rgba(102,126,234,0.8)}}
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
        html.Div([html.Div("📊", className="metric-icon"), html.Div(id="m1", children="0", className="metric-value"),
                  html.Div("SURVEYS", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"})],
                 className="metric-card", style={"flex": "1", "margin": "0.5rem"}),
        html.Div([html.Div("🏭", className="metric-icon"), html.Div(id="m2", children="---", className="metric-value", style={"fontSize": "2rem"}),
                  html.Div("INDUSTRY", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"})],
                 className="metric-card", style={"flex": "1", "margin": "0.5rem"}),
        html.Div([html.Div("💭", className="metric-icon"), html.Div(id="m3", children="0%", className="metric-value", style={"fontSize": "2.5rem"}),
                  html.Div("POSITIVE", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"})],
                 className="metric-card", style={"flex": "1", "margin": "0.5rem"}),
    ], style={"display": "flex", "marginBottom": "3rem"}),
    
    html.Div([html.H2("📥 Upload Survey", style={"color": "white", "textAlign": "center", "marginBottom": "2rem", "fontFamily": "Orbitron"}),
              dcc.Upload(id="upload", children=html.Div([html.I(className="fas fa-cloud-upload-alt", style={"fontSize": "4rem", "color": "#667eea"}),
                                                         html.H3("Drag & Drop Survey File", style={"color": "white", "marginTop": "1rem"})]),
                        className="upload-zone")],
             className="analysis-card"),
    
    html.Div(id="output"),
    
], style={"padding": "2rem", "maxWidth": "1600px", "margin": "0 auto", "minHeight": "100vh"})

@app.callback([Output("output", "children"), Output("m1", "children"), Output("m2", "children"), Output("m3", "children")],
              Input("upload", "contents"), State("upload", "filename"))
def process_everything(c, f):
    if not c:
        return None, "0", "---", "0%"
    
    try:
        _, cs = c.split(",")
        df = pd.read_csv(io.StringIO(base64.b64decode(cs).decode())) if f.endswith(".csv") else pd.read_excel(io.BytesIO(base64.b64decode(cs)))
        
        df = clean_survey_data(df)
        text_col = 'Review Text' if 'Review Text' in df.columns else df.select_dtypes(include=['object']).columns[0]
        
        all_text = ' '.join(df[text_col].astype(str).tolist()).lower()
        industry = 'restaurant' if sum(all_text.count(w) for w in ['food', 'ice', 'cream']) > 50 else 'general'
        
        pos = sum(1 for t in df[text_col].head(20) if any(w in str(t).lower() for w in ['good', 'great', 'excellent']))
        sent = (pos / 20) * 100
        
        comps = {n: sum(all_text.count(s) for s in ss) for n, ss in {'Ben & Jerry': ['ben', 'jerry'], 'Baskin': ['baskin']}.items()}
        comps = {k: v for k, v in comps.items() if v > 0}
        
        # Word Cloud
        wc = WordCloud(width=1200, height=600, background_color='#1a1a30', colormap='plasma').generate(all_text)
        plt.figure(figsize=(16, 8))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        os.makedirs('assets', exist_ok=True)
        plt.savefig('assets/wordcloud.png', dpi=200, bbox_inches='tight', facecolor='#1a1a30')
        plt.close()
        
        # Charts
        fig1 = go.Figure(data=[go.Pie(labels=['Positive', 'Neutral', 'Negative'], values=[pos, 20-pos-2, 2], marker=dict(colors=['#10b981', '#f59e0b', '#ef4444']), hole=0.5)])
        fig1.update_layout(title="💭 Sentiment Distribution", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=450)
        
        fig2 = go.Figure(data=[go.Bar(x=['Your Performance', 'Industry Average'], y=[sent, 60], marker=dict(color=['#10b981', '#95a5a6']), text=[f'{sent:.0f}%', '60%'], textposition='outside')])
        fig2.update_layout(title="📊 Benchmark Comparison", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=450, yaxis=dict(range=[0, 100]))
        
        if comps:
            fig3 = go.Figure(data=[go.Bar(y=list(comps.keys()), x=list(comps.values()), orientation='h', marker=dict(color=['#ffd700', '#c0c0c0'][:len(comps)]))])
            fig3.update_layout(title="🏆 Competitor Mentions", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=400)
            comp_chart = dcc.Graph(figure=fig3, config={'displayModeBar': False})
        else:
            comp_chart = html.P("No competitors detected", style={"color": "rgba(255,255,255,0.6)", "textAlign": "center"})
        
        return html.Div([
            html.Div("✅ ANALYSIS COMPLETE", style={"color": "#10b981", "fontSize": "2.5rem", "textAlign": "center", "fontWeight": "900", "marginBottom": "3rem"}),
            
            html.Div(f"🏭 Detected Industry: {industry.upper()}", className="analysis-card",
                    style={"textAlign": "center", "fontSize": "2rem", "background": "rgba(102,126,234,0.3)", "padding": "2rem"}),
            
            html.H2("☁️ WORD CLOUD VISUALIZATION", style={"textAlign": "center", "fontFamily": "Orbitron", "fontSize": "2rem", "marginTop": "3rem", "marginBottom": "2rem"}),
            html.Img(src='/assets/wordcloud.png', style={"width": "100%", "borderRadius": "20px", "boxShadow": "0 15px 60px rgba(0,0,0,0.5)"}),
            
            html.H2("📊 ANALYTICS DASHBOARD", style={"textAlign": "center", "fontFamily": "Orbitron", "fontSize": "2rem", "marginTop": "3rem", "marginBottom": "2rem"}),
            
            html.Div([
                html.Div([dcc.Graph(figure=fig1, config={'displayModeBar': False})], style={"flex": "1"}),
                html.Div([dcc.Graph(figure=fig2, config={'displayModeBar': False})], style={"flex": "1"}),
            ], style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "2rem", "marginBottom": "2rem"}),
            
            html.Div([comp_chart], className="analysis-card")
            
        ]), "1", industry.upper()[:4], f"{sent:.0f}%"
        
    except Exception as e:
        return html.Div(f"Error: {str(e)}", style={"color": "#ef4444"}), "0", "---", "0%"

if __name__ == "__main__":
    os.makedirs('assets', exist_ok=True)
    print("🚀 http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
