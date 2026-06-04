# 📝 Pendientes para la página "Adoremos"

> ✅ ESTADO ITEMS 17–34 (lote completado):
> - 17 ✅ link YouTube rápido · 18 ✅ buscar en YouTube (título/estribillo)
> - 19 ✅ botón guardar lista (existe en el panel) · 20 ✅ completar/fijar links faltantes
> - 21 ✅ búsqueda de links (semi-automática: botones "Buscar"; auto total requiere API de YouTube)
> - 22 ✅ historial con fecha (mejora menor: repeticiones quedan visibles por fecha)
> - 23 ✅ contador de apariciones por tema · 24 ✅ importar de web · 25 ✅ importar de PDF
> - 26 ✅ playlist: fijar links + WhatsApp · 27 ✅ "+ Nueva": importar de internet/PDF
> - 28 ✅ cambiar de grupo (botones de Estilo del item 16, al lado del +)
> - 29 ✅ filtros por grupo/función/tempo · 30 ✅ modo móvil deslizable
> - 31 ✅ compartir lista por número · 32 ✅ búsqueda con y sin acentos
> - 33 ✅ borrar solo admin · 34 ✅ ocultar canciones + cuentas con permisos


Lista de mejoras a implementar más adelante. Se va completando a medida que surjan ideas.

---

## 1. Agrupar las canciones por categorías / grupos de alabanza
**Estado:** ✅ COMPLETADO

Implementado: campo `categoria` en la base, selector con sugerencias en el formulario
(Coros clásicos, Clásicas Pop, Contemporáneas, Nuevas y últimas + se pueden crear nuevas),
y la página principal muestra las canciones agrupadas en secciones desplegables (acordeón).
Las 149 importadas quedaron en "Nuevas y últimas".

Poder organizar las canciones en grupos para separarlas y desplegarlas, por ejemplo:
- **Coros clásicos**
- **Clásicas Pop**
- **Contemporáneas**
- **Nuevas y últimas**
- (y las categorías que se quieran agregar)

**Idea de funcionamiento:**
- En la lista principal, mostrar las canciones agrupadas por categoría.
- Que cada grupo se pueda **desplegar/contraer** (acordeón) para verlas u ocultarlas.
- Cada canción pertenece a una categoría (se elige al crear/editar).

**Notas técnicas (para cuando se haga):**
- Agregar un campo `categoria` a la tabla `canciones` (o reutilizar el campo `etiquetas`).
- Actualizar el formulario de alta/edición con un selector de categoría.
- Modificar `index.html` para mostrar las canciones agrupadas y plegables.

---

## 2. Índice desplegable con buscador avanzado
**Estado:** ✅ COMPLETADO

Implementado: botón "📑 Índice de canciones" que despliega un listado alfabético completo
(en 2 columnas) con un filtro instantáneo (sin recargar) por título o artista, y links
directos a cada canción. El buscador principal ya busca por título, artista, etiqueta,
categoría y dentro de la letra.

- Un **botón** que despliegue un índice de todas las canciones.
- Poder **buscar** por:
  - Nombre / título del tema
  - Un pedazo de la **letra**
  - **Autor / artista**
  - (y demás campos: tono, categoría, etc.)

**Notas técnicas:**
- Buscador que filtre también dentro del campo `letra`.
- Panel/índice plegable (mostrar/ocultar con un botón).

---

## 3. Armar lista para un evento (repertorio)
**Estado:** ✅ COMPLETADO

Implementado: botón ➕ en cada canción para sumarla a "La Lista del evento". Panel lateral
deslizable (botón flotante "🎵 Lista (n)") con las canciones numeradas, el tono en una insignia
adelante, y botones para subir ▲ / bajar ▼ / quitar ✕ cada una, más "Vaciar lista".
Se guarda en el navegador (localStorage), persiste al navegar entre páginas.

- Al hacer **clic** en una canción, que se agregue a una **lista a la derecha** (tipo carrito/repertorio).
- En esa lista:
  - Las canciones aparecen **enumeradas** (1, 2, 3…).
  - Se pueden **mover arriba/abajo** para cambiar el orden.
  - Se pueden **eliminar** de la lista.
