import gpxpy
import folium
import os
import base64
import plotly.graph_objects as go

# ===============================
# 1️⃣ Leer archivo GPX
# ===============================

with open("rutaSTAR.gpx", "r", encoding="utf-8") as archivo:
    gpx = gpxpy.parse(archivo)

latitudes = []
longitudes = []
alturas = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            latitudes.append(point.latitude)
            longitudes.append(point.longitude)
            alturas.append(point.elevation if point.elevation else 0)

# ===============================
# 2️⃣ MAPA 2D CON FOLIUM
# ===============================

mapa_2d = folium.Map(
    location=[latitudes[0], longitudes[0]],
    zoom_start=15,
    tiles="OpenStreetMap"
)

# Dibujar ruta
folium.PolyLine(
    list(zip(latitudes, longitudes)),
    color="blue",
    weight=4
).add_to(mapa_2d)

# ===============================
# 3️⃣ Agregar 5 fotografías (CON LINK)
# ===============================

carpeta_fotos = "fotos"
imagenes = sorted(os.listdir(carpeta_fotos))[:5]

indices = [
    int(len(latitudes)*0.1),
    int(len(latitudes)*0.3),
    int(len(latitudes)*0.5),
    int(len(latitudes)*0.7),
    int(len(latitudes)*0.9)
]

for i, indice in enumerate(indices):
    nombre_imagen = imagenes[i]
    ruta_relativa = f"fotos/{nombre_imagen}"  # importante: ruta relativa

    html = f"""
        <h4>Foto {i+1}</h4>
        <a href="{ruta_relativa}" target="_blank">
            Abrir imagen en nueva ventana
        </a>
    """

    popup = folium.Popup(html, max_width=300)

    folium.Marker(
        location=[latitudes[indice], longitudes[indice]],
        popup=popup,
        icon=folium.Icon(color="red", icon="camera")
    ).add_to(mapa_2d)
    
# Seleccionamos 5 puntos equidistantes
indices = [
    int(len(latitudes)*0.1),
    int(len(latitudes)*0.3),
    int(len(latitudes)*0.5),
    int(len(latitudes)*0.7),
    int(len(latitudes)*0.9)
]

for i, indice in enumerate(indices):
    ruta_imagen = os.path.join(carpeta_fotos, imagenes[i])

    with open(ruta_imagen, "rb") as img:
        imagen_codificada = base64.b64encode(img.read()).decode()

    html = f'''
        <h4>Foto {i+1}</h4>
        <img src="data:image/jpeg;base64,{imagen_codificada}" width="300">
    '''

    iframe = folium.IFrame(html, width=320, height=350)
    popup = folium.Popup(iframe)

    folium.Marker(
        location=[latitudes[indice], longitudes[indice]],
        popup=popup,
        icon=folium.Icon(color="red", icon="camera")
    ).add_to(mapa_2d)

mapa_2d.save("mapa_2D.html")

print("Mapa 2D generado correctamente.")

# ===============================
# 4️⃣ MAPA 3D CON PLOTLY
# ===============================

fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=longitudes,
    y=latitudes,
    z=alturas,
    mode='lines',
    line=dict(width=6),
    name='Ruta'
))

fig.update_layout(
    title="Ruta GPX en 3D",
    scene=dict(
        xaxis_title="Longitud",
        yaxis_title="Latitud",
        zaxis_title="Altura"
    )
)

fig.write_html("mapa_3D.html")

print("Mapa 3D generado correctamente.")