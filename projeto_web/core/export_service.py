"""Serviço de Exportação de Dados do IV EFAC 2026.
Gera relatórios oficiais em formato CSV e PDF (ReportLab).
"""

import io
from datetime import datetime
from typing import List, Dict, Any


def gerar_csv_inscritos(usuarios: List[Any]) -> str:
    """Gera string CSV em UTF-8 (compatível com Excel com BOM)."""
    linhas = [
        "sep=;",  # Instrução para Excel reconhecer separador ponto-e-vírgula
        "ID;Código de Check-in;Nome Completo;E-mail;Instituição / Polo;Modalidade;Eixo Temático;Função / Papel;Presença Confirmada;Data de Cadastro"
    ]
    for u in usuarios:
        if isinstance(u, dict):
            uid = u.get("id", "")
            cod = u.get("codigo", "") or u.get("codigo_inscricao", "")
            nome = u.get("nome", "")
            email = u.get("email", "")
            inst = u.get("instituicao", "")
            mod = u.get("modalidade", "")
            area = u.get("area", "")
            role = u.get("role", "")
            pres_d1 = "SIM" if u.get("presenca_dia1", False) else "NÃO"
            pres_d2 = "SIM" if u.get("presenca_dia2", False) else "NÃO"
            criado = str(u.get("criado_em", ""))
        else:
            uid = getattr(u, "id", "")
            cod = getattr(u, "codigo_inscricao", "")
            nome = getattr(u, "nome", "")
            email = getattr(u, "email", "")
            inst = getattr(u, "instituicao", "")
            mod = getattr(u, "modalidade", "")
            area = getattr(u, "area", "")
            role = getattr(u, "role", "")
            pres_d1 = "SIM" if getattr(u, "presenca_dia1", False) else "NÃO"
            pres_d2 = "SIM" if getattr(u, "presenca_dia2", False) else "NÃO"
            criado = str(getattr(u, "criado_em", ""))

        # Sanitizar campos contra ponto-e-vírgula
        linha = [
            str(uid),
            f'"{cod}"',
            f'"{str(nome).replace(";", ",")}"',
            f'"{str(email).replace(";", ",")}"',
            f'"{str(inst).replace(";", ",")}"',
            f'"{mod}"',
            f'"{str(area).replace(";", ",")}"',
            f'"{str(role).upper()}"',
            f'"{pres_d1}"',
            f'"{pres_d2}"',
        ]
        linhas.append(";".join(linha))

    return "\ufeff" + "\n".join(linhas)


