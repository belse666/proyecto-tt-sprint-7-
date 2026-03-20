import streamlit as st 
import pandas as pd 
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

# Leer los datos del archivo CSV
car_data= pd.read_csv('/home/abdel/tripletent/proyecto/proyecto-sprint-7-abdel-/vehicles_us.csv')

# --- SECCIÓN 1: VISUALIZACIÓN DE TABLA ---

# Encabezado
st.header('📊 Datos de Vehículos en Inventario')

st.subheader('Explorador de datos')

# Casilla de verificación para mostrar/ocultar el dataframe
show_df = st.checkbox('Mostrar tabla de datos')

if show_df:
    st.write(car_data)


#---SECCION 2: GRAFICO DE BARRAS INTERACTIVO---

# Extraemos la primera palabra (la marca)
# .str.split().str[0] toma la primera palabra antes del espacio
car_data['marca'] = car_data['model'].str.split().str[0]
#convierte a mayuscula la primera letra
car_data['marca'] = car_data['marca'].str.capitalize()
# Encabezado
st.title("🚗 Tipos de veiculos por marca")

# Agrupamos por marca y tipo para tener el efecto "coloreado" por categorías
datos_grafico = car_data.groupby(['marca','type']).size().reset_index(name='count')

# Ordenar por precio para el efecto de ascenso/descenso
datos_grafico = datos_grafico.sort_values(by='marca', ascending=True)
#codigo del grafico
fig_bar = px.bar(
    datos_grafico, 
    x="marca", 
    y="count", 
    color="type", # colores por categoría ,
    barmode="stack",# estilo de barras en el grafico 
    template='plotly_white',
    color_discrete_sequence=px.colors.qualitative.Pastel # Paleta de colores
)

# Mejorar diseño
fig_bar.update_layout(
    xaxis_tickangle=-45,
    yaxis_title="Cantidad de veiculos",
    xaxis_title="Marca del vehiculo"
)

# Mostrar en Streamlit
st.plotly_chart(fig_bar, use_container_width=True)

#----SECCION 3: HISTOGRAMA INTERACTIVO----

st.title("Histograma de condicion vs año del vehiculo")
# Agrupamos por año y condicion para tener el efecto "coloreado" por categorias 
datos_grafico_2= car_data.groupby(['model_year','condition']).size().reset_index(name='count')

#codigo del grafico 

fig_hist = px.histogram(datos_grafico_2,
                        x="model_year",
                        y='count',
                        color='condition',
                        marginal='rug',
                        template='plotly_white',
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                        
)
# Mejorar diseño
fig_hist.update_layout(
    xaxis_title='Año del vehiculo',
    yaxis_title='Cantidad de vehiculos' 
)
#Cambio en el eje x
fig_hist.update_xaxes(
    dtick=20, # forsamos el salto de las etiquetas cada 20 unidades 
    tick0=2000 # punto de referencia para que los saltos sean(1980, 2000, 2020...)
)
# mostramos en streamlit
st.plotly_chart(fig_hist,use_container_width=True)

#----SECCION 4: COMPARADOR DE PRECIOS MARCAS----

# Encabezado  

st.title('💵Comparacion de precios de distribucion entre marcas')
# filtramos las marcas disponibles 
marcas_disponibles= car_data['marca'].unique()
# agregamos none al principio de la lista 
marcas_con_vacio= [None] + list(marcas_disponibles)
# selector de m,arca #1
marca_seleccionada= st.selectbox("Selecciona la primer marca:", marcas_con_vacio,index=0)
# selector de marca #2
marca_seleccionada2= st.selectbox('Selecciona la segunda marca:', marcas_con_vacio,index=0)
# filtro de marcas seleccionadas 
df_filtrado= car_data[car_data['marca'].isin([marca_seleccionada,marca_seleccionada2])]

# Codigo del grafico
fig_comp =px.histogram(
                       df_filtrado,
                       x= 'price',
                       histnorm='percent',
                       color= 'marca',
                       marginal='rug',
                       template='plotly_white',
                       color_discrete_sequence=px.colors.qualitative.Pastel

    )
# cambios en el eje y
fig_comp.update_yaxes(
                      dtick=10,# Forsamos el salto de las etiquetas cada 10 unidades 
                      tick0=0,# punto de inicio de los saltos 
)
# mejoramos el diseño
fig_comp.update_layout(
                       xaxis_title='Precio',
                       yaxis_title='Porcentage (%)'
)
# mostramos en streamlit
st.plotly_chart(fig_comp,use_container_width=True)