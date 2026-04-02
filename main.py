from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import uvicorn
import time
import os

app = FastAPI()

# Liberar o Front-end para falar com o Backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

ADB_PATH = r"C:\Users\Nickolas Cremasco\Dropbox\scrcpy-win64-v3.3.4\scrcpy-win64-v3.3.4\adb.exe"

DESTINOS = {
    "casa": "Rua Nome da Sua Rua, 123 - Bairro",
    "hospital": "Hospital Municipal de São Paulo",
    "mercado": "Supermercado Extra"
}

# Rota para acionar o Uber
@app.get("/api/uber")
async def acionar_uber(local: str):  
    try:
        # 1. Abre o aplicativo da Uber
        os.system(f'"{ADB_PATH}" shell monkey -p com.ubercab -c android.intent.category.LAUNCHER 1')
        time.sleep(8) # Tempo de segurança para o app carregar

        # 2. Clica no campo "Para onde?"
        os.system(f'"{ADB_PATH}" shell input tap 500 900')
        time.sleep(2)

        # 3. Pega o endereço do dicionário ou usa o que veio do front
        endereco = DESTINOS.get(local.lower(), local)
        print(f"🚀 Solicitando Uber para: {endereco}")

        # 4. Digita o endereço (o %s substitui os espaços)
        endereco_adb = endereco.replace(" ", "%s")
        os.system(f'"{ADB_PATH}" shell input text {endereco_adb}')
        time.sleep(1)

        # 5. Pressiona ENTER
        os.system(f'"{ADB_PATH}" shell input keyevent 66')

        return {"status": "sucesso", "local": endereco}
    except Exception as e:
        print(f"Erro: {e}")
        return {"status": "erro", "detalhes": str(e)}

# Rota para Emergência (Ligar para o Filho)
@app.get("/api/emergencia")
async def acionar_emergencia(quem: str):
    print(f"[LOG] ALERTA CRÍTICO: {quem}")
    
    # Exemplo: Faz o celular discar para um número (ex: 192 ou o número do filho)
    numero = "11974557734" if quem == "ambulancia" else "11999999999"
    subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.CALL", "-d", f"tel:{numero}"])
    
    return {"status": "alerta_enviado"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)