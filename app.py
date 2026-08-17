import os
import sys
import subprocess
import time
import signal

def main():
    # The port assigned by Render, defaults to 8000 for local testing
    port = int(os.environ.get("PORT", 8000))
    
    # Internal ports for the backend services
    concept_port = "8001"
    mind_port = "8002"
    synoptic_port = "8003"
    
    # When deployed on Render or another cloud platform, the hostname needs to be bound to 0.0.0.0
    host = "0.0.0.0"

    print(f"Starting orchestration on port {port}...")

    processes = []
    
    p1 = subprocess.Popen([
        sys.executable, "Mapa conceptual/servidor_mapa_conceptual.py", "--port", concept_port
    ])
    processes.append(p1)
    print(f"Started Backend Mapa conceptual on internal port {concept_port}...")

    p2 = subprocess.Popen([
        sys.executable, "Mapa mental/servidor_mapa_mental.py", "--port", mind_port
    ])
    processes.append(p2)
    print(f"Started Backend Mapa mental on internal port {mind_port}...")

    p3 = subprocess.Popen([
        sys.executable, "Cuadro sinoptico/servidor_cuadro_sinoptico.py", "--port", synoptic_port
    ])
    processes.append(p3)
    print(f"Started Backend Cuadro sinoptico on internal port {synoptic_port}...")

    time.sleep(2)

    print(f"Starting main proxy server on {host}:{port}...")
    p_main = subprocess.Popen([
        sys.executable, "servidor_centro_diagramas.py", 
        "--host", host,
        "--port", str(port),
        "--concept-port", concept_port,
        "--mind-port", mind_port
    ])
    processes.append(p_main)

    def cleanup(signum, frame):
        print("\nShutting down all servers...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    try:
        p_main.wait()
    except KeyboardInterrupt:
        cleanup(None, None)

if __name__ == "__main__":
    main()
