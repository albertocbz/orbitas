import time
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st
from scipy.optimize import newton
st.set_page_config(
    page_title="Simulador de órbitas", layout="centered"
)
st.title("Simulador órbitas")
st.write(
    "Ajusta los parámetros con los controles de la izquierda y haz clic en"
    " **Play**."
)
st.sidebar.header("Parámetros")
e=st.sidebar.slider("Excentricidad", 0.0, 1.0, 0.5, 0.01)
r_0=st.sidebar.slider("Posición inicial en x (UA)", 0.5, 10.0, 1.0, 0.5)
r_0=r_0*1.496e11
M = st.sidebar.slider("Masa de la estrella (masas solares)", 1.0, 100.0, 10.0, 1.0)
M = M * 1.989e30
m=5.98e24
G=6.67e-11
a=r_0/(1-e**2)
c=e*a
col1=st.sidebar.columns(1)
play=col1[0].button("Play")
fondo = Image.open("fondo-2.jpg")
planeta = Image.open("tierra.png")
sol= Image.open("sol.png")
if "animando" not in st.session_state:
  st.session_state.animando = False
if play:
  st.session_state.animando = True
contenedor_grafico = st.empty()
def generar_escenario(
        x_anim=None, y_anim=None, mostrar_planeta=False, frame_actual=0
):
    fig, axis = plt.subplots(figsize=(8, 4.5))
    fig.patch.set_facecolor("#1e1e1e")
    axis.set_facecolor("#1e1e1e")
    axis.tick_params(colors="white", which="both")
    for spine in axis.spines.values():
        spine.set_edgecolor("white")
    axis.set_xlim([0, 20*1.496e11])
    axis.set_ylim([0, 20*1.496e11])
    axis.imshow(fondo, extent=[0, 20*1.496e11, 0, 20*1.296e11], zorder=0)
    axis.imshow(sol, extent=[c-1e11, c+1e11,10*1.296e11-1e11,10*1.296e11+1e11], zorder=1)
    if mostrar_planeta and x_anim is not None:
        inicio_estela = max(0, frame_actual - 15)

        axis.plot(
            x_anim[inicio_estela:frame_actual + 1],
            y_anim[inicio_estela:frame_actual + 1],
            color="blue",
            linewidth=3,
            zorder=4,
        )
        axis.imshow(
            planeta,
            extent=[
                x_anim[frame_actual] - 9e10,
                x_anim[frame_actual] + 9e10,
                y_anim[frame_actual] - 9e10,
                y_anim[frame_actual] + 9e10,
            ],
            zorder=9,
        )
    return fig
if st.session_state.animando:
    t_max = 2*np.pi*np.sqrt(a**3/(G*M))
    t = np.linspace(0, t_max, 60)
    n=np.sqrt(G*M/a**3)
    E = newton(
        lambda E: E - e * np.sin(E) - n * t,
        n * t
    )
    x_trayectoria = a*(np.cos(E)-e)
    y_trayectoria = a*np.sqrt(1-e**2)*np.sin(E)
    for i in range(1, len(x_trayectoria)):
        fig = generar_escenario(
            x_trayectoria, y_trayectoria, mostrar_planeta=True, frame_actual=i
        )
        contenedor_grafico.pyplot(fig)
        plt.close(fig)
        time.sleep(0.03)
else:
    fig = generar_escenario()
    contenedor_grafico.pyplot(fig)
    plt.close(fig)
