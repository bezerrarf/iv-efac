"""Testes unitários para a arquitetura CQRS (Command Query Responsibility Segregation)."""

import uuid
import pytest
from sqlmodel import Session, create_engine, SQLModel
from projeto_web.models.usuario import Usuario
from projeto_web.models.atividade import AtividadeModel
from projeto_web.repositories.base import (
    UsuarioCommandRepositoryProtocol,
    UsuarioQueryRepositoryProtocol,
    UsuarioRepositoryProtocol,
    AtividadeCommandRepositoryProtocol,
    AtividadeQueryRepositoryProtocol,
)
from projeto_web.repositories.commands.usuario_commands import SQLiteUsuarioCommandRepository
from projeto_web.repositories.queries.usuario_queries import SQLiteUsuarioQueryRepository
from projeto_web.repositories.commands.atividade_commands import SQLiteAtividadeCommandRepository
from projeto_web.repositories.queries.atividade_queries import SQLiteAtividadeQueryRepository
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository


@pytest.fixture
def memory_session_factory():
    """Engine SQLite em memória isolado para testes rápidos de CQRS."""
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)

    def _factory():
        return Session(engine)

    return _factory


def test_cqrs_usuario_segregation(memory_session_factory):
    """Valida a separação estrita entre comandos (escrita) e queries (leitura)."""
    command_repo = SQLiteUsuarioCommandRepository(session_factory=memory_session_factory)
    query_repo = SQLiteUsuarioQueryRepository(session_factory=memory_session_factory)

    # 1. Command Side: Salvar Usuário
    usuario = Usuario(
        nome="Dr. Richard Feynman",
        email="feynman@caltech.edu",
        instituicao="Caltech",
        modalidade="Presencial",
        area="Física Quântica",
        senha_hash="hash_teste_123",
        codigo_inscricao="CQRS-001",
        role="participante",
        presenca_confirmada=False,
    )
    salvo = command_repo.save(usuario)
    assert salvo.id is not None
    user_id = salvo.id

    # 2. Query Side: Consultar por ID e Email
    buscado = query_repo.find_by_id(user_id)
    assert buscado is not None
    assert buscado.nome == "Dr. Richard Feynman"
    assert buscado.area == "Física Quântica"

    buscado_email = query_repo.find_by_email("FEYNMAN@CALTECH.EDU")
    assert buscado_email is not None
    assert buscado_email.id == user_id

    # 3. Command Side: Atualizações
    atualizado_role = command_repo.update_role(user_id, "supervisor")
    assert atualizado_role.role == "supervisor"

    atualizado_presenca = command_repo.toggle_presenca(user_id)
    assert atualizado_presenca.presenca_confirmada is True

    atualizado_foto = command_repo.update_foto(user_id, "/participantes/feynman.webp")
    assert atualizado_foto.foto_url == "/participantes/feynman.webp"

    atualizado_senha = command_repo.update_senha(user_id, "novo_hash_456")
    assert atualizado_senha.senha_hash == "novo_hash_456"

    # 4. Query Side: Projeções e Estatísticas
    stats = query_repo.obter_estatisticas(capacidade_maxima=200)
    assert stats["total_inscritos"] == 1
    assert stats["vagas_restantes"] == 199
    assert stats["presenciais"] == 1
    assert stats["presentes"] == 1
    assert stats["supervisores"] == 1


def test_cqrs_usuario_facade_compatibility(memory_session_factory):
    """Valida que a fachada SQLiteUsuarioRepository une Commands e Queries perfeitamente."""
    facade = SQLiteUsuarioRepository(session_factory=memory_session_factory)

    # Verifica cumprimento dos protocolos
    assert isinstance(facade, SQLiteUsuarioCommandRepository)
    assert isinstance(facade, SQLiteUsuarioQueryRepository)

    # Executa fluxo híbrido
    user = Usuario(
        nome="Niels Bohr",
        email="bohr@copenhagen.dk",
        instituicao="Universidade de Copenhague",
        modalidade="Online",
        area="Física Quântica",
        senha_hash="hash_bohr_123",
        codigo_inscricao="CQRS-002",
        role="participante",
    )
    facade.save(user)
    assert facade.count() == 1
    assert facade.find_by_email("bohr@copenhagen.dk") is not None


def test_cqrs_atividade_segregation(memory_session_factory):
    """Valida comandos e queries de atividades no padrão CQRS."""
    cmd_repo = SQLiteAtividadeCommandRepository(session_factory=memory_session_factory)
    query_repo = SQLiteAtividadeQueryRepository(session_factory=memory_session_factory)

    ativ = AtividadeModel(
        dia="Dia 1",
        horario="09:00 – 10:30",
        titulo="Mecânica Quântica e Computação",
        palestrante="Prof. Dr. Job Saraiva",
        local="Auditório Principal",
        tipo="Palestra",
        descricao="Fundamentos e aplicações.",
        tipo_color="#818CF8",
        ordem=1,
    )
    criada = cmd_repo.create(ativ)
    assert criada.id is not None

    dia1_itens = query_repo.find_by_dia("Dia 1")
    assert len(dia1_itens) == 1
    assert dia1_itens[0].titulo == "Mecânica Quântica e Computação"

    # Update via Command
    criada.titulo = "Do Grafeno aos Qubits"
    cmd_repo.update(criada)
    dia1_atualizado = query_repo.find_by_dia("Dia 1")
    assert dia1_atualizado[0].titulo == "Do Grafeno aos Qubits"

    # Delete via Command
    assert cmd_repo.delete(criada.id) is True
    assert query_repo.count() == 0


def test_cqrs_usuario_controller_injection(memory_session_factory):
    """Valida o UsuarioController operando com injeção de repositórios segregados de comandos e consultas."""
    from projeto_web.controllers.usuario_controller import UsuarioController
    from projeto_web.core.security import PBKDF2PasswordHasher

    cmd_repo = SQLiteUsuarioCommandRepository(session_factory=memory_session_factory)
    query_repo = SQLiteUsuarioQueryRepository(session_factory=memory_session_factory)
    hasher = PBKDF2PasswordHasher()

    controller = UsuarioController(
        command_repository=cmd_repo,
        query_repository=query_repo,
        hasher=hasher,
        capacidade_maxima=100,
    )

    # Cadastro via Command
    res = controller.cadastrar(
        nome="Marie Curie",
        email="marie.curie@sorbonne.fr",
        senha="Radioatividade123!",
        instituicao="Sorbonne",
        modalidade="Presencial",
        area="Física Quântica",
    )
    assert res.sucesso is True
    assert res.dado.id is not None

    # Autenticação via Query
    auth = controller.autenticar("marie.curie@sorbonne.fr", "Radioatividade123!")
    assert auth.sucesso is True

    # Listagem e Estatísticas via Query
    inscritos = controller.listar_inscritos()
    assert len(inscritos) == 1

    stats = controller.obter_estatisticas()
    assert stats["total_inscritos"] == 1
    assert stats["vagas_restantes"] == 99
