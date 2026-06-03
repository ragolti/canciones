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
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

import database
import acordes

app = Flask(__name__)
# La clave secreta es necesaria para mostrar mensajes flash (avisos).
# En el servidor (Render) se toma de una variable de entorno; en tu PC usa la de respaldo.
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esto-por-cualquier-texto-secreto")


# ---------- Sesión / usuarios ----------

def usuario_actual():
    """Devuelve los datos del usuario logueado (o None si no hay sesión)."""
    if session.get("usuario_id"):
        return {
            "id": session["usuario_id"],
            "usuario": session.get("usuario"),
            "rol": session.get("rol"),
        }
    return None


def es_admin():
    u = usuario_actual()
    return bool(u and u["rol"] == "admin")


@app.context_processor
def inyectar_usuario():
    """Hace que las plantillas conozcan al usuario logueado y los pendientes."""
    pendientes = database.contar_pendientes() if es_admin() else 0
    return {"usuario_actual": usuario_actual(), "pendientes": pendientes}


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not usuario_actual():
            flash("Necesitás iniciar sesión para hacer eso.")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not es_admin():
            flash("Solo el administrador puede hacer eso.")
            return redirect(url_for("inicio"))
        return f(*args, **kwargs)
    return wrapper

# Crea la tabla la primera vez que se ejecuta.
database.inicializar()

# Carga inicial de las 149 canciones de la "Lista Nueva".
# Se ejecuta si faltan canciones (por ejemplo, la primera vez en Neon, o si
# una carga anterior quedó incompleta). Es idempotente: no duplica.
try:
    import importar_lista_nueva
    _esperadas = len(importar_lista_nueva.CANCIONES)
    if database.contar_canciones() < _esperadas:
        _filas = [
            (titulo, artista, tono, "Lista Nueva", letra.strip(), "Nuevas y últimas", "")
            for (titulo, artista, tono, letra) in importar_lista_nueva.CANCIONES
        ]
        database.crear_varias(_filas)
        print(f"Carga inicial: ahora hay {database.contar_canciones()} canciones.")
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


@app.route("/registro", methods=["GET", "POST"])
def registro():
    """Registro de un usuario nuevo. El primero que se registra queda como admin."""
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        email = request.form.get("email", "").strip()
        clave = request.form.get("clave", "")
        clave2 = request.form.get("clave2", "")

        if not usuario or not clave:
            flash("Usuario y contraseña son obligatorios.")
            return render_template("registro.html", datos=request.form)
        if clave != clave2:
            flash("Las contraseñas no coinciden.")
            return render_template("registro.html", datos=request.form)
        if database.obtener_usuario(usuario):
            flash("Ese nombre de usuario ya existe.")
            return render_template("registro.html", datos=request.form)

        # El primer usuario del sistema es el administrador.
        rol = "admin" if database.contar_usuarios() == 0 else "colaborador"
        nuevo_id = database.crear_usuario(
            usuario, email, generate_password_hash(clave), rol
        )
        session["usuario_id"] = nuevo_id
        session["usuario"] = usuario
        session["rol"] = rol
        flash("¡Cuenta creada! " + ("Sos el administrador." if rol == "admin" else "Bienvenido/a."))
        return redirect(url_for("inicio"))

    return render_template("registro.html", datos={})