- Mostrar el **acorde principal (tono)** adelante del nombre del tema o a la derecha — donde quede más visible y entendible.

**Notas técnicas:**
- Panel lateral con la lista (probablemente con JavaScript en el navegador).
- Reordenar (drag o botones ↑↓) y quitar items.

---

## 4. Generar PDF del repertorio con estilos a elegir
**Estado:** ✅ COMPLETADO

Implementado: botón "📄 PDF / Imprimir" en el panel de la lista. Genera una página con
todas las canciones del repertorio en orden (una por hoja, letra en 2 columnas con acordes).
Selector de estilo: Clásico (blanco), Dark (oscuro) y Antiguo (sepia).

- Que la lista armada (item 3) pueda **generar un PDF** cuando se necesite.
- Poder elegir entre **3 o más modelos/estilos** para descargar:
  - **Clásico**
  - **Dark** (fondo oscuro)
  - **Antiguo**
  - (y los que se quieran sumar)

---

## 5. Opciones de página al exportar el PDF
**Estado:** ✅ COMPLETADO

Implementado: selector de hoja en el panel con orientación Horizontal/Vertical.
Predeterminado **Carta (Letter) Horizontal**. La hoja se aplica vía CSS @page.

- Elegir orientación: **vertical u horizontal**.
- Elegir tamaño de hoja.
- **Predeterminado: hoja Carta (Letter) en Horizontal**, para que ocupe toda la pantalla de una notebook o tablet que se use como **pizarra del evento**.

---

## 6. Editar y mover acordes dentro de la letra (modo Edición)
**Estado:** ✅ COMPLETADO

Implementado: página "🎸 Editar acordes" (botón en el detalle de la canción). Las líneas de
acordes se muestran como pastillas arrastrables sobre la letra (monoespaciada). Se pueden
ARRASTRAR con el mouse a izquierda/derecha para alinearlas con la sílaba, editar/borrar con
doble clic, y agregar nuevos con "+ acorde". Al guardar, reconstruye la letra con los acordes
en su nueva posición. (Nota: maneja líneas de acordes solos; los acordes inline dentro de la
letra se siguen editando con el ✏️ Editar normal.)

- En modo **Edición**, poder **cambiar/editar** los acordes que figuran sobre la letra.
- Poder **arrastrar el acorde con el mouse** hacia la izquierda o derecha, para ubicarlo justo en la sílaba/momento exacto de la letra donde cambia.

**Notas técnicas (es el más complejo):**
- Requiere un editor interactivo de acordes (posición carácter por carácter).
- Pensar cómo se guarda la posición exacta de cada acorde sobre la letra.

---

## 7. Cerrar lista con fecha, nombrar el archivo y enviar por WhatsApp
**Estado:** ✅ COMPLETADO

Implementado en el panel de la lista: campo de **fecha** (se formatea en español, ej. "Sábado
13 de junio") que se usa como **nombre del PDF**, campo de **teléfono(s)** WhatsApp (uno o varios
separados por coma), y botón **"📲 Enviar lista por WhatsApp"** que abre WhatsApp con un mensaje
que incluye la fecha + el listado numerado de canciones con su tono. Si hay varios números, abre
un chat por cada uno; si no hay número, abre WhatsApp para elegir el chat.
NOTA: WhatsApp por link no permite adjuntar el PDF automáticamente; el mensaje va como texto y el
PDF se comparte aparte (se descarga con el nombre de la fecha).

- Una vez armada **"La Lista"** (repertorio del item 3):
  - Poder **elegir una fecha** (ej: "Sábado 13 de Junio").
  - Que esa fecha sea el **nombre del archivo** (ej: `Sabado 13 de Junio.pdf`).
  - Botón **"Cerrar lista"**.
  - Botón **"Enviar Lista por WhatsApp"** al número o números de teléfono que se carguen en un espacio arriba, para mandársela a los participantes.

**Notas técnicas:**
- Campo arriba para cargar uno o varios números de teléfono.
- Envío por WhatsApp probablemente vía enlace `wa.me/<numero>?text=...` (manda el mensaje/link; el PDF puede ir como link de descarga).

---

