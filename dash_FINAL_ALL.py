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
from sentiment_analysis import analyze_sentiment

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"],
                suppress_callback_exceptions=True)

app.index_string = '''
<!DOCTYPE html>
<html><head>{%metas%}<title>{%title%}</title>{%css%}
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Inter:wght@400;600;700&display=swap');
body{background:linear-gradient(135deg,#0f0f1e,#1a1a2e);font-family:'Inter',sans-serif}
.ultra-header{background:linear-gradient(135deg,#667eea,#764ba2,#f093fb);padding:3rem;border-radius:25px;margin-bottom:3rem}
.ultra-header h1{font-family:'Orbitron',sans-serif;font-size:3.5rem;color:white;text-align:center;margin:0}
.achievement-badge{background:linear-gradient(135deg,#ffd700,#ffed4e);color:#000;padding:.8rem 1.5rem;border-radius:25px;font-weight:700;margin:.5rem;display:inline-block;cursor:pointer}
.metric-card{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:20px;padding:2rem;text-align:center;transition:all .4s;cursor:pointer}
.metric-card:hover{transform:translateY(-15px) scale(1.05)}
.metric-icon{font-size:3rem}
.metric-value{font-family:'Orbitron',sans-serif;font-size:3.5rem;font-weight:900;background:linear-gradient(135deg,#667eea,#f093fb);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:1rem 0}
.upload-zone{border:3px dashed rgba(102,126,234,.5);border-radius:25px;padding:4rem;text-align:center;background:rgba(102,126,234,.05);cursor:pointer}
.analysis-card{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:2rem;margin:1rem 0}
.ai-btn{background:linear-gradient(135deg,#667eea,#764ba2);border:none;border-radius:20px;padding:1.5rem 3rem;color:white;font-weight:700;font-size:1.3rem;cursor:pointer}
</style>
</head><body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>
'''

app.layout = html.Div([
    html.Div([html.H1("🔬 SURVEY INTELLIGENCE PLATFORM"),
              html.P("✅ All Modules Active",style={"color":"#10b981","fontSize":"1.2rem","textAlign":"center","fontWeight":"700"})],
             className="ultra-header"),
    
    html.Div([html.Span("✅ Question Type",className="achievement-badge"),
              html.Span("✅ Scale Orientation",className="achievement-badge"),
              html.Span("✅ AI Themes",className="achievement-badge"),
              html.Span("✅ Sentiment",className="achievement-badge"),
              html.Span("✅ Benchmark",className="achievement-badge"),
              html.Span("✅ Competitor",className="achievement-badge")],
             style={"textAlign":"center","marginBottom":"3rem"}),
    
    html.Div([
        html.Div([html.Div("��",className="metric-icon"),html.Div(id="m1",children="0",className="metric-value"),
                  html.Div("SURVEYS",style={"color":"rgba(255,255,255,0.7)"})],
                 className="metric-card",style={"flex":"1","margin":"0.5rem"}),
        html.Div([html.Div("🏭",className="metric-icon"),html.Div(id="m2",children="---",className="metric-value",style={"fontSize":"2rem"}),
                  html.Div("INDUSTRY",style={"color":"rgba(255,255,255,0.7)"})],
                 className="metric-card",style={"flex":"1","margin":"0.5rem"}),
        html.Div([html.Div("💭",className="metric-icon"),html.Div(id="m3",children="0%",className="metric-value",style={"fontSize":"2.5rem"}),
                  html.Div("POSITIVE",style={"color":"rgba(255,255,255,0.7)"})],
                 className="metric-card",style={"flex":"1","margin":"0.5rem"}),
    ],style={"display":"flex","marginBottom":"3rem"}),
    
    html.Div([html.H2("📥 Upload",style={"color":"white","textAlign":"center","marginBottom":"2rem"}),
              dcc.Upload(id="u1",children=html.Div([html.I(className="fas fa-cloud-upload-alt",style={"fontSize":"4rem","color":"#667eea"}),
                                                     html.H3("Drop File",style={"color":"white","marginTop":"1rem"})]),
                        className="upload-zone"),
              html.Div(id="s1")],
             style={"background":"rgba(255,255,255,0.03)","borderRadius":"25px","padding":"3rem","marginBottom":"3rem"}),
    
    html.Div(id="auto1"),
    html.Div(id="btn1"),
    html.Div(id="results1"),
    dcc.Store(id='store1'),
],style={"padding":"2rem","minHeight":"100vh"})

