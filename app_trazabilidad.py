import streamlit as st
import pandas as pd

st.set_page_config(page_title="Trazabilidad de Producción - Bripez", layout="wide")

st.title("🧵 Trazabilidad de Producción - Bripez")
st.write("Visualiza y actualiza el estado de los pedidos en cada área del proceso.")

# Cargar archivo Excel
archivo_excel = "produccion_bripez.xlsx"

try:
    df = pd.read_excel(archivo_excel)

    # Calcular progreso
    columnas_areas = ["Corte", "Confección", "Bordado", "Control de Calidad", "Empaque"]
    df["Progreso"] = df[columnas_areas].sum(axis=1) / len(columnas_areas)
    df["Estado"] = df["Progreso"].apply(lambda x: "✅ Completado" if x == 1 else ("⏳ Pendiente" if x == 0 else f"🛠️ En proceso ({int(x*len(columnas_areas))}/{len(columnas_areas)})"))

    st.dataframe(df[["Pedido", "Cliente", "Estado"]])

    st.subheader("Actualizar estado de un pedido")

    pedido_id = st.selectbox("Selecciona un pedido", df["Pedido"])
    pedido = df[df["Pedido"] == pedido_id].iloc[0]

    with st.form(key="formulario_actualizacion"):
        st.write(f"Cliente: {pedido['Cliente']}")
        estado_actual = {area: bool(pedido[area]) for area in columnas_areas}
        nuevos_estados = {}
        for area in columnas_areas:
            nuevos_estados[area] = st.checkbox(area, value=estado_actual[area])
        submitted = st.form_submit_button("Guardar cambios")

        if submitted:
            for area in columnas_areas:
                df.loc[df["Pedido"] == pedido_id, area] = int(nuevos_estados[area])
            df.to_excel(archivo_excel, index=False)
            st.success("✅ Pedido actualizado exitosamente. Recarga la página para ver los cambios.")

except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'produccion_bripez.xlsx'. Asegúrate de que esté en la misma carpeta que esta app.")

