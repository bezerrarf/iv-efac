import reflex as rx
from typing import Optional, List, Dict, Any
from projeto_web.controllers.usuario_controller import UsuarioController
from projeto_web.state.admin_state import AdminState

class SupervisorState(AdminState):
    """Estado isolado para gerenciar credenciamento e presença."""
    superv_busca: str = ""
    superv_inscritos: List[Dict[str, Any]] = []
    superv_presentes_count: int = 0
    superv_total_count: int = 0
    def set_superv_busca(self, termo: str):
        self.superv_busca = termo
        self.carregar_painel_supervisor()
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

