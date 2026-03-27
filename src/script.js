/**
 * BeEgis - Core Script
 * Organizado de cima para baixo: Configurações -> Inicialização -> Ações
 */

// 1. CONFIGURAÇÕES (ROTEAMENTO E PADRÕES)
const ROUTES = {
    'destinos': 'src/pages/trip.html',
    'casa': 'src/pages/house.html',
    'ajuda': 'src/pages/emergency.html',
    'home': '../../index.html'
};

const VIBRATION_PATTERNS = {
    'sos': [100, 50, 100, 50, 100, 50, 500],
    'click': [50]
};

// 2. INICIALIZAÇÃO (ANIMAÇÕES DE ENTRADA)
window.addEventListener("DOMContentLoaded", () => {
    // Garante que o container comece invisível para evitar "pulo" visual
    gsap.from("#app-container", {
        duration: 0.6,
        x: 100,
        opacity: 0,
        ease: "power2.out"
    });
});

// 3. NAVEGAÇÃO
function navigateTo(destination) {
    const targetUrl = ROUTES[destination];

    if (!targetUrl) return;

    // Feedback visual e animação de saída
    gsap.to("#app-container", {
        duration: 0.4,
        x: -100,
        opacity: 0,
        ease: "power2.in",
        onComplete: () => {
            window.location.href = targetUrl;
        }
    });
}

// 4. SISTEMA DE EMERGÊNCIA
function alertar(tipo) {
    executarFeedbackTatico('sos');
    
    const mensagem = obterMensagemDeAlerta(tipo);
    atualizarInterfaceEmergencia(mensagem);
    
    // Futuro: Chamada para o Backend Python aqui
    enviarAlertaServidor(tipo);
}

// 5. FUNÇÕES DE APOIO (HELPERS)
function executarFeedbackTatico(padrao) {
    if ("vibrate" in navigator) {
        navigator.vibrate(VIBRATION_PATTERNS[padrao]);
    }
}

function obterMensagemDeAlerta(tipo) {
    return tipo === 'filho' 
        ? 'Ligando para seu filho...' 
        : 'Acionando SAMU/Ambulância...';
}

function atualizarInterfaceEmergencia(texto) {
    const statusText = document.querySelector('.footer-alert');
    if (statusText) {
        statusText.innerHTML = `<strong>${texto}</strong>`;
        statusText.style.backgroundColor = "#1A1A1A";
    }
}

async function enviarAlertaServidor(tipo) {
    try {
        const response = await fetch(`http://localhost:8000/api/emergencia?quem=${tipo}`);
        const data = await response.json();
        console.log("Resposta do Servidor:", data);
    } catch (error) {
        console.error("Servidor offline. Certifique-se que o main.py está rodando.");
    }
}

// Na tela de Trip, quando clicar no card:
async function solicitarUber(destinoNome) {
    try {
        await fetch(`http://localhost:8000/api/uber?destino=${destinoNome}`);
        navigateTo('casa'); // Vai para a tela de acompanhamento
    } catch (error) {
        alert("Erro ao conectar com o BeEgis Desktop");
    }
}