"""
app.py
------
Aplicación web para administrar canciones con sus letras, tono y acordes.

Cómo arrancarla:
    1. Hacé doble clic en  arrancar.bat   (lo más fácil), o
    2. Desde la terminal:   py app.py

Después abrí el navegador en:  http://127.0.0.1:5000
"""

import os
import re

from flask import Flask, render_template, request, redirect, url_for, flash

import database
import acordes

app = Flask(__name__)
# La clave secreta es necesaria para mostrar mensajes flash (avisos).
# En el servidor (Render) se toma de una variable de entorno; en tu PC usa la de respaldo.
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esto-por-cualquier-texto-secreto")

# Crea la tabla la primera vez que se ejecuta.
database.inicializar()

# Si la base está vacía (por ejemplo, la primera vez en Neon/Postgres online),
# carga automáticamente las 149 canciones de la "Lista Nueva".
if database.contar_canciones() == 0:
    try:
        import importar_lista_nueva
        importar_lista_nueva.main()
    except Exception as e:
        print("No se pudieron cargar las canciones iniciales:", e)


@app.route("/")
def inicio():
    """Página principal: canciones agrupadas por categoría, con buscador."""
    busqueda = request.args.get("q", "").strip()
    canciones = database.listar_canciones(busqueda)
    grupos = database.agrupar_por_categoria(canciones)
    return render_template(
        "index.html",
        grupos=grupos,
        canciones=canciones,   # lista plana alfabética para el índice
        total=len(canciones),
        busqueda=busqueda,
    )


def _leer_semitonos():
    """Lee de la URL cuántos semitonos transponer (parámetro ?t=).

    Se limita al rango -11..+11 por seguridad.
    """
    try:
        t = int(request.args.get("t", 0))
    except (TypeError, ValueError):
        t = 0
    return max(-11, min(11, t))


def _cancion_transpuesta(cancion, semitonos):
    """Devuelve una copia de la canción con tono y letra ya transpuestos."""
    datos = dict(cancion)
    datos["tono"] = acordes.transponer_tono(datos.get("tono", ""), semitonos)
    datos["letra"] = acordes.transponer_letra(datos.get("letra", ""), semitonos)
    return datos


@app.route("/cancion/<int:cancion_id>")
def ver_cancion(cancion_id):
    """Muestra la letra completa de una canción, con opción de transponer."""
    cancion = database.obtener_cancion(cancion_id)
    if cancion is None:
        flash("Esa canción no existe.")
        return redirect(url_for("inicio"))
    semitonos = _leer_semitonos()
    datos = _cancion_transpuesta(cancion, semitonos)
    return render_template("cancion.html", cancion=datos, semitonos=semitonos)


@app.route("/imprimir/<int:cancion_id>")
def imprimir_cancion(cancion_id):
    """Página optimizada para imprimir o guardar como PDF (Ctrl+P)."""
    cancion = database.obtener_cancion(cancion_id)
    if cancion is None:
        flash("Esa canción no existe.")
        return redirect(url_for("inicio"))
    datos = _cancion_transpuesta(cancion, _leer_semitonos())
    return render_template("imprimir.html", cancion=datos)


@app.route("/presentar/<int:cancion_id>")
def presentar_cancion(cancion_id):
    """Modo presentación: letra en grande sobre fondo oscuro."""
    cancion = database.obtener_cancion(cancion_id)
    if cancion is None:
        flash("Esa canción no existe.")
        return redirect(url_for("inicio"))
    datos = _cancion_transpuesta(cancion, _leer_semitonos())
    return render_template("presentar.html", cancion=datos)


@app.route("/repertorio/pdf")
def repertorio_pdf():
    """Página imprimible de toda la lista del evento (repertorio).

    Recibe por la URL los ids en orden y las opciones de estilo/hoja:
      /repertorio/pdf?ids=3,1,7&estilo=clasico&orientacion=horizontal&tamano=letter
    """
    ids_texto = request.args.get("ids", "")
    estilo = request.args.get("estilo", "clasico")
    orientacion = request.args.get("orientacion", "horizontal")
    tamano = request.args.get("tamano", "letter")
    titulo_lista = request.args.get("titulo", "").strip()

    # Mantiene el orden en que vienen los ids.
    ids = [int(x) for x in ids_texto.split(",") if x.strip().isdigit()]
    canciones = [database.obtener_cancion(i) for i in ids]
    canciones = [c for c in canciones if c is not None]

    return render_template(
        "repertorio_pdf.html",
        canciones=canciones,
        estilo=estilo,
        orientacion=orientacion,
        tamano=tamano,
        titulo_lista=titulo_lista,
    )


def _id_youtube(url):
    """Extrae el ID de video de un link de YouTube. Devuelve None si no se reconoce.

    Soporta: youtu.be/ID, watch?v=ID, /embed/ID, /shorts/ID
    """
    if not url:
        return None
    patrones = [
        r"youtu\.be/([\w-]{11})",
        r"[?&]v=([\w-]{11})",
        r"/embed/([\w-]{11})",
        r"/shorts/([\w-]{11})",
    ]
    for p in patrones:
        m = re.search(p, url)
        if m:
            return m.group(1)
    return None


