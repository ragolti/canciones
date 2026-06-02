# -*- coding: utf-8 -*-
"""
importar_lista_nueva.py
-----------------------
Carga en la base de datos todas las canciones del PDF "Lista Nueva".
Cada canción tiene: titulo, artista, tono (intro/acordes iniciales),
etiquetas ("Lista Nueva") y la letra con acordes.

Ejecutar una sola vez:  py importar_lista_nueva.py
Evita duplicados: si ya existe una canción con el mismo título, no la repite.
"""

import database

# Cada entrada: (titulo, artista, tono, letra)
CANCIONES = [
("Glorioso día", "", "D", """ D
Mi vergüenza me sepultó
 Bm7
Yo buscaba un salvador
 G D
Más tu perdón, me liberó
Muerto estaba en mi interior
Me escondía de ti Señor
Más tu perdón, me liberó

 G D
Tu voz me habló... Y a la muerte venció
 G D
Glorioso día, tu sangre me rescató
 G Bm7
Tu voz me habló… y a la muerte venció
Glorioso Día, tu sangre me rescató

Inter: D
Ahora libre soy en tu amor
Es tu gracia la que me salvó
Más tu perdón, a mí me liberó

Estribillo: Tu voz me habló... UooHhhhh ohhhhh
De mi pecado me rescataste
En tu gloria cadenas se rompen
Vivía solo y sin consuelo
Ahora soy ciudadano del cielo
Tú me sanaste estando herido
Jesús por tu amor yo respiro
(Bm7) Tengo futuro (Asus2) ahora veo
xq tú voz me habló (G) y a la muerte venció (D)"""),

("Socorro (Un Corazón)", "Un Corazón", "D", """D ¿De dónde viene mi socorro?
 Mi ayuda viene de Ti
( G D A Bm )
G D A Bm
El cielo cuenta de tus obras poesía escrita por Ti
Estelas de misericordia todas apuntan a Ti
 G Gm D
Si me encuentro perdido sé dónde te puedo encontrar

 G D
Alzaré mis ojos a los montes
 A Bm
Te veré radiante como el sol
Seguiré el brillo de tu gracia
Porque sé que Tú sigues siendo Dios
 G D A Bm
Tú sigues siendo Dios oh oh oh

Si cuidas de todas las aves sé que me cuidas a mí
Ya nada puede separarme
Porque dependo de Ti

¿De dónde vienen mi socorro? Mi ayuda viene de Ti
¿Quién sana corazones rotos? Mi ayuda viene de Ti

Bm A G D ¿De dónde viene mi esperanza?
G A D D/C# Mi ayuda viene de Ti
Bm A G D ¿Quién da descanso para el alma?
G A D D/C# Mi ayuda viene de Ti

Alzaré mis manos a los cielos
Te veré obrando a mi favor
Seguiré tomado de tu mano
Porque sé que tú sigues siendo Dios"""),

("Eres Libre", "", "D#m B F# Bbm", """Intro: D#m B F# Bbm (x3)
 D#m B F# Bbm
Abandona la tumba y la oscuridad
 D#m B C# Bbm
Da un paso adelante, no tengas temor

(PRECORO)
F#-Bbm B D#m C#
Corre a lugares abiertos, gracia te espera
Danza ahora eres libre, gracia te espera

(CORO)
 B F# D#m C#
Su Espíritu está aquí, tu eres libre, eres libre //

(CORO2)
 D#m B
Las sombras atrás ven sin temor
 F# Bbm
a la abundancia de su amor
 D#m B C#
Por qué el Señor está aquí y tú eres libre

(ESTROFA 2)
Presenta tus cargas, todo tu dolor
Regresa al comienzo, a la comunión

Puente Bb - B D#m C# (x2)
En el nombre de Jesús, las cadenas caerán
En el nombre de Jesús, vidas se completarán //"""),

("Ven Espíritu Santo (Barak)", "Barak", "Em D C B7", """(Em D C B7) Estoy aquí, desesperado por ti
Con un corazón sediento
Que espera beber de ti
(C D Am B7) Cuando tu gloria desciende a un lugar
Toda la tierra tiene que adorar
Resucitan los muertos
Se sanan enfermos por tu poder
Queremos de ti, llénanos de ti
Espíritu Santo envuélvenos en ti
Derrama tu gloria, esperamos por ti

(Em D C B7) Ven, ven, ven
Espíritu Santo ven, ven, ven
Llena este lugar //

Señor, acércate (Ven) transfórmame
(Ven) quebrántame (Ven) restáurame
Oh, vivifícame (Ven) libértame
(Ven) envuélveme (Ven) reposa sobre mí

Cuando el Espíritu Santo viene y reposa sobre ti
Él se mueve sobre el caos en tu vida
Sobre todo quebrantamiento en ti
Y al hablar pasas de muerte a vida

Ven, ven, ven, es que no puedo ya vivir sin tu presencia
Te necesito, Señor
Llévame, transfórmame confío en ti"""),

("Manda Lluvia", "", "D", """D
Vengo ante ti
con el corazón rendido a tus pies
con mi vida entregada para ser tuyo Dios
Y te clamaré
por un fuego que llueva sobre mi
por un deseo que transforme mi interior
de traerte honor

 G D/F# Em A
desciende, desciende, desciende sobre mi
desciende, desciende, desciende hoy aquí
Guitar Break: Bm Em Bm G

creo en el poder
cuando te clamo en oración
para ofrecerte todo mi amor en adoración
y te clamaré
que sobre toda mi generación
arda este deseo y pasión de traerte honor

 D G
Manda lluvia, temprana y tardía
 Bm A
que llene hoy mi vida con pasión //
(termina en G)"""),

("Eres Fiel", "", "D A C G", """ D Dmaj7/d G/d C/d
Señor eres fiel y Tu misericordia eterna
 D Dmaj7/d D/d C/d
Señor eres fiel y Tu misericordia eterna
 G A/g
Gente de toda, lengua y nación
 A#/g C/g
de generación, a generación
 D A C G
Te adoramos hoy, aleluya, aleluya
 D/f# Am7 C
Te adoramos hoy, eres Señor
 D/f# Am7 A# C
Te adoramos hoy, eres Señor

Eres Fiel corte -- Intro: Dm (8 compases)
Solo baterías y Trompeta: Dm7 E F - Dm7 C F
Dm (32 compases) cantado Eres fiel"""),

("Santo (Upperroom)", "Upperroom", "B", """ B C# E
Venimos ante Ti, Jesús en adoración
Nacimos para amarte a ti por la eternidad
 E B F# G#m
Y nos unimos al cielo en un canto de amor
 E F# B
Exaltando por siempre al que nos redimió
 E B F# B
Cantando Santo, Santo
Tú eres digno, digno
Cantando Santo, Santo
Tú eres digno, digno

B C# E
Generaciones cantarán de tu verdad
Deseamos de tu trono aquí ven a reinar

 E F# G#m
Tu nombre anunciaremos y lo declararemos
Naciones oirán y lo declararán
Tú eres el más bello y nuestro Dios eterno
Todos te adorarán por siempre reinarás"""),

("De gloria en gloria", "", "Eb Bb9", """ Eb Bb9
Yo, quiero ver
 Gm F9
Tu luz brillando en mi, a través de mi

Y ser un altar
que todos puedan ver
que todos oigan que

Tu eres vida, la esperanza
perfecta gracia que, me ha rescatado
Tu eres vida, la esperanza
perfecta gracia que, me ha rescatado

Ya no vivo yo, Cristo vive en mi
Barro quiero ser, en Tus manos

De gloria en gloria
te veo Dios
De gloria en gloria
transformado soy por Tu Espíritu"""),

("Aguas Profundas", "", "Am F G Em-G", """ Am F G Em-G
Oh, oh, oh, oh
Ven sobre mí como lluvia,
Has tus aguas subir en este lugar.
Libera tu rio sin medida
Y ven a tus aguas agitar
Yo quiero nadar, quiero nadar, en tu rio.
Quiero beber, quiero beber de tus aguas

Dm F G
Existen aguas a los tobillos,
Existen aguas a las rodillas,
Existen aguas a los lomos,
Pero hay aguas profundas ¡yo se!"""),

("Sea exaltado tu nombre", "", "Intro C-Am-G-F", """F maj7
Cielo y tierra Unidos
 C
en un clamor
F maj7 C
Toda la Creación se postra

G Am F maj7 Em
Aleluya, todos canten al Rey
G Am F – G – Am
Aleluya, para siempre

 F maj7 G
Sea exaltado, tu nombre
C /e
Sea exaltado, aquí
 F maj7 G C
Sea exaltado, tu nombre Jesús

C Am G F / Fm
Aleluya, Aleluya, Aleluya al Rey
justo y verdadero, fiel y consejero
tu reino se ha acercado a este lugar ////"""),

("Increíble", "", "D A", """D A
Poderoso, invencible
E F#m
admirable, grande y fuerte Dios
D A
Rey de Reyes, asombroso,
E F#
incomparable...

Eres increíble
todopoderoso, grande
eres increíble
venciste las tinieblas
Cristo exaltado estas...
//D–A - E - f#m //

D A
Tu Increíble, invencible
E F#
dios solo tu, solo tu
Tu eres increíble, invencible
Mi Dios solo tu, solo tu..."""),

("Al que es Digno", "", "Dsus2 G", """ Dsus2 G
Al que es Digno, de recibir la gloria.
Al que es digno
 D/F# Asus4
Al que es Digno, de recibir el honor.

 G A/G F#m7 Bm7
Levantemos nuestras manos y adoremos,
 G A/G F#m7 Am7 D7/G#
a Jesús, Cordero de Gloria
 G A/G F#m7 B7
Y exaltemos su incomparable majestad
Em D/F# G Em D/F# G
Al que viiiveee por siempre, al Gran Yo Soy,
 A D
A Jesús."""),

("Así como David danzaba", "", "Dm C", """ Dm C
Cuando el Señor hiciere volver la cautividad
 Gm A
seremos como los que sueñan

Mi boca llenará de risa, mis labios de alabanza,
Entonces dirán las naciones
Grandes cosas ha hecho el Señor

Me gozaré, me gozaré, me gozaré,
me gozaré en Jehová. [¡Gózate!]
Pues ha llevado todo dolor, me ha hecho libre

Así como David cantaba, así como David danzaba,
así como David fluía en su presencia"""),

("El Poderoso de Israel", "", "Dm", """Dm
Y de noche cantaremos
Celebrando su poder
Con alegría de corazón
Como el que va con la flauta
Al monte del Señor
Celebraremos su poder

El es el Poderoso de Israel
El Poderoso de Israel
Su voz se oirá nadie lo detendrá
Al poderoso de Israel

Y los ojos de los ciegos
Se abrirán ellos verán
Los oídos de los sordos oirán
El cojo saltará con el arpa danzará
La lengua de los mudos cantará

(Cantaré al Señor por siempre)
Em
Cantaré al Señor por siempre, su diestra es todo poder
Echó a la mar quien nos perseguía
Jinete y caballo echó a la mar
Echó a la mar los carros del faraón
Mi padre es Dios, y yo le exalto
Mi padre es Dios, y le exaltaré

(Jehová es mi guerrero)
Em
Jehová es mi guerrero oh,oh,oh
Con mi alabanza pelearé
no es mi guerra si no la de Dios
Danza y pandero yo daré
Címbalo y trompeta sonaré
Con fuerte y alta voz yo gritaré"""),

("Dios está llamando a la guerra", "", "", """Dios está llamando a la guerra
Nos está impulsando hacia afuera
Acudiremos al llamado del Señor
Tomaremos las armas que Él nos preparó

Tú y yo somos su pueblo
Tú y yo, preparados para mostrar las grandezas del Señor
Para tomar la tierra que Él nos entregó

Somos pueblo
Pueblo adquirido por Dios
Nación santa
Gran sacerdocio, linaje escogido por Dios
Para anunciar las virtudes de aquel
Que nos llamó de tinieblas a luz
Admirable
Somos los hijos de luz

Tiempo de vivir, tiempo de morir.
Tiempo de llorar, tiempo de reir.
Tiempo de animar y redarguir hoy es tiempo.
Tiempo de aprender, tiempo de enseñar.
Tiempo de hablar, tiempo de callar.
Tiempo de sembrar y de cosechar hoy es tiempo.
Hoy es tiempo que seamos
ese pueblo glorioso fiel y victorioso de Dios"""),

("Danzaré Cantaré", "", "F# C# D#m B", """Intro: F# C# D#m B → F# C# D#m E → B
F#m E6
¿A donde iré sin ti Señor?
 Dmaj7 E
Si solo Tu Jesús tienes palabras de vida
 F#m E6
Si subiera al monte mas alto, o bajara hasta el fondo del mar
Dmaj7 C#
¿Quien me dará quien me mostrara al amor?

 F# C# D#m B F#
Danzare, cantare derramaré mi corazón delante de ti
 C#m E → B
Es el rio de tu amor

 D#m D#m(maj7) D#m7 G#9
Tantos años yo perdí sin el amor que no pude ver
 G#m7 Bm7
Hasta que encontré la presencia de Dios
 C#
Aquí en el rio"""),

("Tu harás", "", "Cm7 F7", """Intro: Cm7 F7
Cm7 F7
Cuando el mar me dice te hundirás
Me das tierra firme y puedo cruzar
Cuando el monte dice no pasaras
Cm F7 Eb
Tengo Tu palabra y eso bastara
D Db Cm7
Ohhh, Ohhhh

G# Bb
Eres la fuerza que mueve mi vida
C F
Eres mi Dios y Tú harás, más allá de lo que pueda imaginar
 Am7 G F
Más allá de lo que pueda yo soñar
 F G Cm7
eres Dios y harás

Eres Dios de ayer, eres Dios y estas
Sabes lo que fue, sabes que vendrá
Eres gran yo soy, Tú me sostendrás
Tú eres mi Dios en ti puedo confiar

Am7 G Dm7 F Am7
Mi vida has cambiado, salvado hoy
 G Dm7 Em F
Yo vivo por tu gran amor, por tu gran amor

A Dios sea la gloria y la honra hoy, para siempre"""),

("En los montes, en los valles", "", "Dm Bb A", """Intro: ////Dm - Bb - A////
Dm Bb A
Oh - Oh - Oh - Oh - Oh - Oh - Oh
Dm Bb C
En los montes, en los valles, Exaltamos al que es digno de Alabanza.
En las costas de los mares,
Levantamos un sonido de esperanza
Aclamamos, aclamamos,
Hacemos oír la voz de su alabanza.
Con las manos en lo alto
Exaltamos al que reina para siempre.

 Dm Gm
Subamos a adorar en el monte de Sión,
Dm A
Es el gozo de toda nación.
 Dm
Donde la tristeza es gozo,
 Gm
El llanto es alegría
 Dm A
Subamos a adorar al gran Rey"""),

("Con saltos de alegría", "", "G", """ G
Con saltos de alegría y
 D Am C
gritos de victoria yo voy /(4veces)

 G D
Voy a seguir a Jesús
 Am C
Voy a seguir a Jesús
 Em Bm7
Voy a seguir a Jesús
C C Fmaj7
Voy a seguir a Jesús
Voy a danzar con Jesús

Solo tú y yo (repite 8 veces)
Yo soy libre - Yo soy libre
libre para cantar
Yo soy libre, Yo soy libre
libre para danzar

Guitarra: G D Am C Em Bm7 C7-- C7 → Fmaj7
Termina con Intro de Soy de mi Amado:
G D Em C Am // Oh oh oh Am soy de mi amado… C mi amado es mio…"""),

("Soy de mi Amado", "", "D C G", """Intro: G D Em C Am // Oh oh oh soy de mi amado… mi amado es mio…
 D C G
Como una marca en el brazo yo soy tuyo
Como un sello en el corazón tú eres mío
Como brazas de fuego tu estas en mí,
 D C Am
Y las aguas no ahogaran, nuestro amor,
 Bm C7
amor, amor
 D
Danza conmigo

 G D
Soy de mi amado, él es mío
 Em C
Soy de mi amado, él es mío
 G D Em
Soy de mi amado, soy de amado
 C
soy de mi amado, Jesús

En tu lugar secreto quiero estar
Y bajo tu sombra descansar
Escondido en ti, nada temeré
Tu bandera sobre mi es el amor, amor, amor
Danza conmigo
te aplaudimos Jesús"""),

("Tu nombre es Cristo", "", "Dm Gm", """Dm Gm
Todas las naciones hablan de tu nombre
Bb Gm Am
Todo ser creado, confiesen que eres Dios
Todas las criaturas se rinden a tu nombre
Todo el firmamento, confiesen que eres Dios

Bb Gm
Confesamos que tú eres santo
Dm Am
Confesamos que tú eres digno
Confesamos que tú eres santo
Inigualable eres tú

Dm Bb
Tu nombre es Cristo Dios poderoso
Gm Bb Am Dm
Tu nombre es digno Rey asombroso
D Gm Am C
Cantaré, gritaré, gloria, gloria"""),

("Al que Vive", "", "A G D/F#", """Intro: A G D/F# A
 A G D/F# A
Todos unidos a una voz en un mismo corazón levantamos hoy una canción
Se oye un fuerte resonar un estruendo sin igual con los ángeles han de cantar
 G
Todos juntos alabar

 A
Al que vive
 Em
Al que es y quien vendrá
 D G
Al santo de Israel que pronto regresara
 A Em
Al cordero Coronado en majestad
 D G
A nuestro libertador y a nuestro salvador
 A Em D A
A jesuuusss

Preludio:
A G/Em D/F# A
Aleluya al cordero gloria"""),

("Digno", "", "A F#m", """ A F#m
No tengo nada para ofrecer, nada que te pueda sorprender
 Bm7 F#m E
Solo un corazón, quebrantado una y otra vez

 A F#m
Y no hay nada que me enamore más, nada que me apasione mas
 Bm7
Solo tu presencia
 F#m Esus4 E
solo tu mirada me hacen suspirar

 Bm7 Dm
Me inclino ante ti
 A /C#
Rey que perdona
 E
multitud de errores
 Bm7 Dm
Me inclino ante ti

 Asus-A F#m
Digno eternamente Digno
 E D Dm
Impresionante digno solo ante ti yo me inclino"""),

("Al que está sentado en el trono", "", "A", """A
Quiero conocerte,
 F#m7
cada día mas a ti
 D Maj9
Entrar en tu presencia
 E Maj7(add2)
y adorar.
F#m9
Revélanos tu gloria
 A/E
Deseamos ir mucho más en ti
 D Maj9 E Sus2 E
Queremos tu presencia Jesús

 A
Al que está sentado en el trono
Fm Maj7
Al que vive para siempre y siempre
 Bm7 C#m7
Sea la gloria, Sea la honra y el poder
 D Maj9 E sus4 E
Sea la gloria, Sea la honra y el poder

Tu eres Santo, Santo,
Santo, Santo
Santo eres tu."""),

("Tu estas aquí", "", "E C#m", """ E C#m
Aunque mis ojos no te pueden ver
 A E
Te puedo sentir, sé que estás aquí
Aunque mis manos, no pueden tocar
Tu rostro señor, sé que estás aquí
Oh oh B sus4

 Bm A
Mi corazón puede sentir tu presencia
 E B sus4
Tú estás aquí, tú estás aquí
 Bm A
Puedo sentir tu majestad
 E B sus4
Tú estás aquí, tú estás aquí

Mi corazón puede mirar tu hermosura
Tú estás aquí, tú estás aquí
Puedo sentir tu gran amor
Tú estás aquí, tú estás aquí"""),

("Soy nueva criatura", "Jesús Adrián Romero", "Am7 G9", """Am7 G9 Am7 / Dm7, Emaj7 / Am7, Fmaj7, Dm7, E
Soy nueva criatura, lo declara la escritura
Él me ha perdonado, con su sangre me ha lavado
Todos mis pecados por su sangre son borrados
Libre soy del pecado//

Libre del pecado y la maldad
Soy libre él ha roto mis cadenas
Libre, libre para dar mi vida al que me salvó//

Soy nueva criatura, lo declara la escritura
Él me ha perdonado, con su sangre me ha lavado
Todos mis pecados por su sangre son borrados
Libre soy del pecado //"""),

("Amor como fuego", "", "Intro: E-C#m-B-A-E", """ E
Anhelo un toque de Tu amor
 C#m
Sólo un destello de Tu gloria en mí Señor
 B
En un momento todo puedes transformar
 A E
Mi vida has cambiado Dios

 E
Y no alcanzo a comprender
 C#m
Tu amor sostiene por completo hoy mi ser
 B
Tu gracia y sangre que mi vida transformó
 A E
Borraste mi pasado Dios

 C#m A E B
Tu amor es como fuego, que arde en mi interior
 C#m A E
Mi único anhelo, rendirte adoración
 B E
Con Tu fuego lléname
 E B
Que Tu amor me atraiga
 C#m
Al lugar donde Tú estás
 (A) E
Quiero más de Ti Señor

 E
Me rindo ante Ti Jesús
Me entrego humilde ante el mensaje de la cruz
Y me abandono en Tu presencia y amor
Jamás seré igual oh Dios"""),

("Dios es Amor", "Hillsong", "F# D#m", """F# D#m
Todo ser, todo corazón, Toda lengua, toda nación
 B
halla fuerza en el amor del Padre
F# C# D#m
Todo el mundo se postrará, su mirada levantará
 C# B
a Jesús salvador hoy y siempre

 F# C#
Esto es amor
 D#m B F# C#
Jesús vino, Él murió y resucitó
 D#m B D#m
alabémosle, nos dio la salvación
 C# B
no existe más temor
 D#m B C#
Dios es amor oh-oh-oh-oh oh-oh-oh-oh

Cada vida que está en dolor, Cada lágrima y oración
halla fuerza en el amor del Padre
Su alabanza declararé, toda gloria ofreceré
A Jesús Salvador hoy y siempre

B F# C# D#m B
Cantaré hoy y por siempre, de su gracia y su perdón
La creación hoy y por siempre, cantará de su amor"""),

("Aquí estoy", "Hillsong / Marcos Witt", "A", """A
Tú eres el principio,
D
Tuya es la eternidad,
 A/C# F#m
Llamaste el mundo a existencia,
 D
Me acerco a ti.
Moriste por mis pecados,
Borraste mi culpa en la cruz,
Cargaste en tus hombros mi carga,
Me acerco a ti.

 D - Bm
¿Qué puedo hacer?
 F#m
¿Qué puedo decir?
 D E
Te ofrezco mi corazón
 F#m
Completamente a ti.

En tu salvación camino
Tu Espíritu vive en mí.
Declararé tus promesas.
Me acerco a ti.

Interludio: Dm Am Em F#m (x4)
D A E F#m
Aquí estoy, con manos alzadas vengo
Pues tú todo lo diste por mí.
Aquí estoy, mi vida a ti entrego,
Tuyo soy, Señor. (x4)"""),

("Ya no soy un esclavo", "", "G", """G
Me envuelves hoy con una canción
 C D G
Melodía de tu amor
Cantas libertad en mi adversidad
Hasta que huya el temor

 C D G
Ya no soy un esclavo del temor
 Em7 D G
Yo soy hijo de Dios
Ya no soy un esclavo del temor
Yo soy hijo de Dios (Na na nara)

 G Bm
Desde el Vientre fuí escogido en ti
 C D G
Me llamó el amor de nuevo nací
Recibido en ti, tu sangre en mi fluyó

 Em7 D G C
Estoy rodeado y por los brazos del padre
Estoy rodeado por canciones de libertad
Fuimos liberados de ataduras
Somos los hijos y las hijas
Cantaremos libres
Hoo hoo hoooo ///

Abriste el mar para que yo camine
Tu amor ahogó todo el temor
Me rescataste y yo cantaré
Yo soy hijo de Dios… //"""),

("Amamos tu presencia", "", "Intro: B - C#m - G# - A", """E C#m
Encuentro sanidad, encuentro libertad
 B A
En tu presencia
 E
Encuentro Hoy perdón
 C#m B
encuentro salvación en tu presencia
 B C#m G#m A
Correremos hacia a ti
el Cielo hoy está aquí

 E C#m B
Amamos tu presencia oh Dios
 A E
Amamos tu presencia oh Dios
A C#m F#m
Amamos tu presencia oh Dios"""),

("Dios Imparable", "", "Intro: F#m D F#m E Sus4", """A sus2/C# D sus2 D/E sus2 E
Eres alabado, Eres exaltado
Tu nombre levantamos
aleluya, aleluya
Eres adorado te glorificamos
Tu nombre levantamos
aleluya, aleluya

 D E F#m D E F#m
A una sola voz, nos unimos hoy
 D E F#m7 E Sus4 E
Te cantamos Dios en adoración

 D E
Dios imparable, Dios de imposibles
 A E/G# F#m
Inigualable, eres invencible
 D E
No tengo temor en mi corazón
 F#m7
Tú tienes el control
 B maj9 E Sus4 F#maj7
No me falta nada si te tengo a ti

 F#m E/G# A E/C# D/B
Y yo sé quién va conmigo va por mi
Y quien a mis enemigos hace huir"""),

("Eres mi plenitud", "", "E A B7", """E A B7 E/C#m B/G#m
Cristo Jesús eres mi plenitud
 A B7 E
Cristo Jesús eres mi plenitud

 A
Si te tengo a ti, lo tengo todo
B E/C# B/G#
Mi amado, mi tesoro
 A B E
Fuera de ti, nada deseo, Señor"""),

("Aquí estas", "", "Am F C", """ Am F C
Aquí estas te vemos mover
 G Am
te adorare, te adorare
Aquí estas obrando en mi
te adorare, te adorare

F
milagroso abres camino
cumples promesas luz en tinieblas
mi Dios así eres tu

aquí estas sanando mi corazón
te adorare te adorare
aquí estas tocando mi corazón
te adorare te adorare

Así eres tu, así eres tu
Aunque no pueda ver estas obrando
Siempre estas siempre estas obrando"""),

("Hashem es varón de guerra", "", "Am G Em", """ Am G Em G
Hashem es varón de guerra
Hashem es su nombre.
 Am G F
Hashem es mi fortaleza y mi cántico

 C G F
El es mi Dios y yo le alabaré
Dios es mi padre y lo enalteceré
 C G Am G F
El es mi Dios y yo le alabaré
Dios es mi padre y lo enalteceré"""),

("A tus pies", "", "Asus2 E", """ Asus2 E
A tus pies arde mi corazón
 F#m Dsus2
A tus pies entrego lo que soy
Es el lugar de mi seguridad
Donde nadie me puede señalar

 Dsus2
Me perdonaste
 E
Me acercaste a tu presencia
 F#m
Me levantaste
 E
Y hoy me postro, adorarte

 A/C# Dsus2
No hay lugar más alto
 E
Más grande
 F#m
Que estar a tus pies
 C#m7
Que estar a tus pies

 Dsus2 E
Y aquí permaneceré
 A E/G# F#m
Postrado a tus pies
 F#m C#m7
A los pies de Cristo."""),

("Dios ha sido bueno", "", "", """Dios ha sido bueno
Dios ha sido bueno
Dios ha sido bueno
Bueno es Dios

Su bondad me alcanzó
Su amor me rescató
Su gracia me salvó
Bueno es Dios
Por eso cantaré
Y siempre alabaré
Y nunca olvidaré
Bueno es Dios

Mis manos alzaré
Mi vida entregaré
Mi voz levantaré
Bueno es Dios

Y no me cansaré
De darle todo a él
Yo quiero serle fiel
Bueno es Dios"""),

("Dios ha sido fiel", "", "", """Puede oscurecer
Puedo ser rodeado de lo que nunca esperé
Estar en la neblina de un gran dolor
Y pensar que no hay salida para mí
Pero hay una verdad
Que nunca me dejará desfallecer
Y aunque yo no la deba merecer, me sostiene

Dios ha sido fiel
Dios ha sido fiel
Su fidelidad, nunca acabará
Permanecerá, siempre crecerá
Él ha sido fiel
Y por siempre lo será

Aunque en mi vida haya duda en plena noche oscura
Él extiende sus brazos de amor
Y estando es la tormenta
Su mirada me alienta
Y otra vez me deja ver que ha sido…"""),

("Cuan bello es el Señor", "", "D Em", """D Em
Cuan bello es el Señor,
A D
cuan hermoso es el Señor
Cuan bello es el Señor
hoy le quiero adorar

D7 G
La belleza de mi Señor
A F#m/ Bm
nunca se agotará
 Em
La hermosura de mi Señor
A
siempre resplandecerá."""),

("Tu Misericordia", "", "E", """E
Tu misericordia incomprensible es Señor"""),

("Dios de Pactos", "", "Asus2 Dsus2", """ Asus2 Dsus2
Dios de pactos que guardas tus promesas
 Dmaj7 Bm7 E6sus4 E
Que cumples tu palabra, Que guías mi destino
Dios de pactos confío en tus promesas
Descanso en tu palabra, Por tu gracia estoy aquí

F G
En la intimidad, al abrigo de tu gloria
 C Em6 Am7 Am7/G
Puedo estar, junto a ti
Al ver tu santidad estoy maravillado
Ante ti y tu amor
F Dm Dm7/C E7sus4 E7
Nunca más seré igual al salir de este santísimo lugar

(ESTRIBILLO)
Tengo redención por la sangre que descansa
En tu altar para mi
La gracia y el perdón son los frutos de vivir
En comunión y adoración
Nunca más seré igual al salir de este santísimo lugar"""),

("Como en el Cielo", "Elevation Worship", "G D A", """ G D A
La atmósfera cambiando está

Tu espíritu está aquí
Es evidente tu mover
Tu espíritu está aquí //

G
Llena este lugar
 Bm
Derramando tu amor
 A (F#m)
Tu amor me envuelve

He venido por ti
A tus brazos de amor
Tu amor me envuelve"""),

("Vivo estas", "", "Bm7 Fm# Gsus2", """ Bm7 Fm# Gsus2
Roto estaba mi corazón
 Gsus2 Bm7 Asus4
Pero tu mano me rescató
Del polvo yo volví a nacer
La salvación en ti encontré

Tu amor no puedo expresar
Te seguiré por la eternidad
En tu gracia caminaré
En libertad siempre viviré

En ti, en ti, en ti, soy libre
Sé exaltado, sé exaltado
Tu amor, tu amor, tu amor no se acaba
oh oh oh
Tú vivo estás en mí
No hay nadie en tu lugar
Te necesito Dios
Eres mi libertad, oh-oh-oh

Al pasar por la oscuridad
Su luz siempre me guiará
Mis cadenas Jesús rompió
Con su mano me rescató

Este mundo terminará
Te seguiré hasta el final
Haz en mí, Dios tu voluntad
Venga tu reino a este lugar"""),

("Gracia Sublime es", "", "A", """A
Quien rompe el poder del pecado
 D
su amor es fuerte y poderoso
F#m E D
El rey de gloria el rey de majestad
Conmueve al mundo con su estruendo
Y nos asombra con maravillas
El rey de gloria el rey de majestad

Gracia sublime es, perfecto es tu amor
Tomaste mi lugar, cargaste tu mi cruz
Tu vida diste ahí y ahora libre soy
Jesús te adoro por lo que hiciste en mí

Pusiste en orden todo el caos
Nos adoptaste como tus hijos
El que gobierna con su justicia
Y resplandece con su belleza

PUENTE: //A D //
Digno es el cordero de Dios,
Digno es el rey que la muerte venció////"""),

("Tumbas a Jardines", "", "A D", """ A D A
Un mundo busqué
y no pudo llenarme
 Fm# E sus
Ningún tesoro que pueda ganar
Me saciará D2
Mas llegaste tú me diste vida nueva
Y cada deseo se cumplirá
Aquí en tu amor, ¡eh!

Oh, no hay nada A
Nada mejor
No hay nada Fm#
Nada mejor
No hay nada D
Nada mejor que mi Dios A

Vengo a ti
Sin miedo, sin reservas
Cada fracaso has visto Señor
Y aún tu amigo soy
Porque el Dios de los montes
Es el Dios de los valles
No hay lugar que me pueda alejar
De tu gracia y amor

 A D D D A
Cambias lamento en danza
De cenizas traes vida
Cambias culpa por gloria
Sé que solo Tú lo harás #F D A

De las ruinas y tumbas
Nacen nuevos jardines
Resucitas los huesos
Sé que solo Tú lo harás
Uoh-oh-oh-oh"""),

("Espíritu Santo lléname", "", "A D A", """A D A
Espíritu Santo lléname
 F# E
Derrama tu gloria sobre mi
 D
Inunda mi alma
 A
En tu presencia
 F# E
Quiero vivir en tu verdad
 D A F# E
En tu verdad"""),

("Hosana (Hosanna a Cristo nuestro Rey)", "", "G", """G
Hosanna a Cristo nuestro Rey
León de la tribu de Judá
Hosanna a Cristo nuestro Rey
Nuestro Dios ha vencido y vencerá

 C G C G C G
Hosanna, gloria, honores a
 Am D
nuestro Rey
Hosanna, gloria, honores a nuestro Rey

Hosanna a Cristo nuestro Rey
traemos ofrendas de amor
Hosanna a Cristo nuestro Rey
Voces de júbilo ante El"""),

("Lo harás otra vez", "", "Intro: D B A", """D
Muros rodeando estoy
A/c#
pensé que caerían hoy
Bm/d A
mas nunca me has fallado Dios
la espera terminará
sé que has vencido ya
nunca me has fallado Dios

D/f -> (F#m) E/g#
En Ti confiaré
 A
Tu promesa sigue en pié
 D
Tú eres fiel
Confiado andaré
en Tus manos estaré
siempre has sido fiel

La noche acabará
Tu Palabra se cumplirá
mi corazón te alabará
Cristo, mi Salvador
cúbreme con Tu amor
mi corazón te alabará

//A/c# / D
Yo sé que Tú mueves montañas
//E/g# / A
yo creo en Ti, sé que lo harás otra vez
Abriste el mar en el desierto
yo creo en Ti, sé que lo harás otra vez//"""),

("La generación que danza", "", "D7 Bm7", """ D7
Tu gracia nos hace danzar
 Bm7
Con todas las fuerzas celebrar
 G D
Danzaremos, libres, por tu amor
Tu gloria nos hace cantar
Tu santo nombre levantar
Cantaremos, gloria a ti Señor

 Em F#m
Nuestro corazón comienza a desbordar
 G A
Al conocerte a ti, no podemos callar
 D
Seremos la generación que danza
 Em7 G
Goza tu misericordia oh Dios,
 D
Tu misericordia oh Dios
Seremos la generación que Canta
Y que celebra dándote gloria Oh Dios"""),

("Que se llene tu casa", "", "Am7 G C", """Am7 G C Dm7 C G
Sálvanos, restáuranos
Am7 G C F
Avívanos, oh, Dios
Sálvanos, restáuranos
Avívanos, oh, Dios
Oh, Dios

 C G
Que se llene tu casa
 Am7 F
con tu gloria
 C G F
Llena tu casa, oh, Dios"""),

("Golpe de espada", "", "", """Golpe de espada
es la alabanza
golpe de guerra
que sale de Dios
Cantos de gloria
traen la victoria
en la batalla del
pueblo de Dios

//y cada golpe de la espada
de Dios, es con pandero
con trompeta y tambor//

Sera con cantos de jubilo
cantos de jubilo
cantos de jubilo
cantos de jubilo"""),

("El Volverá", "", "D G D", """ D G D
Como el relámpago que sale del oriente
 G D A-G C D
y va al occidente así será, cuando venga el Señor
Como un ladrón que viene en la noche
y nadie lo espera así será cuando vuelva Jesús

 D-G-A Bm G
El volverá y a su gloria me transformará
Regresará y en una nube me arrebatara
 Em D/F# G A D
con poder y gran gloria, Cristo Jesús volverá

Con voz de mando descenderá del cielo
y toca trompeta así será, cuando vuelva el Señor
El llamará a los que han dormido
Y a los que hemos creído
así será cuando Vuelva Jesús

Em D/F# G D/F#
Velad y orad el tiempo se acerca ya
 Em D/F#
Purifícate a Él, conságrate a El
G/B A G
que tu Señor volverá"""),

("Tus Cuerdas De Amor", "", "Intro: F# Dm7 Bb F F", """ Dm7 Bb F
Aunque pase el tiempo sé
 Dm Bb F
que tu promesa cumplirás
nada en ti se perderá
esa es mi seguridad

 C
Tus cuerdas de amor
 F C/e Dm
cayeron sobre mí
tus cuerdas de amor
cayeron sobre mí F C

 C F
Es tu amor que me sostiene
 Dm7 Am7
el que me levanta, el que me da paz
 Bb
me da seguridad

 Gm Dm7
De lo que vendrá, Tú tienes el control
 C9
nunca pierdes el control
 Dm7 Bb F
Escucho el eco de tu voz
resonando en mi interior
tus palabras me sostendrán
esa es mi seguridad
Los velos se están cayendo hoy
hoy puedo ver con claridad
mi fe se está encendiendo hoy
y hoy me vuelvo a levantar"""),

("Yo quiero más de ti", "", "Intro: Emaj7, F#/E, Ebm7, G#m", """B2 E2/B
Yo quiero mas de Tí
 F#/B B F#/A#
y habitar en tu presencia
 G#m B+5/G# B/G#
menguar para que crezcas Tú
y cada día seré más como Tú

 B2/Eb Emaj7 F#/E
Quebranta mi corazón
 D#m G#m
quebranta mi vida
 C#m7 F# B A/B
te entrego mi voluntad a Tí
todo lo que soy, Señor
todo cuanto tengo es tuyo
yo quiero menguar para que crezcas Tú

Final
Yo quiero menguar para que crezcas tu
Yo quiero menguar para que crezcas tuuuuuu-uhhh"""),

("Es exaltado", "", "F F/A", """F F/A
Es exaltado en lo alto.
 Bb
Exaltado es el Rey,
 Gm9 C
le alabaré.
F F/A
Es exaltado en lo alto.
 Bb C Dm C/E Dsus4
Exaltado y yo le alabaré.

D Gm Dm C F
El es Señor, por siempre
 C/E Dm Dm/C
él reinará.
Gm Dm C
Su creación
 F C/E Dm Dm7
por siempre se gozará.
Bb Gm7
Es exaltado en lo alto.
 C7 F
Exaltado es el Rey."""),

("Majestad", "", "", """MAJESTAD, TE ADORO MAJESTAD
DOY A CRISTO TODA GLORIA, ALABANZA Y HONOR
MAJESTAD, REINO Y AUTORIDAD
DESDE TU TRONO, FLUYE POR SIEMPRE TU MAJESTAD

ALABAD Y EXALTAD EL NOMBRE DE CRISTO
MAGNIFICAD Y GLORIFICAD A CRISTO EL REY
MAJESTAD, TE ADORO MAJESTAD
AQUEL QUE MURIÓ Y RESUCITÓ ES REY Y SEÑOR"""),

("Cuán grande es Él", "", "", """MI CORAZÓN ENTONA LA CANCIÓN
CUAN GRANDE ES EL
CUAN GRANDE ES EL
MI CORAZÓN ENTONA LA CANCIÓN
CUAN GRANDE ES EL
CUAN GRANDE ES EL"""),

("Alabemos", "", "Am", """Am
Alabemos con panderos C
Alabemos con salterio G
Alabemos todos juntos F
Alabemos, Alabemos
Alabemos con trompetas
Alabemos con las flautas
Alabemos con las palmas
Alabemos, Alabemos

Am C
Todo lo que tenga vida
 G
Todo lo que aun respira
Dm F
Con canciones de alegría
Am G
Alabemos, Alabemos
Levantemos manos santas
Celebremos con la danza
Que se escuche la alabanza
Alabemos, Alabemos

C Csus C G
Te Alabamos Dios
 Dm F Am G
Te Alabamos Dios"""),

("Fiesta", "", "Cm", """ Cm
Lo que se canta en el cielo
 Fm
cantamos en la tierra
 Bb
Al que se adora en el cielo
 G
Adoramos en la tierra
 Ab Gm
Al Santo, Digno
 Fm Eb G
al Cordero que vive para siempre
Hacemos

Cm Fm
Fiesta, hoy hacemos una fiesta
 Bb
Unidos hoy danzamos
con gozo celebramos
 G
oh uh oh uh oh
Fiesta, Hoy hacemos una fiesta
En la tierra cantamos
juntos gritamos
oh uh oh uh oh"""),

("Espíritu Santo bienvenido", "", "C F", """ C F
Espíritu Santo bienvenido a este lugar
 G F C
Jesucristo bienvenido a este lugar
 C C/E F
Padre omnipotente de gracia y amor
 G C
Bienvenido a este lugar

 C
Bienvenido espíritu de Dios
 Am
Damos Gloria solo a ti Señor
 G
Bienvenido espíritu de Dios
 Dm G
Hoy rendimos coronas a tus pies"""),

("Pablo y Silas", "", "A# - D# - Gm - F", """D# Gm F
//En mí angustia yo clamé a tí
No te veo pero te puedo sentir
Tú estás aquí
Te puedo sentir//

D# Gm
Y si Pablo y Silas te adoraron y las cadenas les fueron quitadas
F
Así quiero adorarte

 D#
Tú amor rompe cadenas
 F
No tiene fronteras
 Gm
Tú luz rompe condena
No tiene barreras Dios, Dios, Dios

///El velo que impedía tu presencia en mí vida
Se rompió, se rompió///

///Llegó Jesús el que pelea mis batallas
 Gm F
Llegó Jesús el que mueve las montañas
 Gm
Llegó mi amado
 Dm
Llegó mi amado///"""),

("Preciosa sangre", "", "INTRO: Bm - A - F#m - C#m", """Bm A F#m C#m
Preciosa sangre se derramó
Preciosa sangre fluyó por amor
Bm A F#m
Sobre ti el dolor
D
Tus venas lloraron
 A F#m C#m E
Jesús, Jesús, Jesús

D A
Hay poder en la sangre
F#m E
Que fluyó por amor
D A
Hay poder en la sangre
 E
Que Él derramó

 Bm F#m
Tu sangre me transformó
 D A E
Tu sangre me perdonó
 Bm F#m
Tu sangre me limpió
E
Tu sangre me sanó"""),

("Libre para adorar", "", "Introd.: D F#m7 G Em", """D F#m7
Nada me separara de Tu amor por mí
 G Em
Pues fue tu amor por mi que arrebato mi corazón
D F#m7
Nada me distanciara de tu amor por mí
 G Em
Pues fue tu amor por mí que despertó esta canción, ohh

 G Bm7
Libre para adorar
 A
Rasgar mi corazón
 Em
Y demostrarte mi pasión, Jesús Soy libre…

…Nada me separará de tu amor por mí

G Bm7 A Em
Santo, eres Santo, inmensurable sin igual eres mi canción"""),

("Libre para danzar", "", "Intro: D – G – Bm - A", """D
Los ciegos verán por ti
los mudos cantarán
G
los muertos vivirán
los pueblos te adoraran
Bm A
Las tinieblas huirán
por ti yo grito

 D
Yo soy libre, (Yo soy libre)
Libre para correr
Libre para danzar
Libre para vivir por ti
Yo soy libre (Yo soy libre)

UOoOoOh (UOoOoOh) Uo oh oh oh oh
Libre (libreee)
Libre para correr… Yo soy libre"""),

("Vine a adorarte", "", "D A Em G", """D A
Tú eres la luz
 Em Gadd9
Que brillo en las tinieblas
 D A Gadd9
Abrió mis ojos pude ver
Mi corazón adora Tu hermosura
Esperanza de vida eres Tú

 D A
Vine a adorarte, vine a postrarme
 D/F# Gadd9
Vine a decir que eres mi Dios
 D A/C#
Solo tú eres grande Solo tu eres digno
 D/F# Gadd9
eres asombroso para mi

 D A
Tu eres el rey
 Em7
Grandemente exaltado
 D A Gadd9
Glorioso por siempre Señor
El mundo que creaste humilde viviste
Y pobre te hiciste por Amor

 A D/F# G
Nunca sabré cuanto costo
 A/C# D/F# G
Ver mi maldad sobre esa cruz ////

Oh, oh, oh! Asombroso! Rey de Gloria!
Oh, oh, oh! Asombroso! Poderoso!"""),

("Abre mis ojos oh Cristo", "", "E9", """E9
Abre mis ojos oh Cristo
B/Eb
Abre mis ojos Te pido
 E9/A A
Yo quiero verte
 E9
Yo quiero verte

 B Sus4 E/C#
Y contemplar tu majestad
B Sus4/A B Sus4 B
Y el resplandor de tu gloria
 B Sus4 E/C#
Derrama tu amor y poder
E/A B Sus4 B
Cuando cantamos santo santo

 E Sus4
Santo, Santo, Santo
B/Eb
Santo, Santo, Santo
 E9/A A
Santo, Santo, Santo
 E Sus4
Yo quiero verte"""),

("Vamos A Cantar", "", "E - Cm7 - B - A - E", """Vamos a cantar
Con la música del cielo vamos a cantar
Alegres porque escuchas cuando
Cantamos para exaltar tu nombre

Amamos todo de ti
Cielo y tierra te adoran
Los reinos se rinden
Hijo de Dios tú eres por quien
Tú eres por quien Vivimos hoy

Tu eres quien nos liberta
Eres la luz que guía
Como fuego ardiente
Hijo de Dios tú eres por quien
Tú eres por quien vivimos hoy"""),

("Yo danzo en el río", "", "Intro: Bm G D A", """ G Bm
Un estruendo de muchas aguas
 A
Se escucha aquí
G
Trae sanidad, trae libertad
Bm A
Gozo y salvación

G
Es el río del Señor
 Bm A
Que nace de su corazón
G
Nunca se secará
 Bm A
Y esta ciudad se alegrará.

 D A
Yo danzo en el río, Yo danzo en el río
 Em Bm A
En el río de Dios, en el río de Dios

G
Ríos de vida están brotando
En mi interior
Fuente inagotable
Que viene del cielo fluye aquí

 Bm G D A
Hay vida en el río de Dios
Hay gozo en el río de Dios
Soy libre, libre
El río de Dios está aquí"""),

("Poderoso Dios", "", "C Am9", """C Am9
Al que está sentado en el trono
 F Dm G
y al cordero, sea el honor
 C Am
sea la gloria, sea la honra
 F Dm
sea el dominio
 G
por los siglos de los siglos...

 C
Poderoso Dios
 Am
Poderoso Dios
 F Dm
Poderoso Dios
 G
Mi alma clama por ti.."""),

("Eres Todopoderoso", "", "Bm G D A", """Bm G D A
La única razón de mi adoración eres tu mi Jesús
Mi único motivo para vivir eres tu mi señor
Mi única verdad está en ti eres mi luz y mi salvación
Mi único amor eres tu Señor y por siempre te alabaré

Tú eres todopoderoso eres grande y majestuoso,
eres fuerte, invencible y no hay nadie como Tú"""),

("Atrae Mi Corazón", "", "C9 F9", """C9 F9
Es a Ti a quien anhelo
 Dm9
Es por Ti que yo suspiro
 F G9
Más allá del velo yo voy
 Am7 G9 C9
a decirte que te quiero

 F9
Atrae mi corazón
 Dm7
Atrae mi corazón
 F9 G9
Atrae mi corazón Jesús
 Am7 G9 C9
Me muero de amor por Ti

Quiero que el mundo sepa
Quiero que el mundo vea
Que Tú eres mi amado y yo soy tuyo
 F9 Dm7 Am7
Yo en Ti y Tu en mí Jesús
 G9
Este es el pacto"""),

("Mi corazón te adora", "", "(Bb-Eb-Cm7)", """ Bb Eb
Mi corazón te adora, mi corazón te adora
 Cm7 Eb
Jesús, Jesús
Bb-Cm7 Bbm-Eb F5-F
Jesús, Jesús

Bb
Todo es para ti
Fm F-Fm
Todo es para ti
 Cm7 Eb F5-F
Jesús, Jesús

Bb
Todo me rindo
Eb Cm7 Bbm-Eb
Todo, Jesús, Jesús

 Bb Eb
Mi corazón te adora, mi corazón te adora
 Cm7 Bbm-Eb F-Bb
Jesús, mi Amado"""),

("Eres el mas hermoso (Salmo 45)", "", "Bm G D A", """Bm G D A
Mi corazón reboza de palabras buenas
 Bm G A
Dedico a ti esta canción
Bm G D A A/C# G
Mis labios cantarán esta poesía a ti, a ti

 Bm G D A
///Eres el más hermoso///
 A A/C# G
De los hijos de los hombres

Tu trono es eterno, reinas para siempre
Lleno de justicia y amor
El cetro de tu reino es el cetro eterno, //Oh Dios//

Em D G A Em D G A
Jesús triunfarás y tu verdad reinará"""),

("Hosana (Hossana al Rey)", "", "Bm A", """Bm A
Levantamos un clamor
F#m G
por sanidad y redención
Muestranos lo que Tu ves
los secretos de Tu corazón
Un pueblo unido pide hoy
Tu libertad y salvación
Armanos con Tu valor
lo que deseamos es revolución.

G A G
Que el cielo se parta en dos... inundanos
 A
en el desierto broten ríos
 Bm
vida sopla hoy

 Bm D
Hossana al Rey de Salvación
 Em
Hossana al Dios Altisimo
 G A Bm
Hossana, Jesucristo, Jesucristo es Rey

G A G A Bm C#m
Hossana Hossana Hossana al rey"""),

("Acuérdate oh Señor", "", "Eb/G G A D", """ Eb/G G A D
Acuérdate oh Señor
 D G Bb/D D
de las naciones de la tierra acuérdate
 Eb/G Asus4 -A# Ab/Bb D
que tu favor y tu amor
sean derramados sobre el mundo oh Señor
 Asus4 -A# Asus D
En tu bondad acuérdate
En tu bondad acuérdate"""),

("Sana Nuestra tierra", "", "Intro: G Em C Am D", """G Em C
Vengo a Ti, guíame
 D G
Santifícame en Ti
 Em
Yo quiero andar
 C
En tu verdad
Tómame, abrázame
Mi corazón hoy vuelvo a Ti
Solo a Ti

G Em
Quiero humillarme, buscar tu rostro
C Am D
Hoy me arrepiento, delante de Ti
Vengo a invocarte, inclina tu oído
Escucha y perdona, mi rebelión
Am Em D
Sana nuestra Tierra
Sana nuestra Tierra

Eb F G
Escucha hoy mi oración
Eb F D
A Ti levanto mi clamor"""),

("Sananos", "", "E A", """E A
Somos tu pueblo
Y hoy venimos humillados ante Ti
 E A C#m B A
Somos tu pueblo, necesitados de Ti

Hemos pecado
hemos dejado tu camino tu verdad
Nos humillamos
nuestra tierra sana hoy

 B C#m
¡Sananos! ¡Sananos!
 A E C#m B
Es el clamor de este pueblo, Humillado ante Ti
¡Sálvanos! ¡Sálvanos!
Es la oración de tus hijos, Postrados ante Ti.

Somos tus hijos, Reconocemos, nuestro orgullo nuestro error
Somos tus hijos, Te pedimos hoy perdón

 B C#m
Invocamos hoy Tu nombre, Y
 A B
buscamos tu favor
 B C#m
Que tu luz nos alumbre
 A G#m F#m E B
para honrarte a Ti Señor"""),

("Los muros caerán", "", "Cm - Ab - Bb Cm", """ Cm2 Bb
Cuando le canto la tierra se estremece
Cm/Ab Bb Cm
los muros caerán
 Cm Bb
cuando le adoro se rompen las cadenas
 Ab Bb Cm
Los muros caerán

 Cm Ab
Los muros caerán los muros caerán
 Bb Gm Cm
Al sonar mi cantico caerán
Los muros caerán los muros caerán
con gritos de júbilo caerán

cuando yo danzo aumenta Dios mis fuerzas
los muros caerán
cuando yo grito mis enemigos huyen
los muros caerán

Caen los muros, caen los muros (X 8)
Saltando, saltando los muros caerán
Gritando, gritando los muros caerán"""),

("Es aquí, es ahora", "", "INTRO: //D,(Am-C-C#-D) F, E//", """D
Es aquí, es ahora
Mueve en mi, Dios haz tu obra
 G D F
Muévete con tu poder sobrenatural

Necesito acercarme
Yo deseo embriagarme con tu amor y tu poder sobrenatural

 A G D
Dios sobrenatural
 A G
Dios sobrenatural

 D
Muévete en las naciones
 E
Muévete en los corazones
 G C D
Muévete con tu poder sobrenatural
Muévete en mi vida
Muévete cada día

//// F - C/E - D ////
Sobrenatural
Sobrenatural
Sobrenatural"""),

("Mi Pan mi Luz", "", "F2(9) G C2/G", """ F2(9) G C2/G
Al entrar a tu santo lugar
Me asombra que me pueda acercar
 F2(9) G Am
Para ver tu gloria y tu belleza
 Bb G
Y adorarte en intimidad

En confianza yo me puedo acercar
De tú mesa quiero participar
Todo lo que puedo hacer es postrarme
Y con mis labios proclamar

 C2/G G Am F
Mi pan, mi luz, mi oración
 C2/G G
Eres tú Jesús
 C2/G G Am F
Mi Dios, mi amor y mi canción
 C2/G G F Em
Eres tú Jesús, sólo Tú

 Am Em F C G
Me cuidas, me abrazas
Me cantas, me amas

 D A Bm G
Mi pan, mi luz, mi oración
 D A
Eres tú Jesús
Mi Dios, mi amor y mi canción
Eres tú Jesús, sólo Tú"""),

("Sobrenatural", "", "G D/F# Cadd9", """G D/F# Cadd9
Sobrenatural
Em7 D/F# Cadd9
Eres Dios sin Igual
G D/F# Cadd9
Dueño del Cielo y Mar
 Am C
Sobrenatural
Sobrenatural
Habitas la eternidad
Eres el manantial
Sobrenatural

G D/F# Em
Dios de mi vida eres Dios
 Cadd9 G
De los cielos eres Dios
 D/F# Em
De los mares eres Dios
Cadd9 G
Sobrenatural
De la tierra eres Dios
Mi sustento eres Dios
Siempre eterno eres Dios
Sobrenatural"""),

("La Anunciación", "", "Na ra na ra na → D C# F# / G E", """ D Asus2
El Ángel Gabriel fue enviado por Dios
 F#m7 Esus4 E
Algo grande estaba por suceder
 D Asus2
A una mujer llamada María
 F#m Esus4 E
De la ciudad de Nazaret

C#m7 D
Le dijo no temas
 C#m7 F#m7
Gracia has hallado ante Dios
C#m7 D
Un hijo darás a luz
 G Esus4 E
Lo llamarás Jesús

 D A E F#m7
Será grande Hijo del Altísimo
 D A Esus4 E
Y reinará para siempre.
 D A E F#m7
El Señor Dios le dará el Trono
 D A G
Y su reino no tendrá fin

Ella preguntó: ¿cómo puede ser?
Si no soy nada especial
Pero sé que para Dios No hay nada imposible
Hágase en mi hoy su voluntad

G Dsus2 F C Bbsus2 Gm Esus4 E
Admirable, consejero, príncipe de paz"""),

("Eres sorprendente", "", "INTRO: Bb – Cm – Eb – F – Cm – Bb – F", """Bb
Nunca imaginé
Nunca lo esperé
Cm
Nunca lo planeé
No lo anticipé
 Eb
Lo que planeabas Tú
 F Bb Eb – F – Bb
Por mucho superó mi imaginación

Tu gracia y favor
Tu inmensurable amor
Nunca me dejó, Me favoreció
Lo que pensabas Tú
Siempre superó lo que pensaba yo

Gm Jesús, eres sorprendente
Cm Lo mejor ha sido conocerte
 Eb
Cuando pienso en tus maravillas
 F D G
Caigo de rodillas

 Bb Cm
Eres inexplicable
 Eb F
Tu amor es interminable
 Bb Cm
Eres insuperable
 Eb F
Amarte es inevitable

C Nunca imaginé
 Dm
Todo lo que Tú pensabas, Dios
 F G
Cada día eres la razón
 C
De vivir tu sorprendente amor"""),

("Grande y fuerte", "", "Am F Em Am", """ Am F Em Am
Grande y fuerte es nuestro Dios
 Am F G Asus4 - A7
Grande y fuerte es nuestro Dios

 Dm G
Vestido en majestad
 Dm Am
coronado con poder
 Dm G Am G A7
Digno De toda la adoración
Vestido en majestad
Coronado con poder
 F G Am
Toda Gloria y honra sean para ti

La do mi fa mi do la … (punteo de bajo)
Grande Fuerte es nuestro Dios
¡Grande Fuerte es nuestro Dios! X4"""),

("Bajando el cielo", "", "G D Em Bm C G C D", """G D
Hey! Alcemos nuestra voz
 Em
gritemos al mundo hoy
 C
lo que tenemos en el corazón
Hey! No hay nada que esperar,
es hora de adorar
y hacerlo 24/7

D Em
Y con pies sobre la tierra
C G
pero ojos en el cielo
D Em
yo con mi adoración
 C D
estoy bajando el cielo

G D
Cantamos y saltamos y lo hacemos para él
 Em Bm
Cantamos y saltamos y lo hacemos para él
 C G
Para que Jesús fije sus ojos aquí
 C D
El cielo y la tierra hoy se van a unir

 C D
Estoy bajando el cielo

G D Em Bm
Jesús es mi pasión, Jesús es mi pasión
C G Am D G
Jesús es mi pasión, enamorado estoy de Él //"""),

("El fuego en tus ojos", "", "F Dm C Gm7 Bb", """Dm C
Me acerqué, permanecí
 Gm
Y tu mirada me consumió
Bb C
Yo soy solo tuyo

 Dm C
El fuego de tus ojos
 Gm Bb C
Me hizo enamorarme más
 Dm C
Quemó los otros amores
 Gm Bb C
Quemó los otros amores

Todavía tengo hambre
Todavía tengo leña
Yo quiero quemar
Yo quiero quemar"""),

("Siento tu amor", "", "C", """ C
Siento tu amor
 F
que viene sobre mi
 C Am G
siento que una nube desciende
 F G
Llévame a tu hogar, arriba
 Em Am
que mi lámpara esté siempre encendida
 F Dm G
quiero adorarte bendecirte Señor"""),

("No tengo nada", "", "", """A tu lado es donde quiero estar
Sentirte cerca es mi debilidad
Estar postrado ante tu majestad
Es donde encuentro totalmente mi paz
Hoy dejo atrás todo mi pecado y maldad
Me centro en ti te doy el primer lugar
Abrazarte y no soltarte jamás
Es lo que haría toda la eternidad

Yo no tengo nada para darte
Solo un corazón que busca amarte
Yo no tengo nada para darte
Solo un corazón que busca adorarte
Yo no tengo nada para darte
Que busca un momento, solo un encuentro contigo Jesús

Muévete en mi interior
Que tu fuego consuma todo lo que soy"""),

("Te conozco bien", "", "Am F", """Am F
Sé que abriste el mar un día de victoria
G Am C D
Como un Libertador
Sé que diste pan y agua de la roca
Cuando quemaba el Sol
Am F Dm
Sé que la muralla que cayó, fue por tu mirada
F E
Te conozco bien

Sé que las tormentas guardan reverencia al escuchar tu voz
Que mil gentes hambrientas comen en tu mesa con multiplicación
Sé que ovejas negras como yo, hallaron su Pastor
Te conozco bien

Cadd2 G F (F – G)
Mira bien que te conozco y quiero alabar
Mira bien que te conozco y quiero adorar
Bb2 F
Me has dado un nuevo vivir
Bb2 F G Am
Me arrodillo ante Ti, Te conozco bien"""),

("Quiero conocer a Jesús", "", "C D", """ C D
Mi orgullo me sacó del jardin
 Em Bm7
Su humildad puso el jardín en mi
 C
Y si vendiese lo que tengo
 D Em Bm7
A cambio de su amor yo fallaría
 C
Porque su amor no se compra
Ni se merece
su amor es un regalo
de gracia se recibe //

Quiero conocer a Jesús
Quiero conocer a Jesús // //

 D C D Em D
Mi amado es lo más bello
 G D
Entre millares y millares ////"""),

("Somos Libres", "", "Bb9 F/A", """Oh oh oh oh ohhh
Bb9 F/A
Somos perdonados, cantamos tu redención
 Gm
Con fuego en el corazón
 Eb Eb/C
con fuego en el corazón
Nada nos detiene, vencemos la oscuridad
Con fuego en el corazón

Somos libres, una generación que Canta tu gracia
Tú eres aquel en quien nos movemos
Tuya es la gloria
Hay un fuego que arde en el corazón
Que nunca se apagará
Somos libres y tuya es la gloria

Resucitados, vivimos para ti
La pasión no morirá, la pasión no morirá

Eb
Resucitaste con poder, te levantaste
 Bb9
y nos levantamos, nos levantamos
Hacia el mundo que tú amas, caminaremos
y nos levantamos, nos levantamos
 Cm Eb
Nos levantamos"""),

("Anclado", "Majo Solis", "Intro C#m-B-A", """C#m
En todo tiempo
 B A
En cada paso, eres fiel
En la tormenta
Eres mi fuerza, eres fiel
En la tempestad
Tu paz me abraza
En debilidad
Tu amor me levanta
Oh Dios

En ti esperaré
En tu gracia confiaré
Dejo todo atrás
Y me rindo a tus pies
Anclado estoy en ti
Pues tu amor no fallará
Te amo, te amo

Mi Redentor
Mi Salvador, eres fiel
Mi Padre Eterno
Eres mi luz, eres fiel
Y en tu promesa
Pondré mi confianza
Tú eres mi fuerza
Yo confío en ti
Mi roca eterna
Y mi esperanza
Tu amor es eterno
Yo confío en ti"""),

("Mi mejor adoración", "", "G#m7 E", """ G#m7 E
///Mi mejor adoración es mi corazón
 B D#m7
rendido a tus pies///
 G#m7 E
Mi mejor adoración es mi corazón
 B F#sus4 F#
rendido a tus pies

CORO
 B
Entonces me rendiré y adoraré
 E
con todo mi corazón
 C#m7 E
Derramaré mi voluntad,
 G#m7 E F#
ante tu trono yo te voy a adorar,
yo te voy a adorar

Unidos, estamos, para adorar al Rey
Rendidos, Postrados, En Tu presencia queremos estar"""),

("Levántate y sálvame", "", "Am F C G", """Am F
Aunque un ejercito
 C G
acampe contra mi no temeré
Am F
Aunque haya guerra hoy
 C G
alrededor de mí, en Ti confiaré

 F G Am
No temeré a diez mil gentes
 F C --- G
que hagan sitio contra mi
 F G G
aunque la tierra se estremezca
 F G
mi salvación está en Ti

 F G Am
Porque Tu eres mi escudo
Tu mi fortaleza
Tu eres mi gloria
 F C G
Y quien levanta mi cabeza

Aunque afligido este
Tu pensaras en mi, no temeré
aunque mi corazón estremecido este, en Ti confiare
No temeré a ningún hombre, que se junte contra mi
Tu eres mi Dios mi fortaleza
Mi salvación esta en Ti

Levántate y sálvame"""),

("Las naciones proclamen", "", "C C/E", """ C C/E
Las naciones, proclamen
 F Bb
declaren, gobiernas hoy
las naciones, conozcan
tu gloria, tu eres Dios

 Am F C
Levántense las naciones
 Dm F G
Den gloria y honra al Rey
 Am F C
Congréguense en los pueblos
 Dm F G
Doblen su rodilla al Rey
 F Dm
Y esperen en El
 Bb G
Clamen al Rey
 F Dm
Y conozcan a aquel
 Bb G
Que es amor justicia y verdad //

 Am F C
Calle delante de Él toda la tierra
 Am F C
Humíllese ante El Señor y su gran poder"""),

("Océanos", "", "INTRO: Bm - A/C# - D - A - G", """Bm A/C# D
Tu voz me llama a las aguas
 A G
Donde mis pies pueden fallar
Y ahí te encuentro en lo incierto
Caminaré sobre el mar

G D A
A tu nombre clamaré
En ti mis ojos fijaré,
 G
en tempestad
 D A
Descansaré en tu poder
 G A/C# Bm A D A G
Pues tuyo soy hasta el final

Tu gracia abunda en la tormenta
Tu mano Dios, me guiará
Cuando hay temor en mi camino
Tú eres fiel y no cambiarás

Bm G
Que tu Espíritu me guíe sin fronteras
 D A
Más allá de las barreras a donde tú me llames
Tú me llevas más allá de lo soñado
Donde puedo estar confiado al estar en tu presencia"""),

("Eres mi Pastor", "", "G C", """ G C
Voy por tus sendas, Me das nuevas fuerzas
Calmas mi sed, Me das de tu agua
 Em C Am D/F#
No temeré, Conmigo caminas, Eres mi pastor
En la oscuridad, Tú eres mi guía
Bondad y amor, Mi fiel compañía
No temeré, Conmigo caminas, eres mi pastor

 Em C G D/F#
Dios cuidas de mí, Nada me falta
Eres mi pastor, Escucho tu voz

PUENTE
 G C Em C
// Aunque ande en valle de oscuridad, Tu bondad y amor me alcanzará
G C Em D
Viviré en tu presencia que es mi hogar, Que es mi hogar//

SUBE DE TONO
 Fm C# G# D#
Dios cuidas de mí, Nada me falta
Tu eres mi pastor, Escucho tu voz ///"""),

("Dios incomparable", "", "B F# G#m E", """B F# G#m E
Dios de mi corazón, en ti encontré mi salvación
Tu gloria y majestad quiero siempre contemplar
Tu eres mi adoración y mi eterna canción
Todo mi interior es cautivado por tu amor
( E E/F# )

B F# G#m
Eres Dios eterno, solo tu eres bueno
 E B
Dios incomparable eres tú
Nunca me separaré de tu gran amor
Eres mi señor mi salvador
Aleluya, aleluya"""),

("Nada es Imposible", "", "A E F#m", """A E/G#
Por Ti, todo lo puedo
 F#m D
Todo es posible, y la fuerza Tú me das
 A
Nada es imposible
Por Ti, los ojos se abren
Cadenas son rotas, y yo viviré por Fe
Nada es imposible

Interludio: D A Bm D
A Bm D
No Viviré por lo que veo
F#m E D
No Viviré por lo que siento
F#m E D D E/C# Bm
Yo se que aquí conmigo Estas
F#m E Bm E/C# Dadd9
Yo se que Tu Eres Grande Dios

D A
Creo en Ti, creo en Ti
Bm D
Creo en Ti, creo en Ti, Cristo /// ///"""),

("Hermoso Nombre", "", "D", """D
Tú fuiste el verbo en el principio
 G A
Unigénito de Dios
El misterio de tu gloria
Revelado en tu amor

 D
Cuán hermoso su nombre es (Poderoso su nombre)
 A
Cuán hermoso su nombre es (Poderoso su nombre)
 Bm A G
El nombre de Jesús mi Rey
 D/F#
Cuán hermoso su nombre es
 A
Nada se iguala a él (Incomparable es El)
 Bm A G
No hay otro nombre

Dejaste el cielo por salvarme
Me viniste a rescatar
Mi transgresión tú perdonaste
Nada nos separará

 G A
La muerte venciste, el velo partiste
 Bm F#m
La tumba vacía ahora está
Los cielos declaran, tu gloria proclaman
Resucitaste en majestad

Inigualable, Incomparable
Hoy y por siempre reinarás
Tuyo es el reino, tuya es la gloria
Tuyo el poder y autoridad"""),

("Levanto mis manos", "", "Intro: D - Dsus4 - D", """D G Asus2
Levanto mis manos
 F#m Bm
Aunque no tenga fuerzas
 Em7 Asus2
Levanto mis manos
 D Dsus4 D7
Aunque tenga mil problemas.

 -CORO-
 G
Cuando levanto mis manos
 Asus2
Comienzo a sentir
 F#m7 Bm7
Una unción que me hace cantar
 Em7
Cuando levanto mis manos
 Asus2 D D7
Comienzo a sentir el fuego.

 G
Cuando levanto mis manos
 Asus2
Mis cargas se van
 F#m7 F#11/B Bm7
Nuevas fuerzas Tu me das
 B7/D# Em7
Todo eso es posible
 Asus2
Todo eso es posible
 D Dsus4 D
Cuando levanto mis manos:"""),

("El movimiento de Gloria", "", "Intro: Em C D Em", """Em C
El movimiento de Gloria es como una corriente de agua
 D Em
que después crece, y se hace manantial//
Trompetas//

Em C
El manantial se convierte en río,
 D
después en mar,
 Em
y en océano poderoso//

Y la Gloria de Dios cubrirá la Tierra,
como las aguas cubren la mar//
Mi Cristo vendrá
por su Iglesia,
por su Iglesia//

¡Demuestra tu Gloria!
¡demuestra tu Gloria!
¡demuestra tu Gloria!
¡Aquí y ahora!"""),

("Hay Libertad", "", "Bm9 G D A", """Bm9 G
Hoy puedo danzar con libertad,
 D A
xq soy su Hijo, xq soy su hijo
Hoy puedo danzar con libertad,
xq soy amado, xq soy amado

Bm | G | D | A |
 Bm
Podemos sentir, tu gozo,
 G
Podemos sentir, tu río
 D
Hay sanidad en las aguas,
 A
Queremos danzar
Hay libertad en la casa de Dios"""),

("A ti me rindo", "", "Am C G F", """Am
Ante ti postrado
 C
Estoy aquí
 G
Te rindo mi ser
 F
Te rindo mi ser
Con tu amor
Atráeme señor
Vengo a tus pies
 Am
A ti me rindo

 Am
Lléname, de gracia inúndame
Sacia mi sed, Sacia mi sed
Mi corazón levanta un clamor
Háblame Dios, Háblame Dios
//A ti me rindo, A ti me rindo
Te quiero conocer, Más de ti conocer//

///Con tu aliento Dios
Sopla en mi interior
Cumple señor tu voluntad en mí
Con tu gran poder muévete en mi ser
Cumple señor tu voluntad en mí///"""),

("Por quien eres tu", "", "Intro ( Gadd9-C-D) X4", """Gadd9 Am9 G/ B Cmaj9/D D13
Por quien eres tu … yo te daré la gloria
Gadd9 D/F# Em7 Amaj9 (Dm G)
Por quien eres tu… te alabare Señor
 maj7 D/c Fdim/F# B/d# Em
Por quien eres tu… alzaré mi voz a ti
 Am9 D Em9 (A/c#)
Y te adorare porque tu eres mi Dios
 Am9 D/A Gadd9
Y te adorare por quien eres Señor

 Cmaj7 Bm7 Em9
/// Jehová Jireh, mi proveedor
 Cmaj7 F/d G
Jehová Nissi, tu reinas en victoria
 Cmaj7 Fdim/F# B/d# D/e
Jehová Shalom eres Príncipe de paz
 Amaj9 D G
Te adorare por quien eres Señor ///"""),

("Yo se quien soy", "", "G#m E", """ G#m E
Cuando estuve en el desierto
 E B
Tu Palabra me libró
 F#
Con un soplo de tu aliento
 G#m
Mi espíritu vivió
En la noche más oscura
Tu luz me iluminó
Vi resplandecer tu rostro
Todo en mi vida cambió

E F# G#m (a#) B (e) F#
Tanto amor recibí … de ti Señor
 B
Yo sé quién soy
 G#m
soy tu hijo, tengo identidad
 F#
y soy amado por ti soy amado
 E
he sido restaurado //"""),

("Cuando esta iglesia te alaba", "", "G", """ G
Cuando esta iglesia te alaba
 Bm Em
Cuando esta iglesia te exalta
 Am7 G/B C add2 C#dim D Sus4
Se desata desde el cielo tu poder
Cuando tus hijos te alaban
Y tu palabra proclaman
Desciende tu presencia aquí

 Bm7 Em
Decimos santo
 Am9 D G
Roca fuerte eres Tú
 Bm Em
Somos Tu pueblo
 Am9 C add2 Dsus D
Y queremos llevar Tu luz
 Am G/B C D G
//desciende Tu presencia// aquí"""),

("Eres mi amigo fiel", "", "Intro: E C#M F#m E", """E maj9 C#m9
Quien soy yo para que en mi tu pienses
 F# maj9 E maj9
Y que escuches, mi clamor
E maj9 C#m9
Y es verdad lo que tu hoy me dices
F# maj9 D Sus2
Que me amas, me asombras

E maj9
Eres mi amigo fiel
 B/C#
Eres mi amigo fiel
A maj9
Eres mi amigo fiel
F# maj9 E maj9
Tu amigo soy"""),

("Yo me rindo a El", "", "Intro: E9 E dim", """E9 A Maj7/E E9
Todo a Cristo
B Sus4 C dim
yo me entrego
E/C# A Maj7/F# A Maj7/B A dim/B E9
con el fin de serle fiel
para siempre
quiero amarle y agradarle solo a El

E9 D dim/F A Maj7/F#
Yo me rindo a El
B Sus4/b A dim/B E9/C#
yo me rindo a El
E9 A Maj7/F# B Sus4/G# A G dim/Bb
todo a Cristo, yo me entrego
A Maj7/B A dim/B
quiero serle fiel"""),

("Deseable", "", "Intro: Bb/G - D Maj7 - Gm/Eb - F Sus4 - F", """Bb/G D Maj7 Gm/Eb
No sé lo que viste en mí
Bb/G D Maj7 Eb/C
Para amarme tanto así
Bb/D Eb
Tanta paciencia
Bb/D Eb
tanta misericordia
 Bb/C Bb/Bb F/A
Y me hiciste deseable para ti

Me elegiste antes que dijera sí
Tanta gracia yo no puedo resistir
Me llamaste por mi nombre
Me compraste con tu sangre
Y me hiciste deseable para ti

 Eb/Bb F/A
Llévame, Señor
 Bb/C
a tus cámaras de amor
 Bb/D Eb F Sus4
Donde me enamoro más de ti
Llévame, Señor
dentro de tu corazón
Yo encuentro mi lugar en ti"""),

("Creo en Ti", "Julio Melgar", "C#m A E G#m", """C#m A
Quiero levantar a ti mis Manos
 E G#m
Maravilloso Jesús, Milagroso señor
Llena este lugar de tu presencia
Has descender tu poder a los que estamos aquí

 C#m B A
Creo en ti Jesús
 C#m B A
y lo que harás en mi
 E B
En mí, en mí

 C#m
Recibe toda la gloria
 A
Recibe toda la honra
 E B
Precioso hijo de Dios"""),

("Venimos a adorarte", "Coalo Zamorano", "intro: A# F (remate) D#D# A#A# F", """ F Am Dm Gm
Dios hemos venido hoy
 Gm/C Am A#
para adorarte y rendirnos a ti
 Am Dm Gm A# C
para honrarte y demostrártelo así

 A# C Am Dm
Levantando Dios nuestras manos hoy
 Gm C F
elevando a ti nuestras voces señor
 A# C Am C#
te entregamos todo a ti por amor
 Am Dm A# Gm D#
para honrarte y darte adoracion

 D# A# F
Padre recibe la gloria
padre recibe nuestro amor
solo tu eres digno cristo
de recibir adoración"""),

("Temprano yo te buscaré", "", "G C9 D Sus4", """G C9 D Sus4
Temprano yo te buscaré
Am C add2/G D
De madrugada yo me acercaré a Ti
 Gadd9 D
Mi alma te anhela y tiene sed
 G/D Am7 G/D C C6/D
Para ver tu gloria y tu poder

G D/F# Em7 A Sus2/F#
Mi socorro has sido Tú
 G D/F# C13 D Sus2
Y en la sombra de tus alas yo me gozaré
 G D/F# Em7 Em/D
Mi alma está pegada a Ti
 Cadd9 D
Porque tu diestra me ha sostenido
 Cadd9 Am D G
Oh, tu diestra me ha sostenido"""),

("Hermoso momento", "", "Fm G#", """ Fm G#
Que hermoso es cada momento
 D# Bb
Que me visitas y de mi haces un altar
Quiero me lleves más adentro
Toma mi mano, no la sueltes nunca más//

 Fm G# D#
Llévame a un lugar
Dónde solos tú y yo
 Bb Fm G#
Disfrutemos el momento
Te amo mi Papá
 D# Bb
Yo dependo de tu amor
Y sin ti yo sé que muero

Tú me viste en mi tormenta
Me libraste de la prueba
Te llevaste mi tristeza
Me cambió la vida entera
Me vistió con ropas nuevas
Puso aceite en mi cabeza
Me hizo un lugar en su mesa
Como un padre me desea"""),

("Danzando", "", "Bm G D A", """ Bm G
Tu palabra dice
 D A
Que aunque pase por el fuego
 Bm G
no me quemaré
 D A Bm G
Y si paso por las aguas, no me ahogaré
 D A Bm G
Aunque haya oscuridad, con fe, caminaré
 D A
Pues Tú siempre vas conmigo

Tu palabra dice
No hay justo que Tú hayas desamparado
Eres pan para el hambriento y necesitado
En mi mesa nunca, nunca ha faltado
Tú provees y no has fallado

G F#7 G F#7
Yo no temeré, tu promesa es fiel
Tu yugo es fácil, ligera es Tu carga
Te entrego mi vida y mi alabanza
Mi escudo, mi fuerza, mi seguridad
Con Cristo camino y estoy
//Danzando en cada temporada//

Tu palabra dice
Que Tú oyes el clamor del quebrantado
Por Tu llaga en la cruz, fuimos sanados
Sobre toda enfermedad, Tú has ganado
Y mi vida está en Tu mano"""),

("Te Doy Gloria Gloria", "", "C G", """ C G
Cuan! Hermoso Eres JESUS
 Am F
Son Tus Palabras, Es Tu Amor
 C G
Cuan! Glorioso Eres JESUS
 Am F
Es Tu Poder, Fue Tu Cruz
 C G
La Que Me Salvo Me Rescato
 Am F
Un Momento Ahí Nos Dio Libertad.

 C
Te doy gloria, gloria
 G
Te doy gloria, gloria
 Am
Te doy gloria, gloria
 F
A Ti JESUS

 F G
Con Una Corona De Espinos
 Am C
Te Hiciste Rey Por Siempre"""),

("Yo Veré", "", "C#m7 A", """ C#m7 A
Cuando el mundo me rechaza
 E B
y dice que tú no eres real
 C#m7 A E B
sigo firme, adelante, pues tu reino revelarás

 A C#m7 B
No hay necesidad de que me acepten por creer
 G#m7 A C#m7 B
Todo lo que has dicho ante mis ojos vas a hacer

 E B C#m7 A
Yo veré tu reino descender y nos restaurarás para la eternidad
Yo veré tu cielo y majestad pues lo que has prometido sé que tú lo cumplirás
¡yo veré!

Yo veré tu reino aquí
y tu voluntad en mi
en la tierra como en el cielo////"""),

("Tu presencia es el cielo", "", "Bm G D", """Bm G D
Quien como tú en la tierra oh Señor
Hermoso inigualable es tu valor
y nada en este mundo saciara
Jesús tu copa no se secara

A G D
Tu Presencia es el cielo para mi
Tu Presencia es el cielo para mi

Tesoro de mi alma y corazón
Me das tu gracia, aunque débil soy
De mis errores eres redentor
De futuro eres el guardador

 D Bm A
Y cantamos Oh Cristo, Oh Cristo-o
 G
Tu Presencia es el cielo para mi
Oh Cristo, Oh Cristo
Tu presencia es el cielo para mi

Y mientras tenga vida esperare
Cuando cara a cara te veré
y nada en este mundo saciara
Jesús tu copa no se secara
No acabará"""),

("Vasijas rotas", "", "Dm F", """ Dm F
Mi alma estaba rota y herida
Pero tu gracia la restauró
Manos vacías que tu llenaste
 C
Soy libre en ti
 Dm C
Soy libre en ti

 A# C
Sublime gracia del Señor
 Dm A#
Que a un pecador salvó uoh oh oh oh
 F C
Fui ciego más hoy veo yo
 Dm A#
Perdido y Él me halló
 F C
Ahora puedo ver
 Dm A#
Oh puedo ver sus ojos de amor
 F C
Quebrantado fue
 Dm A#
Para darnos su salvación

Tú no me juzgas
Por mis fracasos
Tú me aceptas
Tal como soy"""),

("Esperar en ti", "", "G2 G", """G2 G
Esperar en ti
Em7(add4) Em7
Difícil se que es
 CMa7 Am7
Mi mente dice no
 Dsus4 D
No es posible.
Pero mi corazón
Confiado esta en ti
Tu siempre haz sido fiel
Me haz sostenido.

 C/D D7sus4/G G G/B Cmaj7 D
Y esperare pacientemente
 Am7
Aunque la duda me atormente
 Am/G
Yo no confío con la mente
 Cmaj7 Dsus4
Lo hago con el corazón.
Y esperare en la tormenta
Aunque tardare tu respuesta
Yo confiare en tu providencia
Tu siempre tienes el control."""),

("Portador de su gloria", "", "G", """G F G
los cielos cuentan tu gloria señor
 C#dim D
el firmamento anuncia tus obras
 Em C Am C
día y noche es oída tu voz
 G
proclamando tu grandeza

 D G
y yo proclamare tu grandeza y tu poder
 C#dim D
anunciare con mi vida que tú eres el rey
 C Am C
y como el cielo y las estrellas
 G
portador de tu gloria seré//

Bm Bm7 C
y si tu poder y tu deidad
 Em
son visibles en tu creación
Bm7 D C
quiero que sean visibles
 D G
en mi vida señor"""),

("Glorifícate Señor", "", "Am", """Am
Glorifícate Señor
Glorifícate Señor
 F G
Y que todos tus enemigos
 Am
Caigan ante ti

 C G Am Em/G
Quien es ese rey que se viste de poder
F G Am
Es Jehová de los ejércitos
 C G Am Em/G
Es varón de guerra fuerte y valiente
F Dm F G E
Es el poderoso, vencedor en batalla

Quien es ese rey que se viste de amor
Es Jesús el Cristo
Vino como siervo, pero vuelve como rey
En caballo blanco, con espada y a Juzgar."""),

("Libre soy", "", "Am F C G", """Am F
Salvo soy, mi alegría está en tu amor
 C G
hoy te canto porque tu, me hiciste libre en una cruz
Am F
Exaltare, día y noche adorare
 C G
porque libre soy en ti, eres todo mi vivir

 Am
Las cadenas fueron rotas
 F
en su nombre, yo he vencido
 C G
libre soy, libre soy

 Am F
Me hiciste libre y hoy puedo danzar
 C G
Me hiciste libre por tu gran amor
Me hiciste libre y hoy puedo gritar
que libre so oh oh oh hoy

Libre soy, libre soy"""),

("Sea la Luz", "", "Oh oh ooh A - C#m - E - G#m", """ E Bm
Cristo, eres la luz de mundo
 A
Eres el sol de justicia, Que nunca deja de brillar
 E Bm
Cristo, tu luz no avergüenza
 A Maj9
Tu luz nunca condena, solo muestra tu gloria

 C#m E A
Esta generación se expone a tu luz
 C#m E B
Y cada nación responde a tu voz

 A
Sea la luz, en este lugar
 B
Sea la luz y todo se ordena
 C#m E G#m
Sea la luz y hágase tu voluntad//

 F#m E/G#
Todo se ilumina cuando tú estas
 A
Todo se ordena, todo se transforma////
Tu eres la luz que alumbra mi vida
Eres la luz que el mundo ilumina
Eres la luz, yo amo hacer tu voluntad ////

Jesucristo, luz del mundo, sol de justicia, brilla en mi"""),

("¿Quién Podrá?", "", "Intro: A D A A", """ A D A/C#
Te veré llegar en una nube
 A D A
rodeado en gloria y majestad.
 A/C# D E
Me uniré, me uniré
 A D A
Con los ancianos adorar

 D E
Santo, vestido en gloria
 C#m F#m A/E
Santo, la creación te canta
 D E F#m
Santo, te esperare sin manchas
 D
con vestiduras blancas//

 F#m7 E
Ningún principado, ni las potestades,
 D
ni armas forjadas
 Bm
¿Quién podrá? ¿Quién podrá?
 F#m7 E/G#
No han prevalecido, ha caído el enemigo,
 D
el infierno has vencido
 Bm
¿Quién podrá? ¿Quién podrá?//

 F#m E
Eres digno de desatar los sellos
¿quién podrá contra tu reino?,
¿quién podrá contra tu reino? ////"""),

("Me persigue tu amor", "", "Intro: C-Am-G-F-G", """C
Lo escucho en las noches en mi corazón,
Am
Lo veo en la tarde a la puesta del sol
 F C G
¡Tu amor es tan real!
Lo veo en tus manos clavadas por mí,
Lo veo que lejos de ti yo me fui
¡Tu amor es tan real!

 G F
¡Ahora me rindo y te dejo fluir!

C
Inevitable es tu amor,
Am
Incuestionable tu voz,
 F
No me puedo esconder
 C G
Me persigue tu amor
Inevitable es tu amor
Como la muerte y el sol
No lo puedo evitar.
¡Me persigue tu amor!

Me busca y me encuentra con una canción,
Se vuelve esperanza para mi dolor.
¡Tu amor es tan real!"""),

("Bondad de Dios", "", "G", """ G
Te amo Diós
 C G
Tu amor nunca me falla
 D Em C D
Mi existir en Tus manos está
 Em C
Desde el momento que despierto
 G D Em
Hasta el anochecer
 C D#sus G
Yo cantaré de la bondad de Dios

C G
En mi vida has sido bueno
C G D
En mi vida has sido tan fiel
C G D Em
Con mi ser, con cada aliento
 C D G
Yo cantaré de la bondad de Dios

Yo amo Tu voz, me has guiado por el fuego
tu cerca estás en la oscuridad
te conozco como Padre
Y como amigo fiel
Mi vida está en la bondad de Dios

G /B C D G
Tu fidelidad sigue persiguiéndome
 G /B G
Todo lo que soy te lo entrego hoy
 D Em
A Ti me rendiré"""),

("Derrama de tu Fuego", "", "Intro: Cm Bb Fm", """ Cm A# Fm Cm A# Fm
Grande, poderoso eres tu, mi Dios
Fuerte, poderoso eres tu, mi Rey//

 Cm Eb F
Derrama de tu Fuego sobrenatural
 Cm Eb F
Derrama de tu gloria sobre este lugar //

Cm Bb Fm
Anhelamos mas de ti señor
Anhelamos mas de tu amor
Anhelamos mas de ti señor
Derrama de tu fuego hoy señor"""),

("Tu y Yo", "", "Cm Bb", """Cm Bb
Dios está llamando a la guerra
Cm Bb
nos está impulsando hacia afuera
Fm Cm
acudiremos al llamado del Señor
Fm G
tomaremos las armas que El nos preparó.

Cm Bb Cm Abmaj7
Tú y yo somos un pueblo
Cm Bb Cm Abmaj7
Tú y yo preparado
Bb Cm
para mostrar las grandezas del Señor
Bb Cm/G G Cm
para tomar la tierra que Él nos entregó."""),

("Bendito sea, Jehová la Roca", "", "G", """G
Bendito sea, Jehová la Roca,
 G#dim Am
por toda la eternidad.
 Am G#dim D
Mi escondedero y mi refugio,
C D G
eres tu, bendito Jehová.

G
En tu palabra esperaré
 G7 /f C
y mi confianza en ti pondré
C Cm G Em
¡Oh gloria! ¡Oh aleluya!
 Am D G
Amén, amén, amén, amén"""),

("Ardiendo el fuego en mi alma está", "", "G", """G Am
Ardiendo el fuego en mi alma está
 D G
Ardiendo el fuego en mi alma está
 G G7 C
Gloriosa llama me limpiará
 G D G
Oh aleluya, ardiendo el fuego está

G
¡Oh Señor!
Quiero que ardas en mi ser
Como la zarza
Quiero arder con tu poder
En nuevas lenguas quiero hablar, quiero cantar estoy ardiendo
Con el fuego celestial
Quiero alabarte, y adorarte solo a ti
Como se adora en Espíritu y verdad"""),

("Esfuérzate y se muy valiente", "", "Em", """Em
Esfuérzate y se muy valiente
C D Em
Para obedecer a tu Rey
Bendícelo en todos tus caminos
Para ser sensible a su voz

 G D
No temas ni desmayes
 G D
Dios está contigo
 G B7 Em
Nadie te podrá hacer frente

F G
No se aparte de tu boca, su palabra búscala
No te apoyes en tus propios pensamientos
Am
Y harás prosperar tu camino
 B7
y todo saldrá bien"""),

("Rey", "", "Intro: E B C#m A", """E B C#m
En tu presencia danzamos libres, cúbrenos en tu luz de amor
 A E
Llévanos mucho más profundo, pues somos hijos del gran yo soy
Oh, Dios siempre con nosotros, susurrando restauración
Has de nuestro ser tu morada, tuyos somos

Tu iglesia clama hoy, abre los cielos, con poder, enaltecido
Eres Dios, rompe tinieblas, brilla en gloria

 B C#m A
Oh, oh oh oh Oh, oh oh Oh, oh oh oh
¡En tu presencia Señor!

 E/C#
Tu eres Eres Rey,
 B/D# E
/// Por siempre Rey, Sobre la creación
 A E/C#m
tu eres Rey, tu eres Rey ///"""),

("Lo Único que quiero", "Marcela Gandara", "INTRO: | B | F#/A# | B/D# | C#sus4 C# |", """ B F# D#m7 C#sus4
Anhelo conocerte más, vivir en santidad, en intimidad
 B F# D#m7
Contigo, siempre quiero estar, tu gloria contemplar
 C#sus4
Por la eternidad

 F#/A# B F#
Lo único que quiero es adorarte, Lo único que quiero es adorarte
 D#m7 C#sus4 C#
Vengo a tus pies para entregar, Mi corazón
Lo único que quiero es agradarte, Lo único que quiero es agradarte
Por siempre cantare de tu amor

PUENTE
F#/A# B C#
Amor que me rescató
D#m7
Que me limpió
F#sus4 F#/A#
Que me da vida eterna
B C#
Tu sangre abrió el camino
 D#m7
Nunca se cerrará
 F#sus4 F#/A# B
tengo libertad"""),

("Supe que me amabas", "", "F# B C# F#", """F# B C# F#
Desde el principio cuando te necesite
 B Gm# C#
Desde el momento cuando la mirada alce
 D#m D#m/C# B
Desde ese día cuando sola me encontraba
 G#m C# F#
Cuando tu mirada en mi se fue a poner

 B C#
Supe que me amabas, lo entendí
 D#m D#m/C# B
Supe que buscabas mas de mi
 G#m G#m/F#
Que mucho tiempo me esperaste
 C#
Y no llegue

F# B C#
Supe que me amabas, aunque huí
Lejos de tu casa yo me fui
Y con un beso y con amor
Me regalaste tu perdón
Y estoy aquí

Y cuando lejos me encontraba te sentí
Sabia que entonces me cuidabas y te oi
Como un susurro fue tu voz en el silencio
Cada día me atraías hacia ti"""),

("El Dios que adoramos", "", "INTRO F# - C# - E#m - B - F# - C#", """ F# C#
El Dios que hizo los cielos y la tierra
 E#m
Con el poder de Su palabra
 B
Reina con autoridad
El Dios que aun los vientos le obedecen
Una palabra es suficiente
Para los muertos levantar

 B C#
Nadie es como El, oh gran Yo Soy
 F#
Tú eres el Dios que adoramos
 C#
Todopoderoso y Soberano
 E#m B F# C#
Grande en misericordia y poder para salvar
Tú eres el Dios que adoramos
Quien derrotó la muerte y el pecado
Glorioso Redentor y Rey, te adoramos

El Dios que descendió desde Su trono
Para llevar sobre sus hombros
Nuestra culpa y transgresión
Jesús, exaltado sobre todo
Nombre sobre todo nombre
Solo en El hay Salvación

PUENTE
 B C#
A Él sea la gloria y el poder
 C#/F C#
Todo es de Él y para El"""),

("No me soltaras", "", "B", """ B
Aunque yo esté en valle de la muerte y dolor
 E
tu amor me quita todo temor.
Y si llego a estar en el centro de la tempestad
no dudaré porque estás aquí

 G#m F# B
Y no temeré del mal
pues mi Dios conmigo esta
Y si Dios conmigo esta
 F# E
¿de quién temeré? ¿de quién temeré?

B
No,no,no me soltarás, en la calma la tormenta
G#m
No,no,no me soltaras, en lo alto en lo bajo
F# E B F# E
No,no,no me soltaras, Dios nunca me dejarás.

Puedo ver la luz que se acerca al que busca de ti,
Gloriosa luz cual otra no hay.
Y terminarán los problemas mientras llega el fin,
Viviremos conociéndote a ti."""),

("Estar contigo", "", "Intro: C D", """ G C D
Me has quebrantado, Una y otra vez
 G C D
Me siento olvidado, Como si no me ves
 Em C G C
Y cuando te hablo, Lo único que puedo hacer es esperar

Me has sostenido, Una y otra vez
Creer que conmigo, Sigues siendo fiel
Es por tu Palabra que no me rendiré
yo confiaré

C/E D/F# G D Em
Estar contigo no hay otro lugar que me llene
 C G
En la tempestad me das calma
 D C
nada detendrá tu fidelidad

Mi alma restauras, Una y otra vez
Tu amor me rodea, sigues siendo fiel
Y cuando te hablo escuchas mi clamor
en ti puedo confiar

Tu fidelidad es grande
Tu fidelidad incomparable es…"""),

("Santo por siempre", "", "INTRO: G C Em D, G/B Em D G", """G C G
Mil generaciones, Se postran a adorarle
 Em D C
Le cantan al cordero que venció
Los que nos precedieron, Y los que en El creerán
Le cantarán a aquel que ya venció

 C D/C
Tu nombre es más alto, Tu nombre es más grande
 Em7 D C
Tu nombre, sobre todo es
 C
Sean tronos, dominios
 D/C
Poderes, potestades
 Em D Am7
Tu nombre, sobre todo es

 C D/C
Claman ángeles Santo
 G/B Em7
Clama la creación Santo
 Am7 Dsus4 G
Exaltado Dios Santo, Santo por siempre

Si te ha perdonado y tienes salvación
Cántale al Cordero que venció
Si te ha libertado, Su nombre ha puesto en ti
Cántale al cordero que venció
Cantaremos siempre amén.

Canta el pueblo al Rey, Santo
Soberano es El, Santo
Y por siempre es Santo, Santo por siempre"""),

("Abre hoy los cielos", "", "Intro: F Dm Bb F", """Bb F
Padre quiero estar donde Tu estas
Bb F
Mi vida esté llena de Ti
Gm C
Señor solo quiero ver tu Gloria
Gm Bb C
Y que el fuego del cielo caiga en mi

 F Dm
Mira mi pasión y cuanto te anhelo
 Bb C Bb
Hambriento estoy de Ti
 F Dm
Que no halla motivos que pueda separarme
 Bb C
Cambia mi corazón
Gm A Bb F
Oye mi oración, abre hoy los cielos

En todo lugar puedo sentir
Veremos tu Gloria Descender
Se puede escuchar este clamor
En la boca de cada nación

Oh Señor queremos ver Tu Gloria
Y que el Fuego del cielo caiga aquí"""),

("Rodeado", "", "F", """F
Derramo mi perfume
 Bb
Aunque no te pueda ver
 Dm C/E F
Tú me prometiste
 Bb
que nunca me dejarás //

 Gm Bb Dm Am
Veo ángeles rodear este lugar
 Gm Bb F A7
Veo ángeles rodear este lugar

 Dm
//Estoy rodeado, rodeado, rodeado
 C
De una gloria que no veo, no veo, no veo
 Bm Gm7
Son mirarte yo te siento, te siento, te siento
 A7
Y no puedo de ti escapar//

Tu manto cubre el templo
Tu gloria aquí esta
No me puedo resistir, Ante tu majestad (X6)

Puente 2:
Rodéame, rodéame!!!
Lléname, Lléname, Lléname con tu presencia
… con tu poder … con tu amor"""),

("Por tu Llaga", "Jaime Murrell", "G D/F#", """ G D/F#
Toda Enfermedad tu llevaste al morir
Y por mi sufriste en silencio mi dolor
Por mi rebelión azotado y herido
y por darme paz recibiste mi castigo

Por tu llaga sano soy
soy fruto de tu aflicción
Oh Mesías salvador hoy te rindo adoración
Pusiste tu vida expiación por la mía,
Jesucristo mi rey, glorioso Mesías.

Varón de dolores fuiste desechado,
en todo quebranto experimentado,
Como un cordero al matadero llevado
Y con tu sangre limpiaste mi pecado."""),

("Fiesta en el desierto", "", "C#m", """C#m
En Santiago uno, verso dos
está escrito que tenga gozo
Cuando pase por diversas pruebas
Porque de allí saldré victorioso

 A B
Mi lamento cambiaste por danza
 G# C#m
Ya no hay tristeza, solo alabanza
Mi lamento cambiaste por danza
Ya no hay tristeza

A B G#7
Yo Danzo, danzo, danzo, danzo, danzo, danzo
C#m
En el proceso
Y Grito, grito, grito, grito, grito, grito
No moriré
Doy vueltas, vueltas, vueltas, vueltas, vueltas, vueltas
No me avergüenzo
Hay fiesta, fiesta fiesta, fiesta, fiesta
 G#m
Fiesta en el desierto

C#m
Aunque venga la enfermedad
Mientras viva te alabaré
Aunque mis labios quieran callar
Mientras viva te alabaré
Aunque el desierto me quiera secar
Mientras viva te alabaré
Aunque la higuera no florezca
Mientras viva te alabaré"""),

("La Ola", "New Wine", "Dm A# C", """Dm
Dios nos llama a expandir Su reino y llevar
A# C
Su avivamiento por todo el mundo
Dm
Ábranse las costas y entrará la ola
A# C
Del avivamiento por todo el mundo

A# C
Nunca parará la ola, nunca parará
Dm Am
Nunca parará la ola, nunca parará...

Dm A#
Ven muévete en la corriente
C Am
De Su Espíritu
 Dm A# C
Ven a ver lo que ojo no ha visto
 Gm
Levántate// Wooh oh oh oh

 Gm Dm
Cristo Tu eres la luz del mundo
 F
Nuestra esperanza
 C
Justicia traerás
Tu has derramado tu Espíritu Santo
Lo que muerto está lo resucitarás"""),

("Como te amo", "", "Intro: D F#m Bm G", """Bm A/C# F#m
Apesar de mi fragilidad
 G
Me llamas hija
Y en mi debilidad
En tus brazos me sostienes

Em F#m
No puedo dejar de amarte
Em A
No puedo dejar de llamarte

D F#m G
Papá, papá como te amo
Em A
Eres mi necesidad
Papá, papá como te amo
Eres mi felicidad

Si Tu me amaste primero
Como dejar de amarte
Si acercaste el cielo
Solo con tal de abrazarme"""),

("Inexplicable", "", "D G A", """D G A
que tiene tu Espíritu que cuando me tocas
 D
me haces temblar
 G A
y que es tu presencia que al manifestarse
 D
tengo que llorar
 D/F# G A
es que soy tan pequeño que al tu tocarme siento
 D
que voy a desmayar
y es que se tu presencia no hay aqui en la tierra con que comparar

 D/F# G Em7
no te puedo mirar ni te puedo tocar
 D
no ha llegado el momento
 G Em7
y a veces en mi afan creo que ya tu no estas
 D
pero vuelvo y te siento
 D/F# G A
y cuando me tocas con tu santo espiritu
 D
lloro canto y tiemblo X2

que hay en tu interior que sientes por mi
dime como me amas
que misterio existe que a mi duras pruebas conviertes en calma
yo se que a tu presencia toda la tierra tiembla
y tambien tiembla mi alma"""),

("Santo es el que vive", "", "Intro: D#m, C#, B, A#-G#m, A#", """ D#m
Santo es el que vive, santo es el que reina
 C#
Santo en las alturas, santo aquí en la tierra
 B G#m
Santo en el pesebre, santo en el sepulcro
 A#7
Santa es su sangre derramada en la cruz

 D#m
Corrió su sangre por el madero
 C#
A Él no lo mataron, se entregó primero
 B G#m
De tal manera amó Jesús
 A#7
Que entregó su vida en la Cruz

No dijo nada, no abrió su boca
Le hieren, le golpean, pero Él perdona
De tal manera amó Jesús
Que entregó su vida en la cruz

 B
Todos lo verán
 C#
como Rey en las nubes volverá
 G#m
Coronado en Poder y Autoridad
 B A#7
El Cordero y León reinará"""),

("Oh Ven", "", "Intro: C Maj9", """ G Maj7 Bm7 C Am B B7
Oh ven, oh ven, ante la majestad del supremo Rey
 G Maj7 Bm7 C G
Oh ven, postrémonos ante el Rey de los cielos,
 C Am7 D G
Démosle Gloria, démosle honra
 G Gmaj7 Am D
Al que es y que siempre será
 G G7 C Cm7
El es digno, digno es de mi alabanza
 G Em Am D7 G
Adoremos, alabemos al Rey."""),

("Alfa y Omega", "", "Intro: F Maj9 G Maj9", """A Maj7
Tu que estás sentado en el trono
Siempre reinando, soberano
Ángeles cantan, hombres alaban
Dios reunido con su pueblo

Oh oh Alfa, Omega, Cristo, Hijo
Oh oh ven, oh oh ven, oh oh ven Señor Jesús //

Ansioso espero a tu vuelta
ese gran día en que Tú vendrás
y allí subiremos, contigo estaremos
para siempre aleluya

Maranatha, Cristo, Hijo, Maestro
Oh oh ven, oh oh ven, oh oh ven Señor Jesús //"""),
]


def main():
    database.inicializar()
    # Títulos ya existentes (para no duplicar)
    existentes = {c["titulo"].strip().lower() for c in database.listar_canciones()}
    agregadas = 0
    saltadas = 0
    for titulo, artista, tono, letra in CANCIONES:
        if titulo.strip().lower() in existentes:
            saltadas += 1
            continue
        database.crear_cancion(titulo, artista, tono, "Lista Nueva", letra.strip(),
                                "Nuevas y últimas")
        existentes.add(titulo.strip().lower())
        agregadas += 1
    print(f"Canciones agregadas: {agregadas}")
    print(f"Canciones salteadas (ya existían): {saltadas}")
    print(f"Total en la base: {len(database.listar_canciones())}")


if __name__ == "__main__":
    main()
