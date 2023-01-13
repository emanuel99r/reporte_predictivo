from dash import Dash, html, dcc, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
import json
import math

app = Dash(__name__)

listM1=[]
listM2=[]
listM3=[]
listOtros=[]
listTHDV=[]
listTHDI=[]
# ---------------- VARIABLES (Querys, csv, excel, json...)-------

Data=pd.read_csv("/home/admlinux/7pozos/reporte_predictivo/DataGuardian.csv")
f = open('/home/admlinux/7pozos/reporte_predictivo/pozo.json')
pozo = json.load(f)
for i,var in enumerate(Data.columns): 
    
    if  var!="time" and Data[var].sum()!=0:
        if "M1" in var:
            listM1.append(Data.columns[i])
            if "THDV" in var:
                listTHDV.append(Data.columns[i])
            elif "THDI" in var and var!="THDITPQM1":
                listTHDI.append(Data.columns[i])
        elif "M2" in var:
            listM2.append(Data.columns[i])  
        elif "M3" in var:
            listM3.append(Data.columns[i])   
        else:
            listOtros.append(Data.columns[i])

#Guardar Gráficos (Prueba...)

#io.write_image(fig=figTorta,file="./img.jpg", format="jpeg",scale=None, width=None, height=None)
# pip install -U kaleido


Encabezado = html.Div([html.Div(id="nombre_pozo" , className="Titulo")],className="TituloBox")
Operatividad=html.Div([
    
    html.Div([
        html.Div("Periodo del Reporte", className="TitlePeriodo"),
        html.Div([html.Div("Fecha Inicio: ", className="ItemOp"), html.Div("--", className="ItemOpR", id="fechaIni")], className="Item"),
        html.Div([html.Div("Fecha Fin: ",    className="ItemOp"), html.Div("--", className="ItemOpR", id="fechaFin")], className="Item"),
        ], className="Periodo"),
       
        html.Div([
        html.Div("Operatividad", className="TitleOpe"),
        html.Div(dcc.Graph(id='GraficoTorta', className="GraficoTorta"))
                ]),
       
        html.Div([
        html.Div("Identificación Sistema - Bomba",   className="TitleSistema"),
        html.Div([html.Div("Mod. Operación: ",    className="ItemOp"), html.Div("Frecuencia", className="ItemOpR")], className="Item"),
        html.Div([html.Div("Frecuencia Base: ",      className="ItemOp"), html.Div("60"+" Hz",   className="ItemOpR")], className="Item")
        ], className="IdenSistema")
    
    ],className="OperatividadPadre")
