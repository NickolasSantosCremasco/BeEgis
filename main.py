from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uiautomator2 as u2
import uvicorn
import time

app = FastAPI()

# 1. Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Conexão com o Celular
try:
    d = u2.connect()
    print("✅ Motorola conectado via UIAutomator2")
except Exception as e:
    print(f"❌ Falha na conexão: {e}")

# 3. Favoritos (Ajuste os nomes para serem precisos)
DESTINOS = {
    "casa": "Sua Rua aqui, 123",
    "hospital": "Hospital Israelita Albert Einstein",
    "mercado": "Supermercado Extra"
}

# 4. Rota do Uber
@app.get("/api/uber")
async def acionar_uber(local: str):  
    try:
        print(f"🚀 Iniciando Uber para: {local}")
        
        # Abre o Uber do zero
        d.app_start("com.ubercab", stop=True)
        
        # Espera o campo "Para onde?" aparecer e clica
        if d(text="Para onde?").wait(timeout=15):
            d(text="Para onde?").click()
        else:
            d(description="Para onde?").click()

        time.sleep(1)

        # Busca o endereço e digita
        endereco = DESTINOS.get(local.lower(), local)
        print(f"✍️ Digitando: {endereco}")
        d.send_keys(endereco, clear=True)
        
        # --- LÓGICA DE SELEÇÃO CORRIGIDA (Baseada no seu WEditor) ---
        print("⏳ Aguardando resultados do Uber...")
        time.sleep(5) # Tempo extra para a internet carregar a lista

        # Tentativa 1: Procurar pelo texto na descrição (Content-desc)
        # O Weditor mostrou que o endereço fica guardado aqui
        resultado = d(descriptionContains=endereco)

        if resultado.exists:
            print(f"🎯 Resultado encontrado por descrição! Clicando...")
            resultado.click()
            
        # Tentativa 2: Usar o clique proporcional que você extraiu do Weditor
        # No seu print era (0.7, 0.295). Usamos 0.35 para pegar no centro da caixa.
        else:
            print("🎯 Descrição não achada, usando clique certeiro por coordenada (Weditor)")
            # 0.7 = 70% da largura | 0.35 = 35% da altura
            d.click(0.7, 0.35) 

        return {"status": "sucesso", "local": endereco}
    except Exception as e:
        print(f"⚠️ Erro: {e}")
        return {"status": "erro", "detalhes": str(e)}

# 5. Rota de Emergência
@app.get("/api/emergencia")
async def acionar_emergencia(quem: str):
    numero = "11974557734" if quem == "ambulancia" else "11999999999"
    print(f"🚨 Chamando emergência: {numero}")
    d.shell(f"am start -a android.intent.action.CALL -d tel:{numero}")
    return {"status": "alerta_enviado"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)