import requests
from duckduckgo_search import DDGS
import os

def descargar_imagen(termino_busqueda, nombre_archivo="imagen_descargada.jpg"):
    print(f"🔍 Buscando '{termino_busqueda}' en DuckDuckGo...")
    
    try:
        # Iniciamos la búsqueda en DuckDuckGo
        with DDGS() as ddgs:
            # Buscamos imágenes y limitamos a 1 resultado
            resultados = list(ddgs.images(termino_busqueda, max_results=1))
            
            if not resultados:
                print("❌ No se encontraron imágenes para ese término.")
                return

            # Obtenemos la URL de la primera imagen
            url_imagen = resultados[0]['image']
            print(f"🔗 URL encontrada: {url_imagen}")
            print("⏳ Descargando...")

            # Hacemos la petición para descargar la imagen
            respuesta = requests.get(url_imagen, stream=True, timeout=10)
            respuesta.raise_for_status() # Verifica que la descarga fue exitosa (código 200)

            # Guardamos la imagen en nuestro disco duro
            with open(nombre_archivo, 'wb') as archivo:
                for chunk in respuesta.iter_content(chunk_size=8192):
                    archivo.write(chunk)

            print(f"✅ ¡Imagen guardada exitosamente como '{nombre_archivo}'!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error al descargar la imagen. El servidor de la imagen falló: {e}")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

# ==========================================
# Ejemplo de uso
# ==========================================
if __name__ == "__main__":
    texto_a_buscar = "redes computadoras"
    # Puedes cambiar el nombre del archivo para que coincida con tu búsqueda
    nombre_del_archivo = "base_de_datos.jpg" 
    
    descargar_imagen(texto_a_buscar, nombre_del_archivo)