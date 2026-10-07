import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

MATRIX_GREEN = "#55ff88"
MATRIX_GREEN_2 = "#20c866"
MATRIX_DARK = "#06110a"
GRID = "rgba(85,255,136,0.18)"
AXIS = "rgba(210,255,224,0.72)"


def _mesh_trace(vertices, faces, name, opacity=0.88):
    v = np.asarray(vertices, dtype=float)
    i, j, k = zip(*faces)
    return go.Mesh3d(
        x=v[:, 0], y=v[:, 1], z=v[:, 2],
        i=i, j=j, k=k,
        name=name,
        color=MATRIX_GREEN,
        opacity=opacity,
        flatshading=True,
        lighting=dict(ambient=0.42, diffuse=0.9, roughness=0.32, specular=0.48, fresnel=0.18),
        lightposition=dict(x=80, y=100, z=140),
        hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
    )


def _cube(a):
    h = a / 2
    v = np.array([
        [-h, -h, 0], [h, -h, 0], [h, h, 0], [-h, h, 0],
        [-h, -h, a], [h, -h, a], [h, h, a], [-h, h, a],
    ])
    faces = [
        (0, 1, 2), (0, 2, 3), (4, 6, 5), (4, 7, 6),
        (0, 4, 5), (0, 5, 1), (1, 5, 6), (1, 6, 2),
        (2, 6, 7), (2, 7, 3), (3, 7, 4), (3, 4, 0),
    ]
    return _mesh_trace(v, faces, "Cubo")


def _pyramid(a, h):
    s = a / 2
    v = np.array([[-s,-s,0],[s,-s,0],[s,s,0],[-s,s,0],[0,0,h]])
    faces = [(0,2,1),(0,3,2),(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
    return _mesh_trace(v, faces, "Pirámide")


def _prism(b, t, L):
    z0, z1 = 0.0, L
    v = np.array([
        [-b/2, -t/3, z0], [b/2, -t/3, z0], [0, 2*t/3, z0],
        [-b/2, -t/3, z1], [b/2, -t/3, z1], [0, 2*t/3, z1],
    ])
    faces = [
        (0,2,1),(3,4,5),
        (0,1,4),(0,4,3),
        (1,2,5),(1,5,4),
        (2,0,3),(2,3,5),
    ]
    return _mesh_trace(v, faces, "Prisma triangular")


def _sphere(r):
    u = np.linspace(0, 2*np.pi, 72)
    v = np.linspace(0, np.pi, 46)
    x = r * np.outer(np.cos(u), np.sin(v))
    y = r * np.outer(np.sin(u), np.sin(v))
    z = r + r * np.outer(np.ones_like(u), np.cos(v))
    return go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, "#0b4c27"], [0.52, MATRIX_GREEN_2], [1, "#baffca"]],
        showscale=False, opacity=0.9,
        lighting=dict(ambient=0.4, diffuse=0.9, roughness=0.28, specular=0.45),
        hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
        name="Esfera",
    )


def _cylinder(r, h):
    theta = np.linspace(0, 2*np.pi, 72)
    z = np.linspace(0, h, 35)
    T, Z = np.meshgrid(theta, z)
    X, Y = r*np.cos(T), r*np.sin(T)
    side = go.Surface(
        x=X, y=Y, z=Z,
        colorscale=[[0, "#0a4424"], [1, MATRIX_GREEN]],
        showscale=False, opacity=0.88,
        lighting=dict(ambient=.45,diffuse=.88,roughness=.35,specular=.35),
        name="Cilindro",
        hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
    )
    rr = np.linspace(0, r, 22)
    TT, RR = np.meshgrid(theta, rr)
    Xb, Yb = RR*np.cos(TT), RR*np.sin(TT)
    bottom = go.Surface(x=Xb,y=Yb,z=np.zeros_like(Xb),colorscale=[[0,MATRIX_GREEN_2],[1,MATRIX_GREEN]],showscale=False,opacity=.88,hoverinfo="skip")
    top = go.Surface(x=Xb,y=Yb,z=np.full_like(Xb,h),colorscale=[[0,MATRIX_GREEN_2],[1,MATRIX_GREEN]],showscale=False,opacity=.88,hoverinfo="skip")
    return [side, bottom, top]


def _cone(r, h):
    theta = np.linspace(0, 2*np.pi, 72)
    z = np.linspace(0, h, 42)
    T, Z = np.meshgrid(theta, z)
    R = r * (1 - Z/h)
    X, Y = R*np.cos(T), R*np.sin(T)
    side = go.Surface(
        x=X, y=Y, z=Z,
        colorscale=[[0, "#0b4425"], [1, MATRIX_GREEN]],
        showscale=False, opacity=.9,
        lighting=dict(ambient=.42,diffuse=.9,roughness=.33,specular=.4),
        name="Cono",
        hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
    )
    rr = np.linspace(0, r, 22)
    TT, RR = np.meshgrid(theta, rr)
    base = go.Surface(x=RR*np.cos(TT),y=RR*np.sin(TT),z=np.zeros_like(RR),colorscale=[[0,MATRIX_GREEN_2],[1,MATRIX_GREEN]],showscale=False,opacity=.9,hoverinfo="skip")
    return [side, base]


def camera_for(view):
    cameras = {
        "Isométrica": dict(eye=dict(x=1.55, y=1.55, z=1.25), up=dict(x=0,y=0,z=1)),
        "Frontal XZ": dict(eye=dict(x=0, y=-2.35, z=.75), up=dict(x=0,y=0,z=1)),
        "Lateral YZ": dict(eye=dict(x=2.35, y=0, z=.75), up=dict(x=0,y=0,z=1)),
        "Superior XY": dict(eye=dict(x=.001, y=.001, z=2.75), up=dict(x=0,y=1,z=0)),
    }
    return cameras.get(view, cameras["Isométrica"])


