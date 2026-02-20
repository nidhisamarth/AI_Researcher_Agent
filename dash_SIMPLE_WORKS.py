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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
    html.H1("🔬 SURVEY INTELLIGENCE PLATFORM", 
            style={"textAlign": "center", "color": "white", "padding": "2rem",
                   "background": "linear-gradient(135deg, #667eea, #764ba2)", 
                   "borderRadius": "20px", "marginBottom": "2rem"}),
    
    dcc.Upload(
        id="up",
        children=html.Div(["📥 DROP FILE HERE"], style={"fontSize": "1.5rem"}),
        style={"border": "3px dashed #667eea", "borderRadius": "20px", "padding": "3rem", 
               "textAlign": "center", "cursor": "pointer", "marginBottom": "2rem"}
    ),
    
    html.Div(id="out")
    
], style={"padding": "2rem", "background": "#1a1a2e", "minHeight": "100vh"})

@app.callback(
    Output("out", "children"),
    Input("up", "contents"),
    State("up", "filename")
)
def process(content, filename):
    if not content:
        return html.Div("Upload a file to begin", style={"color": "white", "textAlign": "center", "padding": "2rem"})
    
    try:
        _, cs = content.split(",")
        decoded = base64.b64decode(cs)
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8"))) if filename.endswith(".csv") else pd.read_excel(io.BytesIO(decoded))
        
        out = [
            html.H2(f"✅ {filename}", style={"color": "#10b981", "marginBottom": "2rem"}),
            html.H3(f"📊 {len(df):,} responses | {len(df.columns)} questions", style={"color": "white"}),
            
            html.H3("🔍 Question Types:", style={"color": "white", "marginTop": "3rem", "marginBottom": "1rem"}),
        ]
        
        for col in df.columns:
            qtype = detect_question_type(df[col], col)
            out.append(html.Div(f"✅ {col}: {qtype.upper()}", style={"color": "white", "padding": "0.5rem", "background": "rgba(255,255,255,0.05)", "borderRadius": "10px", "margin": "0.5rem 0"}))
        
        out.append(html.H3("📏 Scale Orientation:", style={"color": "white", "marginTop": "3rem", "marginBottom": "1rem"}))
        
        for col in df.select_dtypes(include=[np.number]).columns:
            clean = df[col].dropna()
            if len(clean) > 0:
                orientation = detect_scale_orientation(clean, col)
                out.append(html.Div(f"✅ {col}: {orientation}", style={"color": "white", "padding": "0.5rem", "background": "rgba(255,255,255,0.05)", "borderRadius": "10px", "margin": "0.5rem 0"}))
        
        # Industry
        text_cols = df.select_dtypes(include=['object']).columns
        industry = "general"
        for col in text_cols:
            if 'id' not in col.lower() and 'url' not in col.lower():
                text = ' '.join(df[col].dropna().astype(str).tolist())
                industry = detect_industry_simple(text)
                if industry != "general":
                    break
        
        out.append(html.H3(f"🏭 Detected Industry: {industry.upper()}", 
                          style={"color": "#10b981", "marginTop": "3rem", "padding": "1rem", 
                                 "background": "rgba(102, 126, 234, 0.2)", "borderRadius": "15px", "textAlign": "center"}))
        
        return html.Div(out, style={"padding": "2rem"})
        
    except Exception as e:
        return html.Div(f"❌ {str(e)}", style={"color": "#ef4444", "padding": "2rem"})

if __name__ == "__main__":
    print("🚀 http://127.0.0.1:8050")
    app.run(debug=True, port=8050)
