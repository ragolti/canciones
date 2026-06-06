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
import json
import html as _html
import urllib.request
from functools import wraps
from datetime import timedelta

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session, abort
)
from werkzeug.security import generate_password_hash, check_password_hash

import database
import acordes
from markupsafe import Markup, escape as _escape

app = Flask(__name__)
# La clave secreta es necesaria para mostrar mensajes flash (avisos).
# En el servidor (Render) se toma de una variable de entorno; en tu PC usa la de respaldo.
app.secret_key = os.environ.get("SECRET_KEY", "cambia-esto-por-cualquier-texto-secreto")
# Mantener la sesión iniciada por 60 días (dispositivos de confianza): así, una vez
# que iniciás sesión, no te vuelve a pedir la contraseña aunque cierres el navegador.
app.permanent_session_lifetime = timedelta(days=60)


# ── Filtros Jinja2 para renderizar letras con acordes en color ──────────────

@app.template_filter("es_linea_acorde")
def filtro_es_linea_acorde(linea):
    """True si la línea contiene solo acordes (para colorearla en las plantillas)."""
    return _es_linea_acorde_ext(linea.strip())


# Separadores típicos entre acordes que no son acordes en sí mismos.
_SEPARADORES_ACORDE = {"-", "–", "—", "|", "//", "////", "...", "…", "+", "(", ")", "x2", "x3", "x4"}


def _es_linea_acorde_ext(linea):
    """Como _es_linea_de_acordes pero también permite guiones y separadores comunes.

    Por ejemplo: 'E - Cm7 - B - A' se considera línea de acordes aunque tenga '-'.
    """
    tokens = linea.split()
    if not tokens:
        return False
    return all(acordes.RE_ACORDE.match(t) or t in _SEPARADORES_ACORDE for t in tokens)