## 8. Links de YouTube por canción
**Estado:** ✅ COMPLETADO

Implementado: campo "Links de YouTube (uno por línea)" en el formulario de alta/edición.
Se guardan en la columna `youtube`. En el detalle de la canción aparecen como botones rojos
"▶ Video 1, 2..." que abren YouTube en otra pestaña. Una canción puede tener uno o varios links.

- Poder **asociar a cada canción uno o más links de YouTube** donde se escucha el tema.
- Cada canción puede tener **1 o varios** links disponibles.

**Notas técnicas:**
- Tabla/campo nuevo para guardar los links de YouTube de cada canción.
- Mostrarlos en el detalle de la canción.

---

## 9. Generar lista de reproducción de YouTube del repertorio
**Estado:** ✅ COMPLETADO

Implementado: botón "🎬 Playlist de YouTube" en el panel de la lista. Abre una página con todos
los videos del repertorio, un botón "▶ Reproducir todas" (playlist anónima de YouTube que encadena
los videos vía watch_videos?video_ids=...), el listado por canción, y "📲 Enviar por WhatsApp"
que comparte el link de la playlist + todos los links (a los teléfonos cargados, igual que el PDF).

- Una vez hecha la lista para enviar (item 7), que **genere una lista de reproducción de YouTube** con los temas, para distribuir a los demás músicos.
- Enviarla **de la misma forma** que el PDF (por WhatsApp).

**Notas técnicas:**
- Combinar los links de YouTube (item 8) de las canciones de la lista en una playlist o en un mensaje con todos los enlaces en orden.

---

## 10. Rediseño estético de la pantalla principal
**Estado:** ✅ COMPLETADO

Implementado: rediseño moderno con sistema de TEMAS (CSS variables + data-theme).
- Tema por defecto: **Noche de Adoración** (oscuro elegante, cabecera con degradé violeta→azul).
- Selector de tema en el encabezado con 3 opciones: 🌙 Noche, 🌅 Amanecer (cálido ámbar→rosa),
  🎨 Violeta (claro). Se guarda en el navegador (localStorage) y se aplica sin parpadeo.
- Cabecera con degradé "hero", tarjetas, controles de formulario y todo adaptado a cada tema.
Pendiente opcional a futuro: sumar foto de cabecera (hero) de banco gratis.

- Diseño **moderno**, con **imágenes**, pero **no muy cargado** (limpio).
- Buena **paleta de colores**.
- **Buscar páginas/sitios de referencia** (inspiración) y elegir un estilo con buenos colores antes de diseñar.

**Notas técnicas:**
- Investigar referencias de diseño (apps de worship/cancioneros, landing pages modernas).
- Proponer 2-3 opciones de paleta + estilo al usuario antes de aplicar.

---

## 11. Publicar el programa como página web pública
**Estado:** ✅ COMPLETADO (online) — falta conectar el dominio propio

- ✅ App publicada en **Render** (plan free): **https://adoremos.onrender.com**
- ✅ Código en GitHub: **github.com/ragolti/canciones** (repo público, auto-deploy activo).
- ✅ Las 149 canciones viajan en la base `canciones.db` incluida en el repo.
- ⏳ PENDIENTE: apuntar el dominio **www.canciones.com.ar** (en trámite en nic.ar) al servicio
  de Render (agregar custom domain en Render + configurar DNS en nic.ar).
- NOTA: plan free de Render "duerme" tras inactividad (1ª visita tarda ~50s).
- ✅ BASE PERSISTENTE RESUELTA: conectada a **Neon (Postgres gratis)** vía variable de entorno
  DATABASE_URL en Render. Persistencia confirmada (los cambios sobreviven a reinicios).
  La app usa doble motor: SQLite en local, Postgres/Neon online. Carga inicial idempotente
  (una conexión, índice único por título, 1 worker). Esto habilita los items 12 y 15.

---

## 12. Registro de usuarios y carga de canciones con aprobación
**Estado:** ✅ COMPLETADO

Implementado: registro (/registro), login (/login), logout. El PRIMER usuario que se registra
queda como **admin**; el resto como **colaborador**. Contraseñas con hash seguro (werkzeug).
- Colaborador: puede agregar/editar canciones, pero quedan en estado **pendiente** (no se ven
  en público hasta que el admin las aprueba).
