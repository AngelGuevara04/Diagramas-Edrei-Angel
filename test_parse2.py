import ast

def parse_code(data_str):
    data_str = data_str.strip()
    
    # Quitar formato de markdown si existe
    if data_str.startswith("```"):
        lines = data_str.split("\n")
        if len(lines) > 1:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        data_str = "\n".join(lines).strip()
        
    # 1. Intentar evaluar como literal directamente (si es solo la lista/diccionario)
    try:
        res = ast.literal_eval(data_str)
        if isinstance(res, str):
            res = ast.literal_eval(res.strip())
        return res
    except Exception:
        pass
        
    # 2. Intentar buscar la asignación en el AST
    try:
        tree = ast.parse(data_str)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                return ast.literal_eval(node.value)
    except Exception:
        pass
        
    # 3. Fallback manual limpiando prefijos
    for prefix in ["concept_map =", "concept_map=", "mapa_ejemplo =", "mapa_ejemplo=", "chart =", "chart="]:
        if data_str.startswith(prefix):
            clean_str = data_str[len(prefix):].strip()
            try:
                res = ast.literal_eval(clean_str)
                if isinstance(res, str):
                    res = ast.literal_eval(res.strip())
                return res
            except Exception:
                pass
                
    raise ValueError("No se pudo parsear el código proporcionado. Verifica que sea una lista o diccionario válido.")

print(parse_code("""
[
    {
        "titulo_principal": "El Sistema Solar",
        "subtitulos": []
    }
]
"""))
