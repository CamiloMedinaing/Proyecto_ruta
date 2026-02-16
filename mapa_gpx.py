import gpxpy
import folium
import os
import plotly.graph_objects as go
import exifread

# =====================================
# FUNCIÓN PARA CONVERTIR EXIF A DECIMAL
# =====================================

def convertir_a_decimal(valor):
    grados = float(valor.values[0].num) / float(valor.values[0].den)
    minutos = float(valor.values[1].num) / float(valor.values[1].den)
    segundos = float(valor.values[2].num) / float(valor.values[2].den)
    return grados + (minutos / 60.0) + (segundos / 3600.0)

def obtener_coordenadas_exif(ruta_imagen):
    with open(ruta_imagen, 'rb') as f:
        tags = exifread.process_file(f)

        if "GPS GPSLatitude" in tags and "GPS GPSLongitude" in tags:
            lat = convertir_a_decimal(tags["GPS GPSLatitude"])
            lon = convertir_a_decimal(tags["GPS GPSLongitude"])

            if tags["GPS GPSLatitudeRef"].values != 'N':
                lat = -lat
            if tags["GPS GPSLongitudeRef"].values != 'E':
                lon = -lon

            return lat, lon
        else:
            return None, None

# =====================================
# 1️⃣ LEER GPX
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

# =====================================
# 2️⃣ MAPA 2D
# =====================================

mapa_2d = folium.Map(
    location=[latitudes[0], longitudes[0]],
    zoom_start=16,
    tiles="OpenStreetMap"
)

# Dibujar ruta
folium.PolyLine(
    list(zip(latitudes, longitudes)),
    color="blue",
    weight=4
).add_to(mapa_2d)

# =====================================
# 3️⃣ AGREGAR FOTOS EN SU POSICIÓN REAL
# =====================================

carpeta_fotos = "fotos"
imagenes = sorted(os.listdir(carpeta_fotos))[:5]

for imagen in imagenes:

    ruta_imagen = os.path.join(carpeta_fotos, imagen)
    lat, lon = obtener_coordenadas_exif(ruta_imagen)

    if lat is not None and lon is not None:

        html = f"""
            <h4>{imagen}</h4>
            <a href="fotos/{imagen}" target="_blank">
                🔍 Ver imagen completa
            </a>
        """

        popup = folium.Popup(html, max_width=300)

        folium.Marker(
            location=[lat, lon],
            popup=popup,
            icon=folium.Icon(color="red", icon="camera")
        ).add_to(mapa_2d)

        print(f"Foto {imagen} ubicada en: {lat}, {lon}")

    else:
        print(f"La imagen {imagen} no tiene datos GPS.")

mapa_2d.save("mapa_2D.html")
print("Mapa 2D generado correctamente.")

# =====================================
# 4️⃣ MAPA 3D
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
print("Mapa 3D generado correctamente.")