- Admin: publica directo, ve el botón "📋 Revisar (n)" y aprueba/rechaza en /revisar.
- Solo el admin puede borrar canciones.
- Columna `estado` (aprobada/pendiente) en canciones; el público ve solo las aprobadas.
NOTA: editar una canción aprobada (por colaborador) la pasa a pendiente hasta re-aprobación.

- Que las personas se puedan **registrar** e iniciar sesión.
- Usuarios registrados pueden **Editar y agregar nuevas canciones**.
- Las canciones nuevas/editadas quedan **pendientes de revisión** y se **dan de alta** recién después de ser aprobadas por un administrador (moderación).

**Notas técnicas:**
- Sistema de login/usuarios y roles (administrador vs. colaborador).
- Estado en cada canción: `borrador / pendiente / aprobada`.
- Panel de administrador para revisar y aprobar/rechazar.
- (Importante para esto: tener base de datos **persistente**, no la temporal del plan gratis de Render.)

---

## 13. Modo proyección en vivo a pantalla gigante (por párrafos)
**Estado:** ✅ COMPLETADO

Implementado: botón "🖥️ Proyectar lista" en el panel. Abre una pantalla de control de 3 zonas:
izquierda = lista de canciones, centro = párrafos SIN acordes (clic para emitir), derecha = vista
previa de lo que sale en la pantalla gigante. Botón "📺 Abrir pantalla de proyección" abre una
ventana aparte (para la pantalla/proyector, F11 pantalla completa) que muestra solo el párrafo
actual, grande y centrado sobre negro. Sincronización en vivo vía BroadcastChannel. Botón
"⬛ Pantalla en negro" para limpiar.

- Poder **proyectar la lista/repertorio a una pantalla gigante** (segunda pantalla / proyector).
- En la proyección: **sin acordes**, solo la letra, mostrada **párrafo por párrafo** (estrofa por estrofa).
- **Pantalla de control con 3 zonas:**
  - **Izquierda:** la lista de canciones del repertorio.
  - **Centro:** los párrafos de la canción seleccionada (para ir eligiendo cuál se emite).
  - **Derecha:** una **vista previa** de lo que se está emitiendo a la pantalla gigante (solo el párrafo actual).

**Notas técnicas:**
- Operador maneja una pantalla (control) y el público ve otra (proyección).
- Probablemente: ventana de proyección aparte + sincronización (mismo origen, localStorage/canal de mensajes o websockets).
- Navegar entre párrafos con teclado/clic.

---

## 14. Fondos para la proyección (fijos o en movimiento)
**Estado:** ✅ COMPLETADO

Implementado en la pantalla de control: sección "Fondo" con presets (⬛ Negro, 🌌 Violeta, 🌊 Azul,
✨ Animado en movimiento), campo para pegar URL de imagen (.jpg/.png) o video (.mp4) de fondo, y
links a Pexels/Unsplash para buscar fondos gratis online. El fondo se aplica en vivo a la ventana
de proyección (con capa oscura para que la letra se lea) y se refleja en la vista previa.
La ventana de proyección, al abrirse, pide el estado actual (texto + fondo) por handshake.

- Al proyectar, poder **agregar fondos**: imágenes **fijas** o **en movimiento** (video/animados).
- Que los fondos se puedan **buscar en internet** desde la app.

**Notas técnicas:**
- Galería de fondos + opción de buscar/traer desde internet.
- Cuidar legibilidad de la letra sobre el fondo (capa oscura/contraste).
- Tener en cuenta licencias/derechos de las imágenes y videos.

---

## 15. Historial de listas de eventos + favoritas
**Estado:** ✅ COMPLETADO

Implementado: botón "💾 Guardar en historial" en el panel del repertorio (requiere login).
Guarda la lista con su nombre/fecha, el usuario que la creó y las canciones. Página /historial:
izquierda = listas guardadas (con autor y cantidad), derecha = detalle de la lista elegida
(canciones con su tono). Filtro por usuario y casilla "⭐ Solo favoritas". Cada lista se puede
marcar/desmarcar como favorita, "📋 Usar esta lista" (la carga en el repertorio) y borrar
(quien la creó o el admin).

