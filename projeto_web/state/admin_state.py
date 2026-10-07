import reflex as rx
from typing import Optional, List, Dict, Any
from datetime import datetime
from projeto_web.core.export_service import gerar_csv_inscritos, gerar_pdf_inscritos
from projeto_web.controllers.evento_controller import EventoController
from projeto_web.state.auth_state import AuthState

class AdminState(AuthState):
    """Estado isolado para gerenciar o Painel Administrativo, Atividades e Crachás."""
    admin_filtro_busca: str = ""
    admin_inscritos: List[Dict[str, Any]] = []
    admin_total_inscritos: int = 0
    admin_total_presenciais: int = 0
    admin_total_onlines: int = 0
    admin_total_presentes: int = 0
    admin_total_supervisores: int = 0
    admin_senha_user_id: int = 0
    admin_senha_user_nome: str = ""
    admin_nova_senha_input: str = ""
    modal_alterar_senha_aberto: bool = False
    admin_propria_senha_input: str = ""
    admin_propria_senha_confirm: str = ""
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
    is_creating_atividade: bool = False
    new_ativ_dia: str = "Dia 1"
    new_ativ_horario: str = "08:00 – 09:30"
    new_ativ_titulo: str = ""
    new_ativ_palestrante: str = ""
    new_ativ_local: str = "Auditório Principal - Campus Brejo Santo"
    new_ativ_tipo: str = "Conferência"
    new_ativ_descricao: str = ""
    admin_carteirinha_aberta: bool = False
    admin_carteirinha_nome: str = ""
    admin_carteirinha_email: str = ""
    admin_carteirinha_inst: str = ""
    admin_carteirinha_mod: str = ""
    admin_carteirinha_cod: str = ""
    admin_carteirinha_foto: str = ""
    admin_carteirinha_role: str = ""
    def set_admin_filtro(self, termo: str):
        self.admin_filtro_busca = termo
        self.carregar_painel_admin()
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

