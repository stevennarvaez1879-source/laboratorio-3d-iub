import math


def metrics(shape, p):
    if shape == "Cubo":
        a=p["lado"]
        return a**3, 6*a*a, "8 vértices · 12 aristas · 6 caras"
    if shape == "Esfera":
        r=p["radio"]
        return 4*math.pi*r**3/3, 4*math.pi*r*r, "Superficie curva · sin aristas · sin vértices"
    if shape == "Cilindro":
        r,h=p["radio"],p["altura"]
        return math.pi*r*r*h, 2*math.pi*r*(r+h), "2 bases circulares · superficie lateral curva"
    if shape == "Cono":
        r,h=p["radio"],p["altura"]; g=math.hypot(r,h)
        return math.pi*r*r*h/3, math.pi*r*(r+g), "1 base circular · 1 vértice · generatriz"
    if shape == "Pirámide":
        a,h=p["lado_base"],p["altura"]; l=math.hypot(h,a/2)
        return a*a*h/3, a*a+2*a*l, "5 vértices · 8 aristas · 5 caras"
    b,t,L=p["base_triangulo"],p["altura_triangulo"],p["longitud"]
    Ab=b*t/2; side=math.hypot(b/2,t); P=b+2*side
    return Ab*L, 2*Ab+P*L, "6 vértices · 9 aristas · 5 caras"


CONTENT = {
"Cubo": {
    "definition":"Poliedro regular de seis caras cuadradas congruentes. En el modelo, la base se centra en el origen del plano XY y la altura crece sobre Z.",
    "equation":r"-\frac{a}{2}\le x\le\frac{a}{2},\quad -\frac{a}{2}\le y\le\frac{a}{2},\quad 0\le z\le a",
    "area":r"A=6a^2", "volume":r"V=a^3",
    "generator":"Se define por ocho vértices cartesianos. Las caras se obtienen conectando grupos de cuatro vértices.",
    "code":'''a = 2.5\nh = a / 2\nvertices = np.array([\n    [-h,-h,0], [h,-h,0], [h,h,0], [-h,h,0],\n    [-h,-h,a], [h,-h,a], [h,h,a], [-h,h,a]\n])\n# Las caras trianguladas se pasan a plotly.graph_objects.Mesh3d.'''
},
"Esfera": {
    "definition":"Conjunto de puntos situados a una distancia constante r de un centro. Para apoyar la figura en Z=0, el centro se ubica en (0,0,r).",
    "equation":r"x^2+y^2+(z-r)^2=r^2",
    "area":r"A=4\pi r^2", "volume":r"V=\frac{4}{3}\pi r^3",
    "generator":"Se parametriza mediante dos ángulos. Esta forma permite generar una malla suave con NumPy.",
    "code":'''u = np.linspace(0, 2*np.pi, 72)\nv = np.linspace(0, np.pi, 46)\nx = r*np.outer(np.cos(u), np.sin(v))\ny = r*np.outer(np.sin(u), np.sin(v))\nz = r + r*np.outer(np.ones_like(u), np.cos(v))'''
},
"Cilindro": {
    "definition":"Cuerpo limitado por dos círculos paralelos y una superficie lateral curva. Su eje coincide con Z.",
    "equation":r"x^2+y^2=r^2,\quad 0\le z\le h",
    "area":r"A=2\pi r(r+h)", "volume":r"V=\pi r^2h",
    "generator":"Una circunferencia de radio r se mantiene constante mientras z recorre el intervalo entre 0 y h.",
    "code":'''theta = np.linspace(0, 2*np.pi, 72)\nz = np.linspace(0, h, 35)\nT, Z = np.meshgrid(theta, z)\nX = r*np.cos(T)\nY = r*np.sin(T)'''
},
"Cono": {
    "definition":"Cuerpo con base circular cuyo radio disminuye linealmente hasta llegar a cero en el vértice.",
    "equation":r"x^2+y^2=\left[r\left(1-\frac{z}{h}\right)\right]^2,\quad 0\le z\le h",
    "area":r"A=\pi r(r+g),\quad g=\sqrt{r^2+h^2}", "volume":r"V=\frac{1}{3}\pi r^2h",
    "generator":"El radio efectivo depende de z: R(z)=r(1-z/h). Al llegar a z=h, el radio vale cero.",
    "code":'''T, Z = np.meshgrid(theta, z)\nR = r*(1 - Z/h)\nX = R*np.cos(T)\nY = R*np.sin(T)'''
},
"Pirámide": {
    "definition":"Poliedro con base cuadrada y cuatro caras triangulares que convergen en un vértice situado sobre el centro.",
    "equation":r"B:\ |x|\le\frac{a}{2},\ |y|\le\frac{a}{2},\ z=0;\qquad V=(0,0,h)",
    "area":r"A=a^2+2al,\quad l=\sqrt{h^2+(a/2)^2}", "volume":r"V=\frac{a^2h}{3}",
    "generator":"Se definen cuatro vértices para la base y un quinto vértice superior. Las caras triangulares conectan la base con el ápice.",
    "code":'''s = a/2\nvertices = np.array([\n    [-s,-s,0], [s,-s,0], [s,s,0], [-s,s,0],\n    [0,0,h]\n])'''
},
"Prisma": {
    "definition":"Prisma triangular generado al trasladar un triángulo sobre el eje Z una distancia L.",
    "equation":r"T(x,y)\ \text{en el plano }XY,\qquad 0\le z\le L",
    "area":r"A=2A_b+P_bL", "volume":r"V=A_bL,\quad A_b=\frac{bt}{2}",
    "generator":"Se construyen dos triángulos congruentes en z=0 y z=L y se conectan sus vértices correspondientes.",
    "code":'''base = np.array([[-b/2,-t/3,0], [b/2,-t/3,0], [0,2*t/3,0]])\ntop = base.copy()\ntop[:,2] = L\nvertices = np.vstack([base, top])'''
}}