def gerar_pdf_inscritos(usuarios: List[Any], stats: Dict[str, Any]) -> bytes:
    """Gera PDF oficial diagramado em formato paisagem com ReportLab."""
    try:
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(letter),
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        elementos = []
        estilos = getSampleStyleSheet()
    except ImportError:
        # Fallback estruturado em PDF puro caso reportlab não esteja presente
        agora_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        total = stats.get("total_inscritos", len(usuarios))
        return (
            f"%PDF-1.4\n"
            f"% IV EFAC 2026 - Relatorio de Inscritos ({agora_str}) - Total: {total}\n"
            f"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            f"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
            f"3 0 obj<</Type/Page/MediaBox[0 0 792 612]/Parent 2 0 R/Resources<<>>>>endobj\n"
            f"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000115 00000 n \n"
            f"trailer<</Size 4/Root 1 0 R>>\nstartxref\n210\n%%EOF\n"
        ).encode("utf-8")

    # Estilos customizados
    estilo_titulo = ParagraphStyle(
        "TituloEFAC",
        parent=estilos["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#103460"),
        alignment=0,
    )
    estilo_subtitulo = ParagraphStyle(
        "SubtituloEFAC",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#00ADB5"),
        alignment=0,
    )
    estilo_meta = ParagraphStyle(
        "MetaEFAC",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#475569"),
        alignment=0,
    )
    estilo_celula = ParagraphStyle(
        "CelulaTabela",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
    )
    estilo_cabecalho_tab = ParagraphStyle(
        "CabecalhoTabela",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )

    # 1. Cabeçalho Oficial
    agora_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    elementos.append(Paragraph("IV EFAC 2026 • Encontro de Física e Astronomia do Cariri", estilo_titulo))
    elementos.append(Paragraph("Universidade Federal do Cariri (UFCA) • Campus Brejo Santo – Ceará", estilo_subtitulo))
    elementos.append(Paragraph(f"Relação Oficial de Participantes, Credenciamento e Presença • Emitido em: {agora_str}", estilo_meta))
    elementos.append(Spacer(1, 12))

    # 2. Resumo Estatístico
    total = stats.get("total_inscritos", len(usuarios))
    presenciais = stats.get("presenciais", 0)
    onlines = stats.get("onlines", 0)
    presentes = stats.get("presentes", 0)
    supervisores = stats.get("supervisores", 0)

    resumo_dados = [
        [
            Paragraph(f"<b>Total de Inscritos:</b> {total}", estilo_meta),
            Paragraph(f"<b>Presenciais:</b> {presenciais}", estilo_meta),
            Paragraph(f"<b>Online:</b> {onlines}", estilo_meta),
            Paragraph(f"<b>Supervisores:</b> {supervisores}", estilo_meta),
            Paragraph(f"<b>Presenças Confirmadas:</b> {presentes}", estilo_meta),
        ]
    ]
    tabela_resumo = Table(resumo_dados, colWidths=[140, 140, 140, 140, 160])
    tabela_resumo.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 14))

    # 3. Tabela de Participantes
    cabecalho = [
        Paragraph("Código", estilo_cabecalho_tab),
        Paragraph("Nome do Participante", estilo_cabecalho_tab),
        Paragraph("E-mail", estilo_cabecalho_tab),
        Paragraph("Instituição / Polo", estilo_cabecalho_tab),
        Paragraph("Modalidade", estilo_cabecalho_tab),
        Paragraph("Função", estilo_cabecalho_tab),
        Paragraph("D1 (11/11)", estilo_cabecalho_tab),
        Paragraph("D2 (12/11)", estilo_cabecalho_tab),
    ]

    linhas_tabela = [cabecalho]
    for u in usuarios:
        cod = getattr(u, "codigo_inscricao", None) or (u.get("codigo") if isinstance(u, dict) else "")
        nome = getattr(u, "nome", None) or (u.get("nome") if isinstance(u, dict) else "")
        email = getattr(u, "email", None) or (u.get("email") if isinstance(u, dict) else "")
        inst = getattr(u, "instituicao", None) or (u.get("instituicao") if isinstance(u, dict) else "")
        mod = getattr(u, "modalidade", None) or (u.get("modalidade") if isinstance(u, dict) else "")
        role = getattr(u, "role", None) or (u.get("role") if isinstance(u, dict) else "participante")
        pres1 = "SIM" if (getattr(u, "presenca_dia1", False) or (isinstance(u, dict) and u.get("presenca_dia1", False))) else "NÃO"
        pres2 = "SIM" if (getattr(u, "presenca_dia2", False) or (isinstance(u, dict) and u.get("presenca_dia2", False))) else "NÃO"

        linhas_tabela.append([
            Paragraph(f"<b>{cod}</b>", estilo_celula),
            Paragraph(str(nome), estilo_celula),
            Paragraph(str(email), estilo_celula),
            Paragraph(str(inst), estilo_celula),
            Paragraph(str(mod), estilo_celula),
            Paragraph(role.upper(), estilo_celula),
            Paragraph(f"<b>{pres1}</b>", estilo_celula),
            Paragraph(f"<b>{pres2}</b>", estilo_celula),
        ])

    # Larguras das colunas em landscape (total ~720 pt)
    larguras = [80, 155, 160, 115, 65, 55, 45, 45]
    tabela_principal = Table(linhas_tabela, colWidths=larguras, repeatRows=1)
    tabela_principal.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#103460")),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabela_principal)

    doc.build(elementos)
    return buffer.getvalue()

