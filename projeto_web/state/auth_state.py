import reflex as rx
import base64
from typing import Optional, List, Dict, Any
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.controllers.usuario_controller import UsuarioController

_hasher = PBKDF2PasswordHasher()
_repo = SQLiteUsuarioRepository()
_usuario_controller = UsuarioController(repository=_repo, hasher=_hasher)

class AuthState(rx.State):
    """Estado responsável por Autenticação, Cadastro e Perfil do Usuário."""
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
    modal_perfil_aberto: bool = False
    perfil_nome_input: str = ""
    perfil_instituicao_input: str = ""
    perfil_modalidade_input: str = "Presencial"
    minha_senha_atual_input: str = ""
    minha_nova_senha_input: str = ""
    minha_nova_senha_confirm: str = ""
    modal_confirmacao_email_aberto: bool = False
    codigo_email_input: str = ""
    codigo_email_enviado_preview: str = "" 
    cad_nome: str = ""
    cad_email: str = ""
    cad_senha: str = ""
    cad_instituicao: str = ""
    cad_modalidade: str = "Presencial"
    cad_area: str = "Ciência de Dados / IA"
    login_email: str = ""
    login_senha: str = ""
    feedback_msg: str = ""
    feedback_tipo: str = ""  # 'success', 'error', 'info', ''
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

        # Sincronização dos painéis ocorre sob demanda na abertura dos componentes

        self.feedback_msg = f"Bem-vindo(a) de volta, {usuario.nome}!"
        self.feedback_tipo = "success"

        self.login_email = ""
        self.login_senha = ""
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
        if hasattr(self, "admin_inscritos"):
            self.admin_inscritos = []
        if hasattr(self, "superv_inscritos"):
            self.superv_inscritos = []
        if hasattr(self, "is_editing_atividade"):
            self.is_editing_atividade = False
        self.feedback_msg = "Sessão encerrada com sucesso."
        self.feedback_tipo = "info"
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