@app.route("/login", methods=["GET", "POST"])
def login():
    """Inicio de sesión."""
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "")
        u = database.obtener_usuario(usuario)
        if u and check_password_hash(u["clave_hash"], clave):
            session["usuario_id"] = u["id"]
            session["usuario"] = u["usuario"]
            session["rol"] = u["rol"]
            flash(f"¡Hola, {u['usuario']}!")
            return redirect(url_for("inicio"))
        flash("Usuario o contraseña incorrectos.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Cierra la sesión."""
    session.clear()
    flash("Sesión cerrada.")
    return redirect(url_for("inicio"))


@app.route("/revisar")
@admin_required
def revisar():
    """Panel del administrador: canciones pendientes de aprobación."""
    pendientes = database.listar_pendientes()
    return render_template("revisar.html", pendientes=pendientes)


@app.route("/aprobar/<int:cancion_id>", methods=["POST"])
@admin_required
def aprobar(cancion_id):
    database.cambiar_estado(cancion_id, "aprobada")
    flash("Canción aprobada y publicada.")
    return redirect(url_for("revisar"))


@app.route("/rechazar/<int:cancion_id>", methods=["POST"])
@admin_required
def rechazar(cancion_id):
    database.borrar_cancion(cancion_id)
    flash("Canción rechazada y eliminada.")
    return redirect(url_for("revisar"))


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
@login_required
def nueva_cancion():
    """Formulario para crear una canción nueva."""
    if request.method == "POST":
        titulo = request.form.get("titulo", "").strip()
        if not titulo:
            flash("El título es obligatorio.")
            return render_template("form.html", cancion=request.form, accion="nueva",
                                   categorias=database.CATEGORIAS_SUGERIDAS)

        # Admin: se publica directo. Colaborador: queda pendiente de aprobación.
        estado = "aprobada" if es_admin() else "pendiente"
        nuevo_id = database.crear_cancion(
            titulo,
            request.form.get("artista", "").strip(),
            request.form.get("tono", "").strip(),
            request.form.get("etiquetas", "").strip(),
            request.form.get("letra", ""),
            request.form.get("categoria", "").strip(),
            request.form.get("youtube", "").strip(),
            estado,
        )
        if estado == "pendiente":
            flash("¡Gracias! Tu canción quedó pendiente de aprobación por el administrador.")
            return redirect(url_for("inicio"))
        flash("Canción guardada y publicada.")
        return redirect(url_for("ver_cancion", cancion_id=nuevo_id))

    # GET: formulario vacío.
    return render_template(
        "form.html", cancion={}, accion="nueva",
        categorias=database.CATEGORIAS_SUGERIDAS,
    )


@app.route("/editar/<int:cancion_id>", methods=["GET", "POST"])
@login_required
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
            return render_template("form.html", cancion=request.form, accion="editar",
                                   categorias=database.CATEGORIAS_SUGERIDAS)

        # Admin: el cambio se publica. Colaborador: la canción pasa a pendiente.
        estado = "aprobada" if es_admin() else "pendiente"
        database.actualizar_cancion(
            cancion_id,
            titulo,
            request.form.get("artista", "").strip(),
            request.form.get("tono", "").strip(),
            request.form.get("etiquetas", "").strip(),
            request.form.get("letra", ""),
            request.form.get("categoria", "").strip(),
            request.form.get("youtube", "").strip(),
            estado,
        )
        if estado == "pendiente":
            flash("Tu edición quedó pendiente de aprobación por el administrador.")
            return redirect(url_for("inicio"))
        flash("Cambios guardados.")
        return redirect(url_for("ver_cancion", cancion_id=cancion_id))

    return render_template(
        "form.html", cancion=cancion, accion="editar",
        categorias=database.CATEGORIAS_SUGERIDAS,
    )


@app.route("/editar-acordes/<int:cancion_id>", methods=["GET", "POST"])
@login_required
def editar_acordes(cancion_id):
    """Editor visual: arrastrar/editar los acordes sobre la letra."""
    cancion = database.obtener_cancion(cancion_id)
    if cancion is None:
        flash("Esa canción no existe.")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        estado = "aprobada" if es_admin() else "pendiente"
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
            estado,
        )
        if estado == "pendiente":
            flash("Tu edición de acordes quedó pendiente de aprobación.")
            return redirect(url_for("inicio"))
        flash("Acordes guardados.")
        return redirect(url_for("ver_cancion", cancion_id=cancion_id))

    return render_template("editor_acordes.html", cancion=cancion)


@app.route("/borrar/<int:cancion_id>", methods=["POST"])
@admin_required
def borrar(cancion_id):
    """Elimina una canción (solo el administrador)."""
    database.borrar_cancion(cancion_id)
    flash("Canción eliminada.")
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    # En tu PC: arranca en modo desarrollo (se recarga sola al editar el código).
    # En el servidor: Render usa gunicorn (ver Procfile), no esta parte.
    puerto = int(os.environ.get("PORT", 5000))
    en_produccion = os.environ.get("RENDER") is not None
    app.run(host="0.0.0.0", port=puerto, debug=not en_produccion)
