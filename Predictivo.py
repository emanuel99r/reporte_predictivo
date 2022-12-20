from dash import Dash, html, dcc, ctx
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as io
import pandas as pd
from dash.dependencies import Input, Output, State

app = Dash(__name__)

# ---------------- VARIABLES (Querys, csv, excel, json...)-------

Data=pd.read_csv("./DataGuardian.csv")

FECHAINI=Data["time"].iloc[0][0:10]
FECHAFIN=Data["time"].iloc[-1][0:10]

VM1=str(round((Data["VABPQM1T_volt"].mean()+Data["VBCPQM1T_volt"].mean()+Data["VCAPQM1T_volt"].mean())/3,2))
VM2=str(round((Data["VABPQM2_volt"].mean()+Data["VBCPQM2_volt"].mean()+Data["VCAPQM2_volt"].mean())/3,2))
VM3=str(round((Data["VABPQM3_volt"].mean()+Data["VBCPQM3_volt"].mean()+Data["VCAPQM3_volt"].mean())/3,2))


HORASON=Data["HORAS_ON"].sum()
HORASOFF=Data["HORAS_OFF"].sum()


#print(Data.columns)

# -----------------------Deben ser "str"--------------------------

# Torta Operatividad, las variables de entrada son int o float

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


Grafico1 = go.Figure()
Grafico1.update_layout(

        showlegend=False,
        paper_bgcolor="rgb(248, 251, 254)",
        margin=dict(t=0, b=0, l=25, r=25)
        
)

Grafico1.add_trace(go.Line(x=Data['time'], y=Data["POACTPQM1T_kW"]))

#----------------------------------------------------------------

#Guardar Gráficos (Prueba...)

#io.write_image(fig=figTorta,file="./img.jpg", format="jpeg",scale=None, width=None, height=None)
# pip install -U kaleido

Encabezado = html.Div([html.Div("REPORTE PREDICTIVO POZO CS-023", className="Titulo")],className="TituloBox")
Operatividad=html.Div([
    
    html.Div([
        html.Div("Periodo del Reporte", className="TitlePeriodo"),
        html.Div([html.Div("Fecha Inicio: ", className="ItemOp"), html.Div(FECHAINI, className="ItemOpR", id="fechaIni")], className="Item"),
        html.Div([html.Div("Fecha Fin: ",    className="ItemOp"), html.Div(FECHAFIN, className="ItemOpR", id="fechaFin")], className="Item"),
        ], className="Periodo"),
       
        html.Div([
        html.Div("Operatividad", className="TitleOpe"),
        html.Div(dcc.Graph(id='GraficoTorta',figure=figTorta, className="GraficoTorta"))
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
                        html.Div("--"+" %",    id="PCARGAMB",  className="CajaHijoVar"),
                        html.Div("--"+" %",    id="EFIMB",     className="CajaHijoVar")
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"810px"}),
                
                html.Div(
                    [
                        html.Div(html.Div("Porcentaje de Carga")),
                        html.Div(html.Div("Eficiencia", style={"text-align": "right", "margin-top":"5px"}))
                    ]
                         ,className="CajaM", style={"top":"50px", "left":"200px"}),
                
                html.Div(
                    [
                        html.Div([html.Div("Freq ",   className="CajaHijoName"),  html.Div("--"+" Hz",   id="FREQ_M1",  className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Iin ",    className="CajaHijoName"),  html.Div("--"+" A",    id="AMP_M1",   className="CajaHijoVar")], className="CajaHijo"),
                        html.Div([html.Div("Vin ",    className="CajaHijoName"),  html.Div(VM1+" V",    id="VRMS_M1",  className="CajaHijoVar")], className="CajaHijo"),
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
                        html.Div([html.Div(VM2+" V",    id="VRMS_M2",  className="CajaHijoVar")], className="CajaHijo"),
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
                        html.Div([html.Div(VM3+" V",    id="VRMS_M3",  className="CajaHijoVar")], className="CajaHijo"),
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
    
                    html.Div(dcc.Dropdown(Data.columns, 'POACTPQM1T_kW', id='DropTags'), className="DropTags"),
                    html.Div(dcc.Graph(id="Grafico1", figure=Grafico1), className="Grafico"),
                    
                    
    
    ],className="GraficosPadre")
Botones=html.Div(
        [
            html.Button('Descargar', id='btn-Descargar', n_clicks=0, className="btn1"),

        ], className="Buttons") 
Cuerpo= html.Div([

    Operatividad,
    Diagrama,
    Graficos,
    Botones
    
],className="Cuerpo")

app.layout = dbc.Container([Encabezado,Cuerpo], class_name="ReportMain")


@app.callback(
    Output('Grafico1', 'figure'),
    Input('DropTags', 'value')
)
def update_output(value):
    
    Grafico1.update_traces(
        x=Data['time'],
        y=Data[str(value)].dropna()
        )
    Grafico1.update_layout(
            xaxis_title="Tiempo",
            yaxis_title=value
            )
    Grafico1.update_traces(line_color='#108DE4')
    
    return Grafico1

if __name__ == '__main__':
    app.run_server(debug=True)