@app.template_filter("letra_html")
def filtro_letra_html(texto):
    """Convierte la letra (texto plano) a HTML con acordes en color.

    Cada línea se envuelve en un <span> con clase:
      .ln-acorde   → línea de acordes (color naranja/rojo)
      .ln-seccion  → indicación de sección como (Coro), [Estrofa], etc.
      .ln-letra    → línea de letra normal
      .ln-vacio    → línea en blanco (espacio entre estrofas)
    """
    if not texto:
        return Markup("")
    partes = []
    for linea in texto.splitlines():
        stripped = linea.strip()
        if not stripped:
            partes.append('<span class="ln-vacio"></span>')
        elif _es_linea_acorde_ext(stripped):
            partes.append(f'<span class="ln-acorde">{_escape(linea)}</span>')
        elif (stripped.startswith("(") and stripped.endswith(")")) or \
             (stripped.startswith("[") and stripped.endswith("]")):
            partes.append(f'<span class="ln-seccion">{_escape(linea)}</span>')
        else:
            partes.append(f'<span class="ln-letra">{_escape(linea)}</span>')
    return Markup("\n".join(partes))


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
            (titulo, artista, tono, "Lista Nueva", letra.strip(), "Nuevas", "")
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
    f_grupo = request.args.get("grupo", "").strip()
    f_funcion = request.args.get("funcion", "").strip()
    f_tempo = request.args.get("tempo", "").strip()
    f_conocidas = request.args.get("conocidas", "").strip()  # "" | "si" | "no"

    canciones = database.listar_canciones(busqueda)
    # Filtros por desplegable (estilo/grupo, función, tempo).
    if f_grupo:
        canciones = [c for c in canciones if (c["categoria"] or "Sin categoría") == f_grupo]
    if f_funcion:
        canciones = [c for c in canciones if (c["funcion"] or "") == f_funcion]
    if f_tempo:
        canciones = [c for c in canciones if (c["tempo"] or "") == f_tempo]

    # Conjunto de canciones que el usuario marcó como "conocidas" (ya las tocó).
    u = usuario_actual()
    conocidas = database.ids_conocidas(u["id"]) if u else set()
    if u and f_conocidas == "si":
        canciones = [c for c in canciones if c["id"] in conocidas]
    elif u and f_conocidas == "no":
        canciones = [c for c in canciones if c["id"] not in conocidas]

    grupos = database.agrupar_por_categoria(canciones)
    return render_template(
        "index.html",
        grupos=grupos,
        canciones=canciones,   # lista plana alfabética para el índice
        total=len(canciones),
        busqueda=busqueda,
        funciones=database.FUNCIONES,
        estilos=database.CATEGORIAS_SUGERIDAS,
        tempos=database.TEMPOS,
        f_grupo=f_grupo, f_funcion=f_funcion, f_tempo=f_tempo,
        conocidas=conocidas, f_conocidas=f_conocidas,
        total_conocidas=database.contar_conocidas(u["id"]) if u else 0,
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
    apariciones = database.fechas_apariciones(cancion_id)
    return render_template("cancion.html", cancion=datos, semitonos=semitonos,
                           apariciones=apariciones)


@app.route("/ocultar/<int:cancion_id>", methods=["POST"])
@login_required
def ocultar_cancion(cancion_id):
    """Oculta una canción (no se ve en público). Admin o quien tenga permiso."""
    if not es_admin():
        flash("Solo el administrador puede ocultar canciones.")
        return redirect(url_for("ver_cancion", cancion_id=cancion_id))
    database.cambiar_estado(cancion_id, "oculta")
    flash("Canción ocultada (ya no se ve en público).")
    return redirect(url_for("ver_cancion", cancion_id=cancion_id))


@app.route("/mostrar/<int:cancion_id>", methods=["POST"])
@admin_required
def mostrar_cancion(cancion_id):
    """Vuelve a mostrar una canción oculta."""
    database.cambiar_estado(cancion_id, "aprobada")
    flash("Canción visible nuevamente.")
    return redirect(url_for("ver_cancion", cancion_id=cancion_id))


@app.route("/lista/<int:lista_id>")
def ver_lista(lista_id):
    """Ver una lista guardada por su número (para compartir: 'la lista 223')."""
    lista = database.obtener_lista(lista_id)
    if lista is None:
        flash("No existe una lista con ese número.")
        return redirect(url_for("historial"))
    import json as _json
    try:
        canciones = _json.loads(lista["canciones_json"] or "[]")
    except Exception:
        canciones = []
    return render_template("ver_lista.html", lista=lista, canciones=canciones)


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
        session.permanent = True   # sesión recordada (60 días)
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
            session.permanent = True   # sesión recordada (60 días)
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


@app.route("/enriquecer", methods=["POST"])
def enriquecer():
    """Completa datos de una canción (autor, año, links). Protegido con token.

    Se usa para la carga automática de datos. Requiere la variable de entorno
    ENRICH_TOKEN y que coincida con el header 'X-Token'.
    """
    token = os.environ.get("ENRICH_TOKEN", "")
    if not token or request.headers.get("X-Token", "") != token:
        return {"ok": False, "error": "Token inválido"}, 403
    datos = request.get_json(silent=True) or {}
    cid = datos.get("id")
    if not cid:
        return {"ok": False, "error": "Falta id"}, 400
    database.enriquecer(
        int(cid),
        artista=datos.get("artista"),
        anio=datos.get("anio"),
        links=datos.get("links") or [],
    )
    return {"ok": True}


@app.route("/clasificar/<int:cancion_id>", methods=["POST"])
@login_required
def clasificar(cancion_id):
    """Botones rápidos de clasificación (función / estilo / tempo) desde la lista."""
    datos = request.get_json(silent=True) or {}
    campo = datos.get("campo") or request.form.get("campo", "")
    valor = datos.get("valor")
    if valor is None:
        valor = request.form.get("valor", "")
    ok = database.clasificar(cancion_id, campo, valor)
    return {"ok": bool(ok)}


@app.route("/conocida/<int:cancion_id>", methods=["POST"])
@login_required
def conocida_toggle(cancion_id):
    """Marca/desmarca una canción como 'conocida' por el usuario actual."""
    u = usuario_actual()
    conocida = database.alternar_conocida(u["id"], cancion_id)
    return {"ok": True, "conocida": conocida}


@app.route("/conocidas/marcar-todas", methods=["POST"])
@login_required
def marcar_todas_conocidas_ruta():
    """Marca como conocidas TODAS las canciones visibles, para el usuario actual."""
    u = usuario_actual()
    canciones = database.listar_canciones(solo_aprobadas=True)
    total = database.marcar_todas_conocidas(u["id"], [c["id"] for c in canciones])
    flash(f"Marqué {total} canción(es) como conocidas para vos.")
    return redirect(url_for("inicio"))


@app.route("/conocidas/quitar-todas", methods=["POST"])
@login_required
def quitar_todas_conocidas_ruta():
    """Quita TODAS las marcas de 'conocida' del usuario actual."""
    u = usuario_actual()
    database.quitar_todas_conocidas(u["id"])
    flash("Quité todas tus marcas de canciones conocidas.")
    return redirect(url_for("inicio"))


@app.route("/importar/lote", methods=["POST"])
def importar_lote():
    """Crea muchas canciones y listas de una vez. Protegido con token.

    Body JSON:
      {
        "canciones": [{"titulo","artista","tono","letra","categoria","etiquetas","youtube"}],
        "listas":    [{"nombre","fecha","usuario","titulos":[...]}]
      }
    Las canciones se insertan sin duplicar (por título). Cada lista guarda sus
    canciones mapeando el título a la canción existente (si la encuentra).
    """
    token = os.environ.get("ENRICH_TOKEN", "")
    if not token or request.headers.get("X-Token", "") != token:
        return {"ok": False, "error": "Token inválido"}, 403
    datos = request.get_json(silent=True) or {}
    canciones = datos.get("canciones") or []
    listas = datos.get("listas") or []

    # 1) Crear canciones (sin duplicar por título).
    filas = [
        (
            c.get("titulo", "").strip(),
            c.get("artista", "") or "",
            c.get("tono", "") or "",
            c.get("etiquetas", "") or "",
            c.get("letra", "") or "",
            c.get("categoria", "Nuevas") or "Nuevas",
            c.get("youtube", "") or "",
        )
        for c in canciones if c.get("titulo", "").strip()
    ]
    if filas:
        database.crear_varias(filas)

    # 2) Recrear listas (mapeando títulos a las canciones ya cargadas).
    todas = database.listar_canciones(solo_aprobadas=False)
    por_titulo = {database.sin_acentos(c["titulo"]): c for c in todas}
    creadas = []
    for L in listas:
        items = []
        for tt in L.get("titulos", []):
            row = por_titulo.get(database.sin_acentos(tt))
            items.append({
                "id": row["id"] if row else None,
                "titulo": row["titulo"] if row else tt,
                "tono": (row["tono"] if row else "") or "",
            })
        if not items:
            continue
        nombre = (L.get("nombre") or "").strip() or f"Lista {L.get('fecha', '')}".strip()
        usuario = (L.get("usuario") or "Ríos de (WhatsApp)").strip()
        database.crear_lista(nombre, usuario, None, json.dumps(items, ensure_ascii=False))
        creadas.append(nombre)

    return {
        "ok": True,
        "canciones_total": database.contar_canciones(),
        "listas_creadas": creadas,
    }


@app.route("/admin/listar", methods=["POST"])
def admin_listar():
    """Devuelve todas las canciones (id, título, autor, largo de letra). Token."""
    token = os.environ.get("ENRICH_TOKEN", "")
    if not token or request.headers.get("X-Token", "") != token:
        return {"ok": False, "error": "Token inválido"}, 403
    filas = database.listar_canciones(solo_aprobadas=False)
    return {
        "ok": True,
        "canciones": [
            {
                "id": c["id"],
                "titulo": c["titulo"],
                "artista": c["artista"] or "",
                "letra_len": len(c["letra"] or ""),
            }
            for c in filas
        ],
    }


@app.route("/admin/borrar", methods=["POST"])
def admin_borrar():
    """Borra canciones por id (lista). Token. Usado para quitar duplicados."""
    token = os.environ.get("ENRICH_TOKEN", "")
    if not token or request.headers.get("X-Token", "") != token:
        return {"ok": False, "error": "Token inválido"}, 403
    ids = (request.get_json(silent=True) or {}).get("ids") or []
    borradas = []
    for i in ids:
        try:
            database.borrar_cancion(int(i))
            borradas.append(int(i))
        except Exception:
            pass
    return {"ok": True, "borradas": borradas, "total": database.contar_canciones()}


@app.route("/completar", methods=["POST"])
def completar():
    """Actualiza letra/tono/autor/año de una canción existente. Protegido con token.

    Body JSON: {"titulo" o "id", "letra", "tono", "artista", "anio"}.
    Se usa para reconstruir las letras con acordes traídas de la web.
    """
    token = os.environ.get("ENRICH_TOKEN", "")
    if not token or request.headers.get("X-Token", "") != token:
        return {"ok": False, "error": "Token inválido"}, 403
    datos = request.get_json(silent=True) or {}
    cid = datos.get("id")
    if not cid and datos.get("titulo"):
        objetivo = database.sin_acentos(datos["titulo"])
        for c in database.listar_canciones(solo_aprobadas=False):
            if database.sin_acentos(c["titulo"]) == objetivo:
                cid = c["id"]
                break
    if not cid:
        return {"ok": False, "error": "Canción no encontrada"}, 404
    c = database.obtener_cancion(int(cid))
    if not c:
        return {"ok": False, "error": "Canción no encontrada"}, 404

    def elegir(nuevo, viejo):
        return nuevo if (nuevo is not None and str(nuevo).strip() != "") else viejo

    # Etiquetas: si llega "etiqueta_extra", se agrega a las existentes (sin repetir).
    etiquetas = c["etiquetas"] or ""
    extra = (datos.get("etiqueta_extra") or "").strip()
    if extra:
        actuales = [e.strip() for e in etiquetas.split(",") if e.strip()]
        if database.sin_acentos(extra) not in [database.sin_acentos(e) for e in actuales]:
            actuales.append(extra)
        etiquetas = ", ".join(actuales)

    anio_actual = c["anio"] if "anio" in c.keys() else ""
    database.actualizar_cancion(
        int(cid),
        c["titulo"],
        elegir(datos.get("artista"), c["artista"]),
        elegir(datos.get("tono"), c["tono"]),
        etiquetas,
        elegir(datos.get("letra"), c["letra"]),
        c["categoria"] if "categoria" in c.keys() else "",
        c["youtube"] if "youtube" in c.keys() else "",
        anio=elegir(datos.get("anio"), anio_actual),
    )
    return {"ok": True, "id": int(cid), "titulo": c["titulo"]}


@app.route("/conocidas/seed", methods=["POST"])
def conocidas_seed():
    """Marca todas las canciones como conocidas para un usuario dado. Protegido con token.

    Sirve para la carga inicial (marcar de una vez las que ya existen). Body JSON:
    {"usuario": "Ruben"}. Si no se pasa usuario (o no existe), devuelve la lista
    de usuarios disponibles para elegir bien.
    """
    token = os.environ.get("ENRICH_TOKEN", "")
    if not token or request.headers.get("X-Token", "") != token:
        return {"ok": False, "error": "Token inválido"}, 403
    datos = request.get_json(silent=True) or {}
    nombre = (datos.get("usuario") or "").strip()
    usuarios = [u["usuario"] for u in database.listar_usuarios()]
    if not nombre:
        return {"ok": False, "error": "Falta 'usuario'", "usuarios": usuarios}, 400
    u = database.obtener_usuario(nombre)
    if not u:
        return {"ok": False, "error": "Usuario no encontrado", "usuarios": usuarios}, 404
    canciones = database.listar_canciones(solo_aprobadas=True)
    total = database.marcar_todas_conocidas(u["id"], [c["id"] for c in canciones])
    return {"ok": True, "usuario": nombre, "conocidas": total}


@app.route("/youtube/<int:cancion_id>", methods=["POST"])
@login_required
def youtube_rapido(cancion_id):
    """Agrega un link de YouTube a una canción desde el listado (rápido)."""
    datos = request.get_json(silent=True) or {}
    link = (datos.get("link") or "").strip()
    if not link:
        return {"ok": False, "error": "El link está vacío."}, 400
    total = database.agregar_youtube(cancion_id, link)
    return {"ok": True, "total": total}


@app.route("/listas/guardar", methods=["POST"])
@login_required
def guardar_lista():
    """Guarda la lista actual del repertorio en el historial (del usuario)."""
    datos = request.get_json(silent=True) or {}
    nombre = (datos.get("nombre") or "").strip() or "Lista sin fecha"
    canciones = datos.get("canciones") or []
    if not canciones:
        return {"ok": False, "error": "La lista está vacía."}, 400

    u = usuario_actual()
    nuevo_id = database.crear_lista(
        nombre, u["usuario"], u["id"], json.dumps(canciones, ensure_ascii=False)
    )
    return {"ok": True, "id": nuevo_id}


@app.route("/sugerencias")
@login_required
def sugerencias():
    """Sugiere canciones que hace tiempo no se cantan (según tus listas)."""
    estilo = request.args.get("estilo", "").strip()
    u = usuario_actual()
    sugeridas = database.sugerencias(u["usuario"], estilo or None, 10)
    return render_template(
        "sugerencias.html",
        sugeridas=sugeridas,
        estilo=estilo,
        estilos=database.CATEGORIAS_SUGERIDAS,
    )


@app.route("/historial")
def historial():
    """Historial de listas guardadas, con filtro por usuario y favoritas."""
    filtro_usuario = request.args.get("usuario", "").strip()
    solo_fav = request.args.get("fav") == "1"
    listas = database.listar_listas(
        usuario=filtro_usuario or None, solo_favoritas=solo_fav
    )
    # Parsear las canciones de cada lista para mostrarlas.
    listas_datos = []
    for l in listas:
        d = dict(l)
        try:
            d["canciones"] = json.loads(l["canciones_json"] or "[]")
        except Exception:
            d["canciones"] = []
        listas_datos.append(d)

    return render_template(
        "historial.html",
        listas=listas_datos,
        usuarios=database.usuarios_de_listas(),
        filtro_usuario=filtro_usuario,
        solo_fav=solo_fav,
    )


@app.route("/listas/<int:lista_id>/favorita", methods=["POST"])
@login_required
def favorita_lista(lista_id):
    lista = database.obtener_lista(lista_id)
    if lista:
        database.cambiar_favorita(lista_id, not lista["favorita"])
    return redirect(request.referrer or url_for("historial"))


@app.route("/listas/<int:lista_id>/borrar", methods=["POST"])
@login_required
def borrar_lista_ruta(lista_id):
    lista = database.obtener_lista(lista_id)
    u = usuario_actual()
    # La puede borrar quien la creó o el administrador.
    if lista and (lista["usuario_id"] == u["id"] or es_admin()):
        database.borrar_lista(lista_id)
        flash("Lista eliminada.")
    else:
        flash("No podés borrar esa lista.")
    return redirect(url_for("historial"))


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
        items.append({"id": c["id"], "titulo": c["titulo"], "links": links, "tiene": bool(links)})

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


@app.route("/repertorio/movil")
def repertorio_movil():
    """Vista móvil: cada canción a pantalla completa, se pasa deslizando el dedo."""
    ids_texto = request.args.get("ids", "")
    ids = [int(x) for x in ids_texto.split(",") if x.strip().isdigit()]
    canciones = [database.obtener_cancion(i) for i in ids]
    canciones = [c for c in canciones if c is not None]
    return render_template("movil.html", canciones=canciones)


def _texto_de_web(url):
    """Descarga una página y extrae (titulo, texto) en texto plano. Best-effort."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", "ignore")
    titulo = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
    if m:
        titulo = re.sub(r"\s+", " ", _html.unescape(m.group(1))).strip()
    # Saca scripts/estilos, convierte saltos, quita etiquetas.
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.I | re.S)
    html = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    html = re.sub(r"</p>", "\n\n", html, flags=re.I)
    texto = _html.unescape(re.sub(r"<[^>]+>", "", html))
    texto = re.sub(r"[ \t]+\n", "\n", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto).strip()
    return titulo, texto


@app.route("/importar")
@login_required
def importar():
    """Página para importar canciones desde una web o un PDF."""
    return render_template("importar.html")


@app.route("/importar/web", methods=["POST"])
@login_required
def importar_web():
    """Trae el texto de una página y precarga el formulario de nueva canción."""
    url = request.form.get("url", "").strip()
    if not url:
        flash("Pegá la dirección (URL) de la página.")
        return redirect(url_for("importar"))
    try:
        titulo, texto = _texto_de_web(url)
    except Exception as e:
        flash(f"No se pudo leer esa página: {e}")
        return redirect(url_for("importar"))
    flash("Revisá y ajustá el texto antes de guardar.")
    return render_template(
        "form.html", accion="nueva", categorias=database.CATEGORIAS_SUGERIDAS,
        cancion={"titulo": titulo, "letra": texto},
    )


@app.route("/importar/pdf", methods=["POST"])
@login_required
def importar_pdf():
    """Sube un PDF y crea una canción por página (texto extraído)."""
    archivo = request.files.get("pdf")
    if not archivo or not archivo.filename.lower().endswith(".pdf"):
        flash("Subí un archivo PDF.")
        return redirect(url_for("importar"))
    try:
        from pypdf import PdfReader
        lector = PdfReader(archivo.stream)
    except Exception as e:
        flash(f"No se pudo leer el PDF: {e}")
        return redirect(url_for("importar"))

    estado = "aprobada" if es_admin() else "pendiente"
    creadas = 0
    for pagina in lector.pages:
        texto = (pagina.extract_text() or "").strip()
        if not texto:
            continue
        lineas = [l for l in texto.splitlines() if l.strip()]
        titulo = lineas[0].strip() if lineas else "Sin título"
        letra = "\n".join(lineas[1:]).strip()
        database.crear_cancion(titulo, "", "", "Importada PDF", letra, "Nuevas", "", estado)
        creadas += 1

    if estado == "pendiente":
        flash(f"Se importaron {creadas} canciones (quedaron pendientes de aprobación).")
    else:
        flash(f"Se importaron {creadas} canciones.")
    return redirect(url_for("inicio"))


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
            request.form.get("anio", "").strip(),
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
