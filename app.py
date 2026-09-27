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
e= st.sidebar.slider("Excentricidad", 0.0, 0.99, 0.5, 0.01)
r_0_ua = st.sidebar.slider("Posición inicial en x (UA)", 0.5, 10.0, 1.0, 0.5)
M_solares = st.sidebar.slider("Masa de la estrella (masas solares)", 1.0, 100.0, 10.0, 1.0)
col1 = st.sidebar.columns(1)
play = col1[0].button("Play")
G = 6.67430e-11
M = M_solares * 1.989e30
r_0 = r_0_ua * 1.496e11
a = r_0 / (1-e)
c = e * a
UA = 1.496e11

fondo = Image.open("fondo-2.jpg")
planeta = Image.open("tierra.png")
sol = Image.open("sol.png")

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
    lim_ua = 80.0
    axis.set_xlim([-lim_ua, lim_ua])
    axis.set_ylim([-lim_ua/2, lim_ua/2])
    axis.imshow(fondo, extent=[-lim_ua, lim_ua, -lim_ua, lim_ua], zorder=0, aspect='auto')
    sol_x = c/UA
    axis.imshow(sol, extent=[sol_x - 1.5, sol_x + 1.5, -1.5, 1.5], zorder=1)
    
    if mostrar_planeta and x_anim is not None:
        x_ua = x_anim / UA
        y_ua = y_anim / UA
        
        inicio_estela = max(0, frame_actual - 15)

        axis.plot(
            x_ua[inicio_estela:frame_actual + 1],
            y_ua[inicio_estela:frame_actual + 1],
            color="cyan",
            linewidth=2.5,
            zorder=4,
        )
        axis.imshow(
            planeta,
            extent=[
                x_ua[frame_actual] - 1.0,
                x_ua[frame_actual] + 1.0,
                y_ua[frame_actual] - 1.0,
                y_ua[frame_actual] + 1.0,
            ],
            zorder=9,
        )
    return fig

if st.session_state.animando:
    M = np.linspace(0, 2 * np.pi, 120)
    
    x_trayectoria = a * np.cos(M)
    y_trayectoria = a * np.sqrt(1 - e**2) * np.sin(M)
    
    for i in range(1, len(x_trayectoria)):
        fig = generar_escenario(
            x_trayectoria, y_trayectoria, mostrar_planeta=True, frame_actual=i
        )
        contenedor_grafico.pyplot(fig)
        plt.close(fig)
        time.sleep(0.03)
else:
    fig = generar_escenario()
    E_estatico = np.linspace(0, 2 * np.pi, 120)
    fig = generar_escenario(
        a * (np.cos(E_estatico) - e), 
        a * np.sqrt(1 - e**2) * np.sin(E_estatico), 
        mostrar_planeta=True, 
        frame_actual=len(E_estatico)-1
    )
    contenedor_grafico.pyplot(fig)
    plt.close(fig)
