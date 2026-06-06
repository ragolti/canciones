// repertorio.js
// ----------------------------------------------------------
// Maneja "La Lista" del evento: agregar canciones, reordenar,
// quitar y vaciar. Se guarda en el navegador (localStorage),
// así no se pierde al cambiar de página.

const REP_KEY = "adoremos_repertorio";

function repCargar() {
    try {
        return JSON.parse(localStorage.getItem(REP_KEY)) || [];
    } catch (e) {
        return [];
    }
}

function repGuardar(lista) {
    localStorage.setItem(REP_KEY, JSON.stringify(lista));
    repRender();
}

function repAgregar(id, titulo, tono) {
    const lista = repCargar();
    if (lista.some(function (c) { return c.id === id; })) {
        repAbrir(); // ya está: solo mostramos el panel
        return;
    }
    lista.push({ id: id, titulo: titulo, tono: tono || "" });
    repGuardar(lista);
    repAbrir();
}

function repQuitar(idx) {
    const lista = repCargar();
    lista.splice(idx, 1);
    repGuardar(lista);
}

function repMover(idx, dir) {
    const lista = repCargar();
    const j = idx + dir;
    if (j < 0 || j >= lista.length) return;
    const tmp = lista[idx];
    lista[idx] = lista[j];
    lista[j] = tmp;
    repGuardar(lista);
}

function repVaciar() {
    if (confirm("¿Vaciar toda la lista del evento?")) {
        repGuardar([]);
    }
}

function escapeHtml(s) {
    const d = document.createElement("div");
    d.textContent = s;
    return d.innerHTML;
}

function repRender() {
    const lista = repCargar();
    const badge = document.getElementById("rep-contador");
    if (badge) badge.textContent = lista.length;

    const cont = document.getElementById("rep-items");
    if (!cont) return;

    if (lista.length === 0) {
        cont.innerHTML =
            '<p class="rep-vacio">Tu lista está vacía.<br>Tocá ➕ en una canción para sumarla.</p>';
        return;
    }

    cont.innerHTML = lista.map(function (c, i) {
        const tono = c.tono
            ? '<span class="rep-tono">' + escapeHtml(c.tono) + "</span>"
            : "";
        return (
            "<li>" +
            '<span class="rep-num">' + (i + 1) + "</span>" +
            tono +
            '<a class="rep-titulo" href="/cancion/' + c.id + '">' +
            escapeHtml(c.titulo) + "</a>" +
            '<span class="rep-acciones">' +
            '<button title="Subir" onclick="repMover(' + i + ',-1)">▲</button>' +
            '<button title="Bajar" onclick="repMover(' + i + ',1)">▼</button>' +
            '<button title="Quitar" onclick="repQuitar(' + i + ')">✕</button>' +
            "</span></li>"
        );
    }).join("");
}

// Devuelve la fecha elegida formateada en español, ej: "Sábado 13 de junio".
// Si no se eligió fecha, devuelve cadena vacía.
function repFechaTexto() {
    const inp = document.getElementById("rep-fecha");
    if (!inp || !inp.value) return "";
    const d = new Date(inp.value + "T00:00:00");
    let txt = d.toLocaleDateString("es-AR", {
        weekday: "long", day: "numeric", month: "long",
    });
    return txt.charAt(0).toUpperCase() + txt.slice(1);
}

function repImprimir() {
    const lista = repCargar();
    if (lista.length === 0) {
        alert("La lista está vacía. Agregá canciones con el botón ➕.");
        return;
    }
    const ids = lista.map(function (c) { return c.id; }).join(",");
    const estilo = (document.getElementById("rep-estilo") || {}).value || "clasico";
    const orientacion = (document.getElementById("rep-orientacion") || {}).value || "horizontal";
    const titulo = repFechaTexto();  // será el nombre del archivo PDF
    const url = "/repertorio/pdf?ids=" + ids +
        "&estilo=" + estilo +
        "&orientacion=" + orientacion +
        "&tamano=letter" +
        (titulo ? "&titulo=" + encodeURIComponent(titulo) : "");
    window.open(url, "_blank");
}

