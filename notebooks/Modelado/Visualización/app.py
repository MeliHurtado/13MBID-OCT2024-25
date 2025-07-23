import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Lectura de datos
df = pd.read_csv("../../../data/final/datos_finales.csv", sep=";")

# Configuración de la página
st.set_page_config(
    page_title="Herramienta de Visualización de Datos - 13MBID",
    page_icon="📊",
    layout="wide",
)

# Título de la aplicación
st.title("Herramienta de Visualización de Datos - 13MBID")
st.write(
    "Esta aplicación permite explorar y visualizar los datos del proyecto en curso."
)
st.write("Desarrollado por: Melissa Hurtado Alvarez")
st.markdown('----')

# Gráficos
st.header("Gráficos")
st.subheader("Caracterización de los créditos otorgados:")

# Cantidad de créditos por objetivo del mismo
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Visualización
st.plotly_chart(creditos_x_objetivo, use_container_width=True)


# Histograma de los importes de créditos otorgados
histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')

# Visualización
st.plotly_chart(histograma_importes, use_container_width=True)


#Se agrega un selector para el tipo de crédito y se aplica en los gráficos siguientes:
tipo_credito = st.selectbox(
    "Selecciona el tipo de crédito",
    df['objetivo_credito'].unique(),
)

st.write("Tipo de crédito seleccionado:", tipo_credito)

# Filtrar el DataFrame según el tipo de crédito seleccionado
df_filtrado = df[df['objetivo_credito'] == tipo_credito]


# Gráfico de barras apiladas: Comparar la distribución de créditos por estado y objetivo
barras_apiladas = px.histogram(df_filtrado, x='objetivo_credito', color='estado_credito_N', 
                               title='Distribución de créditos por estado y objetivo',
                               barmode='stack')
barras_apiladas.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Visualización
st.plotly_chart(barras_apiladas, use_container_width=True)


# Conteo de ocurrencias por estado
estado_credito_counts = df_filtrado['estado_credito_N'].value_counts()

fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
fig.update_layout(title_text='Distribución de créditos por estado registrado')

# Visualización
st.plotly_chart(fig, use_container_width=True)


# Conteo de ocurrencias por caso
falta_pago_counts = df['falta_pago'].value_counts()

fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
fig.update_layout(title_text='Distribución de créditos en función de registro de mora')

# Visualización
st.plotly_chart(fig, use_container_width=True)

# gráfico importes solicitados por antigüedad del cliente
orden_antiguedad = ['menor_2y', '2y_a_4y', 'mayor_4y']

# Ordenar los datos según el orden personalizado
df_ordenado = df.groupby('antiguedad_cliente')['importe_solicitado'].mean().reset_index()
df_ordenado['antiguedad_cliente'] = pd.Categorical(df_ordenado['antiguedad_cliente'], categories=orden_antiguedad, ordered=True)
df_ordenado = df_ordenado.sort_values('antiguedad_cliente')

# Crear el gráfico de líneas
lineas_importes_antiguedad = px.line(df_ordenado, x='antiguedad_cliente', y='importe_solicitado',
                                     title='Evolución de los importes solicitados por antigüedad del cliente')
lineas_importes_antiguedad.update_layout(xaxis_title='Antigüedad del cliente', yaxis_title='Importe solicitado promedio')

# Visualización
st.plotly_chart(lineas_importes_antiguedad, use_container_width=True)


# Crear el gráfico de cajas
fig = px.box(
    df,
    x="objetivo_credito",
    y="importe_solicitado",
    title="Distribución de los importes solicitados por objetivo del crédito",
    labels={
        "objetivo_credito": "Objetivo del Crédito",
        "importe_solicitado": "Importe Solicitado"
    },
    color="objetivo_credito"
)

# Visualización
st.plotly_chart(fig, use_container_width=True)


# Crear gráfico de dispersión
fig_scatter = px.scatter(
    df,
    x="duracion_credito",
    y="importe_solicitado",
    color="estado_credito_N",
    title="Relación entre importe solicitado y duración del crédito",
    labels={
        "duracion_credito": "Duración del Crédito (meses)",
        "importe_solicitado": "Importe Solicitado",
        "estado_credito_N": "Estado del Crédito"
    }
)

# Visualización
st.plotly_chart(fig_scatter, use_container_width=True)