def gerar_pdf_programacao(atividades_dia1: List[Any], atividades_dia2: List[Any]) -> bytes:
    """Gera PDF oficial diagramado com a programação e atividades completas do IV EFAC."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )
        elementos = []
        estilos = getSampleStyleSheet()
    except ImportError:
        agora_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return (
            f"%PDF-1.4\n"
            f"% IV EFAC 2026 - Programacao Oficial ({agora_str})\n"
            f"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
            f"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
            f"3 0 obj<</Type/Page/MediaBox[0 0 595 842]/Parent 2 0 R/Resources<<>>>>endobj\n"
            f"xref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000115 00000 n \n"
            f"trailer<</Size 4/Root 1 0 R>>\nstartxref\n210\n%%EOF\n"
        ).encode("utf-8")

    estilo_titulo = ParagraphStyle(
        "TituloEFACProg",
        parent=estilos["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=colors.HexColor("#103460"),
        alignment=0,
    )
    estilo_subtitulo = ParagraphStyle(
        "SubtituloEFACProg",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor("#00ADB5"),
        alignment=0,
    )
    estilo_meta = ParagraphStyle(
        "MetaEFACProg",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#475569"),
        alignment=0,
    )
    estilo_dia_header = ParagraphStyle(
        "DiaHeaderEFAC",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=7,
        spaceAfter=3,
    )
    estilo_hora = ParagraphStyle(
        "HoraProg",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#00ADB5"),
    )
    estilo_tipo = ParagraphStyle(
        "TipoProg",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#2563EB"),
    )
    estilo_titulo_atv = ParagraphStyle(
        "TituloAtvProg",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
    )
    estilo_palestrante_atv = ParagraphStyle(
        "PalestranteAtvProg",
        parent=estilos["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#334155"),
    )
    estilo_local = ParagraphStyle(
        "LocalProg",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#1e293b"),
    )
    estilo_cabecalho_tab = ParagraphStyle(
        "CabTabProg",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
    )

    agora_str = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    elementos.append(Paragraph("IV EFAC 2026 • Encontro de Física e Astronomia do Cariri", estilo_titulo))
    elementos.append(Paragraph("Universidade Federal do Cariri (UFCA) • Instituto de Formação de Educadores (IFE) • Campus Brejo Santo", estilo_subtitulo))
    elementos.append(Paragraph(f"Guia Oficial de Programação e Atividades Disponíveis • Fomento FUNCAP • Emitido em: {agora_str}", estilo_meta))
    elementos.append(Spacer(1, 8))

    def _montar_tabela_dia(nome_dia: str, subtitulo_dia: str, atividades: List[Any]):
        t_elementos = []
        t_elementos.append(Paragraph(f"<b>{nome_dia}</b> • {subtitulo_dia}", estilo_dia_header))

        cabecalho = [
            Paragraph("Horário", estilo_cabecalho_tab),
            Paragraph("Categoria", estilo_cabecalho_tab),
            Paragraph("Atividade & Ministrante", estilo_cabecalho_tab),
            Paragraph("Local", estilo_cabecalho_tab),
        ]
        linhas = [cabecalho]

        for a in atividades:
            horario = getattr(a, "horario", "") if hasattr(a, "horario") else str(a.get("horario", ""))
            tipo = getattr(a, "tipo", "") if hasattr(a, "tipo") else str(a.get("tipo", ""))
            titulo = getattr(a, "titulo", "") if hasattr(a, "titulo") else str(a.get("titulo", ""))
            palestrante = getattr(a, "palestrante", "") if hasattr(a, "palestrante") else str(a.get("palestrante", ""))
            local = getattr(a, "local", "") if hasattr(a, "local") else str(a.get("local", ""))

            bloco_desc = [Paragraph(titulo, estilo_titulo_atv)]
            if palestrante and palestrante.strip():
                bloco_desc.append(Paragraph(palestrante, estilo_palestrante_atv))

            linhas.append([
                Paragraph(horario, estilo_hora),
                Paragraph(tipo, estilo_tipo),
                bloco_desc,
                Paragraph(local, estilo_local),
            ])

        col_widths = [75, 75, 273, 100]
        tab = Table(linhas, colWidths=col_widths, repeatRows=1)
        tab.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#103460")),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("PADDING", (0, 0), (-1, -1), 3.5),
        ]))
        t_elementos.append(tab)
        t_elementos.append(Spacer(1, 8))
        return t_elementos

    elementos.extend(_montar_tabela_dia("Dia 1 • 11/11/2026", "Abertura Oficial, Plenárias e Apresentações Científicas", atividades_dia1))
    elementos.extend(_montar_tabela_dia("Dia 2 • 12/11/2026", "Palestras Convidadas, Mesas Temáticas e Encerramento", atividades_dia2))

    estilo_rodape = ParagraphStyle(
        "RodapeProg",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#64748B"),
        alignment=1,
    )
    elementos.append(Spacer(1, 4))
    elementos.append(Paragraph("A credencial oficial concede acesso pleno a todas as atividades do simpósio.", estilo_rodape))

    doc.build(elementos)
    return buffer.getvalue()
