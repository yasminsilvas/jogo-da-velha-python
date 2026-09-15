import streamlit as st
import random

st.set_page_config(page_title="Jogo da Velha", page_icon="❌")
st.title("❌ Jogo da Velha (Projeto Python)")

# Controla a memória do jogo no navegador
if "tabuleiro" not in st.session_state:
    st.session_state.tabuleiro = [1, 2, 3, 4, "X", 6, 7, 8, 9] # X começa no meio
    st.session_state.status = "Sua vez! Escolha um quadrado livre."

def obter_livres():
    return [i for i, v in enumerate(st.session_state.tabuleiro) if isinstance(v, int)]

def verificar_vitoria(s):
    t = st.session_state.tabuleiro
    vitorias = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(t[a] == s and t[b] == s and t[c] == s for a, b, c in vitorias)

def reiniciar():
    st.session_state.tabuleiro = [1, 2, 3, 4, "X", 6, 7, 8, 9]
    st.session_state.status = "Sua vez! Escolha um quadrado livre."

def clique(idx):
    if isinstance(st.session_state.tabuleiro[idx], int) and "ganhou" not in st.session_state.status and "Empate" not in st.session_state.status:
        # 1. Turno do Usuário
        st.session_state.tabuleiro[idx] = "O"
        if verificar_vitoria("O"):
            st.session_state.status = "🎉 Você ganhou!"
            return
        
        livres = obter_livres()
        if not livres:
            st.session_state.status = "🤝 Empate!"
            return
            
        # 2. Turno do Computador Inteligente
        vitorias = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        t = st.session_state.tabuleiro
        mov_comp = None
        
        # Regra A: Se o PC puder ganhar nesta jogada, ele ganha
        for a, b, c in vitorias:
            if t[a] == "X" and t[b] == "X" and isinstance(t[c], int): mov_comp = c
            elif t[a] == "X" and t[c] == "X" and isinstance(t[b], int): mov_comp = b
            elif t[b] == "X" and t[c] == "X" and isinstance(t[a], int): mov_comp = a
            if mov_comp is not None: break
            
        # Regra B: Se o jogador estiver para ganhar, o PC bloqueia
        if mov_comp is None:
            for a, b, c in vitorias:
                if t[a] == "O" and t[b] == "O" and isinstance(t[c], int): mov_comp = c
                elif t[a] == "O" and t[c] == "O" and isinstance(t[b], int): mov_comp = b
                elif t[b] == "O" and t[c] == "O" and isinstance(t[a], int): mov_comp = a
                if mov_comp is not None: break
                
        # Regra C: Se não tiver jogada urgente, joga aleatório
        if mov_comp is None:
            mov_comp = random.choice(livres)
            
        st.session_state.tabuleiro[mov_comp] = "X"
        if verificar_vitoria("X"):
            st.session_state.status = "🤖 O computador ganhou!"
            return
        if not obter_livres():
            st.session_state.status = "🤝 Empate!"

# Interface visual em colunas
cols = st.columns(3)
for i in range(9):
    valor = st.session_state.tabuleiro[i]
    bloqueado = not isinstance(valor, int) or "ganhou" in st.session_state.status or "Empate" in st.session_state.status
    with cols[i % 3]:
        st.button(str(valor), key=f"b_{i}", on_click=clique, args=(i,), disabled=bloqueado, use_container_width=True)

st.subheader(st.session_state.status)
st.button("Reiniciar Jogo", on_click=reiniciar)