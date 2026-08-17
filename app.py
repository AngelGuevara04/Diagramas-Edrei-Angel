import os
import sys
import json
import urllib.parse as urlparse
import urllib.request as urlrequest
import urllib.error as urlerror
from typing import Any
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Configurar rutas para los scripts generadores
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, "Mapa conceptual", "codigo", "Scripts"))
sys.path.append(os.path.join(PROJECT_ROOT, "Mapa mental", "codigo", "Scripts"))
sys.path.append(os.path.join(PROJECT_ROOT, "Cuadro sinoptico", "codigo", "Scripts"))

from Mapas_conceptuales import generar_mapa_conceptual
from Mapas_mentales import generar_mapa_mental
from Cuadros_sinopticos import generar_cuadro_sinoptico
from utilidades.imagenes import buscar_candidatos_imagen

load_dotenv()

app = FastAPI()

import ast

# ----- MODELS -----
class GenerateMapReq(BaseModel):
    map_data_str: str
    config: dict

class IACallReq(BaseModel):
    instruction: str
    concept_map: str

class ImageCandidatesReq(BaseModel):
    provider: str
    query: str

def parse_py_literal(text: str) -> Any:
    text = text.strip()
    try:
        tree = ast.parse(text)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id in ("concept_map", "mapa_ejemplo", "chart"):
                        return ast.literal_eval(node.value)
    except Exception:
        pass
    
    # Fallback for simple literal evaluation
    if text.startswith("concept_map ="):
        text = text.split("=", 1)[1].strip()
    if text.startswith("mapa_ejemplo ="):
        text = text.split("=", 1)[1].strip()
    if text.startswith("chart ="):
        text = text.split("=", 1)[1].strip()
    return ast.literal_eval(text)

# ----- IA LOGIC -----
def extract_first_json(text: str) -> Any:
    decoder = json.JSONDecoder()
    cleaned = text.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    cleaned = cleaned.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    for i, ch in enumerate(cleaned):
        if ch not in "{[":
            continue
        try:
            obj, _ = decoder.raw_decode(cleaned[i:])
            return obj
        except json.JSONDecodeError:
            continue
    raise ValueError("No se pudo extraer JSON de la respuesta del modelo.")

def collect_text_from_gemini_response(response_payload: dict[str, Any]) -> str:
    candidates = response_payload.get("candidates") or []
    if not candidates:
        raise ValueError("Gemini no devolvio candidatos.")
    first = candidates[0]
    content = first.get("content") or {}
    parts = content.get("parts") or []
    texts: list[str] = []
    for part in parts:
        if isinstance(part, dict) and isinstance(part.get("text"), str):
            texts.append(part["text"])
    if not texts:
        raise ValueError("Gemini no devolvio texto util en el primer candidato.")
    return "\n".join(texts).strip()

def call_gemini_for_concept_map(api_key: str, model: str, instruction: str, concept_map_text: str) -> tuple[list[Any], str]:
    system_instruction = (
        "Eres un asistente experto en mapas conceptuales de Draw.io.\n"
        "Tu tarea es modificar un concept_map existente siguiendo la instruccion del usuario.\n"
        "Responde solo JSON valido y nada mas."
    )
    user_prompt = (
        "Aplica la instruccion al concept_map actual.\n"
        "Debes devolver un JSON con esta forma exacta:\n"
        "{\n"
        '  "concept_map": [ ... ]\n'
        "}\n\n"
        "Reglas:\n"
        "- Mantener estructura compatible con el generador: lista principal, grupos, subtitulos y ramas.\n"
        "- En ramas, cada entrada conceptual debe ser lista de dos posiciones [texto, conector] o [null, conector].\n"
        "- No uses markdown ni bloques de codigo.\n\n"
        f"Instruccion del usuario:\n{instruction}\n\n"
        f"concept_map actual:\n{concept_map_text}\n"
    )
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{urlparse.quote(model, safe='-._')}:generateContent?key={urlparse.quote(api_key)}"
    payload = {
        "system_instruction": {"parts": [{"text": system_instruction}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
        },
    }
    body = json.dumps(payload).encode("utf-8")
    req = urlrequest.Request(endpoint, data=body, method="POST", headers={"Content-Type": "application/json"})
    try:
        with urlrequest.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except urlerror.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read().decode("utf-8", errors="replace")
        except Exception:
            detail = ""
        raise RuntimeError(f"Gemini HTTP {exc.code}: {detail or exc.reason}") from exc
    except urlerror.URLError as exc:
        raise RuntimeError(f"No se pudo conectar con Gemini: {exc.reason}") from exc

    data = json.loads(raw)
    text = collect_text_from_gemini_response(data)
    extracted = extract_first_json(text)
    if isinstance(extracted, list):
        concept_map = extracted
    elif isinstance(extracted, dict):
        concept_map = extracted.get("concept_map")
    else:
        concept_map = None
    if not isinstance(concept_map, list):
        raise ValueError("La respuesta de Gemini no incluyo 'concept_map' como lista.")
    return concept_map, text

# ----- IA ENDPOINTS -----
@app.get("/api/ia/status")
async def ia_status():
    key_present = bool(os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY"))
    return {
        "ok": True,
        "gemini_configured": key_present,
        "message": "Gemini configurado." if key_present else "Falta GEMINI_API_KEY."
    }

@app.post("/api/ia/concept-map")
async def ia_concept_map(req: IACallReq):
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return JSONResponse({"ok": False, "error": "Falta GEMINI_API_KEY."}, status_code=500)
    try:
        concept_map, raw_text = call_gemini_for_concept_map(
            api_key=api_key,
            model="gemini-2.5-flash-lite",
            instruction=req.instruction,
            concept_map_text=req.concept_map
        )
        return {"ok": True, "concept_map": concept_map, "raw": raw_text}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

# ----- IMAGE ENDPOINTS -----
@app.post("/api/images/candidates")
async def images_candidates(req: ImageCandidatesReq):
    try:
        candidates = buscar_candidatos_imagen(req.provider, req.query)
        return {"ok": True, "candidates": candidates}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)

# ----- GENERATOR ENDPOINTS -----
@app.post("/api/generate/concept")
async def gen_concept(req: GenerateMapReq):
    try:
        req.config["RETURN_XML"] = True
        data = parse_py_literal(req.map_data_str)
        xml = generar_mapa_conceptual(data, req.config)
        return PlainTextResponse(xml)
    except Exception as e:
        return PlainTextResponse(f"Error generando mapa conceptual: {e}", status_code=500)

@app.post("/api/generate/mind")
async def gen_mind(req: GenerateMapReq):
    try:
        req.config["RETURN_XML"] = True
        data = parse_py_literal(req.map_data_str)
        xml = generar_mapa_mental(data, req.config)
        return PlainTextResponse(xml)
    except Exception as e:
        return PlainTextResponse(f"Error generando mapa mental: {e}", status_code=500)

@app.post("/api/generate/synoptic")
async def gen_synoptic(req: GenerateMapReq):
    try:
        req.config["RETURN_XML"] = True
        data = parse_py_literal(req.map_data_str)
        xml = generar_cuadro_sinoptico(data, req.config)
        return PlainTextResponse(xml)
    except Exception as e:
        return PlainTextResponse(f"Error generando cuadro sinoptico: {e}", status_code=500)

# ----- STATIC FILES -----
# Excluir la API antes de montar la raiz
app.mount("/", StaticFiles(directory=PROJECT_ROOT, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
