"""
Survey Intelligence Platform - Enterprise Dashboard
Built with Dash by Plotly - Professional Analytics Interface
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import base64
import io

# Initialize the Dash app with a premium theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]
)

app.title = "Survey Intelligence Platform"

# Simple layout for now - we'll expand after testing
app.layout = html.Div([
    html.Div([
        html.H1("�� Survey Intelligence Platform", 
                style={"textAlign": "center", "color": "white", "marginBottom": "2rem"}),
        html.P("Advanced AI-Powered Survey Analysis System",
               style={"textAlign": "center", "color": "rgba(255,255,255,0.8)"})
    ], style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "padding": "3rem",
        "borderRadius": "20px",
        "marginBottom": "2rem"
    }),
    
    html.Div([
        html.H2("📊 Quick Stats", style={"color": "white", "marginBottom": "2rem"}),
        html.Div([
            html.Div([
                html.H3("1,247", style={"color": "#667eea", "fontSize": "3rem", "margin": "0"}),
                html.P("Total Surveys", style={"color": "rgba(255,255,255,0.6)"})
            ], style={"textAlign": "center", "padding": "2rem", "background": "rgba(255,255,255,0.05)", "borderRadius": "15px"}),
        ], style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "2rem"})
    ], style={"padding": "2rem"}),
    
    dcc.Upload(
        id="upload-data",
        children=html.Div([
            "📥 Drag and Drop or Click to Upload Survey Data"
        ]),
        style={
            "width": "100%",
            "height": "100px",
            "lineHeight": "100px",
            "borderWidth": "2px",
            "borderStyle": "dashed",
            "borderRadius": "15px",
            "borderColor": "#667eea",
            "textAlign": "center",
            "margin": "2rem 0",
            "background": "rgba(102, 126, 234, 0.1)",
            "color": "white",
            "cursor": "pointer"
        },
        multiple=True
    ),
    
    html.Div(id="output-data-upload")
    
], style={
    "background": "linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%)",
    "minHeight": "100vh",
    "padding": "2rem"
})

@app.callback(
    Output("output-data-upload", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def update_output(contents, filenames):
    if contents is None:
        return html.Div("Upload files to see data preview", 
                       style={"color": "rgba(255,255,255,0.6)", "textAlign": "center", "padding": "2rem"})
    
    children = []
    for content, filename in zip(contents, filenames):
        try:
            content_type, content_string = content.split(",")
            decoded = base64.b64decode(content_string)
            
            if filename.endswith(".csv"):
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            elif filename.endswith((".xlsx", ".xls")):
                df = pd.read_excel(io.BytesIO(decoded))
            else:
                continue
            
            children.append(html.Div([
                html.H3(f"📄 {filename}", style={"color": "white"}),
                html.P(f"Rows: {len(df)} | Columns: {len(df.columns)}", 
                      style={"color": "rgba(255,255,255,0.7)"}),
                html.Div("✅ File loaded successfully!", 
                        style={"color": "#10b981", "marginTop": "1rem"})
            ], style={
                "background": "rgba(255,255,255,0.05)",
                "padding": "2rem",
                "borderRadius": "15px",
                "marginBottom": "1rem"
            }))
            
        except Exception as e:
            children.append(html.Div(f"❌ Error: {str(e)}", 
                                   style={"color": "#ef4444", "padding": "1rem"}))
    
    return children

if __name__ == "__main__":
    print("="*60)
    print("🚀 Survey Intelligence Platform Starting...")
    print("="*60)
    print("\n🌐 Open: http://127.0.0.1:8050")
    print("\n"+"="*60+"\n")
    app.run(debug=True, host="127.0.0.1", port=8050)
