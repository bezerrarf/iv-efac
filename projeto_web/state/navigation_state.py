import reflex as rx

class NavigationState(rx.State):
    """Estado isolado para gerenciar a navegação e o sistema de telas responsivo."""
    
    tela_ativa: str = "inicio"
    indice_tela: int = 0
    
    TELAS_ORDEM = ["inicio", "eixos", "palestrantes", "programacao", "submissoes", "local", "sobre"]

    def set_tela(self, tela: str):
        if tela in self.TELAS_ORDEM:
            self.tela_ativa = tela
            self.indice_tela = self.TELAS_ORDEM.index(tela)

    def navegar_para_tela(self, tela: str):
        """Define a tela ativa e redireciona para a home de qualquer rota do site."""
        self.set_tela(tela)
        return rx.redirect("/")

    def proxima_tela(self):
        prox = (self.indice_tela + 1) % len(self.TELAS_ORDEM)
        self.indice_tela = prox
        self.tela_ativa = self.TELAS_ORDEM[prox]

    def tela_anterior(self):
        ant = (self.indice_tela - 1 + len(self.TELAS_ORDEM)) % len(self.TELAS_ORDEM)
        self.indice_tela = ant
        self.tela_ativa = self.TELAS_ORDEM[ant]
