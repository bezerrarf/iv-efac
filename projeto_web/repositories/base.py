"""Contratos e interfaces abstratas para persistência de dados no padrão CQRS (ISP / DIP)."""

from typing import List, Optional, Protocol
from projeto_web.models.usuario import Usuario
from projeto_web.models.atividade import AtividadeModel


# ==============================================================================
# CQRS: USUÁRIO - COMMANDS (ESCRITA / MUTAÇÃO)
# ==============================================================================
class UsuarioCommandRepositoryProtocol(Protocol):
    """Contrato abstrato para operações de escrita/mutação de usuários (CQRS - Command Side)."""

    def save(self, usuario: Usuario) -> Usuario:
        """Cria ou atualiza um usuário no banco de dados."""
        ...

    def update_role(self, user_id: int, role: str) -> Optional[Usuario]:
        """Atualiza a permissão do usuário ('participante', 'supervisor', 'admin')."""
        ...

    def toggle_presenca(self, user_id: int, dia: Optional[str] = None) -> Optional[Usuario]:
        """Alterna o status de presença confirmada."""
        ...

    def update_foto(self, user_id: int, foto_url: str) -> Optional[Usuario]:
        """Atualiza a imagem da credencial."""
        ...

    def update_senha(self, user_id: int, nova_senha_hash: str) -> Optional[Usuario]:
        """Atualiza a senha criptografada do usuário."""
        ...

    def delete(self, user_id: int) -> bool:
        """Exclui um participante do banco de dados."""
        ...


# ==============================================================================
# CQRS: USUÁRIO - QUERIES (LEITURA / CONSULTAS E PROJEÇÕES)
# ==============================================================================
class UsuarioQueryRepositoryProtocol(Protocol):
    """Contrato abstrato para operações de consulta e projeção de usuários (CQRS - Query Side)."""

    def find_by_id(self, user_id: int) -> Optional[Usuario]:
        """Busca usuário por identificador primário."""
        ...

    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca usuário por e-mail sanitizado (case-insensitive)."""
        ...

    def count(self) -> int:
        """Contagem total de inscritos."""
        ...

    def list_all(self) -> List[Usuario]:
        """Lista todos os inscritos ordenados."""
        ...

    def obter_estatisticas(self, capacidade_maxima: int) -> dict:
        """Projeção agregada de métricas do evento."""
        ...


# Fachada que une Command + Query para retrocompatibilidade total
class UsuarioRepositoryProtocol(UsuarioCommandRepositoryProtocol, UsuarioQueryRepositoryProtocol, Protocol):
    """Contrato consolidado para injeção de dependência clássica."""
    ...


# ==============================================================================
# CQRS: ATIVIDADES / EVENTO - COMMANDS E QUERIES
# ==============================================================================
class AtividadeCommandRepositoryProtocol(Protocol):
    """Contrato abstrato para mutação da grade horária do evento (CQRS - Command Side)."""

    def create(self, atividade: AtividadeModel) -> AtividadeModel:
        ...

    def update(self, atividade: AtividadeModel) -> Optional[AtividadeModel]:
        ...

    def update_by_fields(
        self,
        id: int,
        dia: str,
        horario: str,
        titulo: str,
        palestrante: str,
        local: str,
        tipo: str,
        descricao: str,
    ) -> bool:
        ...

    def delete(self, atividade_id: int) -> bool:
        ...

    def clear_all(self) -> bool:
        ...


class AtividadeQueryRepositoryProtocol(Protocol):
    """Contrato abstrato para consultas da grade horária do evento."""

    def find_by_dia(self, dia: str) -> List[AtividadeModel]:
        ...

    def list_all(self) -> List[AtividadeModel]:
        ...

    def count(self) -> int:
        ...
