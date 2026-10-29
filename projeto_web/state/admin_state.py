import reflex as rx
from typing import Optional, List, Dict, Any
from datetime import datetime
from projeto_web.core.export_service import gerar_csv_inscritos, gerar_pdf_inscritos
from projeto_web.controllers.evento_controller import EventoController
from projeto_web.state.auth_state import AuthState
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.controllers.usuario_controller import UsuarioController

_hasher = PBKDF2PasswordHasher()
_repo = SQLiteUsuarioRepository()
_usuario_controller = UsuarioController(repository=_repo, hasher=_hasher)


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
    # Edição Completa de Participante pelo Administrador
    modal_editar_participante_aberto: bool = False
    admin_edit_user_id: int = 0
    admin_edit_nome: str = ""
    admin_edit_email: str = ""
    admin_edit_instituicao: str = ""
    admin_edit_modalidade: str = "Presencial"
    admin_edit_area: str = "Astrofísica"
    admin_edit_role: str = "participante"
    admin_edit_presenca_d1: bool = False
    admin_edit_presenca_d2: bool = False
    # Links dos Modelos de Apresentação e Submissão
    link_modelo_resumo: str = "https://docs.google.com/document/d/1tp2I660zIwhE8SpjEmeSdNa4aGOx5TAN/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true"
    link_modelo_slides: str = "https://docs.google.com/presentation/d/1iUEyNN3E_IglPo508DiXv8wOgi9emzqJ/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true"
    link_modelo_poster: str = "https://docs.google.com/presentation/d/1p12rVh3LbCWgHostLjOYgxG1Z0tpk1qc/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true"
    admin_link_resumo_input: str = "https://docs.google.com/document/d/1tp2I660zIwhE8SpjEmeSdNa4aGOx5TAN/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true"
    admin_link_slides_input: str = "https://docs.google.com/presentation/d/1iUEyNN3E_IglPo508DiXv8wOgi9emzqJ/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true"
    admin_link_poster_input: str = "https://docs.google.com/presentation/d/1p12rVh3LbCWgHostLjOYgxG1Z0tpk1qc/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true"
    is_creating_atividade: bool = False
    new_ativ_dia: str = "Dia 1"
    new_ativ_horario: str = "08:00 – 09:30"
    new_ativ_titulo: str = ""
    new_ativ_palestrante: str = ""
    new_ativ_local: str = "Auditório Principal - Campus Brejo Santo"
    new_ativ_tipo: str = "Conferência"
    new_ativ_descricao: str = ""
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
    def carregar_links_modelos(self):
        """Carrega os links configurados dos modelos a partir do repositório."""
        try:
            from projeto_web.repositories.config_repository import ConfigRepository
            repo = ConfigRepository()
            self.link_modelo_resumo = repo.get("link_modelo_resumo", self.link_modelo_resumo)
            self.link_modelo_slides = repo.get("link_modelo_slides", self.link_modelo_slides)
            self.link_modelo_poster = repo.get("link_modelo_poster", self.link_modelo_poster)
            self.admin_link_resumo_input = self.link_modelo_resumo
            self.admin_link_slides_input = self.link_modelo_slides
            self.admin_link_poster_input = self.link_modelo_poster
        except Exception:
            pass

    def set_admin_link_resumo_input(self, val: str):
        self.admin_link_resumo_input = val

    def set_admin_link_slides_input(self, val: str):
        self.admin_link_slides_input = val

    def set_admin_link_poster_input(self, val: str):
        self.admin_link_poster_input = val

    def salvar_links_modelos(self):
        """Salva novos links de modelos acadêmicos definidos pelo Administrador."""
        if not self.is_admin:
            self.feedback_msg = "Apenas administradores podem atualizar os links dos modelos."
            self.feedback_tipo = "error"
            return
        try:
            from projeto_web.repositories.config_repository import ConfigRepository
            repo = ConfigRepository()
            if self.admin_link_resumo_input.strip():
                self.link_modelo_resumo = self.admin_link_resumo_input.strip()
                repo.set("link_modelo_resumo", self.link_modelo_resumo)
            if self.admin_link_slides_input.strip():
                self.link_modelo_slides = self.admin_link_slides_input.strip()
                repo.set("link_modelo_slides", self.link_modelo_slides)
            if self.admin_link_poster_input.strip():
                self.link_modelo_poster = self.admin_link_poster_input.strip()
                repo.set("link_modelo_poster", self.link_modelo_poster)

            self.feedback_msg = "Links dos modelos atualizados com sucesso no sistema!"
            self.feedback_tipo = "success"
        except Exception as e:
            self.feedback_msg = f"Erro ao salvar links: {str(e)}"
            self.feedback_tipo = "error"

    def carregar_painel_admin(self):
        """Carrega e filtra a lista de inscritos e calcula métricas para o admin."""
        if hasattr(self, "is_admin") and not self.is_admin:
            return
        self.carregar_atividades_admin()
        self.carregar_links_modelos()
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
                "presenca_dia1": bool(getattr(u, "presenca_dia1", False)),
                "presenca_dia2": bool(getattr(u, "presenca_dia2", False)),
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
    def alternar_presenca_dia(self, user_id: Any, dia: str):
        """Alterna a presença de um inscrito em um dia específico."""
        try:
            uid = int(user_id)
        except Exception:
            return
        res = _usuario_controller.alternar_presenca(uid, dia=dia)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        self.carregar_painel_admin()
        if hasattr(self, "carregar_painel_supervisor"):
            self.carregar_painel_supervisor()

    def excluir_participante_admin(self):
        """Exclui o participante atualmente selecionado no modal de edição (Exclusivo para Administradores)."""
        role_atual = getattr(self, "user_role", "admin" if getattr(self, "is_admin", False) else "participante")
        if not getattr(self, "is_admin", False) or role_atual != "admin":
            self.feedback_msg = "Permissão negada: somente administradores podem excluir cadastros."
            self.feedback_tipo = "error"
            return

        if not self.admin_edit_user_id:
            return

        # Impede autoexclusão acidental da própria conta de administrador logado
        meu_user_id = int(getattr(self, "user_id", 0) or 0)
        alvo_user_id = int(self.admin_edit_user_id)
        if meu_user_id and meu_user_id == alvo_user_id:
            self.feedback_msg = "Você não pode excluir sua própria conta de administrador."
            self.feedback_tipo = "error"
            return

        res = _usuario_controller.excluir_participante(alvo_user_id, solicitante_role=role_atual)
        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso:
            self.modal_editar_participante_aberto = False
            self.admin_edit_user_id = 0
            self.carregar_painel_admin()
            if hasattr(self, "carregar_painel_supervisor"):
                self.carregar_painel_supervisor()


    def abrir_modal_editar_participante(self, user_data: Dict[str, Any]):
        """Abre o modal de edição completa com os dados atuais do participante."""
        if not self.is_admin:
            return
        self.admin_edit_user_id = int(user_data.get("id", 0))
        self.admin_edit_nome = str(user_data.get("nome", ""))
        self.admin_edit_email = str(user_data.get("email", ""))
        self.admin_edit_instituicao = str(user_data.get("instituicao", ""))
        self.admin_edit_modalidade = str(user_data.get("modalidade", "Presencial"))
        self.admin_edit_area = str(user_data.get("area", "Astrofísica"))
        self.admin_edit_role = str(user_data.get("role", "participante"))
        self.admin_edit_presenca_d1 = bool(user_data.get("presenca_dia1", False))
        self.admin_edit_presenca_d2 = bool(user_data.get("presenca_dia2", False))
        self.modal_editar_participante_aberto = True

    def fechar_modal_editar_participante(self):
        """Fecha o modal de edição completa."""
        self.modal_editar_participante_aberto = False

    def set_admin_edit_nome(self, val: str):
        self.admin_edit_nome = val

    def set_admin_edit_email(self, val: str):
        self.admin_edit_email = val

    def set_admin_edit_instituicao(self, val: str):
        self.admin_edit_instituicao = val

    def set_admin_edit_modalidade(self, val: str):
        self.admin_edit_modalidade = val

    def set_admin_edit_area(self, val: str):
        self.admin_edit_area = val

    def set_admin_edit_role(self, val: str):
        self.admin_edit_role = val

    def toggle_admin_edit_presenca_d1(self, val: bool):
        self.admin_edit_presenca_d1 = val

    def toggle_admin_edit_presenca_d2(self, val: bool):
        self.admin_edit_presenca_d2 = val

    def salvar_edicao_participante(self):
        """Persiste as alterações completas do participante realizadas pelo admin."""
        if not self.is_admin or not self.admin_edit_user_id:
            return

        res = _usuario_controller.atualizar_participante_completo(
            user_id=self.admin_edit_user_id,
            nome=self.admin_edit_nome,
            email=self.admin_edit_email,
            instituicao=self.admin_edit_instituicao,
            modalidade=self.admin_edit_modalidade,
            area=self.admin_edit_area,
            role=self.admin_edit_role,
            presenca_dia1=self.admin_edit_presenca_d1,
            presenca_dia2=self.admin_edit_presenca_d2,
        )

        self.feedback_msg = res.mensagem
        self.feedback_tipo = "success" if res.sucesso else "error"
        if res.sucesso:
            self.modal_editar_participante_aberto = False
            self.carregar_painel_admin()
            if hasattr(self, "carregar_painel_supervisor"):
                self.carregar_painel_supervisor()

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
            if hasattr(self, "carregar_programacao_publica"):
                self.carregar_programacao_publica()
        else:
            self.feedback_msg = "Erro ao salvar alterações da atividade."
            self.feedback_tipo = "error"
    def excluir_atividade(self, ativ_id: Any):
        """Exclui uma atividade da grade oficial pelo Administrador."""
        if not self.is_admin:
            return
        try:
            aid = int(ativ_id)
        except Exception:
            return
        ok = EventoController.excluir_atividade(aid)
        if ok:
            self.feedback_msg = "Atividade excluída com sucesso da grade oficial!"
            self.feedback_tipo = "success"
            self.is_editing_atividade = False
            self.carregar_atividades_admin()
            if hasattr(self, "carregar_programacao_publica"):
                self.carregar_programacao_publica()
        else:
            self.feedback_msg = "Erro ao excluir atividade."
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
            if hasattr(self, "carregar_programacao_publica"):
                self.carregar_programacao_publica()
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
            if hasattr(self, "carregar_programacao_publica"):
                self.carregar_programacao_publica()
        else:
            self.feedback_msg = "Erro ao delegar nova atividade."
            self.feedback_tipo = "error"

    def abrir_modal_senha(self, user_id: Any, user_nome: str):
        try:
            self.admin_senha_user_id = int(user_id)
        except Exception:
            self.admin_senha_user_id = 0
        self.admin_senha_user_nome = str(user_nome)
        self.admin_nova_senha_input = ""
        self.modal_alterar_senha_aberto = True

    def fechar_modal_senha(self):
        self.modal_alterar_senha_aberto = False
        self.admin_senha_user_id = 0
        self.admin_nova_senha_input = ""
