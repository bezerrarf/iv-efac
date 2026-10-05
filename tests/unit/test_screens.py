"""Testes unitários para a navegação do sistema de telas (Screen Switcher)."""

from projeto_web.state.evento_state import EventoState


def test_navegacao_sistema_de_telas():
    state = EventoState()
    assert state.tela_ativa == "inicio"
    assert state.indice_tela == 0

    # Próxima tela: inicio -> eixos (1)
    state.proxima_tela()
    assert state.tela_ativa == "eixos"
    assert state.indice_tela == 1

    # Próxima tela: eixos -> palestrantes (2)
    state.proxima_tela()
    assert state.tela_ativa == "palestrantes"
    assert state.indice_tela == 2

    # Voltar tela: palestrantes -> eixos (1)
    state.tela_anterior()
    assert state.tela_ativa == "eixos"
    assert state.indice_tela == 1

    # Seleção direta de tela
    state.set_tela("submissoes")
    assert state.tela_ativa == "submissoes"
    assert state.indice_tela == 4

    # Seleção de Sobre (último item, índice 6)
    state.set_tela("sobre")
    assert state.tela_ativa == "sobre"
    assert state.indice_tela == 6

    # Seleção de tela inválida não altera estado
    state.set_tela("tela_inexistente")
    assert state.tela_ativa == "sobre"
    assert state.indice_tela == 6

    # Ciclo circular: de sobre (6) para inicio (0)
    state.proxima_tela()
    assert state.tela_ativa == "inicio"
    assert state.indice_tela == 0

    # Ciclo circular reverso: de inicio (0) para sobre (6)
    state.tela_anterior()
    assert state.tela_ativa == "sobre"
    assert state.indice_tela == 6