Diagrama = html.Div(
                [
                html.Div("",className="DiagramaECP"),

                html.Div(html.Div("VFD"),           className="CajaM", style={"top":"20px", "left":"415px"}),
                html.Div(html.Div("SUT"),           className="CajaM", style={"top":"20px", "left":"600px"}),
                html.Div(html.Div("MOTOR - BOMBA"), className="CajaM", style={"top":"20px", "left":"790px"}),
                
                html.Div(
                    [
                        html.Div("--"+" %",    id="PCARGAVFD",  className="CajaHijoVar"),
                        html.Div("--"+" %",    id="EFIVFD",     className="CajaHijoVar")
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"390px"}),
                
                html.Div(
                    [
                        html.Div("--"+" %",    id="PCARGASUT",  className="CajaHijoVar"),
                        html.Div("--"+" %",    id="EFISUT",     className="CajaHijoVar")
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"575px"}),
                
                html.Div(
                    [
                        html.Div("--"+" %",    id="EFIMB",     className="CajaHijoVar")
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"810px"}),
                
                html.Div(
                    [
                        html.Div(html.Div("Eficiencia")),
                        html.Div(html.Div("Porcentaje de Carga", style={"text-align": "right", "margin-top":"5px"}))
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"200px"}),
                
                html.Div(
                    [
                        html.Div([html.Div("Freq ",   className="CajaHijoName"),  html.Div("--"+" Hz",   id="FREQ_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Iin ",    className="CajaHijoName"),  html.Div("--"+" A",    id="AMP_M1",   className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Vin ",    className="CajaHijoName"),  html.Div("--"+" V",    id="VRMS_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("P. Ac ",  className="CajaHijoName"),  html.Div("--"+" kW",   id="POATC_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("P. Ap ",  className="CajaHijoName"),  html.Div("--"+" kVA",  id="POAPC_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("P. Re ",  className="CajaHijoName"),  html.Div("--"+" kVAr", id="POREC_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("FPin ",   className="CajaHijoName"),  html.Div("--"+" %",    id="FPOT_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Desv I ", className="CajaHijoName"),  html.Div("--"+" %",    id="DESVI_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Desv V ", className="CajaHijoName"),  html.Div("--"+" %",    id="DESVV_M1", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("THDV ",   className="CajaHijoName"),  html.Div("--"+" %",    id="THDV_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("THDI ",   className="CajaHijoName"),  html.Div("--"+" %",    id="THDI_M1",  className="CajaHijoVar")], className="CajaHijo")
                    ]
                         ,className="CajaM", style={"top":"250px", "left":"260px"}),
                
                html.Div(
                    [
                        html.Div([html.Div("--"+" Hz",   id="FREQ_M2",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" A",    id="AMP_M2",   className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" V",    id="VRMS_M2",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kW",   id="POATC_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVA",  id="POAPC_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVAr", id="POREC_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="FPOT_M2",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVI_M2", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVV_M2", className="CajaHijoVar")], className="CajaHijo")
                    ]
                         ,className="CajaM", style={"top":"250px", "left":"480px"}),
                
                html.Div(
                    [
                        html.Div([html.Div("--"+" Hz",   id="FREQ_M3",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" A",    id="AMP_M3",   className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" V",    id="VRMS_M3",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kW",   id="POATC_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVA",  id="POAPC_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" kVAr", id="POREC_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="FPOT_M3",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVI_M3", className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("--"+" %",    id="DESVV_M3", className="CajaHijoVar")], className="CajaHijo")
                    ]
                         ,className="CajaM", style={"top":"250px", "left":"660px"}),
                
                ],className="ImagenPadre")
Graficos=html.Div([
    
        html.Div("Análisis de Tendencias", className="TituloTendencias"),
    
        html.Div([
            html.Div(dcc.Dropdown(listM1, 'POACTPQM1T_kW', id='DropM1', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoM1"), className="Grafico")
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listM2, 'POACTPQM2_kW', id='DropM2', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoM2"), className="Grafico")
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listM3, 'POACTPQM3_kW', id='DropM3', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoM3"), className="Grafico")
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listOtros, 'PIP_PSIG', id='DropOtro', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoOtro"), className="Grafico")
        ], className="GraficoHijo"),
                    
                    
    ],className="GraficosPadre")
Armónicos=html.Div([
    
        html.Div("Análisis de Armónicos", className="TituloTendencias"),
        
        html.Div([
            html.Div("",style={"height":"45px"}),
            html.Div(dcc.Graph(id="GraficoTHDV"), className="Grafico")
        ], className="GraficoHijo"),
    
        html.Div([
            html.Div(dcc.Dropdown(listTHDI, 'THDI7PQM1', id='DropTHDI', clearable=False), className="DropTags"),
            html.Div(dcc.Graph(id="GraficoTHDI"), className="Grafico")
        ], className="GraficoHijo")
    
    
    ],className="ArmónicosPadre")
Vibraciones=html.Div([
    
        html.Div("Análisis de Vibraciones", className="TituloTendencias"),
    
    
    ],className="VibracionesPadre")
Botones=html.Div(
        [
            html.Button('Descargar', id='btn-Descargar', n_clicks=0, className="btn1"),

        ], className="Buttons") 

Cuerpo= html.Div([

    Encabezado,
    Operatividad,
    Diagrama,
    Graficos,
    Armónicos,
    Vibraciones,
    Botones
    
],className="Cuerpo")

app.layout = dbc.Container([Cuerpo], class_name="ReportMain")

def Rotulos(value):
    if value.find("_")!=-1:
        und=value[value.find("_")+1:]
        var=value[0:value.find("_")]
    else:
        var=value
        und=""
        
    return [und, var]

#Cambio en Gráficos
@app.callback(
    Output('GraficoM1', 'figure'),
    Output('GraficoM2', 'figure'),
    Output('GraficoM3', 'figure'),
    Output('GraficoOtro', 'figure'),
    Output('GraficoTHDV', 'figure'),
    Output('GraficoTHDI', 'figure'),
    
    Input('DropM1', 'value'),
    Input('DropM2', 'value'),
    Input('DropM3', 'value'),
    Input('DropTHDI', 'value'),
    Input('DropOtro', 'value')
)
def update_output(DropM1, DropM2, DropM3, DropTHDI, DropOtro):
    Data=pd.read_csv("/home/admlinux/7pozos/reporte_predictivo/DataGuardian.csv")
    
    GraficoM1 = go.Figure()
    GraficoM1.add_trace(go.Line(x=Data['time'], y=Data[str(DropM1)].dropna()))
    [undM1, varM1]=Rotulos(DropM1)
    GraficoM1.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undM1+"</b>",
            title={
            'text': f"<b>{varM1}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropM1)].min(),1.001*Data[str(DropM1)].max()]
            )
    GraficoM1.update_traces(line_color='#108DE4', line_width=1)
    GraficoM1.add_hrect(
        y0=Data[str(DropM1)].mean(), y1=Data[str(DropM1)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropM1)].mean(),2)} {undM1}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")

    GraficoM2 = go.Figure()
    GraficoM2.add_trace(go.Line(x=Data['time'], y=Data[str(DropM2)].dropna()))
    [undM2, varM2]=Rotulos(DropM2)
    GraficoM2.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undM2+"</b>",
            title={
            'text': f"<b>{varM2}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropM2)].min(),1.001*Data[str(DropM2)].max()]
            )
    GraficoM2.update_traces(line_color='#108DE4', line_width=1)
    GraficoM2.add_hrect(
        y0=Data[str(DropM2)].mean(), y1=Data[str(DropM2)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropM2)].mean(),2)} {undM2}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")
    
    GraficoM3 = go.Figure()
    GraficoM3.add_trace(go.Line(x=Data['time'], y=Data[str(DropM3)].dropna()))
    [undM3, varM3]=Rotulos(DropM3)
    GraficoM3.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undM3+"</b>",
            title={
            'text': f"<b>{varM3}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropM3)].min(),1.001*Data[str(DropM3)].max()]
            )
    GraficoM3.update_traces(line_color='#108DE4', line_width=1)
    GraficoM3.add_hrect(
        y0=Data[str(DropM3)].mean(), y1=Data[str(DropM3)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropM3)].mean(),2)} {undM3}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")
    
    GraficoOtro = go.Figure()
    GraficoOtro.add_trace(go.Line(x=Data['time'], y=Data[str(DropOtro)].dropna()))
    [undOtro, varOtro]=Rotulos(DropOtro)
    GraficoOtro.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+undOtro+"</b>",
            title={
            'text': f"<b>{varOtro}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.999*Data[str(DropOtro)].min(),1.001*Data[str(DropOtro)].max()]
            )
    GraficoOtro.update_traces(line_color='#108DE4', line_width=1)
    GraficoOtro.add_hrect(
        y0=Data[str(DropOtro)].mean(), y1=Data[str(DropOtro)].mean(), 
        line_color="#ff7f0e", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropOtro)].mean(),2)} {undOtro}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#ff7f0e")
    
    GraficoTHDV = go.Figure()
    GraficoTHDV.add_trace(go.Line(x=Data['time'], y=Data["THDVTPQM1T"].dropna()))
    [und, var]=Rotulos("THDVTPQM1T")
    GraficoTHDV.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+und+"</b>",
            title={
            'text': f"<b>{var}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.1*Data["THDVTPQM1T"].min(),1.3*Data["THDVTPQM1T"].max()]
            )
    GraficoTHDV.update_traces(line_color='#EF721B', line_width=1)
    GraficoTHDV.add_hrect(
        y0=Data["THDVTPQM1T"].mean(), y1=Data["THDVTPQM1T"].mean(), 
        line_color="#00552D", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data['THDVTPQM1T'].mean(),2)} {und}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#00552D",
        line_dash="dot",
        row="3",
        col="all")
    GraficoTHDV.add_vrect(
        x0="2022-11-26T18:00",
        x1="2022-11-27T06:00", 
        annotation_text="Fuera de Rango (ejemplo)",
        annotation_position="top left",
        fillcolor="#72EF1B", 
        opacity=0.25, 
        line_width=0)  
    GraficoTHDV.add_hrect(
        y0=8,
        y1=1.3*Data["THDVTPQM1T"].max(),
        line_width=0,
        fillcolor="red", 
        opacity=0.1,
        annotation_text="Max: 8%", 
        annotation_position="bottom right"
        )
    
    GraficoTHDI = go.Figure()
    GraficoTHDI.add_trace(go.Line(x=Data['time'], y=Data[str(DropTHDI)].dropna()))
    [und, var]=Rotulos(DropTHDI)
    GraficoTHDI.update_layout(
            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=15, b=0, l=0, r=0),
            width=620,
            height=300,
            font_size=10,
            yaxis_title="<b>"+und+"</b>",
            title={
            'text': f"<b>{var}</b>",
            'y':1,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
            yaxis_range=[0.2*Data[str(DropTHDI)].min(),1.5*Data[str(DropTHDI)].max()]
            )
    GraficoTHDI.update_traces(line_color='#EF721B', line_width=1)
    GraficoTHDI.add_hrect(
        y0=Data[str(DropTHDI)].mean(), y1=Data[str(DropTHDI)].mean(), 
        line_color="#00552D", opacity=0.6, line_width=1,
        annotation_text=f"<b>{round(Data[str(DropTHDI)].mean(),2)} {und}</b>", 
        annotation_position="bottom right",
        annotation_font_size=10,
        annotation_font_color="white",
        annotation_bgcolor="#00552D",
        line_dash="dot",
        row="3",
        col="all")
    GraficoTHDI.add_hrect(
        y0=15,
        y1=1.5*Data[str(DropTHDI)].max(),
        line_width=0,
        fillcolor="red", 
        opacity=0.1,
        annotation_text="Max: 15%", 
        annotation_position="bottom right"
        )
    
    #Que % está fuera de rango y en qué rangos de tiempo... estadistica de ello
    
    return [GraficoM1, GraficoM2, GraficoM3, GraficoOtro, GraficoTHDV, GraficoTHDI]

