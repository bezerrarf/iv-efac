"""Testes para download de PDF da programação, links dinâmicos de modelos, ausência de impressão e presença segregada por dia."""

import pytest
from projeto_web.core.export_service import gerar_pdf_programacao
from projeto_web.controllers.evento_controller import EventoController
from projeto_web.repositories.config_repository import ConfigRepository
from projeto_web.views.components.painel_supervisor import painel_supervisor_view
from projeto_web.controllers.usuario_controller import UsuarioController
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.core.security import PBKDF2PasswordHasher


def test_gerar_pdf_programacao_sucesso():
    """Valida a geração de PDF da programação completa do evento."""
    dia1 = EventoController.obter_programacao("Dia 1")
    dia2 = EventoController.obter_programacao("Dia 2")
    pdf_bytes = gerar_pdf_programacao(dia1, dia2)

    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 2000
    assert pdf_bytes.startswith(b"%PDF")


def test_config_repository_persistencia():
    """Valida a persistência de links e configurações dinâmicas."""
    repo = ConfigRepository()
    chave_teste = "link_teste_unitario"
    url_teste = "https://drive.google.com/file/d/exemplo123"

    repo.set(chave_teste, url_teste)
    recuperado = repo.get(chave_teste)
    assert recuperado == url_teste


def test_painel_supervisor_sem_botao_imprimir():
    """Garante que o botão de impressão foi completamente removido conforme solicitado."""
    comp = painel_supervisor_view()
    comp_repr = str(comp)
    assert "window.print()" not in comp_repr
    assert "Imprimir Lista" not in comp_repr


def test_presenca_segregada_por_dia():
    """Valida a alternância independente de presença no Dia 1 e no Dia 2."""
    repo = SQLiteUsuarioRepository()
    hasher = PBKDF2PasswordHasher()
    controller = UsuarioController(repository=repo, hasher=hasher)

    # Cadastrar participante para teste
    import uuid
    email_teste = f"presenca_{uuid.uuid4().hex[:6]}@ufca.edu.br"
    cad = controller.cadastrar(
        nome="Participante Presenca",
        email=email_teste,
        senha="SenhaValida123!",
        instituicao="UFCA",
        modalidade="Presencial",
        area="Astrofísica",
    )
    assert cad.sucesso is True
    uid = cad.dado.id

    # Confirmar apenas no Dia 1
    res1 = controller.alternar_presenca(uid, dia="Dia 1")
    assert res1.sucesso is True
    assert res1.dado.presenca_dia1 is True
    assert res1.dado.presenca_dia2 is False
    assert res1.dado.presenca_confirmada is True

    # Confirmar também no Dia 2
    res2 = controller.alternar_presenca(uid, dia="Dia 2")
    assert res2.sucesso is True
    assert res2.dado.presenca_dia1 is True
    assert res2.dado.presenca_dia2 is True

    # Desmarcar Dia 1
    res3 = controller.alternar_presenca(uid, dia="Dia 1")
    assert res3.sucesso is True
    assert res3.dado.presenca_dia1 is False
    assert res3.dado.presenca_dia2 is True
    assert res3.dado.presenca_confirmada is True


def test_admin_atualizar_participante_completo():
    """Valida a edição completa de cadastro de participante pelo administrador."""
    repo = SQLiteUsuarioRepository()
    hasher = PBKDF2PasswordHasher()
    controller = UsuarioController(repository=repo, hasher=hasher)

    import uuid
    email_original = f"orig_{uuid.uuid4().hex[:6]}@ufca.edu.br"
    cad = controller.cadastrar(
        nome="Nome Original",
        email=email_original,
        senha="SenhaOriginal123!",
        instituicao="Universidade Antiga",
        modalidade="Online",
        area="Física Computacional",
    )
    uid = cad.dado.id

    email_novo = f"editado_{uuid.uuid4().hex[:6]}@ufca.edu.br"
    res_edit = controller.atualizar_participante_completo(
        user_id=uid,
        nome="Nome Editado Pelo Admin",
        email=email_novo,
        instituicao="Universidade Federal do Cariri",
        modalidade="Presencial",
        area="Física Quântica",
        role="supervisor",
        presenca_dia1=True,
        presenca_dia2=False,
    )

    assert res_edit.sucesso is True
    assert res_edit.dado.nome == "Nome Editado Pelo Admin"
    assert res_edit.dado.email == email_novo
    assert res_edit.dado.instituicao == "Universidade Federal do Cariri"
    assert res_edit.dado.modalidade == "Presencial"
    assert res_edit.dado.area == "Física Quântica"
    assert res_edit.dado.role == "supervisor"
    assert res_edit.dado.presenca_dia1 is True
    assert res_edit.dado.presenca_dia2 is False
    assert res_edit.dado.presenca_confirmada is True


def test_capacidade_segregada_presencial_e_online():
    """Garante que inscrições Online não bloqueiam vagas da modalidade Presencial."""
    repo = SQLiteUsuarioRepository()
    hasher = PBKDF2PasswordHasher()
    import uuid

    presenciais_iniciais = repo.count_presencial()
    # Limite definido para 2 vagas presenciais a mais do que o estado atual
    controller = UsuarioController(
        repository=repo,
        hasher=hasher,
        capacidade_maxima=presenciais_iniciais + 2,
    )

    # 1. Cadastra 3 participantes Online (não devem consumir as 2 vagas presenciais)
    for i in range(3):
        res = controller.cadastrar(
            nome=f"Online User {i}",
            email=f"online_{uuid.uuid4().hex[:6]}@ufca.edu.br",
            senha="SenhaOnline123!",
            modalidade="Online",
        )
        assert res.sucesso is True

    # 2. Cadastra até o limite de presenciais (+1 e +2)
    cad_p1 = controller.cadastrar(
        nome="Presencial 1",
        email=f"p1_{uuid.uuid4().hex[:6]}@ufca.edu.br",
        senha="SenhaPresencial123!",
        modalidade="Presencial",
    )
    assert cad_p1.sucesso is True

    cad_p2 = controller.cadastrar(
        nome="Presencial 2",
        email=f"p2_{uuid.uuid4().hex[:6]}@ufca.edu.br",
        senha="SenhaPresencial123!",
        modalidade="Presencial",
    )
    assert cad_p2.sucesso is True

    # 3. 3º Presencial (+3) deve ser bloqueado por esgotamento
    cad_p3 = controller.cadastrar(
        nome="Presencial 3",
        email=f"p3_{uuid.uuid4().hex[:6]}@ufca.edu.br",
        senha="SenhaPresencial123!",
        modalidade="Presencial",
    )
    assert cad_p3.sucesso is False
    assert "Limite de vagas presenciais esgotado" in cad_p3.mensagem

    # 4. Mas novo participante Online ainda DEVE ser aceito com sucesso!
    cad_on_extra = controller.cadastrar(
        nome="Online Extra",
        email=f"online_extra_{uuid.uuid4().hex[:6]}@ufca.edu.br",
        senha="SenhaOnline123!",
        modalidade="Online",
    )
    assert cad_on_extra.sucesso is True
