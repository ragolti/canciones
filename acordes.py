"""
acordes.py
----------
Transpone (sube o baja de tono) los acordes de una canción.

Cómo funciona:
- Solo modifica las "líneas de acordes": líneas donde TODO lo escrito son
  acordes (por ejemplo:  "Do  Sol  La m  Fa").
- Las líneas con letra de la canción se dejan intactas, así no se rompe el texto.
- Entiende notación en inglés (C, D, E, F, G, A, B) y en español
  (Do, Re, Mi, Fa, Sol, La, Si).
"""

import re

# Escala cromática de 12 semitonos, con sostenidos y con bemoles.
ESCALA_SOSTENIDOS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
ESCALA_BEMOLES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

# Equivalencias español <-> inglés para la nota base.
ES_A_EN = {"DO": "C", "RE": "D", "MI": "E", "FA": "F", "SOL": "G", "LA": "A", "SI": "B"}
EN_A_ES = {"C": "Do", "D": "Re", "E": "Mi", "F": "Fa", "G": "Sol", "A": "La", "B": "Si"}

# Expresión regular para reconocer un acorde:
#   nota base + (#/b) + sufijo (m, maj7, sus4, etc.) + (/ bajo opcional)
# Importante: las notas españolas (varias letras) van ANTES que [A-G],
# porque la alternancia de regex prueba en orden y "Do"/"Fa" empiezan con
# letras que también son notas inglesas (D, F).
NOTA = r"(?:[Ss][Oo][Ll]|[Dd][Oo]|[Rr][Ee]|[Mm][Ii]|[Ff][Aa]|[Ll][Aa]|[Ss][Ii]|[A-G])"
ALTERACION = r"(?:#|b)?"
SUFIJO = r"(?:m|maj|min|dim|aug|sus|add|°|º|\+|\d)*"
BAJO = r"(?:/" + NOTA + ALTERACION + r")?"
RE_ACORDE = re.compile(r"^" + NOTA + ALTERACION + SUFIJO + BAJO + r"$")


def _indice_nota(nota):
    """Devuelve (indice_cromatico, es_español) para la nota base.

    'nota' es algo como 'C', 'Do', 'sol'. Devuelve None si no se reconoce.
    """
    n = nota.strip()
    # ¿Notación española?
    if n.upper() in ES_A_EN:
        return ESCALA_SOSTENIDOS.index(ES_A_EN[n.upper()]), True
    # ¿Notación inglesa?
    letra = n[0].upper()
    if letra in ESCALA_SOSTENIDOS:
        return ESCALA_SOSTENIDOS.index(letra), False
    return None


def _transponer_nota(nota, alteracion, semitonos, usar_bemoles):
    """Transpone una nota base + alteración la cantidad de semitonos dada."""
    info = _indice_nota(nota)
    if info is None:
        return nota + alteracion  # no se reconoció, se deja igual
    indice, es_espanol = info

    # Aplica la alteración (# sube uno, b baja uno).
    if alteracion == "#":
        indice += 1
    elif alteracion == "b":
        indice -= 1

    # Transpone y vuelve al rango 0-11.
    indice = (indice + semitonos) % 12

    escala = ESCALA_BEMOLES if usar_bemoles else ESCALA_SOSTENIDOS
    resultado_en = escala[indice]

    if es_espanol:
        # Reconstruye en español: nota base + alteración si la hay.
        base = resultado_en[0]
        alt = resultado_en[1:] if len(resultado_en) > 1 else ""
        return EN_A_ES[base] + alt
    return resultado_en


def _transponer_acorde(acorde, semitonos, usar_bemoles):
    """Transpone un acorde completo, conservando el sufijo y el bajo (/x)."""
    # Separa un eventual bajo:  Do/Sol  ->  ['Do', 'Sol']
    partes = acorde.split("/")
    transpuestas = []
    for parte in partes:
        m = re.match(r"^(" + NOTA + r")(" + ALTERACION + r")(.*)$", parte)
        if not m:
            transpuestas.append(parte)
            continue
        nota, alteracion, sufijo = m.group(1), m.group(2), m.group(3)
        nueva = _transponer_nota(nota, alteracion, semitonos, usar_bemoles)
        transpuestas.append(nueva + sufijo)
    return "/".join(transpuestas)


def _es_linea_de_acordes(linea):
    """True si la línea está compuesta solo por acordes y espacios."""
    tokens = linea.split()
    if not tokens:
        return False
    return all(RE_ACORDE.match(t) for t in tokens)


def transponer_letra(letra, semitonos):
    """Transpone solo las líneas de acordes de una letra completa.

    Conserva los espacios para que los acordes sigan alineados sobre la letra.
    """
    if not semitonos:
        return letra

    # Si el original usa bemoles, mantenemos bemoles en el resultado.
    usar_bemoles = "b" in letra and "#" not in letra

    lineas_resultado = []
    for linea in letra.splitlines():
        if _es_linea_de_acordes(linea):
            # Reemplaza cada acorde respetando los espacios originales.
            def reemplazar(match):
                return _transponer_acorde(match.group(0), semitonos, usar_bemoles)

            nueva = re.sub(r"\S+", reemplazar, linea)
            lineas_resultado.append(nueva)
        else:
            lineas_resultado.append(linea)
    return "\n".join(lineas_resultado)


def transponer_tono(tono, semitonos):
    """Transpone el campo 'tono' (ej: 'Sol mayor (G)' o 'C')."""
    if not semitonos or not tono.strip():
        return tono
    usar_bemoles = "b" in tono and "#" not in tono

    def reemplazar(match):
        token = match.group(0)
        if RE_ACORDE.match(token):
            return _transponer_acorde(token, semitonos, usar_bemoles)
        return token

    return re.sub(r"\S+", reemplazar, tono)
