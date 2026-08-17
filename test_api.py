import urllib.request, json
data = {
    'map_data_str': '''concept_map = [
    {
        "titulo_principal": "El Sistema Solar",
        "subtitulos": [
            {
                "titulo": "Estrella Central",
                "conector": "tiene una",
                "ramas": [
                    [
                        (None, "llamada"), 
                        ("Sol", "que proporciona"), 
                        ("Luz y calor", "a los"), 
                        ("Planetas", None)
                    ]
                ]
            }
        ]
    }
]''',
    'config': {
        "FONT_FAMILY": "Arial",
        "FONT_SIZE": 10,
        "FONT_COLOR": "#000000",
        "FONT_BOLD": False,
        "FONT_ITALIC": False,
        "STROKE_W": 1,
        "EDGE_COLOR": "#676363",
        "BOX_ARC_SIZE": 8,
        "BOX_SHADOW": False,
        "MAIN_FILL_COLOR": "#e67c4f",
        "MAIN_STROKE_COLOR": "#000000",
        "SUBTITLE_FILL_COLOR": "#8AAEE0",
        "SUBTITLE_STROKE_COLOR": "#000000",
        "CONNECTOR_FONT_FAMILY": "Arial",
        "CONNECTOR_FONT_SIZE": 8,
        "CONNECTOR_FONT_COLOR": "#000000",
        "CONNECTOR_BG_COLOR": "#FFFFFF",
        "CONNECTOR_BORDER_COLOR": "none",
        "CONNECTOR_SHADOW": False,
        "CONNECTOR_TEXT_SHADOW": False,
        "BOX_W": 80,
        "BOX_H": 40,
        "X_STEP": 120,
        "Y_STEP": 90,
        "POSITION_NOISE": 0,
        "MAIN_TO_SUBTITLE": 130,
        "SUBTITLE_TO_BRANCH": 120,
        "SUBTITLE_GAP": 80,
        "GROUP_GAP": 300,
        "COLOR_SUBTITLE_GROUPS": True,
        "COLOR_NESTED_SUBTOPICS": False,
        "PALETTE": [
            ["#b7d3f6", "#000000"],
            ["#d9f3b0", "#000000"],
            ["#f3caca", "#000000"],
            ["#eccff1", "#000000"]
        ]
    }
}
req = urllib.request.Request('http://localhost:8000/api/generate/concept', method='POST')
req.add_header('Content-Type', 'application/json')
try:
    with urllib.request.urlopen(req, data=json.dumps(data).encode('utf-8')) as res:
        print('HTTP', res.status)
        print(res.read().decode('utf-8')[:100])
except urllib.error.HTTPError as e:
    print('HTTP ERROR', e.code)
    print(e.read().decode('utf-8'))
except Exception as e:
    print('ERROR:', e)
