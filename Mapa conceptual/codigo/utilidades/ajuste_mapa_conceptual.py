from copy import deepcopy
from typing import Any, List, Optional


def _split_words(text: str) -> List[str]:
    return [word for word in text.strip().split() if word]


def _capitalize_first(text: Optional[str]) -> Optional[str]:
    if not text:
        return text
    return text[0].upper() + text[1:]


def _normalize_branch(branch: List[Any], palabras_por_slot: int) -> List[Any]:
    words: List[str] = []
    for entry in branch:
        if isinstance(entry, (list, tuple)):
            for part in list(entry)[:2]:
                if isinstance(part, str):
                    words.extend(_split_words(part))

    index = 0

    def take_chunk() -> Optional[str]:
        nonlocal index
        if index >= len(words):
            return None
        chunk = words[index : index + palabras_por_slot]
        index += len(chunk)
        return " ".join(chunk) if chunk else None

    normalized: List[Any] = []

    for entry in branch:
        if isinstance(entry, (list, tuple)):
            entry_list = list(entry)
            while len(entry_list) < 2:
                entry_list.append(None)
            for pos in range(2):
                if entry_list[pos] is None:
                    continue
                chunk = take_chunk()
                if pos == 0:
                    chunk = _capitalize_first(chunk)
                entry_list[pos] = chunk
            normalized.append(tuple(entry_list))
        else:
            normalized.append(entry)

    while index < len(words):
        first = _capitalize_first(take_chunk())
        second = take_chunk()
        normalized.append((first, second))

    return normalized


def _normalize_rama(rama: Any, palabras_por_slot: int) -> Any:
    if isinstance(rama, dict):
        rama_copia = dict(rama)
        rama_copia["ramas"] = [_normalize_rama(r, palabras_por_slot) for r in rama.get("ramas", [])]
        return rama_copia
    if isinstance(rama, list):
        return _normalize_branch(rama, palabras_por_slot)
    return rama


def normalizar_concept_map(concept_map: Any, palabras_por_slot: int = 2) -> Any:
    """Devuelve una copia de concept_map con tuplas normalizadas a n palabras por lado."""
    if palabras_por_slot <= 0:
        raise ValueError("palabras_por_slot debe ser mayor que 0")
    if not isinstance(concept_map, list):
        return concept_map

    data = deepcopy(concept_map)
    for grupo in data:
        subtitulos = grupo.get("subtitulos", [])
        for subtitulo in subtitulos:
            ramas = subtitulo.get("ramas", [])
            subtitulo["ramas"] = [_normalize_rama(rama, palabras_por_slot) for rama in ramas]
    return data