// Guarda la lista actual en el historial (requiere estar logueado).
// Muestra un modal para elegir: Futura (próximo evento) o Histórica (ya fue).
function repGuardarHistorial() {
    const lista = repCargar();
    if (lista.length === 0) {
        alert("La lista está vacía. Agregá canciones con el botón ➕.");
        return;
    }

    // Crear modal de tipo (futura / histórica)
    var modal = document.createElement("div");
    modal.id = "modal-guardar";
    modal.style.cssText =
        "position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:9999;" +
        "display:flex;align-items:center;justify-content:center;";
    modal.innerHTML =
        '<div style="background:#fff;color:#111;border-radius:14px;padding:28px 32px;' +
        'max-width:420px;width:90%;box-shadow:0 8px 40px rgba(0,0,0,.35);font-family:Arial,sans-serif;">' +
        '<h3 style="margin:0 0 8px;font-size:1.2rem;">💾 Guardar lista</h3>' +
        '<p style="margin:0 0 18px;color:#555;font-size:0.92rem;">' +
        '¿Esta lista es para un evento próximo o ya fue realizado?</p>' +
        '<div style="display:flex;gap:10px;margin-bottom:18px;">' +
        '<button id="mg-futura" style="flex:1;padding:12px 8px;border-radius:8px;border:2px solid #1565c0;' +
        'background:#e8f0fe;cursor:pointer;font-size:0.95rem;font-weight:bold;">' +
        '🗓️ Futura<br><span style="font-weight:normal;font-size:0.78rem;">Evento próximo</span></button>' +
        '<button id="mg-hist" style="flex:1;padding:12px 8px;border-radius:8px;border:2px solid #444;' +
        'background:#f5f5f5;cursor:pointer;font-size:0.95rem;font-weight:bold;">' +
        '📅 Histórica<br><span style="font-weight:normal;font-size:0.78rem;">Ya fue realizado</span></button>' +
        '</div>' +
        '<button id="mg-cancel" style="width:100%;padding:8px;border-radius:8px;border:1px solid #ccc;' +
        'background:#fff;cursor:pointer;color:#666;">Cancelar</button>' +
        '</div>';
    document.body.appendChild(modal);

    function cerrarModal() { document.body.removeChild(modal); }

    document.getElementById("mg-cancel").onclick = cerrarModal;

    function guardarConTipo(tipo) {
        cerrarModal();
        var nombre = repFechaTexto();
        if (!nombre) {
            nombre = prompt("Nombre o fecha de la lista (ej: Sábado 13 de junio):", "");
            if (nombre === null) return;
        }
        fetch("/listas/guardar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nombre: nombre || "Lista sin fecha", canciones: lista, tipo: tipo }),
        })
        .then(function (r) { return r.json(); })
        .then(function (d) {
            if (d.ok) {
                window.location = "/historial?tipo=" + tipo;
            } else {
                alert(d.error || "No se pudo guardar la lista.");
            }
        })
        .catch(function () { alert("No se pudo guardar la lista."); });
    }

    document.getElementById("mg-futura").onclick = function () { guardarConTipo("futura"); };
    document.getElementById("mg-hist").onclick   = function () { guardarConTipo("historica"); };
}

// Reemplaza el repertorio actual por el de una lista guardada (desde el historial).
function repCargarLista(canciones) {
    repGuardar(canciones || []);
    repAbrir();
}

// Abre la vista móvil deslizable (cada canción a pantalla completa).
function repMovil() {
    const lista = repCargar();
    if (lista.length === 0) {
        alert("La lista está vacía. Agregá canciones con el botón ➕.");
        return;
    }
    const ids = lista.map(function (c) { return c.id; }).join(",");
    window.open("/repertorio/movil?ids=" + ids, "_blank");
}

// Abre la pantalla de control de proyección con las canciones de la lista.
function repProyectar() {
    const lista = repCargar();
    if (lista.length === 0) {
        alert("La lista está vacía. Agregá canciones con el botón ➕.");
        return;
    }
    const ids = lista.map(function (c) { return c.id; }).join(",");
    window.open("/proyectar?ids=" + ids, "_blank");
}

// Abre la página de playlist de YouTube del repertorio (para los músicos).
function repYouTube() {
    const lista = repCargar();
    if (lista.length === 0) {
        alert("La lista está vacía. Agregá canciones con el botón ➕.");
        return;
    }
    const ids = lista.map(function (c) { return c.id; }).join(",");
    const titulo = repFechaTexto();
    const campo = document.getElementById("rep-telefonos");
    const tel = campo ? campo.value.trim() : "";
    const url = "/repertorio/youtube?ids=" + ids +
        (titulo ? "&titulo=" + encodeURIComponent(titulo) : "") +
        (tel ? "&tel=" + encodeURIComponent(tel) : "");
    window.open(url, "_blank");
}

// Envía la lista por WhatsApp como mensaje de texto (fecha + canciones).
function repWhatsApp() {
    const lista = repCargar();
    if (lista.length === 0) {
        alert("La lista está vacía. Agregá canciones con el botón ➕.");
        return;
    }
    const fecha = repFechaTexto();
    let msg = "🎵 *Lista de adoración*";
    if (fecha) msg += " — " + fecha;
    msg += "\n\n";
    lista.forEach(function (c, i) {
        msg += (i + 1) + ". " + c.titulo + (c.tono ? "  (" + c.tono + ")" : "") + "\n";
    });

    const texto = encodeURIComponent(msg);
    const campo = document.getElementById("rep-telefonos");
    const crudo = (campo ? campo.value : "").trim();

    if (!crudo) {
        // Sin número: abre WhatsApp para elegir el chat.
        window.open("https://wa.me/?text=" + texto, "_blank");
        return;
    }
    // Uno o varios números separados por coma: abre un chat por cada uno.
    crudo.split(",").forEach(function (n) {
        const numero = n.replace(/\D/g, "");  // solo dígitos
        if (numero) window.open("https://wa.me/" + numero + "?text=" + texto, "_blank");
    });
}

function repAbrir() {
    const p = document.getElementById("rep-panel");
    if (p) p.classList.add("abierto");
}

function repToggle() {
    const p = document.getElementById("rep-panel");
    if (p) p.classList.toggle("abierto");
}

// Botón ➕ de cada canción (delegación de eventos).
document.addEventListener("click", function (e) {
    const b = e.target.closest(".btn-agregar");
    if (b) {
        e.preventDefault();
        repAgregar(Number(b.dataset.id), b.dataset.titulo, b.dataset.tono);
    }
});

document.addEventListener("DOMContentLoaded", repRender);
