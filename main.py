from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uiautomator2 as u2
import uvicorn
import time

app = FastAPI()

# 1. Configuração de CORS (Libera o Front-end)
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

# 3. Seus Favoritos
DESTINOS = {
    "casa": "Rua Nome da Sua Rua, 123 - Bairro",
    "hospital": "Hospital Israelita Albert Einstein Morumbi",
    "mercado": "Supermercado Extra"
}

# 4. Rota do Uber (Lógica de Seleção de Destino)
@app.get("/api/uber")
async def acionar_uber(local: str):  
    try:
        print(f"🚀 Iniciando processo para: {local}")
        
        # Abre o Uber do zero
        d.app_start("com.ubercab", stop=True)
        
        # Espera o botão "Para onde?" aparecer e clica
        if d(text="Para onde?").wait(timeout=15):
            d(text="Para onde?").click()
        else:
            d(description="Para onde?").click()

        time.sleep(1)

        # Busca o endereço e digita
        endereco = DESTINOS.get(local.lower(), local)
        print(f"✍️ Digitando: {endereco}")
        d.send_keys(endereco, clear=True)
        
        # --- AJUSTE PARA CLICAR NO PRIMEIRO RESULTADO ---
        print("⏳ Aguardando lista de sugestões...")
        time.sleep(3) # Tempo para o Uber buscar os endereços na internet

        # Tentativa de clicar no primeiro item da lista de resultados
        # O Uber usa uma lista; clicamos no primeiro elemento que aparece na área de resultados
        # Se o ID abaixo não funcionar, o d.click(500, 600) servirá como "clique manual" no topo da lista
        if d(resourceId="com.ubercab:id/ub__location_search_results_list").exists:
            print("🎯 Clicando no primeiro resultado da lista (via ID)")
            d(resourceId="com.ubercab:id/ub__location_search_results_list").child(index=0).click()
        else:
            print("🎯 Clicando no primeiro resultado (via coordenada)")
            # Coordenada aproximada do primeiro item da lista no Moto G86
            d.click(500, 600) 

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