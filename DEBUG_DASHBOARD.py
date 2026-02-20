import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io

from question_type_detection import detect_question_type
from data_cleaning import clean_survey_data

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE], suppress_callback_exceptions=True)

app.layout = html.Div([
    html.H1("🔬 SURVEY INTELLIGENCE", style={"textAlign": "center", "color": "white", "padding": "2rem", "background": "linear-gradient(135deg,#667eea,#764ba2,#f093fb)", "borderRadius": "20px", "marginBottom": "2rem"}),
    
    dcc.Upload(id="upload", children=html.Div(["📥 CLICK OR DROP FILE"], style={"fontSize": "2rem", "padding": "3rem", "border": "3px dashed #667eea", "borderRadius": "20px", "textAlign": "center", "cursor": "pointer", "color": "white"})),
    
    html.Div(id="debug-info", style={"marginTop": "2rem", "padding": "2rem", "background": "rgba(255,255,255,0.05)", "borderRadius": "15px"}),
    
], style={"padding": "2rem", "background": "#1a1a2e", "minHeight": "100vh"})

@app.callback(
    Output("debug-info", "children"),
    Input("upload", "contents"),
    State("upload", "filename")
)
def test_upload(contents, filename):
    if not contents:
        return html.P("No file uploaded yet...", style={"color": "white"})
    
    try:
        # Decode
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        
        # Read
        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            df = pd.read_excel(io.BytesIO(decoded))
        
        # Clean
        df_clean = clean_survey_data(df)
        
        return html.Div([
            html.H3("✅ SUCCESS!", style={"color": "#10b981"}),
            html.P(f"File: {filename}", style={"color": "white"}),
            html.P(f"Original: {len(df)} rows", style={"color": "white"}),
            html.P(f"After cleaning: {len(df_clean)} rows", style={"color": "white"}),
            html.P(f"Columns: {', '.join(df_clean.columns)}", style={"color": "white"})
        ])
        
    except Exception as e:
        return html.Div([
            html.H3("❌ ERROR", style={"color": "#ef4444"}),
            html.P(f"Error type: {type(e).__name__}", style={"color": "white"}),
            html.P(f"Error message: {str(e)}", style={"color": "white"})
        ])

if __name__ == "__main__":
    print("🚀 DEBUG MODE: http://127.0.0.1:8050")
    print("Upload your file and see what happens!")
    app.run(debug=True, port=8050)