- Las listas de evento suelen ser de **7 u 8 canciones**.
- Guardar un **"Historial"** de todas las listas que se van armando.
- Poder consultarlo con un clic: al elegir una fecha, que aparezca **a la derecha** la lista de esa fecha.
- Cada lista guarda:
  - **Nombre del usuario** que la creó.
  - **Fecha** en que se usó.
- Poder **filtrar por usuario**.
- Sección **"Mis Favoritas"**: marcar listas como favoritas para acceso rápido.

**Notas técnicas:**
- Tabla nueva de "listas" (id, nombre/fecha, usuario, favorita, fecha_uso) + sus canciones en orden.
- Necesita base de datos persistente y, para "nombre del usuario", se apoya en el sistema de
  usuarios (item 12).
- Guardar la lista actual del repertorio al "cerrar lista" (item 7) la suma al historial.

---

## 16. Clasificación de canciones en varias dimensiones (botones por tema)
**Estado:** ✅ COMPLETADO

Implementado: en la lista, debajo de cada canción (solo para usuarios logueados) hay 3 grupos de
botones rápidos que se guardan al instante (AJAX):
- FUNCIÓN: Alabanza / Adoración (campo `funcion`)
- ESTILO: Coros / Clásicas / Contemporáneas / Nuevas (campo `categoria`, agrupa la lista)
- TEMPO: Rápida / Media / Lenta (campo `tempo`)
Volver a tocar un botón activo lo deselecciona. Campo validado con lista blanca (seguro).
La TEMÁTICA se maneja con el campo 'etiquetas' (libre) en el formulario de edición.
Migración: los estilos viejos se unificaron (Nuevas y últimas→Nuevas, etc.).
PENDIENTE OPCIONAL futuro: filtros arriba del listado por función/tempo.

Pedido del usuario: al lado de cada canción, botones para clasificar:
- **Función:** "Alabanza" vs "Adoración" (un recuadro).
- **Estilo/época:** "Coros", "Clásicas", "Contemporáneas", "Nuevas" (otro recuadro a la derecha).

Investigación (foros/sitios de adoración) — dimensiones que se usan:
1. FUNCIÓN/MOMENTO: Alabanza (festiva, rápida) vs Adoración (íntima, lenta).
   A veces más fino: Júbilo/Entrada → Alabanza → Adoración → Íntimo/Comunión.
2. ESTILO/ÉPOCA: Coros clásicos, Clásicas, Contemporáneas, Nuevas.
3. TEMPO: Rápida / Media / Lenta (clave para ordenar el setlist).
4. TEMÁTICA: Cruz/Sangre, Espíritu Santo, Guerra espiritual, Gratitud, Avivamiento,
   Comunión, Navidad, Libertad, Victoria, etc.

Propuesta técnica:
- Campo nuevo `funcion` (Alabanza/Adoración) además del `categoria` actual (estilo).
- Opcional: `tempo` y reutilizar `etiquetas` para temática.
- Botones rápidos de clasificación en la lista (sin entrar a editar), guardando vía AJAX.
- Filtros por cada dimensión arriba del listado.

Fuentes consultadas:
- worshipleader.me/blog/categoriesofsongs (4 categorías de canciones)
- davidsantistevan.com (cómo armar un setlist que fluye)
- praisecharts.com/explore/themes (temáticas)
- compellingtruth.org / lacorriente.com (alabanza vs adoración)

---

## 17. Agregar link de YouTube desde la lista (rápido)
**Estado:** ✅ COMPLETADO
En el listado (logueado), cada canción tiene un botón "🎬 + Link" que pide el link de YouTube y
lo guarda al instante (AJAX, sin entrar a editar, sin duplicar). Muestra "▶ N" con la cantidad
de links que ya tiene. Ruta POST /youtube/<id>.

## 18. Buscar en YouTube desde el lápiz (por título, sino por estribillo)
**Estado:** pendiente
Al hacer clic en editar (lápiz), un botón que abra/busque en YouTube usando el TÍTULO del tema;
y si no, por una línea de la LETRA del estribillo. Para encontrar el video fácil y pegarlo.

