# app.py
import streamlit as st
from grua import CalculadoraGrua
import pandas as pd
from datetime import datetime, timedelta, timezone

# CONFIGURACIÓN DE PÁGINA (Mantiene el formato expandido premium)
st.set_page_config(layout="wide")

# Inicializar la memoria del historial si no existe
if "historial_calculos" not in st.session_state:
    st.session_state.historial_calculos = []

# ==========================================
# 1. COMPONENTES VISUALES ENLAZADOS
# ==========================================

class LogoUnica:
    """Gestiona el Escudo de la UNICA (.PNG) para que se fusione sin fondo."""
    def __init__(self):
        self.archivo = "logo_unica.png"
        self.universidad = "Universidad Cardenal Miguel Obando Bravo"

    def renderizar(self, tamano=200):
        try:
            return st.image(self.archivo, width=tamano)
        except Exception:
            return st.error(f"⚠️ No se encontró '{self.archivo}'")


class IconoGruaIco:
    """Gestiona tu nuevo icono de la Grúa (.ICO) para el interior."""
    def __init__(self):
        self.archivo = "icono_grua.ico"

    def renderizar(self, tamano=65):
        try:
            return st.image(self.archivo, width=tamano)
        except Exception:
            return st.error(f"⚠️ No se encontró '{self.archivo}' en tu carpeta.")


# ==========================================
# 2. PORTADA DE BIENVENIDA (LIMPÌA Y SIMÉTRICA)
# ==========================================

class PortadaInicio:
    """Renderiza la portada exclusivamente con el logo de la UNICA al centro."""
    def __init__(self):
        self.logo = LogoUnica()

    def renderizar(self):
        st.markdown("<div style='padding-top: 60px;'></div>", unsafe_allow_html=True)

        col_izq, col_centro, col_der = st.columns([1, 0.6, 1])
        with col_centro:
            st.markdown(
                """
                <style>
                    .stImage > img {
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                        mix-blend-mode: lighten; 
                    }
                </style>
                """, 
                unsafe_allow_html=True
            )
            self.logo.renderizar(tamano=180)

        st.markdown("<h1 style='text-align: center; color: #f59e0b; font-size: 44px; font-weight: bold; margin-top: 15px;'>CALCULADORA DE GRÚA TORRE</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px; margin-bottom: 5px;'>Proyecto Integrador — Ingeniería Industrial</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 1.5px solid #f59e0b; width: 50%; margin: 10px auto;'/>", unsafe_allow_html=True)
        st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)

        col_btn_izq, col_btn_centro, col_btn_der = st.columns([2, 0.8, 2])
        with col_btn_centro:
            if st.button("▶ INGRESAR", use_container_width=True, type="primary"):
                st.session_state.ingresado = True
                st.rerun()

        st.markdown("<div style='padding-top: 90px;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569; font-size: 13px;'>© 2026 — Proyecto Grúa Torre UNICA</p>", unsafe_allow_html=True)


# ==========================================
# 3. INTERFAZ INTERNA DETALLADA (BOTÓN + HISTORIAL ACTIVO)
# ==========================================

