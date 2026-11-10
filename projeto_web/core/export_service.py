"""Serviço de Exportação de Dados do IV EFAC 2026.
Gera relatórios oficiais em formato CSV e PDF (ReportLab) com suporte completo a UTF-8 e acentuação pt-BR (NFC).
"""

import io
import os
import unicodedata
from xml.sax.saxutils import escape as xml_escape
from datetime import datetime
from typing import List, Dict, Any, Tuple


def normalizar_texto_ptbr(valor: Any) -> str:
    """Normaliza qualquer texto para Unicode NFC (padrão pt-BR composto), repara eventual mojibake (cp1252/latin1) e remove BOM invisível (\ufeff)."""
    if valor is None:
        return ""
    texto = str(valor).replace("\ufeff", "").replace("\u200b", "")
    if "Ã" in texto or "Â" in texto:
        for enc in ("cp1252", "latin1"):
            try:
                reparado = texto.encode(enc).decode("utf-8")
                if len(reparado) < len(texto):
                    texto = reparado
                    break
            except Exception:
                pass
    return unicodedata.normalize("NFC", texto)


def _escapar_pdf_texto(valor: Any) -> str:
    """Normaliza em NFC e escapa caracteres especiais XML (&, <, >) para uso seguro em Paragraph do ReportLab."""
    return xml_escape(normalizar_texto_ptbr(valor))


def _configurar_fontes_utf8_pdf() -> Tuple[str, str, str]:
    """Registra fontes TrueType com suporte completo aos acentos do Português do Brasil (UTF-8).
    Retorna a tupla (font_regular, font_bold, font_italic).
    """
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        familias_candidatas = [
            (
                "EFACDejaVu",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf",
            ),
            (
                "EFACLiberation",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf",
            ),
            (
                "EFACUbuntu",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-RI.ttf",
                "/usr/share/fonts/truetype/ubuntu/Ubuntu-BI.ttf",
            ),
        ]

        for nome_base, reg_path, bold_path, italic_path, bold_italic_path in familias_candidatas:
            if os.path.exists(reg_path) and os.path.exists(bold_path):
                f_reg = f"{nome_base}-Regular"
                f_bold = f"{nome_base}-Bold"
                f_italic = f"{nome_base}-Italic"
                f_bi = f"{nome_base}-BoldItalic"
                if f_reg not in pdfmetrics.getRegisteredFontNames():
                    pdfmetrics.registerFont(TTFont(f_reg, reg_path))
                    pdfmetrics.registerFont(TTFont(f_bold, bold_path))
                    pdfmetrics.registerFont(TTFont(f_italic, italic_path if os.path.exists(italic_path) else reg_path))
                    pdfmetrics.registerFont(TTFont(f_bi, bold_italic_path if os.path.exists(bold_italic_path) else bold_path))
                    pdfmetrics.registerFontFamily(
                        f_reg,
                        normal=f_reg,
                        bold=f_bold,
                        italic=f_italic,
                        boldItalic=f_bi,
                    )
                return (f_reg, f_bold, f_italic)
    except Exception:
        pass

    return ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique")


