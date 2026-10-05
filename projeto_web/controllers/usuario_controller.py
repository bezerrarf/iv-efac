"""Controller para orquestração de regras de negócio de usuários e participantes (C de MVC)."""

from dataclasses import dataclass
from typing import Generic, List, Optional, TypeVar
from projeto_web.core.config import CAPACIDADE_MAXIMA_EVENTO
from projeto_web.core.security import PasswordHasherProtocol
from projeto_web.models.usuario import Usuario
from projeto_web.repositories.base import UsuarioRepositoryProtocol

T = TypeVar("T")


@dataclass
class ControllerResult(Generic[T]):
    """Resultado padronizado para operações do Controller."""

    sucesso: bool
    mensagem: str
    dado: Optional[T] = None


class UsuarioController:
    """Controller de Usuários com inversão de dependência (DIP)."""

    def __init__(
        self,
        repository: UsuarioRepositoryProtocol,
        hasher: PasswordHasherProtocol,
        capacidade_maxima: int = CAPACIDADE_MAXIMA_EVENTO,
    ):
        self._repository = repository
        self._hasher = hasher
        self._capacidade_maxima = capacidade_maxima

    def cadastrar(
        self,
        nome: str,
        email: str,
        senha: str,
        instituicao: str = "Não informada",
        modalidade: str = "Presencial",
        area: str = "Ciência de Dados / IA",
    ) -> ControllerResult[Usuario]:
        """Aplica validações e registra um novo participante no evento."""
        nome_clean = nome.strip()
        email_clean = email.strip().lower()

        if not nome_clean or not email_clean or not senha:
            return ControllerResult(
                sucesso=False,
                mensagem="Nome, e-mail e senha são obrigatórios.",
            )

        if "@" not in email_clean or "." not in email_clean:
            return ControllerResult(
                sucesso=False,
                mensagem="Forneça um endereço de e-mail válido.",
            )

        if len(senha) < 6:
            return ControllerResult(
                sucesso=False,
                mensagem="A senha deve conter no mínimo 6 caracteres.",
            )

        # Validação de capacidade para modalidade presencial
        if modalidade == "Presencial" and self._repository.count() >= self._capacidade_maxima:
            return ControllerResult(
                sucesso=False,
                mensagem="Limite de vagas presenciais esgotado. Escolha a modalidade Online.",
            )

        # Validação de unicidade de e-mail
        if self._repository.find_by_email(email_clean) is not None:
            return ControllerResult(
                sucesso=False,
                mensagem="Este e-mail já está cadastrado no evento.",
            )

        novo_usuario = Usuario(
            nome=nome_clean,
            email=email_clean,
            instituicao=instituicao.strip() or "Não informada",
            modalidade=modalidade,
            area=area,
            senha_hash=self._hasher.hash(senha),
            role="participante",
        )

        salvo = self._repository.save(novo_usuario)
        return ControllerResult(
            sucesso=True,
            mensagem="Inscrição realizada com sucesso!",
            dado=salvo,
        )

    def autenticar(self, email: str, senha: str) -> ControllerResult[Usuario]:
        """Valida credenciais de um participante já cadastrado."""
        email_clean = email.strip().lower()
        if not email_clean or not senha:
            return ControllerResult(
                sucesso=False,
                mensagem="Informe e-mail e senha para acessar.",
            )

        usuario = self._repository.find_by_email(email_clean)
        if usuario is None:
            return ControllerResult(
                sucesso=False,
                mensagem="Usuário não encontrado. Verifique seu e-mail.",
            )

        if not self._hasher.verify(senha, usuario.senha_hash):
            return ControllerResult(
                sucesso=False,
                mensagem="Senha incorreta. Tente novamente.",
            )

        return ControllerResult(
            sucesso=True,
            mensagem="Login autenticado com sucesso!",
            dado=usuario,
        )

    def alterar_modalidade(self, user_id: int, nova_modalidade: str) -> ControllerResult[Usuario]:
        """Permite ao participante alterar entre Presencial e Online."""
        usuario = self._repository.find_by_id(user_id)
        if usuario is None:
            return ControllerResult(
                sucesso=False,
                mensagem="Participante não localizado.",
            )

        usuario.modalidade = nova_modalidade
        atualizado = self._repository.save(usuario)
        return ControllerResult(
            sucesso=True,
            mensagem=f"Modalidade alterada para {nova_modalidade} com sucesso!",
            dado=atualizado,
        )

    def listar_inscritos(self, termo: Optional[str] = None) -> List[Usuario]:
        """Retorna todos os inscritos filtrados por termo de busca opcional."""
        todos = self._repository.list_all()
        if not termo or not termo.strip():
            return todos
        termo_clean = termo.strip().lower()
        return [
            u for u in todos
            if (
                termo_clean in u.nome.lower()
                or termo_clean in u.email.lower()
                or termo_clean in u.codigo_inscricao.lower()
                or termo_clean in u.instituicao.lower()
                or termo_clean in u.role.lower()
            )
        ]

    def alterar_role(self, user_id: int, nova_role: str) -> ControllerResult[Usuario]:
        """Permite ao administrador conceder ou revogar permissões de supervisor."""
        if nova_role not in ["participante", "supervisor", "admin"]:
            return ControllerResult(sucesso=False, mensagem="Permissão inválida.")

        atualizado = self._repository.update_role(user_id, nova_role)
        if not atualizado:
            return ControllerResult(sucesso=False, mensagem="Inscrito não encontrado.")

        status_label = "Supervisor(a)" if nova_role == "supervisor" else "Participante Regular"
        return ControllerResult(
            sucesso=True,
            mensagem=f"Poderes de {status_label} atualizados para {atualizado.nome}!",
            dado=atualizado,
        )

    def alternar_presenca(self, user_id: int) -> ControllerResult[Usuario]:
        """Permite ao supervisor/admin marcar conferência de presença do participante."""
        atualizado = self._repository.toggle_presenca(user_id)
        if not atualizado:
            return ControllerResult(sucesso=False, mensagem="Inscrito não encontrado.")

        status = "CONFIRMADA" if atualizado.presenca_confirmada else "PENDENTE"
        return ControllerResult(
            sucesso=True,
            mensagem=f"Presença de {atualizado.nome} marcada como {status}!",
            dado=atualizado,
        )

    def atualizar_foto(self, user_id: int, foto_url: str) -> ControllerResult[Usuario]:
        """Atualiza a foto de identificação do participante ou palestrante."""
        atualizado = self._repository.update_foto(user_id, foto_url.strip())
        if not atualizado:
            return ControllerResult(sucesso=False, mensagem="Inscrito não encontrado.")

        return ControllerResult(
            sucesso=True,
            mensagem="Foto do cartão de identificação atualizada com sucesso!",
            dado=atualizado,
        )

    def alterar_senha(self, user_id: int, nova_senha: str) -> ControllerResult[Usuario]:
        """Permite alterar a senha de qualquer participante ou a senha do próprio administrador."""
        if not nova_senha or len(nova_senha.strip()) < 6:
            return ControllerResult(
                sucesso=False,
                mensagem="A nova senha deve possuir no mínimo 6 caracteres.",
            )

        usuario = self._repository.find_by_id(user_id)
        if not usuario:
            return ControllerResult(sucesso=False, mensagem="Usuário não encontrado.")

        hash_novo = self._hasher.hash(nova_senha.strip())
        atualizado = self._repository.update_senha(user_id, hash_novo)
        return ControllerResult(
            sucesso=True,
            mensagem=f"Senha de {usuario.nome} atualizada com sucesso no banco de dados!",
            dado=atualizado,
        )

    def obter_estatisticas(self) -> dict:
        """Calcula métricas de vagas e inscritos."""
        total = self._repository.count()
        todos = self._repository.list_all()
        presenciais = sum(1 for u in todos if u.modalidade == "Presencial")
        onlines = sum(1 for u in todos if u.modalidade == "Online")
        presentes = sum(1 for u in todos if getattr(u, "presenca_confirmada", False))
        supervisores = sum(1 for u in todos if getattr(u, "role", "") == "supervisor")

        return {
            "total_inscritos": total,
            "capacidade_maxima": self._capacidade_maxima,
            "vagas_restantes": max(0, self._capacidade_maxima - total),
            "presenciais": presenciais,
            "onlines": onlines,
            "presentes": presentes,
            "supervisores": supervisores,
        }
