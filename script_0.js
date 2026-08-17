
    const defaultCode = `concept_map = [
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
            },
            {
                "titulo": "Cuerpos Celestes",
                "conector": "formado por",
                "ramas": [
                    [
                        (None, "se dividen en"),
                        {
                            "texto": "Categorías",
                            "conector": "que son",
                            "bifurcaciones": [
                                [
                                    (None, "los"), 
                                    ("Rocosos", "como la"), 
                                    ("Tierra y Marte", None)
                                ],
                                [
                                    (None, "y los"), 
                                    ("Gaseosos", "como"), 
                                    ("Júpiter y Saturno", None)
                                ]
                            ]
                        }
                    ],
                    [
                        (None, "también incluye"),
                        ("Asteroides", "y"),
                        ("Cometas", None)
                    ]
                ]
            }
        ]
    }
]`;

    let configData = {
        "FONT_FAMILY": "Arial",
        "FONT_SIZE": 10,
        "FONT_COLOR": "#000000",
        "FONT_BOLD": false,
        "FONT_ITALIC": false,
        "STROKE_W": 1,
        "EDGE_COLOR": "#676363",
        "BOX_ARC_SIZE": 8,
        "BOX_SHADOW": false,
        "MAIN_FILL_COLOR": "#e67c4f",
        "MAIN_STROKE_COLOR": "#000000",
        "SUBTITLE_FILL_COLOR": "#8AAEE0",
        "SUBTITLE_STROKE_COLOR": "#000000",
        "CONNECTOR_FONT_FAMILY": "Arial",
        "CONNECTOR_FONT_SIZE": 8,
        "CONNECTOR_FONT_COLOR": "#000000",
        "CONNECTOR_BG_COLOR": "#FFFFFF",
        "CONNECTOR_BORDER_COLOR": "none",
        "CONNECTOR_SHADOW": false,
        "CONNECTOR_TEXT_SHADOW": false,
        "BOX_W": 80,
        "BOX_H": 40,
        "X_STEP": 120,
        "Y_STEP": 90,
        "POSITION_NOISE": 0,
        "MAIN_TO_SUBTITLE": 130,
        "SUBTITLE_TO_BRANCH": 120,
        "SUBTITLE_GAP": 80,
        "GROUP_GAP": 300,
        "COLOR_SUBTITLE_GROUPS": true,
        "COLOR_NESTED_SUBTOPICS": false,
        "PALETTE": [
            ["#b7d3f6", "#000000"],
            ["#d9f3b0", "#000000"],
            ["#f3caca", "#000000"],
            ["#eccff1", "#000000"],
        ]
    };

    // Tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.target).classList.add('active');
        if(btn.dataset.target === 'editorTab') editor.refresh();
      });
    });

    // CodeMirror
    const editor = CodeMirror(document.getElementById('editorTabContent'), {
      value: defaultCode,
      mode: "python",
      theme: "monokai",
      lineNumbers: true,
      indentUnit: 4,
    });

    let debounceTimer;
    editor.on("change", () => {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(updatePreview, 800);
    });

    async function updatePreview() {
      const code = editor.getValue();
      const meta = document.getElementById("previewMeta");
      meta.innerText = "Generando...";
      try {
        const res = await fetch("/api/generate/concept", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            map_data_str: code,
            config: configData
          })
        });
        if(!res.ok) throw new Error(await res.text());
        const xml = await res.text();
        
        const iframe = document.getElementById('drawioIframe');
        iframe.contentWindow.postMessage(JSON.stringify({action: 'load', xml: xml}), '*');
        meta.innerText = "Sincronizado";
      } catch (err) {
        meta.innerText = "Error";
        console.error(err);
      }
    }

    // IA Logic
    document.getElementById("btnApplyGemini").addEventListener("click", async () => {
      const prompt = document.getElementById("geminiPrompt").value;
      if(!prompt) return;
      const status = document.getElementById("iaStatus");
      status.innerText = "Pensando...";
      
      try {
        const res = await fetch("/api/ia/concept-map", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            instruction: prompt,
            concept_map: editor.getValue()
          })
        });
        const data = await res.json();
        if(data.ok) {
           const jsonStr = JSON.stringify(data.concept_map, null, 4);
           // Convert JSON format back to Python tuples for UI
           let pythonStr = "concept_map = " + jsonStr.replace(/\\[null,/g, "(None,");
           editor.setValue(pythonStr);
           status.innerText = "¡Aplicado!";
        } else {
           status.innerText = "Error: " + data.error;
        }
      } catch (err) {
        status.innerText = "Error de red.";
      }
    });

    // Form builder logic
    function buildForm() {
       const form = document.getElementById("configForm");
       form.innerHTML = "";
       for(const key in configData) {
          if(key === "PALETTE") continue;
          const div = document.createElement("div");
          div.style.marginBottom = "5px";
          const label = document.createElement("label");
          label.innerText = key + ": ";
          label.style.display = "inline-block";
          label.style.width = "180px";
          const input = document.createElement("input");
          input.value = configData[key];
          if(typeof configData[key] === "boolean") {
              input.type = "checkbox";
              input.checked = configData[key];
              input.onchange = (e) => { configData[key] = e.target.checked; updatePreview(); };
          } else {
              input.type = "text";
              input.onchange = (e) => { 
                let val = e.target.value;
                if(!isNaN(val)) val = parseFloat(val);
                configData[key] = val; 
                updatePreview(); 
              };
          }
          div.appendChild(label);
          div.appendChild(input);
          form.appendChild(div);
       }
    }
    buildForm();

    // Iframe communication
    window.addEventListener('message', function(e) {
        if (e.data == 'ready') {
            updatePreview();
        }
    });

    // Guardar .drawio
    document.getElementById("btnSaveAs").addEventListener("click", async () => {
        try {
            const res = await fetch("/api/generate/concept", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                map_data_str: editor.getValue(),
                config: configData
              })
            });
            const xml = await res.text();
            const blob = new Blob([xml], { type: "application/xml" });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "Mapa_Conceptual.drawio";
            a.click();
        } catch(e) { console.error(e); }
    });

  