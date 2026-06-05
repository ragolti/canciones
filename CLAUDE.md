# Proyecto: Administrador de Canciones 🎵

App web local (en español) para administrar canciones con su letra, tono y acordes.

## Stack
- **Python** + **Flask** (servidor web)
- **SQLite** como base de datos (archivo `canciones.db`, se crea solo)
- Plantillas **Jinja2** en `templates/` y estilos en `static/style.css`
- Sin frameworks de frontend: HTML + CSS plano

## Arquitectura / archivos
- `app.py` — rutas Flask y lógica de las páginas. Punto de entrada (`py app.py`).
- `database.py` — todas las operaciones SQLite (crear/listar/leer/editar/borrar).
- `acordes.py` — transposición de acordes (sube/baja semitonos). Solo modifica
  "líneas de acordes" (líneas compuestas únicamente por acordes); entiende
  notación inglesa (C, D, E…) y española (Do, Re, Mi…).
- `templates/`
  - `base.html` — layout común (header, footer, avisos flash).
  - `index.html` — lista + buscador.
  - `cancion.html` — detalle, con transponer / presentar / imprimir.
  - `form.html` — alta y edición (compartido).
  - `imprimir.html` — vista para imprimir o guardar como PDF (Ctrl+P).
  - `presentar.html` — modo presentación (letra grande, fondo oscuro, A+/A−).
- `arrancar.bat` — crea el venv la primera vez, instala deps y lanza la app.

## Modelo de datos (tabla `canciones`)
`id, titulo (obligatorio), artista, tono, etiquetas (texto separado por comas),
letra, creada_en, modificada_en`

## Cómo arrancar
- Fácil: doble clic en `arrancar.bat` → http://127.0.0.1:5000
- Manual: `py app.py` (con el venv `.venv` activado)

## Funciones implementadas
- CRUD de canciones + buscador (título / artista / etiqueta)
- Transposición de acordes en vivo (parámetro `?t=` en semitonos, rango -11..+11)
- Impresión / exportar a PDF (vía diálogo de impresión del navegador)
- Modo presentación con tamaño de letra ajustable

## Convenciones
- **Todo el código y la UI en español** (nombres de variables, comentarios, textos).
- Comentarios pensados para alguien que recién empieza a programar.
- Mantener cero dependencias pesadas: preferir lo que ya trae Python / el navegador.

## Ideas pendientes (futuro)
- Listas / repertorios ordenados de canciones.
- Exportar varias canciones juntas a un solo PDF (cancionero).
- Importar/exportar canciones a archivos de texto.
- **Importar canciones desde un listado de WhatsApp**: el usuario pega el texto
  copiado de un chat/grupo donde publicaron muchas canciones (títulos, a veces
  con autor o con la letra) y la app las agrega en lote, evitando duplicados.
  Probablemente convenga una pantalla "pegar texto" que detecte títulos y, si
  hay letra, la separe; dejar las nuevas como "pendientes de aprobación".
- **Servidor propio (auto-hospedaje) en la sala de equipos del usuario**: correr
  la app en una PC modesta o Raspberry Pi con Linux (Ubuntu Server), detrás del
  router MikroTik CCR2116 (que ya está siempre online y con UPS). Objetivo:
  eliminar el "arranque lento" del plan gratis de Render y no pagar hosting.
  Requiere: abrir puertos 80/443 en el MikroTik, DDNS (el MikroTik lo trae
  gratis) para la IP dinámica, candado HTTPS (Let's Encrypt), PostgreSQL local
  y backups automáticos de la base. La app es muy liviana: con 2–4 GB de RAM y
  un SSD de 30–60 GB sobra. Pendiente: armar el plan paso a paso cuando se
  decida. (Mantenimiento y seguridad pasan a ser responsabilidad del usuario.)
