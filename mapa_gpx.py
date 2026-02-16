import gpxpy
import folium
import os
import plotly.graph_objects as go

# =====================================
# 1️⃣ LEER ARCHIVO GPX
# =====================================

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

if len(latitudes) == 0:
    print("No se encontraron puntos en el archivo GPX.")
    exit()

print("GPX cargado correctamente.")

# =====================================
# 2️⃣ CREAR MAPA 2D
# =====================================

mapa_2d = folium.Map(
    location=[latitudes[0], longitudes[0]],
    zoom_start=16,
    tiles="OpenStreetMap"
)

# Dibujar la ruta
folium.PolyLine(
    list(zip(latitudes, longitudes)),
    color="blue",
    weight=4
).add_to(mapa_2d)

print("Ruta dibujada en mapa 2D.")

# =====================================
# 3️⃣ AGREGAR 5 FOTOGRAFÍAS COMO LINK
# =====================================

carpeta_fotos = "fotos"

if not os.path.exists(carpeta_fotos):
    print("La carpeta 'fotos' no existe.")
    exit()

imagenes = sorted(os.listdir(carpeta_fotos))[:5]

if len(imagenes) < 5:
    print("Debe haber al menos 5 imágenes en la carpeta 'fotos'.")
    exit()

# Elegimos 5 puntos distribuidos en la ruta
indices = [
    int(len(latitudes) * 0.1),
    int(len(latitudes) * 0.3),
    int(len(latitudes) * 0.5),
    int(len(latitudes) * 0.7),
    int(len(latitudes) * 0.9)
]

for i, indice in enumerate(indices):

    nombre_imagen = imagenes[i]
    ruta_relativa = f"fotos/{nombre_imagen}"

    html = f"""
        <h4>Foto {i+1}</h4>
        <p>Punto de la ruta</p>
        <a href="{ruta_relativa}" target="_blank">
            🔍 Abrir imagen en nueva ventana
        </a>
    """

    popup = folium.Popup(html, max_width=300)

    folium.Marker(
        location=[latitudes[indice], longitudes[indice]],
        popup=popup,
        icon=folium.Icon(color="red", icon="camera")
    ).add_to(mapa_2d)

print("Fotografías agregadas como links.")

# Guardar mapa 2D
mapa_2d.save("mapa_2D.html")
print("Mapa 2D guardado como 'mapa_2D.html'.")

# =====================================
# 4️⃣ CREAR MAPA 3D
# =====================================

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

print("Mapa 3D guardado como 'mapa_3D.html'.")
print("Proceso finalizado correctamente.")