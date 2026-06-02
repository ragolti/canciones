# 🎵 Mis Canciones

Aplicación web local para administrar canciones con su **título, artista, tono/acordes, etiquetas y letra completa**.

Hecha con Python + Flask. Los datos se guardan en una base SQLite (`canciones.db`) en esta misma carpeta.

---

## ▶️ Cómo usarla (modo fácil)

1. Hacé **doble clic en `arrancar.bat`**.
   - La primera vez tarda un poco porque crea el entorno e instala Flask.
2. Abrí el navegador en: **http://127.0.0.1:5000**
3. Para cerrarla: cerrá la ventana negra o presioná `Ctrl + C` en ella.

---

## ▶️ Cómo usarla (desde la terminal)

```bat
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
py app.py
```

Luego abrí http://127.0.0.1:5000

---

## ✨ Qué se puede hacer

- ➕ Agregar canciones nuevas
- ✏️ Editar canciones existentes
- 🗑️ Borrar canciones (con confirmación)
- 🔍 Buscar por título, artista o etiqueta
- 📄 Ver la letra completa con su tono y acordes

---

## 📁 Archivos del proyecto

| Archivo            | Para qué sirve                                       |
|--------------------|------------------------------------------------------|
| `app.py`           | La aplicación web (las páginas y su lógica).         |
| `database.py`      | Guardar/leer canciones en la base de datos.          |
| `templates/`       | El HTML de cada página.                              |
| `static/style.css` | Los colores y el diseño visual.                      |
| `canciones.db`     | La base de datos (se crea sola). **Acá están tus canciones.** |
| `arrancar.bat`     | Arranca todo con doble clic.                         |
| `requirements.txt` | Lista de lo que hay que instalar (Flask).            |

> 💾 **Copia de seguridad:** para respaldar tus canciones, copiá el archivo `canciones.db`.

---

## 🛠️ Ideas para ampliar más adelante

- Exportar una canción a PDF para imprimir.
- Transponer acordes (subir/bajar de tono).
- Armar listas o repertorios.
- Modo presentación (letra grande en pantalla).