def gerar_csv_inscritos(usuarios: List[Any]) -> str:
    """Gera string CSV em UTF-8 puro normalizado em NFC (sem BOM \\ufeff na string em memória e sem 'sep=;' que força ANSI no Excel)."""
    linhas = [
        "ID;Código de Check-in;Nome Completo;E-mail;Instituição / Polo;Modalidade;Eixo Temático;Função / Papel;Presença Dia 1 (11/Nov);Presença Dia 2 (12/Nov)"
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

        # Normalizar para NFC e sanitizar contra ponto-e-vírgula e caracteres invisíveis
        linha = [
            normalizar_texto_ptbr(uid),
            f'"{normalizar_texto_ptbr(cod)}"',
            f'"{normalizar_texto_ptbr(nome).replace(";", ",")}"',
            f'"{normalizar_texto_ptbr(email).replace(";", ",")}"',
            f'"{normalizar_texto_ptbr(inst).replace(";", ",")}"',
            f'"{normalizar_texto_ptbr(mod)}"',
            f'"{normalizar_texto_ptbr(area).replace(";", ",")}"',
            f'"{normalizar_texto_ptbr(role).upper()}"',
            f'"{normalizar_texto_ptbr(pres_d1)}"',
            f'"{normalizar_texto_ptbr(pres_d2)}"',
        ]
        linhas.append(";".join(linha))

    return "\r\n".join(linhas)


def gerar_csv_inscritos_bytes(usuarios: List[Any]) -> bytes:
    """Gera os bytes finais do arquivo físico .csv adicionando o BOM UTF-8 (0xEF, 0xBB, 0xBF) exclusivamente nos bytes binários.
    - No transporte WebSocket/JSON (Reflex rx.download), os bytes são codificados em Base64 ASCII ('77u/...'), nunca expondo '\\ufeff' ao motor JS do iOS.
    - Ao salvar o arquivo físico no disco, os 3 bytes iniciais 0xEF 0xBB 0xBF (sem 'sep=;') garantem que o Microsoft Excel abra em UTF-8 perfeito.
    """
    csv_limpo = gerar_csv_inscritos(usuarios)
    return b"\xef\xbb\xbf" + csv_limpo.encode("utf-8")


def gerar_pdf_inscritos(usuarios: List[Any], stats: Dict[str, Any]) -> bytes:
    """Gera PDF oficial diagramado em formato paisagem com ReportLab e fontes TrueType UTF-8 (pt-BR)."""
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

    font_reg, font_bold, _ = _configurar_fontes_utf8_pdf()

    # Estilos customizados com fontes TrueType UTF-8 completas
    estilo_titulo = ParagraphStyle(
        "TituloEFAC",
        parent=estilos["Heading1"],
        fontName=font_bold,
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#103460"),
        alignment=0,
    )
    estilo_subtitulo = ParagraphStyle(
        "SubtituloEFAC",
        parent=estilos["Normal"],
        fontName=font_bold,
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#00ADB5"),
        alignment=0,
    )
    estilo_meta = ParagraphStyle(
        "MetaEFAC",
        parent=estilos["Normal"],
        fontName=font_reg,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#475569"),
        alignment=0,
    )
    estilo_celula = ParagraphStyle(
        "CelulaTabela",
        parent=estilos["Normal"],
        fontName=font_reg,
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#0f172a"),
    )
    estilo_cabecalho_tab = ParagraphStyle(
        "CabecalhoTabela",
        parent=estilos["Normal"],
        fontName=font_bold,
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
            Paragraph(f"<b>{_escapar_pdf_texto(cod)}</b>", estilo_celula),
            Paragraph(_escapar_pdf_texto(nome), estilo_celula),
            Paragraph(_escapar_pdf_texto(email), estilo_celula),
            Paragraph(_escapar_pdf_texto(inst), estilo_celula),
            Paragraph(_escapar_pdf_texto(mod), estilo_celula),
            Paragraph(_escapar_pdf_texto(role).upper(), estilo_celula),
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
    """Gera PDF oficial diagramado com a programação e atividades completas do IV EFAC (UTF-8 / pt-BR)."""
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

    font_reg, font_bold, font_italic = _configurar_fontes_utf8_pdf()

    estilo_titulo = ParagraphStyle(
        "TituloEFACProg",
        parent=estilos["Heading1"],
        fontName=font_bold,
        fontSize=14,
        leading=17,
        textColor=colors.HexColor("#103460"),
        alignment=0,
    )
    estilo_subtitulo = ParagraphStyle(
        "SubtituloEFACProg",
        parent=estilos["Normal"],
        fontName=font_bold,
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor("#00ADB5"),
        alignment=0,
    )
    estilo_meta = ParagraphStyle(
        "MetaEFACProg",
        parent=estilos["Normal"],
        fontName=font_reg,
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#475569"),
        alignment=0,
    )
    estilo_dia_header = ParagraphStyle(
        "DiaHeaderEFAC",
        parent=estilos["Heading2"],
        fontName=font_bold,
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=7,
        spaceAfter=3,
    )
    estilo_hora = ParagraphStyle(
        "HoraProg",
        parent=estilos["Normal"],
        fontName=font_bold,
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#00ADB5"),
    )
    estilo_tipo = ParagraphStyle(
        "TipoProg",
        parent=estilos["Normal"],
        fontName=font_bold,
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#2563EB"),
    )
    estilo_titulo_atv = ParagraphStyle(
        "TituloAtvProg",
        parent=estilos["Normal"],
        fontName=font_bold,
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
    )
    estilo_palestrante_atv = ParagraphStyle(
        "PalestranteAtvProg",
        parent=estilos["Normal"],
        fontName=font_italic,
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#334155"),
    )
    estilo_local = ParagraphStyle(
        "LocalProg",
        parent=estilos["Normal"],
        fontName=font_reg,
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#1e293b"),
    )
    estilo_cabecalho_tab = ParagraphStyle(
        "CabTabProg",
        parent=estilos["Normal"],
        fontName=font_bold,
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
        t_elementos.append(Paragraph(f"<b>{_escapar_pdf_texto(nome_dia)}</b> • {_escapar_pdf_texto(subtitulo_dia)}", estilo_dia_header))

        cabecalho = [
            Paragraph("Horário", estilo_cabecalho_tab),
            Paragraph("Categoria", estilo_cabecalho_tab),
            Paragraph("Atividade &amp; Ministrante", estilo_cabecalho_tab),
            Paragraph("Local", estilo_cabecalho_tab),
        ]
        linhas = [cabecalho]

        for a in atividades:
            horario = getattr(a, "horario", "") if hasattr(a, "horario") else str(a.get("horario", ""))
            tipo = getattr(a, "tipo", "") if hasattr(a, "tipo") else str(a.get("tipo", ""))
            titulo = getattr(a, "titulo", "") if hasattr(a, "titulo") else str(a.get("titulo", ""))
            palestrante = getattr(a, "palestrante", "") if hasattr(a, "palestrante") else str(a.get("palestrante", ""))
            local = getattr(a, "local", "") if hasattr(a, "local") else str(a.get("local", ""))

            bloco_desc = [Paragraph(_escapar_pdf_texto(titulo), estilo_titulo_atv)]
            if palestrante and palestrante.strip():
                bloco_desc.append(Paragraph(_escapar_pdf_texto(palestrante), estilo_palestrante_atv))

            linhas.append([
                Paragraph(_escapar_pdf_texto(horario), estilo_hora),
                Paragraph(_escapar_pdf_texto(tipo), estilo_tipo),
                bloco_desc,
                Paragraph(_escapar_pdf_texto(local), estilo_local),
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
        fontName=font_reg,
        fontSize=7,
        leading=9,
        textColor=colors.HexColor("#64748B"),
        alignment=1,
    )
    elementos.append(Spacer(1, 4))
    elementos.append(Paragraph("A credencial oficial concede acesso pleno a todas as atividades do simpósio.", estilo_rodape))

    doc.build(elementos)
    return buffer.getvalue()
