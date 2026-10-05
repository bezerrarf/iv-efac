"""Testes unitários para o EventoController do IV EFAC."""

import pytest
from projeto_web.controllers.evento_controller import EventoController


def test_obter_dimensoes_e_eixos():
    eixos = EventoController.obter_eixos_tematicos()
    assert len(eixos) == 4
    numeros = [e.numero for e in eixos]
    assert numeros == [1, 2, 3, 4]

    dimensoes = EventoController.obter_dimensoes()
    assert len(dimensoes) == 4
    for d in dimensoes:
        assert d.cor.startswith("#")
        assert len(d.nome) > 0
        assert len(d.descricao) > 0


def test_obter_programacao_dias_oficiais():
    dia1 = EventoController.obter_programacao("Dia 1")
    assert len(dia1) >= 9  # 9 atividades oficiais no Dia 1

    dia2 = EventoController.obter_programacao("Dia 2")
    assert len(dia2) >= 9  # 9 atividades oficiais no Dia 2

    # Horários oficiais do PDF
    assert "08:00" in dia1[0].horario
    assert "18:00" in dia1[-1].horario
    assert "08:30" in dia2[0].horario
    assert "19:15" in dia2[-1].horario


def test_obter_palestrantes_oficiais():
    palestrantes = EventoController.obter_palestrantes()
    assert len(palestrantes) == 6
    nomes = [p.nome for p in palestrantes]
    assert any("Cesar Lenzi" in n for n in nomes)
    assert any("Ronaldo Vieira Lobato" in n for n in nomes)
    assert any("Eliane Angela Veit" in n for n in nomes)
    assert any("Iarley Lobato" in n for n in nomes)
    assert any("Jonathan" in n for n in nomes)
    assert any("Célio Rodrigues Muniz" in n for n in nomes)


def test_obter_normas_submissao():
    normas = EventoController.obter_normas_submissao()
    assert "Resumo Expandido" in normas.formato
    assert len(normas.criterios) == 5
    assert "Oral" in normas.modalidade


def test_obter_todas_atividades():
    todas = EventoController.obter_todas_atividades()
    assert len(todas) >= 18


def test_atualizar_atividade_e_restaurar():
    todas = EventoController.obter_todas_atividades()
    assert len(todas) > 0
    primeira = todas[0]
    primeiro_id = primeira.id

    if primeiro_id is not None:
        # Alterar atividade
        ok = EventoController.atualizar_atividade(
            id=primeiro_id,
            dia=primeira.dia,
            horario="07:45 – 08:45",
            titulo="Credenciamento Antecipado Especial",
            palestrante=primeira.palestrante,
            local=primeira.local,
            tipo=primeira.tipo,
            descricao="Recepção adiantada",
        )
        assert ok is True

        # Verificar se refletiu no método obter_programacao
        atualizadas = EventoController.obter_programacao(primeira.dia)
        match = [a for a in atualizadas if a.id == primeiro_id]
        assert len(match) == 1
        assert match[0].titulo == "Credenciamento Antecipado Especial"
        assert match[0].horario == "07:45 – 08:45"

        # Restaurar grade padrão
        restaurou = EventoController.restaurar_programacao_padrao()
        assert restaurou is True
        restauradas = EventoController.obter_programacao(primeira.dia)
        match_restaurado = [a for a in restauradas if a.id == primeiro_id or a.ordem == 1]
        assert len(match_restaurado) >= 1
        assert "Credenciamento" in match_restaurado[0].titulo