def build_3d_figure(shape, params, view="Isométrica", show_grid=True):
    fig = go.Figure()
    if shape == "Cubo":
        fig.add_trace(_cube(params["lado"]))
    elif shape == "Esfera":
        fig.add_trace(_sphere(params["radio"]))
    elif shape == "Cilindro":
        for tr in _cylinder(params["radio"], params["altura"]): fig.add_trace(tr)
    elif shape == "Cono":
        for tr in _cone(params["radio"], params["altura"]): fig.add_trace(tr)
    elif shape == "Pirámide":
        fig.add_trace(_pyramid(params["lado_base"], params["altura"]))
    else:
        fig.add_trace(_prism(params["base_triangulo"], params["altura_triangulo"], params["longitud"]))

    scene_axis = dict(
        showbackground=True,
        backgroundcolor="rgba(2,9,5,.84)",
        gridcolor=GRID if show_grid else "rgba(0,0,0,0)",
        zerolinecolor=AXIS,
        color="#bdf6ca",
        title_font=dict(color="#bdf6ca"),
        showgrid=show_grid,
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0,r=0,t=8,b=0),
        height=620,
        showlegend=False,
        scene=dict(
            xaxis={**scene_axis, "title":"X"},
            yaxis={**scene_axis, "title":"Y"},
            zaxis={**scene_axis, "title":"Z"},
            aspectmode="data",
            camera=camera_for(view),
        ),
        transition=dict(duration=420, easing="cubic-in-out"),
    )
    return fig


def _style_2d(fig, titles=("Plano XY", "Corte XZ")):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(2,10,5,.72)",
        margin=dict(l=25,r=20,t=48,b=28), height=520,
        font=dict(color="#dfffe8"), showlegend=False,
    )
    for col in (1,2):
        fig.update_xaxes(scaleanchor=f"y{'' if col==1 else '2'}", scaleratio=1, showgrid=True, gridcolor=GRID, zerolinecolor=AXIS, row=1, col=col)
        fig.update_yaxes(showgrid=True, gridcolor=GRID, zerolinecolor=AXIS, row=1, col=col)
    return fig


def build_2d_figure(shape, params):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Plano XY", "Corte XZ"), horizontal_spacing=.12)
    line = dict(color=MATRIX_GREEN, width=4)
    fill = "rgba(85,255,136,.12)"

    if shape == "Cubo":
        a=params["lado"]; h=a/2
        x=[-h,h,h,-h,-h]; y=[-h,-h,h,h,-h]
        fig.add_trace(go.Scatter(x=x,y=y,mode="lines",line=line,fill="toself",fillcolor=fill),1,1)
        fig.add_trace(go.Scatter(x=x,y=[0,0,a,a,0],mode="lines",line=line,fill="toself",fillcolor=fill),1,2)
    elif shape == "Esfera":
        r=params["radio"]; t=np.linspace(0,2*np.pi,240); x=r*np.cos(t); y=r*np.sin(t)
        fig.add_trace(go.Scatter(x=x,y=y,mode="lines",line=line,fill="toself",fillcolor=fill),1,1)
        fig.add_trace(go.Scatter(x=x,y=r+r*np.sin(t),mode="lines",line=line,fill="toself",fillcolor=fill),1,2)
    elif shape == "Cilindro":
        r,h=params["radio"],params["altura"]; t=np.linspace(0,2*np.pi,240)
        fig.add_trace(go.Scatter(x=r*np.cos(t),y=r*np.sin(t),mode="lines",line=line,fill="toself",fillcolor=fill),1,1)
        fig.add_trace(go.Scatter(x=[-r,r,r,-r,-r],y=[0,0,h,h,0],mode="lines",line=line,fill="toself",fillcolor=fill),1,2)
    elif shape == "Cono":
        r,h=params["radio"],params["altura"]; t=np.linspace(0,2*np.pi,240)
        fig.add_trace(go.Scatter(x=r*np.cos(t),y=r*np.sin(t),mode="lines",line=line,fill="toself",fillcolor=fill),1,1)
        fig.add_trace(go.Scatter(x=[-r,r,0,-r],y=[0,0,h,0],mode="lines",line=line,fill="toself",fillcolor=fill),1,2)
    elif shape == "Pirámide":
        a,h=params["lado_base"],params["altura"]; s=a/2
        fig.add_trace(go.Scatter(x=[-s,s,s,-s,-s],y=[-s,-s,s,s,-s],mode="lines",line=line,fill="toself",fillcolor=fill),1,1)
        fig.add_trace(go.Scatter(x=[-s,s,0,-s],y=[0,0,h,0],mode="lines",line=line,fill="toself",fillcolor=fill),1,2)
    else:
        b,t,L=params["base_triangulo"],params["altura_triangulo"],params["longitud"]
        fig.add_trace(go.Scatter(x=[-b/2,b/2,0,-b/2],y=[-t/3,-t/3,2*t/3,-t/3],mode="lines",line=line,fill="toself",fillcolor=fill),1,1)
        fig.add_trace(go.Scatter(x=[-b/2,b/2,b/2,-b/2,-b/2],y=[0,0,L,L,0],mode="lines",line=line,fill="toself",fillcolor=fill),1,2)

    return _style_2d(fig)