#Actualización de Variables
@app.callback(
    Output('GraficoTorta', 'figure'),
    Output('nombre_pozo', 'children'),
    Output('fechaIni', 'children'),
    Output('fechaFin', 'children'),
    Output('VRMS_M1', 'children'),
    Output('VRMS_M2', 'children'),
    Output('VRMS_M3', 'children'),
    Output('FREQ_M1', 'children'),
    Output('AMP_M1', 'children'),
    Output('POATC_M1', 'children'),
    Output('POAPC_M1', 'children'),
    Output('POREC_M1', 'children'),
    Output('FPOT_M1', 'children'),
    Output('DESVI_M1', 'children'),
    Output('DESVV_M1', 'children'),
    #Output('THDV_M1', 'children'),
    Output('FREQ_M2', 'children'),
    Output('AMP_M2', 'children'),
    

    Input('PCARGAVFD', 'children')
)
def actualizar_vars(var):
    
    Data=pd.read_csv("/home/admlinux/7pozos/reporte_predictivo/DataGuardian.csv")
    print(Data.columns)
    f = open('/home/admlinux/7pozos/reporte_predictivo/pozo.json')
    pozo = json.load(f)

    #-----------Operatividad----------------------------------------------
    nombre_pozo = "REPORTE PREDICTIVO POZO "+pozo["pozo"]
    FECHAINI=Data["time"].iloc[0][0:10]
    FECHAFIN=Data["time"].iloc[-1][0:10]
    HORASON=Data["HORAS_ON"].sum()
    HORASOFF=Data["HORAS_OFF"].sum()

    labels = ['ON','OFF']
    values = [round(HORASON,2),round(HORASOFF,2)]  #Variables de Entrada Torta

    figTorta = go.Figure(data=[go.Pie(labels=labels, values=values)])
    figTorta.update_layout(

            showlegend=False,
            paper_bgcolor="rgb(248, 251, 254)",
            margin=dict(t=0, b=0, l=25, r=25),
            annotations=[
            {
                "font": {
                "size": 10
                },
                "showarrow": False,
                "text": str(sum(values))+" Hrs",
                "x": 0.5,
                "y": 0.48
            },
            {
                "font": {
                "size": 10
                },
                "showarrow": False,
                "text": '<b>TOTAL</b>',
                "x": 0.5,
                "y": 0.55
            }]
                
    )
    figTorta.update_traces(
        hoverinfo='value',
        textinfo='label+percent',
        textfont_size=10,
        hole=.4,
        marker=dict(colors=["#108DE4", "#E42465"])
        )

    #-------------M1--------------------------------------------------------------------------------------------------
    
    VM1=str(round((Data["VABPQM1T_volt"].mean()+Data["VBCPQM1T_volt"].mean()+Data["VCAPQM1T_volt"].mean())/3,2))
    VM2=str(round((Data["VABPQM2_volt"].mean()+Data["VBCPQM2_volt"].mean()+Data["VCAPQM2_volt"].mean())/3,2))
    VM3=str(round((Data["VABPQM3_volt"].mean()+Data["VBCPQM3_volt"].mean()+Data["VCAPQM3_volt"].mean())/3,2))
    FREQM1 = str(round(Data["FREQPQM1_Hz"].mean(),2))
    AMPM1 = str(round((Data["AMPAPQM1T_amp"].mean()+Data["AMPBPQM1T_amp"].mean()+Data["AMPCPQM1T_amp"].mean())/3,2))
    POACTM1 = str(round(Data["POACTPQM1T_kW"].mean(),2))
    POAPM1 = str(round(math.sqrt(Data["POACTPQM1T_kW"].mean()**2+Data["PORETPQM1T_kvar"].mean()**2),2))
    POREM1 = str(round(Data["PORETPQM1T_kvar"].mean(),1))
    FPOTM1 = str(round(Data["FPTPQM1T"].mean(),2))
    DESVIM1 = str(round(Data["DESAMPM1_%"].mean(),2))
    DESVVM1 = str(round(Data["DESVMPM1_%"].mean(),2))
    '''
    if Data["THDVTPQM1T"]:
        THDVM1 = str(round(Data["THDVTPQM1T"],2))
    else:
        THDVM1 = ""    
    '''
    FREQM2 = str(round(Data["FREQPQM2_Hz"].mean(),2))
    AMPM2 = str(round((Data["AMPAPQM2_amp"].mean()+Data["AMPBPQM2_amp"].mean()+Data["AMPCPQM2_amp"].mean())/3,2))


    return [figTorta, nombre_pozo, FECHAINI, FECHAFIN, VM1+" V", VM2+" V", VM3+" V", FREQM1+" Hz", AMPM1+" A",
            POACTM1+" kW", POAPM1+" kVA", POREM1+" kVAR", FPOTM1+" %", DESVIM1+" %", DESVVM1+" %", FREQM2+" Hz",
            AMPM2+" A"]

if __name__ == '__main__':
    app.run_server(host="10.232.24.9",port="3838")