@app.route("/repertorio/youtube")
def repertorio_youtube():
    """Arma la lista de YouTube del repertorio para distribuir a los músicos.

    /repertorio/youtube?ids=3,1&titulo=Sábado...&tel=549...,549...
    """
    ids_texto = request.args.get("ids", "")
    titulo_lista = request.args.get("titulo", "").strip()
    telefonos = request.args.get("tel", "").strip()

    ids = [int(x) for x in ids_texto.split(",") if x.strip().isdigit()]
    canciones = [database.obtener_cancion(i) for i in ids]
    canciones = [c for c in canciones if c is not None]

    # Para cada canción: sus links y los IDs de video extraídos.
    items = []
    todos_los_ids = []
    for c in canciones:
        links = [l.strip() for l in (c["youtube"] or "").splitlines() if l.strip()]
        vid_ids = [vid for vid in (_id_youtube(l) for l in links) if vid]
        todos_los_ids.extend(vid_ids)
        items.append({"titulo": c["titulo"], "links": links, "tiene": bool(links)})

    # Playlist anónima de YouTube que reproduce todos los videos en orden.
    playlist_url = ""
    if todos_los_ids:
        playlist_url = "https://www.youtube.com/watch_videos?video_ids=" + ",".join(todos_los_ids)

    return render_template(
        "repertorio_youtube.html",
        items=items,
        playlist_url=playlist_url,
        titulo_lista=titulo_lista,
        telefonos=telefonos,
    )


@app.route("/proyectar")
def proyectar():
    """Pantalla de control de proyección (operador): lista · párrafos · vista previa."""
    ids_texto = request.args.get("ids", "")
    ids = [int(x) for x in ids_texto.split(",") if x.strip().isdigit()]
    canciones = [database.obtener_cancion(i) for i in ids]
    canciones = [
        {"titulo": c["titulo"], "letra": c["letra"] or ""}
        for c in canciones if c is not None
    ]
    return render_template("proyectar.html", canciones=canciones)


@app.route("/proyeccion")
def proyeccion():
    """Ventana de proyección (pantalla gigante): muestra el párrafo actual."""
    return render_template("proyeccion.html")


@app.route("/nueva", methods=["GET", "POST"])
def nueva_cancion():
    """Formulario para crear una canción nueva."""
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        if not titulo:
            flash("El título es obligatorio.")
            return render_template("form.html", cancion=request.form, accion="nueva")

        nuevo_id = database.crear_cancion(
            titulo,
            request.form.get("artista", "").strip(),
            request.form.get("tono", "").strip(),
            request.form.get("etiquetas", "").strip(),
            request.form.get("letra", ""),
            request.form.get("categoria", "").strip(),
            request.form.get("youtube", "").strip(),
        )
        flash("Canción guardada.")
        return redirect(url_for("ver_cancion", cancion_id=nuevo_id))

    # GET: formulario vacío.
    return render_template(
        "form.html", cancion={}, accion="nueva",
        categorias=database.CATEGORIAS_SUGERIDAS,
    )


@app.route("/editar/<int:cancion_id>", methods=["GET", "POST"])
def editar_cancion(cancion_id):
    """Formulario para modificar una canción existente."""
    cancion = database.obtener_cancion(cancion_id)
    if cancion is None:
        flash("Esa canción no existe.")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        if not titulo:
            flash("El título es obligatorio.")
            return render_template("form.html", cancion=request.form, accion="editar")

        database.actualizar_cancion(
            cancion_id,
            titulo,
            request.form.get("artista", "").strip(),
            request.form.get("tono", "").strip(),
            request.form.get("etiquetas", "").strip(),
            request.form.get("letra", ""),
            request.form.get("categoria", "").strip(),
            request.form.get("youtube", "").strip(),
        )
        flash("Cambios guardados.")
        return redirect(url_for("ver_cancion", cancion_id=cancion_id))

    return render_template(
        "form.html", cancion=cancion, accion="editar",
        categorias=database.CATEGORIAS_SUGERIDAS,
    )


@app.route("/editar-acordes/<int:cancion_id>", methods=["GET", "POST"])
def editar_acordes(cancion_id):
    """Editor visual: arrastrar/editar los acordes sobre la letra."""
    cancion = database.obtener_cancion(cancion_id)
    if cancion is None:
        flash("Esa canción no existe.")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        # Solo cambia la letra (con los acordes reposicionados); el resto igual.
        database.actualizar_cancion(
            cancion_id,
            cancion["titulo"],
            cancion["artista"],
            cancion["tono"],
            cancion["etiquetas"],
            request.form.get("letra", ""),
            cancion["categoria"] if "categoria" in cancion.keys() else "",
            cancion["youtube"] if "youtube" in cancion.keys() else "",
        )
        flash("Acordes guardados.")
        return redirect(url_for("ver_cancion", cancion_id=cancion_id))

    return render_template("editor_acordes.html", cancion=cancion)


@app.route("/borrar/<int:cancion_id>", methods=["POST"])
def borrar(cancion_id):
    """Elimina una canción (se llama desde un botón con confirmación)."""
    database.borrar_cancion(cancion_id)
    flash("Canción eliminada.")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    # En tu PC: arranca en modo desarrollo (se recarga sola al editar el código).
    # En el servidor: Render usa gunicorn (ver Procfile), no esta parte.
    puerto = int(os.environ.get("PORT", 5000))
    en_produccion = os.environ.get("RENDER") is not None
    app.run(host="0.0.0.0", port=puerto, debug=not en_produccion)