@app.callback([Output("s1","children"),Output("m1","children"),Output("auto1","children"),Output("btn1","children"),Output("store1","data")],
              Input("u1","contents"),State("u1","filename"))
def upload(c,f):
    if not c:return None,"0",None,None,None
    _,cs=c.split(",")
    df=pd.read_csv(io.StringIO(base64.b64decode(cs).decode("utf-8")))if f.endswith(".csv")else pd.read_excel(io.BytesIO(base64.b64decode(cs)))
    
    s=html.Div([html.H3(f"✅ {f}",style={"color":"#10b981"}),html.P(f"{len(df):,} rows",style={"color":"white"})],className="analysis-card")
    
    types=[]
    for col in df.columns:
        qtype=detect_question_type(df[col],col)
        icon="⭐"if qtype=="rating_scale"else"📝"if qtype=="open_text"else"🔢"
        types.append(html.Div([html.Span(icon,style={"marginRight":"1rem"}),html.Span(f"{col}: ",style={"color":"white","fontWeight":"600"}),
                              html.Span(qtype.upper(),style={"color":"#667eea","fontWeight":"700"})],style={"padding":"0.5rem 0"}))
    
    scales=[]
    for col in df.select_dtypes(include=[np.number]).columns:
        clean=df[col].dropna()
        if len(clean)>0:
            scales.append(html.Div(f"{col}: {detect_scale_orientation(clean,col)}",style={"color":"white","padding":"0.5rem"}))
    
    auto=html.Div([html.Div([html.H3("🔍 Question Types",style={"color":"white"}),html.Div(types)],className="analysis-card"),
                   html.Div([html.H3("📏 Scale Orientation",style={"color":"white"}),html.Div(scales)],className="analysis-card")])
    
    btn=html.Div([html.H2("🤖 Complete Analysis",style={"color":"white","textAlign":"center","marginBottom":"2rem"}),
                  html.Button("🚀 Run Full AI Analysis",id="b1",n_clicks=0,className="ai-btn",style={"display":"block","margin":"0 auto"})],
                 style={"background":"rgba(255,255,255,0.03)","borderRadius":"25px","padding":"3rem","marginTop":"3rem"})
    
    return s,"1",auto,btn,df.to_dict('records')

@app.callback([Output("results1","children"),Output("m2","children"),Output("m3","children")],
              Input("b1","n_clicks"),State("store1","data"),prevent_initial_call=True)
def ai(n,d):
    df=pd.DataFrame(d)
    
    # Industry
    text_col=df.select_dtypes(include=['object']).columns[0]
    industry=detect_industry_simple(' '.join(df[text_col].head(200).tolist()))
    
    # Sentiment (first 10 reviews)
    pos=0
    for text in df[text_col].head(10):
        if analyze_sentiment(text)=='Positive':
            pos+=1
    sent_pct=(pos/10)*100
    
    # Benchmark
    standards={'restaurant':60,'hotel':65,'airline':55}
    industry_std=standards.get(industry,60)
    vs_industry=sent_pct-industry_std
    
    # Competitors (simple count)
    all_text=' '.join(df[text_col].astype(str)).lower()
    competitors={'Starbucks':all_text.count('starbucks'),'Dunkin':all_text.count('dunkin'),'Peets':all_text.count('peets')}
    top_comp=max(competitors,key=competitors.get)
    
    return html.Div([
        html.H3("✅ Complete!",style={"color":"#10b981","textAlign":"center","fontSize":"2rem"}),
        html.H4(f"🏭 Industry: {industry.upper()}",style={"color":"white","textAlign":"center","marginTop":"2rem","background":"rgba(102,126,234,0.3)","padding":"1.5rem","borderRadius":"15px"}),
        html.H4(f"💭 Sentiment: {sent_pct:.0f}% Positive",style={"color":"#10b981" if sent_pct>=70 else "#f59e0b","textAlign":"center","marginTop":"1rem"}),
        html.H4(f"📊 Benchmark: {vs_industry:+.0f}% vs Industry ({industry_std}%)",style={"color":"#10b981" if vs_industry>0 else "#ef4444","textAlign":"center","marginTop":"1rem"}),
        html.H4(f"🏆 Top Competitor: {top_comp} ({competitors[top_comp]} mentions)",style={"color":"white","textAlign":"center","marginTop":"1rem"})
    ],className="analysis-card"),industry.upper()[:4],f"{sent_pct:.0f}%"

if __name__=="__main__":
    print("🚀 http://127.0.0.1:8050")
    app.run(debug=True,port=8050)
