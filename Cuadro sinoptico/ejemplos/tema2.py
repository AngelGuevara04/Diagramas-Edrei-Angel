"""
Ejemplo pequeno de cuadro sinoptico.
Tema: Scrum basico.

Incluye:
- Ramas intermedias (dict anidados).
- Listas de ideas (list).
- Nodos hoja sin llave ([]).
- Un nodo tipo texto directo (str).
- Dos estilos de llave (rounded y plain) para probar el diseno.
"""
{
    "Scrum (resumen rapido)": {
        "Roles": {
            "Product Owner": [
                "Define prioridad del Product Backlog.",
                "Alinea valor de negocio con el objetivo del sprint.",
            ],
            "Scrum Master": [
                "Facilita eventos y elimina bloqueos del equipo.",
                "Promueve mejora continua y buenas practicas agiles.",
            ],
            "Equipo de desarrollo": {
                "Responsabilidades": [
                    "Construir incremento funcional en cada sprint.",
                    "Autoorganizarse para cumplir el Sprint Goal.",
                ],
                "Nota": "Equipo pequeno y multidisciplinario para entregar valor frecuente.",
            },
        },
        "Eventos": {
            "Sprint Planning": [
                "Define objetivo y selecciona trabajo comprometido.",
            ],
            "Daily Scrum": [
                "Sincronizacion diaria de 15 minutos.",
            ],
            "Review": [
                "Se presenta el incremento a interesados y se recibe retroalimentacion.",
            ],
            "Retrospective": [],
        },
        "Artefactos": {
            "Product Backlog": [
                "Lista viva y ordenada de necesidades del producto.",
            ],
            "Sprint Backlog": [
                "Plan del equipo para alcanzar el objetivo del sprint.",
            ],
            "Incremento": [
                "Resultado util y potencialmente liberable.",
            ],
        },
        "Idea clave": [
            "Iterar corto, inspeccionar seguido y adaptar decisiones con datos reales.",
        ],
    }
}

