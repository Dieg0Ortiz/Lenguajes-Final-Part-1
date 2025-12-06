import re
from typing import Dict, List, Tuple


def cargar_diccionario(ruta: str) -> Dict[str, str]:
    diccionario = {}
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip()
                if linea:
                    partes = linea.split()
                    if len(partes) >= 2:
                        lexema = partes[0]
                        tipo_token = partes[1]
                        diccionario[lexema] = tipo_token
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta}'")
    except Exception as e:
        print(f"Error al leer el diccionario: {e}")
    
    return diccionario


def es_identificador_valido(palabra: str) -> bool:
    patron_identificador = r'^[a-z]([a-z]|[0-9])*$'
    return bool(re.match(patron_identificador, palabra))


def clasificar_token(palabra: str, diccionario: Dict[str, str]) -> Tuple[str, str]:
    if palabra in diccionario:
        return (diccionario[palabra], palabra)
    
    if es_identificador_valido(palabra):
        return ("IDENTIFICADOR", palabra)
    
    return ("ERROR_LEXICO", palabra)


def analizar_texto(diccionario: Dict[str, str], 
                   ruta_entrada: str, 
                   ruta_salida: str) -> List[Tuple[str, str]]:
    tokens = []
    
    try:
        with open(ruta_entrada, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        
        palabras = contenido.split()
        
        for palabra in palabras:
            token = clasificar_token(palabra, diccionario)
            tokens.append(token)
        
        generar_salida(tokens, ruta_salida)
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_entrada}'")
    except Exception as e:
        print(f"Error al analizar el texto: {e}")
    
    return tokens


def generar_salida(tokens: List[Tuple[str, str]], ruta_salida: str) -> None:
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as archivo:
            archivo.write(f"{'Token':<20} {'Lexema':<20}\n")
            archivo.write("-" * 40 + "\n")
            
            for tipo_token, lexema in tokens:
                archivo.write(f"{tipo_token:<20} {lexema:<20}\n")
        
        print(f"Archivo de salida generado: '{ruta_salida}'")
        
    except Exception as e:
        print(f"Error al generar archivo de salida: {e}")


def mostrar_resultados(tokens: List[Tuple[str, str]]) -> None:
    print("\n" + "=" * 50)
    print("RESULTADOS DEL ANÁLISIS LÉXICO")
    print("=" * 50)
    print(f"\n{'Token':<20} {'Lexema':<20}")
    print("-" * 40)
    
    for tipo_token, lexema in tokens:
        print(f"{tipo_token:<20} {lexema:<20}")
    
    print("-" * 40)
    print(f"Total de tokens procesados: {len(tokens)}")
    
    palabras_clave = sum(1 for t, _ in tokens if t.startswith("KW_"))
    identificadores = sum(1 for t, _ in tokens if t == "IDENTIFICADOR")
    errores = sum(1 for t, _ in tokens if t == "ERROR_LEXICO")
    
    print(f"\nEstadísticas:")
    print(f"  - Palabras clave:  {palabras_clave}")
    print(f"  - Identificadores: {identificadores}")
    print(f"  - Errores léxicos: {errores}")
    print("=" * 50)


def main():
    print("\n" + "=" * 50)
    print("ANALIZADOR LÉXICO (SCANNER)")
    print("Práctica 1 - Lenguajes de Programación")
    print("=" * 50)
    
    ruta_diccionario = "diccionario.txt"
    ruta_entrada = "texto_entrada.txt"
    ruta_salida = "tokens_salida.txt"
    
    print("\n[1] Cargando diccionario de palabras clave...")
    diccionario = cargar_diccionario(ruta_diccionario)
    
    if diccionario:
        print(f"    Palabras clave cargadas: {len(diccionario)}")
        for lexema, tipo in diccionario.items():
            print(f"      {lexema} -> {tipo}")
    else:
        print("    Error: No se pudo cargar el diccionario")
        return
    
    print(f"\n[2] Analizando archivo '{ruta_entrada}'...")
    tokens = analizar_texto(diccionario, ruta_entrada, ruta_salida)
    
    if tokens:
        mostrar_resultados(tokens)
    else:
        print("    No se encontraron tokens para procesar")


if __name__ == "__main__":
    main()
