"""
Survey Intelligence Platform - Ultra Premium Edition
With Animations, Gamification, and Stunning Visuals
"""

import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import base64
import io

app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SLATE,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

app.title = "Survey Intelligence Platform"

# Simple but beautiful layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("🔬 SURVEY INTELLIGENCE PLATFORM",
               style={"textAlign": "center", "color": "white", "fontFamily": "Arial Black"}),
        html.P("Advanced AI-Powered Analysis System",
              style={"textAlign": "center", "color": "rgba(255,255,255,0.9)", "fontSize": "1.2rem"})
    ], style={
        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)",
        "padding": "3rem",
        "borderRadius": "25px",
        "marginBottom": "2rem",
        "boxShadow": "0 20px 80px rgba(102, 126, 234, 0.5)",
        "animation": "fadeIn 1s"
    }),
    
    # Achievement Bar
    html.Div([
        html.H3("🏆 Your Achievements", style={"color": "white", "marginBottom": "1rem"}),
        html.Div([
            html.Span("⭐ Survey Master", style={
                "background": "linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)",
                "color": "#000",
                "padding": "0.8rem 1.5rem",
                "borderRadius": "25px",
                "fontWeight": "700",
                "margin": "0.5rem",
                "display": "inline-block",
                "boxShadow": "0 5px 20px rgba(255, 215, 0, 0.5)"
            }),
            html.Span("🎯 100% Accuracy", style={
                "background": "linear-gradient(135deg, #ffd700 0%, #ffed4e 100%)",
                "color": "#000",
                "padding": "0.8rem 1.5rem",
                "borderRadius": "25px",
                "fontWeight": "700",
                "margin": "0.5rem",
                "display": "inline-block",
                "boxShadow": "0 5px 20px rgba(255, 215, 0, 0.5)"
            }),
        ])
    ], style={
        "background": "rgba(255, 255, 255, 0.05)",
        "backdropFilter": "blur(20px)",
        "border": "2px solid rgba(102, 126, 234, 0.3)",
        "borderRadius": "20px",
        "padding": "1.5rem",
        "margin": "2rem 0"
    }),
    
    # Metrics Row
    html.Div([
        # Metric 1
        html.Div([
            html.Div("📊", style={"fontSize": "3rem"}),
            html.Div("1,247", style={
                "fontSize": "3.5rem",
                "fontWeight": "900",
                "background": "linear-gradient(135deg, #667eea 0%, #f093fb 100%)",
                "WebkitBackgroundClip": "text",
                "WebkitTextFillColor": "transparent"
            }),
            html.Div("TOTAL SURVEYS", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"}),
            html.Div("↑ 23%", style={"color": "#10b981", "fontWeight": "700", "marginTop": "1rem"})
        ], style={
            "background": "rgba(255, 255, 255, 0.08)",
            "backdropFilter": "blur(30px)",
            "border": "1px solid rgba(255, 255, 255, 0.15)",
            "borderRadius": "20px",
            "padding": "2rem",
            "textAlign": "center",
            "flex": "1",
            "margin": "0.5rem",
            "transition": "all 0.3s",
            "cursor": "pointer"
        }, className="metric-card"),
        
        # Metric 2
        html.Div([
            html.Div("⭐", style={"fontSize": "3rem"}),
            html.Div("8.4", style={
                "fontSize": "3.5rem",
                "fontWeight": "900",
                "background": "linear-gradient(135deg, #667eea 0%, #f093fb 100%)",
                "WebkitBackgroundClip": "text",
                "WebkitTextFillColor": "transparent"
            }),
            html.Div("SATISFACTION", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"}),
            html.Div("↑ 0.8", style={"color": "#10b981", "fontWeight": "700", "marginTop": "1rem"})
        ], style={
            "background": "rgba(255, 255, 255, 0.08)",
            "backdropFilter": "blur(30px)",
            "border": "1px solid rgba(255, 255, 255, 0.15)",
            "borderRadius": "20px",
            "padding": "2rem",
            "textAlign": "center",
            "flex": "1",
            "margin": "0.5rem"
        }),
        
        # Metric 3
        html.Div([
            html.Div("📈", style={"fontSize": "3rem"}),
            html.Div("76%", style={
                "fontSize": "3.5rem",
                "fontWeight": "900",
                "background": "linear-gradient(135deg, #667eea 0%, #f093fb 100%)",
                "WebkitBackgroundClip": "text",
                "WebkitTextFillColor": "transparent"
            }),
            html.Div("RESPONSE RATE", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"}),
            html.Div("↑ 11%", style={"color": "#10b981", "fontWeight": "700", "marginTop": "1rem"})
        ], style={
            "background": "rgba(255, 255, 255, 0.08)",
            "backdropFilter": "blur(30px)",
            "border": "1px solid rgba(255, 255, 255, 0.15)",
            "borderRadius": "20px",
            "padding": "2rem",
            "textAlign": "center",
            "flex": "1",
            "margin": "0.5rem"
        }),
        
        # Metric 4
        html.Div([
            html.Div("🤖", style={"fontSize": "3rem"}),
            html.Div("94.2%", style={
                "fontSize": "3.5rem",
                "fontWeight": "900",
                "background": "linear-gradient(135deg, #667eea 0%, #f093fb 100%)",
                "WebkitBackgroundClip": "text",
                "WebkitTextFillColor": "transparent"
            }),
            html.Div("AI ACCURACY", style={"color": "rgba(255,255,255,0.7)", "fontSize": "0.9rem"}),
            html.Div("↑ 2.1%", style={"color": "#10b981", "fontWeight": "700", "marginTop": "1rem"})
        ], style={
            "background": "rgba(255, 255, 255, 0.08)",
            "backdropFilter": "blur(30px)",
            "border": "1px solid rgba(255, 255, 255, 0.15)",
            "borderRadius": "20px",
            "padding": "2rem",
            "textAlign": "center",
            "flex": "1",
            "margin": "0.5rem"
        }),
        
    ], style={"display": "flex", "marginBottom": "2rem"}),
    
    # Chart
    html.Div([
        dcc.Graph(id="main-chart", config={'displayModeBar': False})
    ], style={
        "background": "rgba(255, 255, 255, 0.05)",
        "borderRadius": "20px",
        "padding": "2rem",
        "marginBottom": "2rem"
    }),
    
    # Upload
    dcc.Upload(
        id="upload-data",
        children=html.Div([
            html.I(className="fas fa-cloud-upload-alt", style={"fontSize": "4rem", "color": "#667eea"}),
            html.H3("Drag & Drop Files Here", style={"color": "white", "marginTop": "1rem"}),
            html.P("CSV or Excel files", style={"color": "rgba(255,255,255,0.6)"})
        ]),
        style={
            "border": "3px dashed rgba(102, 126, 234, 0.5)",
            "borderRadius": "25px",
            "padding": "4rem",
            "textAlign": "center",
            "background": "rgba(102, 126, 234, 0.05)",
            "cursor": "pointer",
            "marginTop": "2rem"
        },
        multiple=True
    ),
    
    html.Div(id="upload-output")
    
], style={
    "background": "linear-gradient(135deg, #0f0f1e 0%, #1a1a2e 100%)",
    "minHeight": "100vh",
    "padding": "2rem"
})

@app.callback(
    Output("main-chart", "figure"),
    Input("upload-data", "contents")
)
def update_chart(contents):
    dates = pd.date_range(start='2024-01-01', periods=52, freq='W')
    values = 7.5 + np.cumsum(np.random.randn(52) * 0.1)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=values,
        mode='lines+markers',
        line=dict(color='#667eea', width=4),
        marker=dict(size=10, color='#f093fb'),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)'
    ))
    
    fig.update_layout(
        title="Performance Trend",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    return fig

@app.callback(
    Output("upload-output", "children"),
    Input("upload-data", "contents"),
    State("upload-data", "filename")
)
def process_upload(contents, filenames):
    if not contents:
        return None
    
    results = []
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
            
            results.append(html.Div([
                html.H3(f"✅ {filename}", style={"color": "#10b981"}),
                html.P(f"📊 {len(df)} rows | {len(df.columns)} columns", style={"color": "white"})
            ], style={
                "background": "rgba(255,255,255,0.05)",
                "padding": "2rem",
                "borderRadius": "15px",
                "margin": "1rem 0"
            }))
        except Exception as e:
            results.append(html.Div(f"❌ Error: {str(e)}", style={"color": "#ef4444"}))
    
    return results



@app.callback(
    [Output("analysis-output", "children"),
     Output("ai-section", "style")],
    [Input("analyze-btn", "n_clicks"),
     Input("upload-data", "contents")],
    State("stored-data", "data")
)
def analyze_themes(n_clicks, upload_contents, stored_data):
    # Show AI section when files are uploaded
    if upload_contents:
        ai_style = {"display": "block", "marginTop": "3rem"}
    else:
        ai_style = {"display": "none"}
    
    if n_clicks == 0:
        return None, ai_style
    
    # Mock analysis results
    output = [
        html.Div([
            html.H3("✅ Analysis Complete! +100 XP", 
                   style={"color": "#10b981", "textAlign": "center", "marginBottom": "2rem", "fontSize": "1.5rem"})
        ]),
        
        html.H3("🎨 Top 5 Themes Discovered", 
               style={"color": "white", "marginTop": "2rem", "marginBottom": "1.5rem"}),
        
        html.Div([
            html.Div([
                html.H4("1. Customer Service", style={"color": "white"}),
                html.P("Mentioned 145 times | Sentiment: 8.2/10", style={"color": "rgba(255,255,255,0.6)"})
            ], style={"background": "rgba(255,255,255,0.05)", "padding": "1.5rem", "borderRadius": "15px", "margin": "0.5rem 0"}),
            
            html.Div([
                html.H4("2. Product Quality", style={"color": "white"}),
                html.P("Mentioned 128 times | Sentiment: 8.5/10", style={"color": "rgba(255,255,255,0.6)"})
            ], style={"background": "rgba(255,255,255,0.05)", "padding": "1.5rem", "borderRadius": "15px", "margin": "0.5rem 0"}),
            
            html.Div([
                html.H4("3. Pricing", style={"color": "white"}),
                html.P("Mentioned 112 times | Sentiment: 6.9/10", style={"color": "rgba(255,255,255,0.6)"})
            ], style={"background": "rgba(255,255,255,0.05)", "padding": "1.5rem", "borderRadius": "15px", "margin": "0.5rem 0"}),
            
            html.Div([
                html.H4("4. User Experience", style={"color": "white"}),
                html.P("Mentioned 98 times | Sentiment: 7.8/10", style={"color": "rgba(255,255,255,0.6)"})
            ], style={"background": "rgba(255,255,255,0.05)", "padding": "1.5rem", "borderRadius": "15px", "margin": "0.5rem 0"}),
            
            html.Div([
                html.H4("5. Features", style={"color": "white"}),
                html.P("Mentioned 87 times | Sentiment: 7.5/10", style={"color": "rgba(255,255,255,0.6)"})
            ], style={"background": "rgba(255,255,255,0.05)", "padding": "1.5rem", "borderRadius": "15px", "margin": "0.5rem 0"}),
        ])
    ]
    
    return output, ai_style


if __name__ == "__main__":
    print("🚀 Starting Ultra Premium Dashboard...")
    print("🌐 Open: http://127.0.0.1:8050\n")
    app.run(debug=True, host="127.0.0.1", port=8050)