## 19. Botón "Guardar la lista" más visible
**Estado:** parcial (ya existe "💾 Guardar en historial" en el panel; revisar que sea claro/accesible).

## 20. Generar playlist y completar links faltantes en el listado general
**Estado:** pendiente
Al generar la playlist de YouTube, si a una canción le falta el link y se encuentra uno, que se
inserte/guarde en el listado general (queda con su link permanente para la próxima).

## 21. Búsqueda automática de links de YouTube
**Estado:** pendiente (a evaluar)
Que el sistema busque solo los links de YouTube de las canciones (automático). NOTA: requiere
API de YouTube (clave) o scraping; evaluar viabilidad/costo/límites.

## 22. Listado de listas guardadas con última fecha de evento (y repeticiones)
**Estado:** pendiente (mejora del item 15)
En el historial, mostrar al lado de cada lista su última fecha de evento; y si una misma lista se
usó en más de un evento, mostrar esas fechas/repeticiones.

## 23. Contador de cuántas veces salió cada tema en los eventos
**Estado:** pendiente
Ver, en cualquier canción, cuántas veces apareció en las distintas listas/eventos guardados.

## 24. Importar temas con acordes desde páginas web
**Estado:** pendiente (a evaluar cómo)
Pegar una URL de una página de acordes y que traiga título + letra + acordes. NOTA: cada sitio
tiene formato distinto; evaluar enfoque (pegar texto vs. importador por sitio).

## 25. Importar desde PDFs (con botón)
**Estado:** pendiente (a evaluar cómo)
Botón para subir un PDF y extraer las canciones (como hicimos con "Lista Nueva", pero desde la
web). NOTA: requiere lectura de PDF en el servidor y separar canciones.

## 26. Playlist YouTube: fijar links al general + compartir por WhatsApp
**Estado:** pendiente (mejora de items 9 y 20)
En la página de Playlist de YouTube: al encontrar un link, poder "fijarlo" para que quede en el
listado general. Y compartir la playlist al grupo por WhatsApp desde ahí (ya existe parcialmente).

## 27. "+ Nueva canción": buscar en Internet y cargar desde ahí
**Estado:** pendiente (a evaluar)
Al crear una canción, poder buscarla en páginas de internet (letra/acordes) y cargarla desde
el resultado. Relacionado con items 24 y 25.

## 28. Cambiar de grupo desde el botón + del listado
**Estado:** parcial (item 16 ya permite cambiar Estilo con botones rápidos al estar logueado;
acá se pide además un acceso desde el menú del símbolo +). Revisar/ajustar.

## 29. Desplegable para elegir/filtrar qué listado (grupo) ver
**Estado:** pendiente
Un desplegable arriba (donde dice el grupo, ej. "Nuevas") para elegir y filtrar qué grupo/listado
mostrar. También filtros por función/tempo.

## 30. Modo PDF/proyección móvil horizontal, pantalla completa, deslizable
**Estado:** pendiente
Al tocar "PDF / Imprimir" (en celular): vista horizontal (girar el teléfono), cada canción ocupa
la pantalla completa, se pasa de canción deslizando el dedo (siguiente/anterior), con el TÍTULO
arriba y el NÚMERO de página en una esquina (para que el cantante se ubique).

## 31. Compartir lista por número (ej. "lista 223")
**Estado:** pendiente
Cada lista guardada tiene un número; para compartir, basta decir el número y los demás (músicos
y proyección) la buscan en el programa por ese número.

## 32. Búsqueda con y sin acentos
**Estado:** pendiente
Que el buscador encuentre igual escribiendo con o sin acentos (ej. "adoracion" = "adoración").

## 33. Borrar solo con credenciales de Administrador
**Estado:** ✅ YA HECHO (item 12: solo el admin puede borrar). Confirmar que cumple.

## 34. Cuentas individuales con permisos (borrar/modificar/ocultar)
**Estado:** parcial (item 12 ya da cuentas y roles). Falta: poder "OCULTAR" canciones (además de
borrar/modificar) y afinar permisos por usuario.

---

<!-- Próximos items se agregan acá debajo -->
