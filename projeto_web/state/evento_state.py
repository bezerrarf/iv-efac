from projeto_web.core.quotes_service import carregar_frases_cientistas
"""Ponte reativa (Reflex State) que consome os Controllers (MVC)."""

from typing import List, Dict, Any, Optional
from datetime import datetime
import reflex as rx
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.core.export_service import gerar_csv_inscritos, gerar_pdf_inscritos
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
    usuario_logado_email_confirmado: bool = False
    email_confirmado: bool = False
    is_admin: bool = False
    is_supervisor: bool = False

    # Gestão de Perfil do Participante
    modal_perfil_aberto: bool = False
    perfil_nome_input: str = ""
    perfil_instituicao_input: str = ""
    perfil_modalidade_input: str = "Presencial"

    # Gestão de Senha Pessoal
    minha_senha_atual_input: str = ""
    minha_nova_senha_input: str = ""
    minha_nova_senha_confirm: str = ""

    # Confirmação de E-mail
    modal_confirmacao_email_aberto: bool = False
    codigo_email_input: str = ""
    codigo_email_enviado_preview: str = "" 

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

    # Gestão de Senhas pelo Administrador
    admin_senha_user_id: int = 0
    admin_senha_user_nome: str = ""
    admin_nova_senha_input: str = ""
    modal_alterar_senha_aberto: bool = False

    admin_propria_senha_input: str = ""
    admin_propria_senha_confirm: str = ""

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

    # Criação e Delegação de Nova Atividade pelo Admin
    is_creating_atividade: bool = False
    new_ativ_dia: str = "Dia 1"
    new_ativ_horario: str = "08:00 – 09:30"
    new_ativ_titulo: str = ""
    new_ativ_palestrante: str = ""
    new_ativ_local: str = "Auditório Principal - Campus Brejo Santo"
    new_ativ_tipo: str = "Conferência"
    new_ativ_descricao: str = ""

    # Visualização e Emissão da Carteirinha pelo Admin
    admin_carteirinha_aberta: bool = False
    admin_carteirinha_nome: str = ""
    admin_carteirinha_email: str = ""
    admin_carteirinha_inst: str = ""
    admin_carteirinha_mod: str = ""
    admin_carteirinha_cod: str = ""
    admin_carteirinha_foto: str = ""
    admin_carteirinha_role: str = ""

    # --- Painel de Supervisão / Conferência de Presença ---
    superv_busca: str = ""
    superv_inscritos: List[Dict[str, Any]] = []
    superv_presentes_count: int = 0
    superv_total_count: int = 0

    # --- Contagem Regressiva & Mensagens Inspiradoras dos Cientistas ---
    evento_iniciado_preview: bool = False
    frase_cientista_indice: int = 0

    FRASES_CIENTISTAS: List[Dict[str, str]] = carregar_frases_cientistas()

    def alternar_preview_evento_iniciado(self):
        """Alterna entre o relógio de contagem e a mensagem comemorativa com frases dos cientistas."""
        self.evento_iniciado_preview = not self.evento_iniciado_preview

    def proxima_frase_cientista(self):
        """Avança para a próxima frase inspiradora."""
        self.frase_cientista_indice = (self.frase_cientista_indice + 1) % len(self.FRASES_CIENTISTAS)

    def frase_anterior_cientista(self):
        """Retorna para a frase inspiradora anterior."""
        self.frase_cientista_indice = (self.frase_cientista_indice - 1 + len(self.FRASES_CIENTISTAS)) % len(self.FRASES_CIENTISTAS)

    @rx.var
    def frase_cientista_autor(self) -> str:
        idx = self.frase_cientista_indice % len(self.FRASES_CIENTISTAS)
        return self.FRASES_CIENTISTAS[idx]["autor"]

    @rx.var
    def frase_cientista_area(self) -> str:
        idx = self.frase_cientista_indice % len(self.FRASES_CIENTISTAS)
        return self.FRASES_CIENTISTAS[idx]["area"]

    @rx.var
    def frase_cientista_texto(self) -> str:
        idx = self.frase_cientista_indice % len(self.FRASES_CIENTISTAS)
        return self.FRASES_CIENTISTAS[idx]["frase"]

    @rx.var
    def frase_cientista_cor(self) -> str:
        idx = self.frase_cientista_indice % len(self.FRASES_CIENTISTAS)
        return self.FRASES_CIENTISTAS[idx]["cor"]

    @rx.var
    def frase_cientista_icone(self) -> str:
        idx = self.frase_cientista_indice % len(self.FRASES_CIENTISTAS)
        return self.FRASES_CIENTISTAS[idx].get("icone", "sparkles")

    @rx.var
    def frase_cientista_paginacao(self) -> str:
        idx = self.frase_cientista_indice % len(self.FRASES_CIENTISTAS)
        return f"Mensagem {idx + 1} de {len(self.FRASES_CIENTISTAS)}"



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

    def set_badge_foto_input(self, val: Any):
        if isinstance(val, str):
            self.badge_foto_input = val
        else:
            self.badge_foto_input = ""

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
        self.usuario_logado_email_confirmado = bool(getattr(usuario, "email_confirmado", False))
        self.email_confirmado = self.usuario_logado_email_confirmado
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
        self.usuario_logado_email_confirmado = bool(getattr(usuario, "email_confirmado", False))
        self.email_confirmado = self.usuario_logado_email_confirmado
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

    async def handle_upload_foto(self, files: List[rx.UploadFile]):
        """Recebe o arquivo de imagem enviado do computador ou dispositivo móvel (celular/tablet)."""
        if not self.is_logged_in or not self.user_id:
            self.feedback_msg = "Você precisa estar logado para atualizar sua foto."
            self.feedback_tipo = "error"
            return

        if not files:
            self.feedback_msg = "Nenhum arquivo de imagem foi selecionado."
            self.feedback_tipo = "error"
            return

        import base64
        for file in files:
            upload_data = await file.read()
            if len(upload_data) > 6 * 1024 * 1024:
                self.feedback_msg = "A foto selecionada ultrapassa o limite de 6MB."
                self.feedback_tipo = "error"
                return

            nome_arq = (file.filename or "").lower()
            mime = "image/jpeg"
            if nome_arq.endswith(".png"):
                mime = "image/png"
            elif nome_arq.endswith(".webp"):
                mime = "image/webp"

            b64_str = base64.b64encode(upload_data).decode("utf-8")
            data_uri = f"data:{mime};base64,{b64_str}"

            res = _usuario_controller.atualizar_foto(self.user_id, data_uri)
            if res.sucesso and res.dado:
                self.user_foto_url = data_uri
                self.feedback_msg = "Foto da carteirinha enviada com sucesso do seu dispositivo!"
                self.feedback_tipo = "success"
                return
            else:
                self.feedback_msg = res.mensagem
                self.feedback_tipo = "error"
                return

    # --- Ações do Admin ---
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

    # --- Gestão de Senhas (Inscritos e Próprio Admin) ---
    def abrir_modal_senha(self, user_id: Any, user_nome: str):
        """Abre o formulário de alteração de senha de um participante."""
        try:
            self.admin_senha_user_id = int(user_id)
        except Exception:
            return
        self.admin_senha_user_nome = str(user_nome)
        self.admin_nova_senha_input = ""
        self.modal_alterar_senha_aberto = True

    def fechar_modal_senha(self):
        """Fecha o formulário modal de alteração de senha."""
        self.modal_alterar_senha_aberto = False
        self.admin_senha_user_id = 0
        self.admin_senha_user_nome = ""
        self.admin_nova_senha_input = ""

    def set_admin_nova_senha(self, val: str):
        self.admin_nova_senha_input = val

    def salvar_nova_senha_inscrito(self):
        """Persiste a nova senha definida pelo administrador para o inscrito selecionado."""
        if not self.is_admin or not self.admin_senha_user_id:
            return
        res = _usuario_controller.alterar_senha(self.admin_senha_user_id, self.admin_nova_senha_input)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso:
            self.modal_alterar_senha_aberto = False
            self.admin_nova_senha_input = ""

    def set_admin_propria_senha(self, val: str):
        self.admin_propria_senha_input = val

    def set_admin_propria_senha_confirm(self, val: str):
        self.admin_propria_senha_confirm = val

    def salvar_propria_senha_admin(self):
        """Admin altera com segurança a sua própria credencial de acesso."""
        if not self.is_admin or not self.user_id:
            return
        if not self.admin_propria_senha_input or len(self.admin_propria_senha_input.strip()) < 6:
            self.feedback_msg = "A nova senha deve possuir no mínimo 6 caracteres."
            self.feedback_tipo = "error"
            return
        if self.admin_propria_senha_input != self.admin_propria_senha_confirm:
            self.feedback_msg = "A confirmação de senha não coincide com a nova senha digitada."
            self.feedback_tipo = "error"
            return
        res = _usuario_controller.alterar_senha(self.user_id, self.admin_propria_senha_input)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso:
            self.admin_propria_senha_input = ""
            self.admin_propria_senha_confirm = ""

    # --- Exportação Oficial da Lista de Inscritos (CSV e PDF) para Admin e Supervisores ---
    def exportar_inscritos_csv(self):
        """Gera e dispara o download da relação de participantes em formato CSV para Admin e Supervisores."""
        if not (self.is_admin or self.is_supervisor):
            self.feedback_msg = "Permissão negada: apenas administradores e supervisores podem baixar a lista."
            self.feedback_tipo = "error"
            return
        usuarios = _usuario_controller.listar_inscritos()
        csv_str = gerar_csv_inscritos(usuarios)
        data_tag = datetime.now().strftime("%Y%m%d_%H%M")
        return rx.download(data=csv_str, filename=f"inscritos_iv_efac_{data_tag}.csv")

    def exportar_inscritos_pdf(self):
        """Gera e dispara o download do relatório oficial de credenciamento em PDF para Admin e Supervisores."""
        if not (self.is_admin or self.is_supervisor):
            self.feedback_msg = "Permissão negada: apenas administradores e supervisores podem baixar a lista."
            self.feedback_tipo = "error"
            return
        usuarios = _usuario_controller.listar_inscritos()
        stats = _usuario_controller.obter_estatisticas()
        pdf_bytes = gerar_pdf_inscritos(usuarios, stats)
        data_tag = datetime.now().strftime("%Y%m%d_%H%M")
        return rx.download(data=pdf_bytes, filename=f"relatorio_oficial_inscritos_iv_efac_{data_tag}.pdf")

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

    # Criação e Delegação Manual de Atividades pelo Admin
    def abrir_criacao_atividade(self):
        """Abre o formulário para criar e delegar uma nova atividade na grade."""
        self.is_creating_atividade = True
        self.new_ativ_titulo = ""
        self.new_ativ_palestrante = ""
        self.new_ativ_descricao = ""

    def fechar_criacao_atividade(self):
        self.is_creating_atividade = False

    def set_new_ativ_dia(self, val: str):
        self.new_ativ_dia = val

    def set_new_ativ_horario(self, val: str):
        self.new_ativ_horario = val

    def set_new_ativ_titulo(self, val: str):
        self.new_ativ_titulo = val

    def set_new_ativ_palestrante(self, val: str):
        self.new_ativ_palestrante = val

    def set_new_ativ_local(self, val: str):
        self.new_ativ_local = val

    def set_new_ativ_tipo(self, val: str):
        self.new_ativ_tipo = val

    def set_new_ativ_descricao(self, val: str):
        self.new_ativ_descricao = val

    def criar_nova_atividade(self):
        """Persiste nova atividade criada e delegada pelo admin."""
        if not self.is_admin:
            return
        if not self.new_ativ_titulo.strip():
            self.feedback_msg = "Informe o título ou tema da atividade."
            self.feedback_tipo = "error"
            return

        ok = EventoController.adicionar_atividade(
            dia=self.new_ativ_dia,
            horario=self.new_ativ_horario,
            titulo=self.new_ativ_titulo,
            palestrante=self.new_ativ_palestrante,
            local=self.new_ativ_local,
            tipo=self.new_ativ_tipo,
            descricao=self.new_ativ_descricao,
        )
        if ok:
            self.feedback_msg = "Nova atividade criada e delegada com sucesso!"
            self.feedback_tipo = "success"
            self.is_creating_atividade = False
            self.carregar_atividades_admin()
        else:
            self.feedback_msg = "Erro ao delegar nova atividade."
            self.feedback_tipo = "error"

    # Inspeção e Emissão de Carteirinha de Participante pelo Admin
    def ver_carteirinha_admin(self, user_id: Any):
        """Abre a carteirinha oficial do participante selecionado para visualização/impressão."""
        try:
            uid = int(user_id)
        except Exception:
            return
        u = _usuario_controller._repository.find_by_id(uid)
        if u:
            self.admin_carteirinha_nome = u.nome
            self.admin_carteirinha_email = u.email
            self.admin_carteirinha_inst = u.instituicao
            self.admin_carteirinha_mod = u.modalidade
            self.admin_carteirinha_cod = u.codigo_inscricao
            self.admin_carteirinha_foto = u.foto_url or ""
            self.admin_carteirinha_role = u.role
            self.admin_carteirinha_aberta = True

    def fechar_carteirinha_admin(self):
        self.admin_carteirinha_aberta = False

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
        self.usuario_logado_email_confirmado = False
        self.email_confirmado = False
        self.modal_perfil_aberto = False
        self.modal_confirmacao_email_aberto = False
        self.is_admin = False
        self.is_supervisor = False
        self.admin_inscritos = []
        self.superv_inscritos = []
        self.is_editing_atividade = False
        self.feedback_msg = "Sessão encerrada com sucesso."
        self.feedback_tipo = "info"


    # --- Gestão de Perfil, Senha e Confirmação de E-mail ---
    def abrir_modal_perfil(self):
        """Abre o modal de edição de perfil e sincroniza os campos atuais."""
        if not self.is_logged_in:
            return
        self.perfil_nome_input = self.user_nome
        self.perfil_instituicao_input = self.user_instituicao
        self.perfil_modalidade_input = self.user_modalidade
        self.minha_senha_atual_input = ""
        self.minha_nova_senha_input = ""
        self.minha_nova_senha_confirm = ""
        self.modal_perfil_aberto = True

    def fechar_modal_perfil(self):
        self.modal_perfil_aberto = False

    def set_perfil_nome(self, val: str):
        self.perfil_nome_input = val

    def set_perfil_instituicao(self, val: str):
        self.perfil_instituicao_input = val

    def set_perfil_modalidade(self, val: str):
        self.perfil_modalidade_input = val

    def salvar_meu_perfil(self):
        """Salva as alterações de perfil no banco de dados."""
        if not self.is_logged_in or not self.user_id:
            return
        res = _usuario_controller.atualizar_perfil(
            user_id=self.user_id,
            nome=self.perfil_nome_input,
            instituicao=self.perfil_instituicao_input,
            modalidade=self.perfil_modalidade_input,
        )
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso and res.dado:
            self.user_nome = res.dado.nome
            self.user_instituicao = res.dado.instituicao
            self.user_modalidade = res.dado.modalidade
            self.modal_perfil_aberto = False

    def set_minha_senha_atual(self, val: str):
        self.minha_senha_atual_input = val

    def set_minha_nova_senha(self, val: str):
        self.minha_nova_senha_input = val

    def set_minha_nova_senha_confirm(self, val: str):
        self.minha_nova_senha_confirm = val

    def salvar_minha_nova_senha(self):
        """Altera com segurança a senha do usuário logado (participante ou admin)."""
        if not self.is_logged_in or not self.user_id:
            return
        res = _usuario_controller.alterar_minha_senha(
            user_id=self.user_id,
            senha_atual=self.minha_senha_atual_input,
            nova_senha=self.minha_nova_senha_input,
            confirma_senha=self.minha_nova_senha_confirm,
        )
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso:
            self.minha_senha_atual_input = ""
            self.minha_nova_senha_input = ""
            self.minha_nova_senha_confirm = ""

    def abrir_confirmacao_email(self):
        self.modal_confirmacao_email_aberto = True
        self.codigo_email_input = ""

    def fechar_confirmacao_email(self):
        self.modal_confirmacao_email_aberto = False

    def set_codigo_email(self, val: str):
        self.codigo_email_input = val

    def solicitar_codigo_email(self):
        """Gera um código de confirmação com orientações anti-spam."""
        if not self.is_logged_in or not self.user_id:
            return
        res = _usuario_controller.gerar_codigo_confirmacao(self.user_id)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso and res.dado:
            self.codigo_email_enviado_preview = res.dado

    def confirmar_email_codigo(self):
        """Valida o código digitado pelo participante e libera as submissões."""
        if not self.is_logged_in or not self.user_id:
            return
        res = _usuario_controller.confirmar_email(self.user_id, self.codigo_email_input)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso:
            self.usuario_logado_email_confirmado = True
            self.email_confirmado = True
            self.modal_confirmacao_email_aberto = False

    def confirmar_email_direto(self):
        """Confirmação direta de e-mail com 1 clique."""
        if not self.is_logged_in or not self.user_id:
            return
        res = _usuario_controller.confirmar_email(self.user_id)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso:
            self.usuario_logado_email_confirmado = True
            self.email_confirmado = True
            self.modal_confirmacao_email_aberto = False

    # --- Emissão da Carteirinha Oficial em Imagem PNG de Alta Resolução ---
    def baixar_minha_carteirinha_png(self):
        """Gera e baixa a imagem oficial PNG da carteirinha do participante logado."""
        if not self.is_logged_in:
            return
        from projeto_web.core.badge_service import BadgeService
        img_bytes = BadgeService.gerar_imagem_carteirinha(
            nome=self.user_nome,
            email=self.user_email,
            instituicao=self.user_instituicao,
            modalidade=self.user_modalidade,
            role=self.user_role,
            codigo=self.user_codigo,
            email_confirmado=self.usuario_logado_email_confirmado,
            foto_url=self.user_foto_url or None,
            base_assets_path="assets",
        )
        cod_clean = self.user_codigo.replace(" ", "_")
        return rx.download(data=img_bytes, filename=f"carteirinha_ivefac_{cod_clean}.png")

    def baixar_carteirinha_admin_png(self):
        """Gera e baixa a imagem PNG da carteirinha selecionada pelo Admin."""
        from projeto_web.core.badge_service import BadgeService
        img_bytes = BadgeService.gerar_imagem_carteirinha(
            nome=self.admin_carteirinha_nome,
            email=self.admin_carteirinha_email,
            instituicao=self.admin_carteirinha_inst,
            modalidade=self.admin_carteirinha_mod,
            role=self.admin_carteirinha_role,
            codigo=self.admin_carteirinha_cod,
            email_confirmado=True,
            foto_url=self.admin_carteirinha_foto or None,
            base_assets_path="assets",
        )
        cod_clean = (self.admin_carteirinha_cod or "001").replace(" ", "_")
        return rx.download(data=img_bytes, filename=f"carteirinha_ivefac_{cod_clean}.png")
