"""Testes unitários para o EventoController do IV EFAC."""

import pytest
from projeto_web.controllers.evento_controller import EventoController


def test_obter_dimensoes_e_eixos():
    eixos = EventoController.obter_eixos_tematicos()
    assert len(eixos) == 5
    numeros = [e.numero for e in eixos]
    assert numeros == [1, 2, 3, 4, 5]

    dimensoes = EventoController.obter_dimensoes()
    assert len(dimensoes) == 5
    for d in dimensoes:
        assert d.cor.startswith("#")
        assert len(d.nome) > 0
        assert len(d.descricao) > 0


def test_obter_programacao_dias_oficiais():
    dia1 = EventoController.obter_programacao("Dia 1")
    assert len(dia1) >= 9

    dia2 = EventoController.obter_programacao("Dia 2")
    assert len(dia2) >= 9

    # Horários oficiais do simpósio
    assert "08:00" in dia1[0].horario
    assert "18:00" in dia1[-1].horario
    assert "08:30" in dia2[0].horario
    assert any("19:" in a.horario or "18:00" in a.horario for a in dia2)


def test_obter_palestrantes_oficiais():
    palestrantes = EventoController.obter_palestrantes()
    assert len(palestrantes) == 9
    nomes = [p.nome for p in palestrantes]
    assert any("Lenzi" in n for n in nomes)
    assert any("Ronaldo Vieira Lobato" in n for n in nomes)
    assert any("Eliane Angela Veit" in n for n in nomes)
    assert any("Iarley" in n and "Lobo" in n for n in nomes)
    assert any("Jonathan" in n for n in nomes)
    assert any("Célio" in n and "Muniz" in n for n in nomes)
    assert any("Crisanto" in n for n in nomes)
    assert any("Job Saraiva" in n for n in nomes)
    assert any("Marcos" in n and "Barros" in n for n in nomes)


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

        atualizadas = EventoController.obter_programacao(primeira.dia)
        match = [a for a in atualizadas if a.id == primeiro_id]
        assert len(match) == 1
        assert match[0].titulo == "Credenciamento Antecipado Especial"
        assert match[0].horario == "07:45 – 08:45"

        restaurou = EventoController.restaurar_programacao_padrao()
        assert restaurou is True
        restauradas = EventoController.obter_programacao(primeira.dia)
        match_restaurado = [a for a in restauradas if a.id == primeiro_id or a.ordem == 1]
        assert len(match_restaurado) >= 1
        assert "Credenciamento" in match_restaurado[0].titulo


def test_excluir_atividade_e_cache():
    # Testa cache de 1 minuto
    assert EventoController.CACHE_TTL_SEGUNDOS == 60.0

    # Cria atividade temporária para exclusão
    ok_add = EventoController.adicionar_atividade(
        dia="Dia 1",
        horario="21:00 – 22:00",
        titulo="Atividade Temporária para Teste de Exclusão",
        palestrante="Palestrante Teste",
        local="Sala Virtual",
        tipo="Sessão Extra",
        descricao="Teste automatizado de remoção",
    )
    assert ok_add is True

    todas = EventoController.obter_todas_atividades()
    temp = [a for a in todas if a.titulo == "Atividade Temporária para Teste de Exclusão"]
    assert len(temp) == 1
    temp_id = temp[0].id
    assert temp_id is not None

    # Exclui a atividade
    ok_del = EventoController.excluir_atividade(temp_id)
    assert ok_del is True

    # Verifica se saiu da lista
    todas_depois = EventoController.obter_todas_atividades()
    assert not any(a.id == temp_id for a in todas_depois)
