import ast

def parse_code(code_str):
    code_str = code_str.strip()
    if code_str.startswith("```"):
        lines = code_str.split("\n")
        if len(lines) > 1:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code_str = "\n".join(lines).strip()
    
    # Try literal eval directly
    try:
        return ast.literal_eval(code_str)
    except:
        pass
        
    # Try ast.parse to find assignment
    try:
        tree = ast.parse(code_str)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                return ast.literal_eval(node.value)
    except:
        pass
        
    # Try strip variable name
    for prefix in ["concept_map =", "concept_map=", "mapa_ejemplo =", "mapa_ejemplo=", "chart =", "chart="]:
        if code_str.startswith(prefix):
            code_str = code_str[len(prefix):].strip()
            try:
                return ast.literal_eval(code_str)
            except:
                pass
                
    raise ValueError("Could not parse")

print(parse_code("""
```python
concept_map = [{"test": 1}]
```
"""))
