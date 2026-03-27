from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import uvicorn

app = FastAPI()

# Liberar o Front-end para falar com o Backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota para acionar o Uber
@app.get("/api/uber")
async def acionar_uber(destino: str):
    print(f"[LOG] Solicitando transporte para: {destino}")
    
    try:
        # 1. Abre o app do Uber via ADB
        # O comando 'am start' inicia uma Activity específica
        subprocess.run(["adb", "shell", "am", "start", "-n", "com.ubercab/com.ubercab.presidio.app.core.root.RootActivity"], check=True)
        
        # 2. Simulação de automação: Espera o app abrir e clica no campo de busca
        # (Os valores de X e Y variam por aparelho, use 'adb shell wm size' para calibrar)
        # subprocess.run(["adb", "shell", "input", "tap", "500", "1000"]) 
        
        return {"status": "sucesso", "destino": destino}
    except Exception as e:
        return {"status": "erro", "detalhes": str(e)}

# Rota para Emergência (Ligar para o Filho)
@app.get("/api/emergencia")
async def acionar_emergencia(quem: str):
    print(f"[LOG] ALERTA CRÍTICO: {quem}")
    
    # Exemplo: Faz o celular discar para um número (ex: 192 ou o número do filho)
    numero = "192" if quem == "ambulancia" else "11999999999"
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.CALL", "-d", f"tel:{numero}"])
    
    return {"status": "alerta_enviado"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)