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
a_ua = a / UA
b_ua = a * np.sqrt(1 - e**2) / UA
fondo = Image.open("fondo-2.jpg")
planeta = Image.open("tierra.png")
sol = Image.open("sol.png")

if "animando" not in st.session_state:
    st.session_state.animando = False

if play:
    st.session_state.animando = True

contenedor_grafico = st.empty()

if st.session_state.animando:
    M_values = np.linspace(0, 2 * np.pi, 120)

    x_trayectoria = a * np.cos(M_values)
    y_trayectoria = a * np.sqrt(1 - e**2) * np.sin(M_values)


    frecuencia_relativa = np.sqrt(M_solares / 10.0)
    tiempo_pausa = 0.01 / frecuencia_relativa

  
    fig, axis = plt.subplots(figsize=(8, 4.5))

    fig.patch.set_facecolor("#1e1e1e")
    axis.set_facecolor("#1e1e1e")
    axis.tick_params(colors="white", which="both")

    for spine in axis.spines.values():
        spine.set_edgecolor("white")

    lim_x = a_ua * 1.15
    lim_y = b_ua * 1.15

    axis.set_xlim(-lim_x, lim_x)
    axis.set_ylim(-lim_y, lim_y)

    # Fondo y Sol: se dibujan una sola vez
    axis.imshow(
        fondo,
        extent=[-lim_x, lim_x, -lim_y, lim_y],
        zorder=0,
        aspect="auto"
    )

    sol_x = c / UA
    t_sol = lim_x * 0.075
    t_tierra = lim_x * 0.05

    axis.imshow(
        sol,
        extent=[
            sol_x - t_sol, sol_x + t_sol,
            -t_sol, t_sol
        ],
        zorder=1
    )


    estela, = axis.plot(
        [], [],
        color="cyan",
        linewidth=2.5,
        zorder=4
    )

    planeta_artist = axis.imshow(
        planeta,
        extent=[
            x_trayectoria[0] / UA - t_tierra,
            x_trayectoria[0] / UA + t_tierra,
            y_trayectoria[0] / UA - t_tierra,
            y_trayectoria[0] / UA + t_tierra
        ],
        zorder=9
    )

    try:
        for i in range(1, len(x_trayectoria)):
            x_ua = x_trayectoria[i] / UA
            y_ua = y_trayectoria[i] / UA

    
            inicio_estela = max(0, i - 15)

            estela.set_data(
                x_trayectoria[inicio_estela:i + 1] / UA,
                y_trayectoria[inicio_estela:i + 1] / UA
            )


            planeta_artist.set_extent([
                x_ua - t_tierra,
                x_ua + t_tierra,
                y_ua - t_tierra,
                y_ua + t_tierra
            ])


            contenedor_grafico.pyplot(
                fig,
                clear_figure=False
            )

            time.sleep(max(0.001, tiempo_pausa))

    finally:
        plt.close(fig)
        st.session_state.animando = False

