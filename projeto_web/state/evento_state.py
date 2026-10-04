"""Ponte reativa (Reflex State) que consome os Controllers (MVC)."""

from typing import List, Dict, Any, Optional
import reflex as rx
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.repositories.database import init_db
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.controllers.usuario_controller import UsuarioController
from projeto_web.controllers.evento_controller import EventoController

# Inicialização do banco na subida do backend
init_db()

# Injeção de dependências do Controller (DIP)
_hasher = PBKDF2PasswordHasher()
_repo = SQLiteUsuarioRepository()
_usuario_controller = UsuarioController(repository=_repo, hasher=_hasher)


class EventoState(rx.State):
    """Estado global reativo da interface visual do IV EFAC."""

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
    user_role: str = "participante"  # 'participante', 'supervisor', 'admin'
    user_foto_url: str = ""
    user_presenca: bool = False
    is_admin: bool = False
    is_supervisor: bool = False

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

    # --- Cartão de Identificação Digital / Crachá (Badge) ---
    badge_modo: str = "participante"  # 'participante' ou 'palestrante'
    badge_foto_input: str = ""
    badge_palestrante_nome: str = "Prof.(a) Dr.(a) Convidado(a)"
    badge_palestrante_inst: str = "UFCA / Instituição Parceira"
    badge_palestrante_tema: str = "Astrofísica Teórica, Ondas Gravitacionais e Matéria Densa"
    badge_palestrante_horario: str = "18h00 • Conferência Magna"

    # --- Painel do Administrador ---
    admin_filtro_busca: str = ""
    admin_inscritos: List[Dict[str, Any]] = []
    admin_total_inscritos: int = 0
    admin_total_presenciais: int = 0
    admin_total_onlines: int = 0
    admin_total_presentes: int = 0
    admin_total_supervisores: int = 0

    # Editor de Atividades / Programação pelo Admin
    admin_atividades: List[Dict[str, Any]] = []
    edit_ativ_id: int = 0
    edit_ativ_dia: str = "Dia 1"
    edit_ativ_horario: str = ""
    edit_ativ_titulo: str = ""
    edit_ativ_palestrante: str = ""
    edit_ativ_local: str = ""
    edit_ativ_tipo: str = ""
    edit_ativ_descricao: str = ""
    is_editing_atividade: bool = False

    # --- Painel de Supervisão / Conferência de Presença ---
    superv_busca: str = ""
    superv_inscritos: List[Dict[str, Any]] = []
    superv_presentes_count: int = 0
    superv_total_count: int = 0

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

    def set_badge_modo(self, modo: str):
        if modo in ["participante", "palestrante"]:
            self.badge_modo = modo

    def set_badge_foto_input(self, val: str):
        self.badge_foto_input = val

    def set_admin_filtro(self, termo: str):
        self.admin_filtro_busca = termo
        self.carregar_painel_admin()

    def set_superv_busca(self, termo: str):
        self.superv_busca = termo
        self.carregar_painel_supervisor()

    def set_edit_ativ_dia(self, val: str):
        self.edit_ativ_dia = val

    def set_edit_ativ_horario(self, val: str):
        self.edit_ativ_horario = val

    def set_edit_ativ_titulo(self, val: str):
        self.edit_ativ_titulo = val

    def set_edit_ativ_palestrante(self, val: str):
        self.edit_ativ_palestrante = val

    def set_edit_ativ_local(self, val: str):
        self.edit_ativ_local = val

    def set_edit_ativ_tipo(self, val: str):
        self.edit_ativ_tipo = val

    def set_edit_ativ_descricao(self, val: str):
        self.edit_ativ_descricao = val

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
        self.user_role = getattr(usuario, "role", "participante")
        self.user_foto_url = getattr(usuario, "foto_url", "") or ""
        self.user_presenca = bool(getattr(usuario, "presenca_confirmada", False))
        self.is_admin = (self.user_role == "admin")
        self.is_supervisor = (self.user_role in ["supervisor", "admin"])

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
        self.user_role = getattr(usuario, "role", "participante")
        self.user_foto_url = getattr(usuario, "foto_url", "") or ""
        self.user_presenca = bool(getattr(usuario, "presenca_confirmada", False))
        self.is_admin = (self.user_role == "admin")
        self.is_supervisor = (self.user_role in ["supervisor", "admin"])

        if self.is_admin:
            self.carregar_painel_admin()
            self.carregar_atividades_admin()
        if self.is_supervisor:
            self.carregar_painel_supervisor()

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

    def salvar_foto_perfil(self):
        """Atualiza a foto do participante para exibição no cartão."""
        if not self.is_logged_in or not self.user_id:
            return
        foto_str = str(self.badge_foto_input or "").strip()
        if not foto_str:
            self.feedback_msg = "Informe a URL da foto ou selecione um preset."
            self.feedback_tipo = "error"
            return

        res = _usuario_controller.atualizar_foto(self.user_id, foto_str)
        if res.sucesso and res.dado:
            self.user_foto_url = res.dado.foto_url or ""
            self.feedback_msg = "Foto do cartão atualizada com sucesso!"
            self.feedback_tipo = "success"
            self.badge_foto_input = ""
        else:
            self.feedback_msg = res.mensagem
            self.feedback_tipo = "error"

    def definir_avatar_preset(self, url: Any):
        """Aplica um avatar pré-definido ao perfil do usuário."""
        if isinstance(url, dict):
            return
        self.badge_foto_input = str(url)
        self.salvar_foto_perfil()

    # --- Ações do Super Admin ---
    def carregar_painel_admin(self):
        """Carrega e filtra a lista de inscritos e calcula métricas para o admin."""
        usuarios = _usuario_controller.listar_inscritos(self.admin_filtro_busca)
        self.admin_inscritos = [
            {
                "id": u.id,
                "nome": u.nome,
                "email": u.email,
                "instituicao": u.instituicao,
                "modalidade": u.modalidade,
                "area": u.area,
                "codigo": u.codigo_inscricao,
                "role": getattr(u, "role", "participante"),
                "is_supervisor": (getattr(u, "role", "participante") == "supervisor"),
                "presenca_confirmada": bool(getattr(u, "presenca_confirmada", False)),
            }
            for u in usuarios
        ]

        stats = _usuario_controller.obter_estatisticas()
        self.admin_total_inscritos = stats["total_inscritos"]
        self.admin_total_presenciais = stats["presenciais"]
        self.admin_total_onlines = stats["onlines"]
        self.admin_total_presentes = stats["presentes"]
        self.admin_total_supervisores = stats["supervisores"]

    def promover_supervisor(self, user_id: Any):
        """Admin concede poderes de supervisor a um participante."""
        if not self.is_admin:
            return
        try:
            uid = int(user_id)
        except Exception:
            return
        res = _usuario_controller.alterar_role(uid, "supervisor")
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        self.carregar_painel_admin()

    def rebaixar_supervisor(self, user_id: Any):
        """Admin revoga poderes de supervisor de um participante."""
        if not self.is_admin:
            return
        try:
            uid = int(user_id)
        except Exception:
            return
        res = _usuario_controller.alterar_role(uid, "participante")
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        self.carregar_painel_admin()

    # Editor de Atividades / Palestras
    def carregar_atividades_admin(self):
        """Carrega todas as atividades salvas para edição no painel admin."""
        atividades = EventoController.obter_todas_atividades()
        self.admin_atividades = [
            {
                "id": a.id or 0,
                "dia": a.dia,
                "horario": a.horario,
                "titulo": a.titulo,
                "palestrante": a.palestrante,
                "local": a.local,
                "tipo": a.tipo,
                "descricao": a.descricao,
            }
            for a in atividades
        ]

    def abrir_edicao_atividade(self, ativ_id: Any):
        """Abre o formulário de edição com os dados da atividade selecionada."""
        try:
            aid = int(ativ_id)
        except Exception:
            return
        for at in self.admin_atividades:
            if at["id"] == aid:
                self.edit_ativ_id = aid
                self.edit_ativ_dia = at["dia"]
                self.edit_ativ_horario = at["horario"]
                self.edit_ativ_titulo = at["titulo"]
                self.edit_ativ_palestrante = at["palestrante"]
                self.edit_ativ_local = at["local"]
                self.edit_ativ_tipo = at["tipo"]
                self.edit_ativ_descricao = at["descricao"]
                self.is_editing_atividade = True
                return

    def fechar_edicao_atividade(self):
        self.is_editing_atividade = False
        self.edit_ativ_id = 0

    def salvar_edicao_atividade(self):
        """Persiste as alterações da palestra/atividade no banco de dados."""
        if not self.is_admin or not self.edit_ativ_id:
            return

        ok = EventoController.atualizar_atividade(
            id=self.edit_ativ_id,
            dia=self.edit_ativ_dia,
            horario=self.edit_ativ_horario,
            titulo=self.edit_ativ_titulo,
            palestrante=self.edit_ativ_palestrante,
            local=self.edit_ativ_local,
            tipo=self.edit_ativ_tipo,
            descricao=self.edit_ativ_descricao,
        )

        if ok:
            self.feedback_msg = "Atividade e tema atualizados com sucesso no cronograma oficial!"
            self.feedback_tipo = "success"
            self.is_editing_atividade = False
            self.carregar_atividades_admin()
        else:
            self.feedback_msg = "Erro ao salvar alterações da atividade."
            self.feedback_tipo = "error"

    def restaurar_grade_padrao(self):
        """Restaura todas as atividades para os valores originais."""
        if not self.is_admin:
            return
        ok = EventoController.restaurar_programacao_padrao()
        if ok:
            self.feedback_msg = "Grade oficial de programação restaurada com sucesso!"
            self.feedback_tipo = "success"
            self.carregar_atividades_admin()
        else:
            self.feedback_msg = "Erro ao restaurar a grade de programação."
            self.feedback_tipo = "error"

    # --- Ações de Supervisor (Conferência de Presença) ---
    def carregar_painel_supervisor(self):
        """Carrega lista de inscritos para credenciamento e presença."""
        usuarios = _usuario_controller.listar_inscritos(self.superv_busca)
        self.superv_inscritos = [
            {
                "id": u.id,
                "nome": u.nome,
                "email": u.email,
                "instituicao": u.instituicao,
                "modalidade": u.modalidade,
                "codigo": u.codigo_inscricao,
                "presenca_confirmada": bool(getattr(u, "presenca_confirmada", False)),
            }
            for u in usuarios
        ]
        self.superv_total_count = len(self.superv_inscritos)
        self.superv_presentes_count = sum(1 for item in self.superv_inscritos if item["presenca_confirmada"])

    def alternar_presenca_participante(self, user_id: Any):
        """Supervisor ou admin marca/desmarca presença do inscrito."""
        if not self.is_supervisor:
            return
        try:
            uid = int(user_id)
        except Exception:
            return
        res = _usuario_controller.alternar_presenca(uid)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        self.carregar_painel_supervisor()
        if self.is_admin:
            self.carregar_painel_admin()

    def logout(self):
        """Encerra a sessão do usuário."""
        self.is_logged_in = False
        self.user_id = 0
        self.user_nome = ""
        self.user_email = ""
        self.user_codigo = ""
        self.user_role = "participante"
        self.user_foto_url = ""
        self.user_presenca = False
        self.is_admin = False
        self.is_supervisor = False
        self.admin_inscritos = []
        self.superv_inscritos = []
        self.is_editing_atividade = False
        self.feedback_msg = "Sessão encerrada com sucesso."
        self.feedback_tipo = "info"
