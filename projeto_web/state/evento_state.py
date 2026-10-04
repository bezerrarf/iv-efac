"""Ponte reativa (Reflex State) que consome os Controllers (MVC)."""

import reflex as rx
from typing import Optional
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.repositories.database import init_db
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.controllers.usuario_controller import UsuarioController

# Inicialização do banco na subida do backend
init_db()

# Injeção de dependências do Controller (DIP)
_hasher = PBKDF2PasswordHasher()
_repo = SQLiteUsuarioRepository()
_usuario_controller = UsuarioController(repository=_repo, hasher=_hasher)


class EventoState(rx.State):
    """Estado global reativo da interface visual."""

    # --- Estatísticas ---
    total_inscritos: int = 0
    vagas_restantes: int = 300

    # --- Sessão do Usuário ---
    is_logged_in: bool = False
    user_id: int = 0
    user_nome: str = ""
    user_email: str = ""
    user_instituicao: str = ""
    user_modalidade: str = ""
    user_area: str = ""
    user_codigo: str = ""

    # --- Formulário de Cadastro ---
    cad_nome: str = ""
    cad_email: str = ""
    cad_senha: str = ""
    cad_instituicao: str = ""
    cad_modalidade: str = "Presencial"
    cad_area: str = "Ciência de Dados / IA"

    # --- Formulário de Login ---
    login_email: str = ""
    login_senha: str = ""

    # --- Mensagens de Feedback ---
    feedback_msg: str = ""
    feedback_tipo: str = ""  # 'success', 'error', 'info', ''

    # --- Filtros de Cronograma ---
    dia_selecionado: str = "Dia 1"

    # --- Sistema de Telas Responsivo (Screen Switcher) ---
    tela_ativa: str = "inicio"
    indice_tela: int = 0

    TELAS_ORDEM = ["inicio", "eixos", "palestrantes", "programacao", "submissoes", "local", "sobre"]

    def set_tela(self, tela: str):
        if tela in self.TELAS_ORDEM:
            self.tela_ativa = tela
            self.indice_tela = self.TELAS_ORDEM.index(tela)

    def proxima_tela(self):
        prox = (self.indice_tela + 1) % len(self.TELAS_ORDEM)
        self.indice_tela = prox
        self.tela_ativa = self.TELAS_ORDEM[prox]

    def tela_anterior(self):
        ant = (self.indice_tela - 1 + len(self.TELAS_ORDEM)) % len(self.TELAS_ORDEM)
        self.indice_tela = ant
        self.tela_ativa = self.TELAS_ORDEM[ant]

    # --- Setters explícitos ---
    def set_cad_nome(self, val: str):
        self.cad_nome = val

    def set_cad_email(self, val: str):
        self.cad_email = val

    def set_cad_senha(self, val: str):
        self.cad_senha = val

    def set_cad_instituicao(self, val: str):
        self.cad_instituicao = val

    def set_cad_modalidade(self, val: str):
        self.cad_modalidade = val

    def set_cad_area(self, val: str):
        self.cad_area = val

    def set_login_email(self, val: str):
        self.login_email = val

    def set_login_senha(self, val: str):
        self.login_senha = val

    def set_dia(self, dia: str):
        self.dia_selecionado = dia

    def carregar_stats(self):
        """Atualiza números consumindo o Controller."""
        stats = _usuario_controller.obter_estatisticas()
        self.total_inscritos = stats["total_inscritos"]
        self.vagas_restantes = stats["vagas_restantes"]

    def limpar_feedback(self):
        self.feedback_msg = ""
        self.feedback_tipo = ""

    def realizar_cadastro(self):
        """Dispara caso de uso de cadastro no Controller."""
        self.limpar_feedback()
        res = _usuario_controller.cadastrar(
            nome=self.cad_nome,
            email=self.cad_email,
            senha=self.cad_senha,
            instituicao=self.cad_instituicao,
            modalidade=self.cad_modalidade,
            area=self.cad_area,
        )

        if not res.sucesso or res.dado is None:
            self.feedback_msg = res.mensagem
            self.feedback_tipo = "error"
            return

        usuario = res.dado
        self.is_logged_in = True
        self.user_id = usuario.id or 0
        self.user_nome = usuario.nome
        self.user_email = usuario.email
        self.user_instituicao = usuario.instituicao
        self.user_modalidade = usuario.modalidade
        self.user_area = usuario.area
        self.user_codigo = usuario.codigo_inscricao

        self.feedback_msg = f"{res.mensagem} Seu código oficial é {usuario.codigo_inscricao}"
        self.feedback_tipo = "success"

        # Limpa formulário
        self.cad_nome = ""
        self.cad_email = ""
        self.cad_senha = ""
        self.cad_instituicao = ""
        self.carregar_stats()

    def realizar_login(self):
        """Dispara caso de uso de autenticação no Controller."""
        self.limpar_feedback()
        res = _usuario_controller.autenticar(
            email=self.login_email,
            senha=self.login_senha,
        )

        if not res.sucesso or res.dado is None:
            self.feedback_msg = res.mensagem
            self.feedback_tipo = "error"
            return

        usuario = res.dado
        self.is_logged_in = True
        self.user_id = usuario.id or 0
        self.user_nome = usuario.nome
        self.user_email = usuario.email
        self.user_instituicao = usuario.instituicao
        self.user_modalidade = usuario.modalidade
        self.user_area = usuario.area
        self.user_codigo = usuario.codigo_inscricao

        self.feedback_msg = f"Bem-vindo(a) de volta, {usuario.nome}!"
        self.feedback_tipo = "success"

        self.login_email = ""
        self.login_senha = ""

    def alterar_modalidade_usuario(self, nova_modalidade: str):
        """Permite ao usuário logado alterar sua modalidade via Controller."""
        if not self.is_logged_in or not self.user_id:
            return

        res = _usuario_controller.alterar_modalidade(
            user_id=self.user_id,
            nova_modalidade=nova_modalidade,
        )

        if res.sucesso and res.dado is not None:
            self.user_modalidade = res.dado.modalidade
            self.feedback_msg = res.mensagem
            self.feedback_tipo = "success"
        else:
            self.feedback_msg = res.mensagem
            self.feedback_tipo = "error"

    def logout(self):
        """Encerra a sessão do usuário."""
        self.is_logged_in = False
        self.user_id = 0
        self.user_nome = ""
        self.user_email = ""
        self.user_codigo = ""
        self.feedback_msg = "Sessão encerrada com sucesso."
        self.feedback_tipo = "info"
