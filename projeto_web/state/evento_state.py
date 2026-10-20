import time
import asyncio
from projeto_web.state.supervisor_state import SupervisorState
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


def _obter_atividades_iniciais(dia: str) -> List[Dict[str, Any]]:
    return [
        {
            "id": a.id or 0,
            "horario": a.horario,
            "titulo": a.titulo,
            "palestrante": a.palestrante,
            "local": a.local,
            "tipo": a.tipo,
            "descricao": a.descricao,
            "tipo_color": a.tipo_color,
        }
        for a in EventoController.obter_programacao_padrao(dia)
    ]


class EventoState(SupervisorState):
    """Estado global reativo da interface visual do IV EFAC."""

    # --- Estatísticas ---
    total_inscritos: int = 0
    vagas_restantes: int = 300

    # --- Sessão do Usuário ---

    # Gestão de Perfil do Participante

    # Gestão de Senha Pessoal

    # Confirmação de E-mail

    # --- Formulário de Cadastro ---

    # --- Formulário de Login ---

    # --- Mensagens de Feedback ---

    # --- Filtros de Cronograma ---
    dia_selecionado: str = "Dia 1"
    atividades_dia1: List[Dict[str, Any]] = _obter_atividades_iniciais("Dia 1")
    atividades_dia2: List[Dict[str, Any]] = _obter_atividades_iniciais("Dia 2")
    ultima_atualizacao_programacao: float = 0.0



    # --- Cartão de Identificação Digital / Crachá (Badge) ---
    badge_modo: str = "participante"  # 'participante' ou 'palestrante'
    badge_foto_input: str = ""
    badge_palestrante_nome: str = "Prof.(a) Dr.(a) Convidado(a)"
    badge_palestrante_inst: str = "UFCA / Instituição Parceira"
    badge_palestrante_tema: str = "Astrofísica Teórica, Ondas Gravitacionais e Matéria Densa"
    badge_palestrante_horario: str = "18h00 • Conferência Magna"

    # --- Painel do Administrador ---

    # Gestão de Senhas pelo Administrador


    # Editor de Atividades / Programação pelo Admin

    # Criação e Delegação de Nova Atividade pelo Admin

    # Visualização e Emissão da Carteirinha pelo Admin

    # --- Painel de Supervisão / Conferência de Presença ---

    # --- Contagem Regressiva & Reflexões Cientificas ---
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








    def carregar_programacao_publica(self):
        """Carrega e sincroniza a programação oficial com cache de 1 minuto."""
        d1 = EventoController.obter_programacao("Dia 1")
        d2 = EventoController.obter_programacao("Dia 2")
        self.atividades_dia1 = [
            {
                "id": a.id or 0,
                "horario": a.horario,
                "titulo": a.titulo,
                "palestrante": a.palestrante,
                "local": a.local,
                "tipo": a.tipo,
                "descricao": a.descricao,
                "tipo_color": a.tipo_color,
            }
            for a in d1
        ]
        self.atividades_dia2 = [
            {
                "id": a.id or 0,
                "horario": a.horario,
                "titulo": a.titulo,
                "palestrante": a.palestrante,
                "local": a.local,
                "tipo": a.tipo,
                "descricao": a.descricao,
                "tipo_color": a.tipo_color,
            }
            for a in d2
        ]
        self.ultima_atualizacao_programacao = time.time()

    @rx.event(background=True)
    async def monitor_programacao_background(self):
        """Monitora e atualiza a programação a cada 60s (1 minuto) de forma reativa."""
        while True:
            await asyncio.sleep(60)
            async with self:
                self.carregar_programacao_publica()

    def set_dia(self, dia: str):
        self.dia_selecionado = dia
        if not self.atividades_dia1 or not self.atividades_dia2 or (time.time() - self.ultima_atualizacao_programacao > 60.0):
            self.carregar_programacao_publica()

    def set_badge_modo(self, modo: str):
        if modo in ["participante", "palestrante"]:
            self.badge_modo = modo

    def set_badge_foto_input(self, val: Any):
        if isinstance(val, str):
            self.badge_foto_input = val
        else:
            self.badge_foto_input = ""










    def carregar_stats(self):
        """Atualiza números consumindo o Controller."""
        stats = _usuario_controller.obter_estatisticas()
        self.total_inscritos = stats["total_inscritos"]
        self.vagas_restantes = stats["vagas_restantes"]




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


    # --- Ações do Admin ---

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






    # --- Exportação Oficial da Lista de Inscritos (CSV e PDF) para Admin e Supervisores ---


    # Editor de Atividades / Palestras





    # Criação e Delegação Manual de Atividades pelo Admin










    # Inspeção e Emissão de Carteirinha de Participante pelo Admin


    # --- Ações de Supervisor (Conferência de Presença) ---




    # --- Gestão de Perfil, Senha e Confirmação de E-mail ---
















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
    def baixar_pdf_programacao(self):
        """Gera e baixa o PDF oficial com toda a programação das atividades do IV EFAC para todos os usuários."""
        from projeto_web.core.export_service import gerar_pdf_programacao
        from projeto_web.controllers.evento_controller import EventoController

        dia1 = EventoController.obter_programacao("Dia 1")
        dia2 = EventoController.obter_programacao("Dia 2")
        pdf_bytes = gerar_pdf_programacao(dia1, dia2)
        data_tag = datetime.now().strftime("%Y%m%d_%H%M")
        return rx.download(data=pdf_bytes, filename=f"programacao_atividades_iv_efac_{data_tag}.pdf")
