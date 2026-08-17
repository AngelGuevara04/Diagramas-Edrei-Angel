"""
Descarga una imagen de internet relacionada con un texto.

Fuentes 100% gratuitas (sin API key, sin registro):
    1. Openverse  (https://api.openverse.org)  - imagenes Creative Commons
    2. Wikimedia Commons (fallback)            - imagenes libres de Wikipedia

Requisitos:
    pip install requests

Uso:
    python descargar_imagen.py
    python descargar_imagen.py "Base de datos"
"""

import os
import re
import sys
import requests


HEADERS = {
    'User-Agent': (
        'DescargadorImagenes/1.0 '
        '(proyecto-educativo; contacto: estudiante@ejemplo.com)'
    )
}


def limpiar_nombre(texto: str) -> str:
    """Convierte el texto en un nombre de archivo valido para Windows."""
    nombre = re.sub(r'[<>:"/\\|?*]', '', texto)
    nombre = nombre.strip().replace(' ', '_')
    return nombre[:80] if nombre else 'imagen'


def extension_desde_respuesta(url: str, content_type: str) -> str:
    """Determina la extension del archivo a partir de la respuesta HTTP."""
    ct = (content_type or '').lower()
    if 'jpeg' in ct or 'jpg' in ct:
        return 'jpg'
    if 'png' in ct:
        return 'png'
    if 'webp' in ct:
        return 'webp'
    if 'gif' in ct:
        return 'gif'
    if 'svg' in ct:
        return 'svg'
    ext = url.split('?')[0].split('.')[-1].lower()
    return ext if ext in ('jpg', 'jpeg', 'png', 'webp', 'gif', 'svg') else 'jpg'


def buscar_openverse(texto: str) -> list:
    """Devuelve una lista de URLs de imagenes desde Openverse."""
    try:
        r = requests.get(
            'https://api.openverse.org/v1/images/',
            params={'q': texto, 'page_size': 10, 'license_type': 'all'},
            headers=HEADERS,
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        return [item['url'] for item in data.get('results', []) if item.get('url')]
    except Exception as e:
        print(f'    [Openverse] Error: {e}')
        return []


def buscar_wikimedia(texto: str) -> list:
    """Devuelve URLs de imagenes desde Wikimedia Commons."""
    try:
        r = requests.get(
            'https://commons.wikimedia.org/w/api.php',
            params={
                'action': 'query',
                'format': 'json',
                'generator': 'search',
                'gsrsearch': f'{texto} filetype:bitmap',
                'gsrnamespace': 6,        # namespace File:
                'gsrlimit': 10,
                'prop': 'imageinfo',
                'iiprop': 'url|mime',
                'iiurlwidth': 800,
            },
            headers=HEADERS,
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        paginas = data.get('query', {}).get('pages', {})
        urls = []
        for p in paginas.values():
            info = (p.get('imageinfo') or [{}])[0]
            url = info.get('thumburl') or info.get('url')
            if url:
                urls.append(url)
        return urls
    except Exception as e:
        print(f'    [Wikimedia] Error: {e}')
        return []


def descargar_imagen(texto, carpeta='imagenes_descargadas'):
    """
    Busca y descarga una imagen relacionada con texto.
    Devuelve la ruta del archivo o None si no se logra.
    """
    os.makedirs(carpeta, exist_ok=True)
    print(f'[*] Buscando imagenes para: "{texto}"')

    fuentes = [
        ('Openverse', buscar_openverse),
        ('Wikimedia Commons', buscar_wikimedia),
    ]

    urls = []
    for nombre_fuente, buscar in fuentes:
        print(f'[*] Consultando {nombre_fuente}...')
        urls = buscar(texto)
        if urls:
            print(f'    {len(urls)} resultado(s) encontrados.')
            break
        print('    Sin resultados, probando siguiente fuente...')

    if not urls:
        print('[!] No se encontraron imagenes en ninguna fuente.')
        return None

    nombre_base = limpiar_nombre(texto)

    for i, url in enumerate(urls, start=1):
        try:
            print(f'[*] Descargando ({i}/{len(urls)}): {url[:90]}...')
            resp = requests.get(url, headers=HEADERS, timeout=15, stream=True)
            resp.raise_for_status()

            ext = extension_desde_respuesta(url, resp.headers.get('Content-Type', ''))
            ruta = os.path.join(carpeta, f'{nombre_base}.{ext}')

            with open(ruta, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            tam_kb = os.path.getsize(ruta) / 1024
            if tam_kb < 1:  # archivo sospechosamente pequeno
                os.remove(ruta)
                print('    [X] Archivo demasiado pequeno, descartado.')
                continue

            print(f'[OK] Imagen guardada en: {ruta} ({tam_kb:.1f} KB)')
            return ruta

        except Exception as e:
            print(f'    [X] Fallo: {e}')
            continue

    print('[!] No se pudo descargar ninguna imagen.')
    return None


def main():
    if len(sys.argv) > 1:
        texto = ' '.join(sys.argv[1:])
    else:
        texto = input('Escribe el texto a buscar: ').strip()

    if not texto:
        print('[!] Texto vacio. Saliendo.')
        return

    descargar_imagen(texto)


if __name__ == '__main__':
    main()