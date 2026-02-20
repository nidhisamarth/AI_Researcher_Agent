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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("🔬 SURVEY INTELLIGENCE", style={"textAlign": "center", "color": "white", "padding": "2rem", "background": "linear-gradient(135deg,#667eea,#764ba2)", "borderRadius": "20px"}),
    
    html.Br(),
    
    dcc.Upload(id="u", children=html.Div(["📥 DROP FILE HERE"], style={"fontSize": "2rem", "padding": "3rem", "border": "3px dashed #667eea", "borderRadius": "20px", "textAlign": "center", "cursor": "pointer"})),
    
    html.Div(id="output", style={"marginTop": "2rem"}),
], style={"padding": "2rem", "maxWidth": "1400px", "margin": "0 auto"})

@app.callback(Output("output", "children"), Input("u", "contents"), State("u", "filename"))
def process(c, f):
    if not c:
        return html.Div("Upload a file to begin", style={"color": "white", "textAlign": "center", "padding": "2rem"})
    
    try:
        _, cs = c.split(",")
        df = pd.read_csv(io.StringIO(base64.b64decode(cs).decode())) if f.endswith(".csv") else pd.read_excel(io.BytesIO(base64.b64decode(cs)))
        
        # Clean
        df = clean_survey_data(df)
        
        # Find text column
        text_col = 'Review Text' if 'Review Text' in df.columns else df.select_dtypes(include=['object']).columns[0]
        
        # Analysis
        types = [html.Li(f"{col}: {detect_question_type(df[col], col).upper()}") for col in df.columns]
        
        all_text = ' '.join(df[text_col].astype(str).tolist()).lower()
        industry = 'restaurant' if 'food' in all_text or 'ice' in all_text else 'general'
        
        pos = sum(1 for t in df[text_col].head(20) if 'good' in str(t).lower() or 'great' in str(t).lower())
        sent = (pos / 20) * 100
        
        # Word Cloud
        wc = WordCloud(width=1000, height=500, background_color='#1a1a30').generate(all_text)
        plt.figure(figsize=(12, 6))
        plt.imshow(wc)
        plt.axis('off')
        os.makedirs('assets', exist_ok=True)
        plt.savefig('assets/wc.png', dpi=150, bbox_inches='tight', facecolor='#1a1a30')
        plt.close()
        
        # Competitors
        comps = {n: all_text.count(s) for n, s in {'Ben & Jerry': 'ben', 'Baskin': 'baskin'}.items()}
        comps = {k: v for k, v in comps.items() if v > 0}
        
        # Chart
        if comps:
            fig = go.Figure(data=[go.Bar(y=list(comps.keys()), x=list(comps.values()), orientation='h', marker=dict(color='#667eea'))])
            fig.update_layout(title="🏆 Competitors", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=400)
            chart = dcc.Graph(figure=fig)
        else:
            chart = html.P("No competitors found", style={"color": "white"})
        
        return html.Div([
            html.H2(f"✅ {f}", style={"color": "#10b981"}),
            html.H3(f"🏭 Industry: {industry.upper()}", style={"color": "white", "padding": "1rem", "background": "rgba(102,126,234,0.3)", "borderRadius": "15px"}),
            html.H4(f"💭 Sentiment: {sent:.0f}% Positive", style={"color": "#10b981"}),
            html.Br(),
            html.H3("🔍 Question Types:", style={"color": "white"}),
            html.Ul(types, style={"color": "white"}),
            html.Br(),
            html.H3("☁️ WORD CLOUD:", style={"color": "white"}),
            html.Img(src='/assets/wc.png', style={"width": "100%", "borderRadius": "20px"}),
            html.Br(),
            chart,
        ], style={"padding": "2rem"})
        
    except Exception as e:
        return html.Div(f"❌ Error: {str(e)}", style={"color": "#ef4444", "padding": "2rem"})

if __name__ == "__main__":
    print("🚀 http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