class InterfazCalculadora:
    def __init__(self):
        self.logo = LogoUnica()
        self.icono_ico = IconoGruaIco()
        self.calculadora = CalculadoraGrua()

    def renderizar(self):
        # Cabecera
        col_header_logo, col_header_text = st.columns([0.06, 1])
        with col_header_logo:
            self.icono_ico.renderizar(tamano=55)
        with col_header_text:
            st.markdown("<h1 style='margin: 0; font-size: 36px; font-weight: bold; color: #ffffff;'>CALCULADORA DE GRÚA TORRE</h1>", unsafe_allow_html=True)
            st.markdown("<p style='margin: 0; color: #94a3b8; font-size: 15px;'>Proyecto Integrador — Ingeniería Industrial (UNICA)</p>", unsafe_allow_html=True)
        
        st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #334155;'/>", unsafe_allow_html=True)

        # MENÚ DE PESTAÑAS
        tab_calculos, tab_historial, tab_graficas, tab_exportar = st.tabs([
            "Cálculos", "Historial", "Gráficas", "Exportar"
        ])

        # ================= PESTAÑA 1: CÁLCULOS =================
        with tab_calculos:
            st.markdown("<h2 style='font-size: 24px; font-weight: bold;'>Datos de Entrada</h2>", unsafe_allow_html=True)
            
            col_input_izq, col_input_der = st.columns(2)
            
            with col_input_izq:
                peso_carga = st.number_input("Masa de la carga a elevar (Toneladas):", min_value=0.1, max_value=12.0, value=3.0, step=0.5)
                distancia_carro = st.number_input("Distancia al carro / Radio desde el eje (m):", min_value=1.0, max_value=60.0, value=25.0, step=1.0)
            
            with col_input_der:
                altura_izaje = st.number_input("Altura de elevación requerida (m):", min_value=0.0, max_value=80.0, value=15.0, step=5.0)
                angulo_giro = st.number_input("Ángulo de giro de la pluma (°):", min_value=0.0, max_value=360.0, value=0.0, step=45.0)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # EL BOTÓN EXPLIČITO DE CALCULAR
            btn_calcular = st.button("▶ EJECUTAR CÁLCULO TÉCNICO", type="primary", use_container_width=True)
            
            if btn_calcular:
                res = self.calculadora.calcular_estabilidad(peso_carga, distancia_carro, altura_izaje)
                st.session_state.ultimo_resultado = res
                
                # CORRECCIÓN DE HORA: Forzar Zona Horaria UTC-6 (Nicaragua / Centroamérica)
                zona_horaria_local = timezone(timedelta(hours=-6))
                hora_exacta = datetime.now(zona_horaria_local).strftime("%H:%M:%S")
                
                # Insertar en el historial global
                nuevo_registro = {
                    "Hora": hora_exacta,
                    "Carga (Ton)": peso_carga,
                    "Radio (m)": distancia_carro,
                    "Momento (t·m)": f"{res['momento_carga']:.1f}",
                    "F. Seguridad": f"{res['factor_seguridad']:.2f}",
                    "Resultado": "SEGURO" if res["es_seguro"] else "PELIGRO"
                }
                st.session_state.historial_calculos.append(nuevo_registro)

            st.markdown("<hr style='border: 0.5px dashed #475569;'/>", unsafe_allow_html=True)
            st.markdown("<h2 style='font-size: 24px; font-weight: bold;'>Diagnóstico y Resultados</h2>", unsafe_allow_html=True)

            if "ultimo_resultado" in st.session_state:
                resultados = st.session_state.ultimo_resultado
                
                if resultados["es_seguro"]:
                    st.success(f"DIAGNÓSTICO: {resultados['estado']}")
                else:
                    st.error(f"DIAGNÓSTICO: {resultados['estado']}")

                col_m1, col_m2, col_m3 = st.columns(3)
                col_m1.metric("Momento Solicitado (Volcante)", f"{resultados['momento_carga']:.1f} t·m")
                col_m2.metric("Factor de Seguridad Real (FS)", f"{resultados['factor_seguridad']:.2f}")
                col_m3.metric("Capacidad Máx. en este Radio", f"{resultados['carga_max_distancia']:.2f} Ton")

                st.markdown("<br>", unsafe_allow_html=True)
                st.subheader("Matriz de Estabilidad Estática")
                data_tabla = {
                    "Parámetro Analizado": ["Momento Límite de Volcado", "Momento Efectivo Frontal", "Límite Estructural Fijo"],
                    "Magnitud Calculada": [f"{resultados['momento_estabilidad']:.1f} t·m", f"{resultados['momento_carga']:.1f} t·m", "12.0 Toneladas Máx."]
                }
                st.table(data_tabla)
            else:
                st.info("💡 Modifica los valores arriba y presiona el botón 'EJECUTAR CÁLCULO TÉCNICO' para ver el diagnóstico estructural.")

        # ================= PESTAÑA 2: HISTORIAL =================
        with tab_historial:
            st.markdown("<h2 style='font-size: 24px; font-weight: bold;'>📄 Historial Técnico de Operaciones</h2>", unsafe_allow_html=True)
            if len(st.session_state.historial_calculos) > 0:
                df_historial = pd.DataFrame(st.session_state.historial_calculos)
                st.dataframe(df_historial, use_container_width=True)
                if st.button("🗑️ Limpiar Historial"):
                    st.session_state.historial_calculos = []
                    st.rerun()
            else:
                st.warning("Aún no se han ejecutado cálculos en esta sesión. Ve a la pestaña 'Cálculos' e ingresa datos.")
        
        # ================= PESTAÑA 3: GRÁFICAS =================
        with tab_graficas:
            st.markdown("<h2 style='font-size: 24px; font-weight: bold;'>📈 Curva Límite de Carga de la Grúa</h2>", unsafe_allow_html=True)
            st.info("Muestra la correlación inversa entre la distancia del carro y la carga admisible (Tope: 12 Ton).")
            radios = list(range(10, 65, 5))
            cargas_limite = [min(12.0, 120.0 / r) for r in radios]
            chart_data = pd.DataFrame({"Radio de Pluma (m)": radios, "Carga Máxima Permitida (Toneladas)": cargas_limite})
            st.line_chart(chart_data.set_index("Radio de Pluma (m)"))
            
        # ================= PESTAÑA 4: EXPORTAR =================
        with tab_exportar:
            st.markdown("<h2 style='font-size: 24px; font-weight: bold;'>💾 Exportación de Reportes</h2>", unsafe_allow_html=True)
            st.info("Módulo de Ingeniería Industrial habilitado para impresión de hojas de ruta de izaje.")
            if len(st.session_state.historial_calculos) > 0:
                st.download_button(
                    label="📥 Descargar Registro Técnico (.CSV)",
                    data=pd.DataFrame(st.session_state.historial_calculos).to_csv(index=False).encode('utf-8'),
                    file_name="reporte_estabilidad_grua.csv",
                    mime="text/csv"
                )
            else:
                st.write("Realiza cálculos primero para poder descargar un informe.")

        # Botón de retorno limpio
        st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Volver a Portada de Inicio"):
            st.session_state.ingresado = False
            if "ultimo_resultado" in st.session_state:
                del st.session_state.ultimo_resultado
            st.rerun()


# ==========================================
# 4. CONTROLADOR CENTRAL DE FLUJO
# ==========================================

if __name__ == "__main__":
    if 'ingresado' not in st.session_state:
        st.session_state.ingresado = False

    if not st.session_state.ingresado:
        pantalla_inicio = PortadaInicio()
        pantalla_inicio.renderizar()
    else:
        sistema_calculo = InterfazCalculadora()
        sistema_calculo.renderizar()