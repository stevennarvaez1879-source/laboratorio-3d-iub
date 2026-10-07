import streamlit as st
from figures import build_3d_figure, build_2d_figure
from math_content import CONTENT, metrics

st.set_page_config(
    page_title="Matrix 3D Lab | IUB",
    page_icon="🟩",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = r'''
<style>
:root{--mx:#55ff88;--mx2:#1ed760;--bg:#020704;--panel:rgba(5,20,11,.86);--line:rgba(85,255,136,.20);}
html,body,[class*="css"]{font-family:Inter,system-ui,-apple-system,Segoe UI,Arial,sans-serif}
.stApp{background:
 radial-gradient(circle at 15% 0%,rgba(33,255,111,.12),transparent 32%),
 radial-gradient(circle at 90% 10%,rgba(14,106,52,.15),transparent 30%),
 linear-gradient(180deg,#010402 0%,#031009 58%,#010402 100%);color:#eaffef;}
.stApp:before{content:"01001011   IUB   00110101   PYTHON   01010110   NUMPY   00110011   MATRIX 3D LAB";position:fixed;z-index:0;left:0;right:0;top:0;white-space:nowrap;overflow:hidden;color:rgba(85,255,136,.07);font:700 12px/1.4 monospace;letter-spacing:.5em;animation:mxscan 18s linear infinite;pointer-events:none}
@keyframes mxscan{from{text-indent:-25%}to{text-indent:10%}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 rgba(85,255,136,0)}50%{box-shadow:0 0 28px rgba(85,255,136,.10)}}
@keyframes enter{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.block-container{position:relative;z-index:1;padding-top:2rem;max-width:1500px}
[data-testid="stSidebar"]{background:rgba(2,11,6,.95);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:#dffff0}
div[data-testid="stMetric"]{background:linear-gradient(180deg,rgba(7,27,15,.86),rgba(3,15,8,.92));border:1px solid var(--line);border-radius:16px;padding:14px 16px;animation:enter .45s ease both}
div[data-testid="stMetricValue"]{color:#eaffef}
div[data-testid="stMetricLabel"]{color:#8fcda2}
.mx-hero{padding:28px 30px;border:1px solid var(--line);border-radius:24px;background:linear-gradient(135deg,rgba(3,18,9,.95),rgba(7,33,17,.84));animation:pulse 4s ease-in-out infinite, enter .5s ease both;margin-bottom:18px;overflow:hidden;position:relative}
.mx-hero:after{content:"";position:absolute;inset:0;background:repeating-linear-gradient(180deg,rgba(255,255,255,.018) 0,rgba(255,255,255,.018) 1px,transparent 2px,transparent 5px);pointer-events:none}
.mx-kicker{font:800 12px monospace;letter-spacing:.17em;color:var(--mx);text-transform:uppercase}
.mx-title{font-size:clamp(32px,5vw,58px);line-height:1.02;margin:.25rem 0 .6rem;font-weight:850;letter-spacing:-.03em;text-shadow:0 0 28px rgba(85,255,136,.12)}
.mx-sub{max-width:920px;color:#b9e9c7;font-size:16px;line-height:1.65}
.mx-meta{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:18px}
.mx-meta>div{border:1px solid var(--line);border-radius:13px;background:rgba(3,13,7,.55);padding:10px 12px;color:#c9f5d5;font-size:12px}
.mx-meta b{display:block;color:#7df99d;margin-bottom:3px;text-transform:uppercase;letter-spacing:.07em;font-size:10px}
.mx-card{border:1px solid var(--line);border-radius:18px;background:linear-gradient(180deg,rgba(6,24,13,.86),rgba(2,13,7,.9));padding:18px;animation:enter .45s ease both;margin:8px 0 14px}
.mx-card h3{margin:0 0 8px;color:#eefff3}
.mx-card p{color:#b8dec3;line-height:1.65;margin:.35rem 0}
.mx-equation{font-family:Georgia,serif;color:#dffff0;font-size:17px;border-left:3px solid var(--mx);padding:9px 12px;background:rgba(5,25,12,.55);border-radius:0 12px 12px 0}
.mx-chip{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:6px 10px;color:#7df99d;background:rgba(4,18,10,.7);font:700 11px monospace;letter-spacing:.06em;margin-right:5px;margin-bottom:5px}
.stTabs [data-baseweb="tab-list"]{gap:8px;background:rgba(3,15,8,.72);padding:6px;border:1px solid var(--line);border-radius:14px}
.stTabs [data-baseweb="tab"]{border-radius:10px;color:#a8d8b6;padding:.55rem .9rem}
.stTabs [aria-selected="true"]{background:rgba(27,111,51,.42)!important;color:#eaffef!important}
.stButton>button,.stDownloadButton>button{border:1px solid rgba(85,255,136,.28);background:linear-gradient(135deg,#113921,#061b0e);color:#eaffef;border-radius:12px;font-weight:700}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:#55ff88;color:#fff;box-shadow:0 0 20px rgba(85,255,136,.12)}
hr{border-color:rgba(85,255,136,.12)}
code{color:#8dffab!important}
@media(max-width:900px){.mx-meta{grid-template-columns:1fr 1fr}}
@media(max-width:600px){.mx-meta{grid-template-columns:1fr}.mx-hero{padding:21px}}
</style>
'''
st.markdown(CSS, unsafe_allow_html=True)

if "presentation" not in st.session_state:
    st.session_state.presentation = False

# Sidebar controls
with st.sidebar:
    st.markdown("### ◈ MATRIX 3D LAB")
    st.caption("Control geométrico · Python / NumPy / Plotly")
    shape = st.selectbox("Figura geométrica", ["Cubo","Esfera","Cilindro","Cono","Pirámide","Prisma"])

    params = {}
    if shape == "Cubo":
        params["lado"] = st.slider("Lado a", .5, 5.0, 2.5, .1)
    elif shape == "Esfera":
        params["radio"] = st.slider("Radio r", .5, 5.0, 2.2, .1)
    elif shape in ("Cilindro","Cono"):
        params["radio"] = st.slider("Radio r", .5, 5.0, 1.8 if shape=="Cilindro" else 2.0, .1)
        params["altura"] = st.slider("Altura h", .5, 6.0, 3.5, .1)
    elif shape == "Pirámide":
        params["lado_base"] = st.slider("Lado de la base a", .5, 5.0, 3.2, .1)
        params["altura"] = st.slider("Altura h", .5, 6.0, 3.4, .1)
    else:
        params["base_triangulo"] = st.slider("Base del triángulo b", .5, 5.0, 3.0, .1)
        params["altura_triangulo"] = st.slider("Altura del triángulo t", .5, 5.0, 2.6, .1)
        params["longitud"] = st.slider("Longitud L", .5, 6.0, 4.0, .1)

    st.divider()
    view = st.selectbox("Vista de cámara", ["Isométrica","Frontal XZ","Lateral YZ","Superior XY"])
    show_grid = st.toggle("Mostrar cuadrícula XYZ", True)
    st.session_state.presentation = st.toggle("Modo exposición", st.session_state.presentation)

# Hero
st.markdown('''
<div class="mx-hero">
  <div class="mx-kicker">INSTITUCIÓN UNIVERSITARIA DE BARRANQUILLA IUB · SISTEMA GEOMÉTRICO ACTIVO</div>
  <div class="mx-title">Creación de figuras geométricas 3D utilizando Python</div>
  <div class="mx-sub">Laboratorio interactivo que conecta la representación matemática en 2D y 3D con su implementación en Python. Las figuras se construyen sobre el plano <b>XY</b>, con <b>Z</b> como eje vertical.</div>
  <div class="mx-meta">
    <div><b>Programa</b>Licenciatura en Tecnología e Informática</div>
    <div><b>Asignatura</b>Fundamentos Matemáticos</div>
    <div><b>Docente</b>Wilson Emilio Montaño Santamaría</div>
    <div><b>Integrantes</b>Lina Marín · Marlon Villa · Steven Narvaez · Valentina Maza</div>
  </div>
</div>
''', unsafe_allow_html=True)

volume, area, props = metrics(shape, params)
content = CONTENT[shape]

# Presentation mode: clean, projection-friendly view
if st.session_state.presentation:
    st.markdown(f"<span class='mx-chip'>MODO EXPOSICIÓN</span><span class='mx-chip'>{shape.upper()}</span><span class='mx-chip'>XY → BASE</span><span class='mx-chip'>Z → ALTURA</span>", unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Volumen", f"{volume:.3f} u³")
    c2.metric("Área total", f"{area:.3f} u²")
    c3.metric("Propiedades", props)
    fig = build_3d_figure(shape, params, view=view, show_grid=show_grid)
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo":False,"scrollZoom":True})
    st.markdown("<div class='mx-card'><h3>Ecuación / representación matemática</h3></div>", unsafe_allow_html=True)
    st.latex(content["equation"])
    if st.button("Salir del modo exposición"):
        st.session_state.presentation = False
        st.rerun()
    st.stop()

# Normal mode navigation
nav = st.radio("Navegación", ["Laboratorio 2D/3D","Matemáticas","Código Python","Comparación"], horizontal=True, label_visibility="collapsed")

if nav == "Laboratorio 2D/3D":
    mode = st.segmented_control("Modo de visualización", ["3D interactivo","2D matemático"], default="3D interactivo")
    c1,c2,c3 = st.columns(3)
    c1.metric("Volumen", f"{volume:.3f} u³")
    c2.metric("Área total", f"{area:.3f} u²")
    c3.metric("Propiedades", props)

    if mode == "3D interactivo":
        st.markdown("<div class='mx-card'><h3>Visualización tridimensional</h3><p>Arrastra la figura para rotarla. Usa la rueda del mouse dentro de la gráfica para acercar o alejar. La base está apoyada en Z = 0.</p></div>", unsafe_allow_html=True)
        fig = build_3d_figure(shape, params, view=view, show_grid=show_grid)
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo":False,"scrollZoom":True,"responsive":True})
    else:
        st.markdown("<div class='mx-card'><h3>Construcción en dos dimensiones</h3><p>Se muestran simultáneamente la huella sobre el plano XY y un corte XZ para visualizar la relación entre base, radio y altura.</p></div>", unsafe_allow_html=True)
        fig2 = build_2d_figure(shape, params)
        st.plotly_chart(fig2, use_container_width=True, config={"displaylogo":False,"responsive":True})

    st.markdown(f"<div class='mx-card'><h3>Lenguaje matemático de {shape}</h3><p>{content['definition']}</p><div class='mx-equation'>Ecuación o condición generadora:</div></div>", unsafe_allow_html=True)
    st.latex(content["equation"])
    colA,colB = st.columns(2)
    with colA:
        st.caption("Volumen")
        st.latex(content["volume"])
    with colB:
        st.caption("Área total")
        st.latex(content["area"])

elif nav == "Matemáticas":
    st.markdown(f"<div class='mx-card'><h3>{shape}: estructura matemática</h3><p>{content['definition']}</p><p><b>Cómo se genera:</b> {content['generator']}</p></div>", unsafe_allow_html=True)
    st.subheader("Ecuación / definición espacial")
    st.latex(content["equation"])
    a,b = st.columns(2)
    with a:
        st.subheader("Área")
        st.latex(content["area"])
    with b:
        st.subheader("Volumen")
        st.latex(content["volume"])
    st.info(f"Con los parámetros actuales: área = {area:.3f} u² y volumen = {volume:.3f} u³.")
    st.plotly_chart(build_2d_figure(shape, params), use_container_width=True, config={"displaylogo":False})

elif nav == "Código Python":
    st.markdown(f"<div class='mx-card'><h3>{shape}: del lenguaje matemático a Python</h3><p>El siguiente fragmento representa la lógica principal empleada para generar la geometría seleccionada con NumPy.</p></div>", unsafe_allow_html=True)
    st.code(content["code"], language="python", line_numbers=True)
    st.markdown("<div class='mx-card'><h3>Flujo del programa</h3><p>1. Se reciben los parámetros → 2. NumPy genera coordenadas → 3. Plotly construye la superficie o malla → 4. Streamlit actualiza la interfaz → 5. Las fórmulas recalculan área y volumen.</p></div>", unsafe_allow_html=True)
    st.download_button("Descargar módulo figures.py", data=open("figures.py","rb").read(), file_name="figures.py", mime="text/x-python")

else:
    st.markdown("<div class='mx-card'><h3>Comparación geométrica</h3><p>La tabla relaciona la naturaleza matemática de cada sólido con la estrategia usada para programarlo.</p></div>", unsafe_allow_html=True)
    rows = [
        ["Cubo","Poliedro","Lado","Vértices + caras","Desigualdades cartesianas"],
        ["Esfera","Cuerpo redondo","Radio","Superficie paramétrica","Ecuación cuadrática"],
        ["Cilindro","Cuerpo redondo","Radio, altura","Superficie paramétrica","Circunferencia + intervalo Z"],
        ["Cono","Cuerpo redondo","Radio, altura","Radio variable con Z","Ecuación radial"],
        ["Pirámide","Poliedro","Base, altura","Vértices + caras","Base + ápice"],
        ["Prisma","Poliedro","Triángulo, longitud","Extrusión de base","Traslación sobre Z"],
    ]
    import pandas as pd
    st.dataframe(pd.DataFrame(rows, columns=["Figura","Tipo","Parámetros","Construcción Python","Modelo matemático"]), use_container_width=True, hide_index=True)
    st.plotly_chart(build_3d_figure(shape, params, view="Isométrica", show_grid=True), use_container_width=True, config={"displaylogo":False})

st.caption("Matrix 3D Lab · IUB · Python + NumPy + Plotly + Streamlit · La estética está inspirada visualmente en interfaces de ciencia ficción digital tipo Matrix.")
