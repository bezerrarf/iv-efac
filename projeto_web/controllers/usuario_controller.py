"""Controller para orquestração de regras de negócio de usuários e participantes (C de MVC)."""

from dataclasses import dataclass
from typing import Generic, Optional, TypeVar
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

    def obter_estatisticas(self) -> dict:
        """Calcula métricas de vagas e inscritos."""
        total = self._repository.count()
        return {
            "total_inscritos": total,
            "capacidade_maxima": self._capacidade_maxima,
            "vagas_restantes": max(0, self._capacidade_maxima - total),
        }
