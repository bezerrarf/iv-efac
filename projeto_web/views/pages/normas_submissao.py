"""Página Oficial de Normas de Submissão e Apresentação do IV EFAC 2026.
Transcrição 100% fiel ao documento oficial em PDF (normas_submissao_iv_efac.pdf).
Disponibiliza botões para retornar à área do usuário e download direto do PDF original.
"""

import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import footer
from projeto_web.views.components.cosmic_background import cosmic_background
from projeto_web.styles.theme import (
    COLOR_BG,
    COLOR_SURFACE_GLASS,
    COLOR_BORDER_CYAN,
    COLOR_BORDER_SUBTLE,
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_TEXT_PRIMARY,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
    STYLE_BUTTON_CHIP,
)


def _secao_card(titulo: str, conteudo: rx.Component) -> rx.Component:
    """Card padrão para seções normativas do documento."""
    return rx.card(
        rx.vstack(
            rx.heading(
                titulo,
                size="4",
                weight="bold",
                color=COLOR_CYAN_LIGHT,
                style=STYLE_HEADING_RESPONSIVE,
            ),
            rx.divider(color_scheme="gray", opacity="0.2"),
            conteudo,
            spacing="3",
            align="start",
            width="100%",
        ),
        padding=rx.breakpoints(initial="1.25rem", sm="1.75rem"),
        border_radius="14px",
        background=COLOR_SURFACE_GLASS,
        backdrop_filter="blur(16px)",
        border=f"1px solid {COLOR_BORDER_CYAN}",
        box_shadow="0 6px 25px rgba(0, 0, 0, 0.35)",
        width="100%",
    )


def normas_submissao_page() -> rx.Component:
    return rx.box(
        # Fundo Cósmico Vetorial Imersivo e Fixo
        cosmic_background(),

        navbar(),

        rx.box(
            rx.vstack(
                # Barra de Ações: Voltar ao Espaço do Usuário & Baixar PDF Oficial
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="arrow-left", size=16),
                                rx.text("Voltar ao Espaço do Usuário", weight="bold"),
                                spacing="2",
                                align="center",
                            ),
                            size="2",
                            variant="surface",
                            color_scheme="cyan",
                            radius="full",
                            style=STYLE_BUTTON_CHIP,
                        ),
                        href="/inscricao",
                    ),
                    rx.spacer(),
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="download", size=16),
                                rx.text("Baixar PDF Original", weight="bold"),
                                spacing="2",
                                align="center",
                            ),
                            size="2",
                            variant="solid",
                            color_scheme="amber",
                            radius="full",
                            style=STYLE_BUTTON_CHIP,
                        ),
                        href="/normas_submissao_iv_efac.pdf",
                        is_external=True,
                    ),
                    width="100%",
                    align="center",
                    wrap="wrap",
                    gap="2",
                    margin_bottom="1rem",
                ),

                # Cabeçalho Oficial do Documento
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.badge("Documento Oficial", color_scheme="cyan", variant="solid", size="2", style=STYLE_BUTTON_CHIP),
                            rx.badge("Apoio: FUNCAP (Edital 03/2026)", color_scheme="indigo", variant="surface", size="2", style=STYLE_BUTTON_CHIP),
                            spacing="2",
                            align="center",
                            wrap="wrap",
                        ),
                        rx.heading(
                            "IV EFAC 2026 • Normas Oficiais de Submissão e Apresentação",
                            size=rx.breakpoints(initial="5", sm="6", md="7"),
                            weight="bold",
                            color=COLOR_TEXT_PRIMARY,
                            text_align="center",
                            style=STYLE_HEADING_RESPONSIVE,
                        ),
                        rx.text(
                            "IV Encontro de Física e Astronomia do Cariri (11 e 12 de Novembro de 2026)",
                            size="3",
                            weight="medium",
                            color=COLOR_CYAN,
                            text_align="center",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        rx.text(
                            "Universidade Federal do Cariri (UFCA) • Instituto de Formação de Educadores (IFE) – Campus Brejo Santo",
                            size="2",
                            color="#CBD5E1",
                            text_align="center",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    padding=rx.breakpoints(initial="1.5rem", sm="2rem"),
                    border_radius="16px",
                    background="linear-gradient(145deg, rgba(16, 52, 96, 0.4), rgba(6, 8, 20, 0.8))",
                    border=f"1.5px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.4)",
                    width="100%",
                    text_align="center",
                ),

                # 1. Apresentação e Objetivos
                _secao_card(
                    "1. Apresentação e Objetivos",
                    rx.vstack(
                        rx.text(
                            "O IV Encontro de Física e Astronomia do Cariri (IV EFAC) consolidou-se como o principal fórum de debate, integração acadêmica e divulgação científica nas áreas de Astrofísica, Gravitação, Cosmologia, Física Computacional e Ensino de Ciências no interior do Estado do Ceará.",
                            size="2",
                            color="#E2E8F0",
                            line_height="1.7",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        rx.text(
                            "A chamada de trabalhos destina-se a docentes, pesquisadores, estudantes de pós-graduação e graduação (Iniciação Científica, TCC, estágios e projetos de ensino/extensão) que desejam compartilhar suas investigações com a comunidade científica regional e os renomados palestrantes convidados do evento.",
                            size="2",
                            color="#E2E8F0",
                            line_height="1.7",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),

                # 2. Eixos Temáticos
                _secao_card(
                    "2. Eixos Temáticos",
                    rx.vstack(
                        rx.text(
                            "Os trabalhos submetidos devem enquadrar-se obrigatoriamente em um dos quatro eixos temáticos do IV EFAC:",
                            size="2",
                            color="#E2E8F0",
                            line_height="1.7",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        rx.box(
                            rx.vstack(
                                rx.text(
                                    rx.text.strong("Eixo 1: Astrofísica de Objetos Compactos e Astrofísica Geral: ", color=COLOR_CYAN_LIGHT),
                                    "Matéria sob condições extremas de densidade e pressão, física nuclear aplicada a estrelas de nêutrons, anãs brancas, equações de estado relativísticas, pulsares, remanescentes de supernova e evolução estelar.",
                                    size="2",
                                    color="#CBD5E1",
                                    line_height="1.6",
                                ),
                                rx.text(
                                    rx.text.strong("Eixo 2: Relatividade Geral, Gravitação e Cosmologia: ", color=COLOR_CYAN_LIGHT),
                                    "Gravitação clássica e modificada, buracos negros, termodinâmica relativística, ondas gravitacionais, perturbações cosmológicas e cosmologia observacional/teórica.",
                                    size="2",
                                    color="#CBD5E1",
                                    line_height="1.6",
                                ),
                                rx.text(
                                    rx.text.strong("Eixo 3: Física Computacional e Ciência de Dados: ", color=COLOR_CYAN_LIGHT),
                                    "Modelagem e simulação numérica, métodos estocásticos, inteligência artificial e aprendizado de máquina aplicados à astrofísica e física estatística, inferência Bayesiana e análise de grandes catálogos astronômicos.",
                                    size="2",
                                    color="#CBD5E1",
                                    line_height="1.6",
                                ),
                                rx.text(
                                    rx.text.strong("Eixo 4: Ensino de Física, História da Ciência e Divulgação Científica: ", color=COLOR_CYAN_LIGHT),
                                    "Metodologias inovadoras no ensino básico e superior, experimentação didática, história e filosofia da ciência, formação continuada de professores e iniciativas de extensão/astronomia comunitária (e.g., Observatório Kariri).",
                                    size="2",
                                    color="#CBD5E1",
                                    line_height="1.6",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            padding="1rem",
                            border_radius="10px",
                            background="rgba(15, 23, 42, 0.6)",
                            border="1px solid rgba(255, 255, 255, 0.08)",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),

                # 3. Formato do Trabalho Escrito: Resumo Expandido (Até 2 Páginas)
                _secao_card(
                    "3. Formato do Trabalho Escrito: Resumo Expandido (Até 2 Páginas)",
                    rx.vstack(
                        rx.text(
                            "A submissão escrita é requisito indispensável para todas as modalidades (tanto para Pôster quanto para Apresentação Oral).",
                            size="2",
                            weight="medium",
                            color="#E2E8F0",
                            line_height="1.7",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        rx.heading("3.1 Regra de Limite de Extensão (Imprescindível)", size="3", weight="bold", color="white", margin_top="0.5rem"),
                        rx.vstack(
                            rx.hstack(
                                rx.icon(tag="alert-triangle", size=16, color="#F59E0B"),
                                rx.text(
                                    rx.text.strong("O trabalho deve ter no máximo 2 (duas) páginas", color="white"),
                                    ", já englobando cabeçalho, resumo, seções textuais, figuras, tabelas, fórmulas e referências bibliográficas.",
                                    size="2",
                                    color="#CBD5E1",
                                ),
                                spacing="2",
                                align="start",
                            ),
                            rx.hstack(
                                rx.icon(tag="x-circle", size=16, color="#EF4444"),
                                rx.text(
                                    "Submissões com 3 páginas ou mais serão rejeitadas preliminarmente sem avaliação de mérito.",
                                    size="2",
                                    color="#EF4444",
                                    weight="medium",
                                ),
                                spacing="2",
                                align="center",
                            ),
                            spacing="2",
                            width="100%",
                            padding="0.85rem",
                            border_radius="8px",
                            background="rgba(239, 68, 68, 0.08)",
                            border="1px solid rgba(239, 68, 68, 0.25)",
                        ),
                        rx.heading("3.2 Formatação e Templates Oficiais", size="3", weight="bold", color="white", margin_top="0.8rem"),
                        rx.text(
                            "A comissão organizadora disponibiliza templates padronizados em duas plataformas:",
                            size="2",
                            color="#E2E8F0",
                        ),
                        rx.vstack(
                            rx.text(
                                rx.text.strong("a) LaTeX (.tex): "),
                                "Recomendado fortemente para as áreas de física teórica e computacional. Compilação direta via pdflatex.",
                                size="2",
                                color="#CBD5E1",
                            ),
                            rx.text(
                                rx.text.strong("b) Microsoft Word / LibreOffice (.docx): "),
                                "Configurado com os exatos parâmetros tipográficos e diagramação de 2 colunas.",
                                size="2",
                                color="#CBD5E1",
                            ),
                            spacing="1",
                            width="100%",
                            padding_left="0.5rem",
                        ),
                        rx.text.strong("Estrutura do Documento:", color="white", margin_top="0.5rem"),
                        rx.vstack(
                            rx.text("• Cabeçalho: Logomarcas do evento e da UFCA, título em negrito (máximo 20 palavras), relação completa de autores, afiliações institucionais com siglas e e-mail de contato do apresentador.", size="2", color="#CBD5E1"),
                            rx.text("• Identificação do Eixo Temático e Modalidade Pretendida (Oral ou Pôster).", size="2", color="#CBD5E1"),
                            rx.text("• Resumo Textual: Parágrafo único contendo de 150 a 250 palavras, sintetizando contextualização, objetivos, método, principais resultados e conclusões.", size="2", color="#CBD5E1"),
                            rx.text("• Palavras-chave: 3 a 5 termos separados por ponto e vírgula.", size="2", color="#CBD5E1"),
                            rx.text("• Seções Textuais (2 colunas): 1. Introdução (fundamentação e objetivos); 2. Metodologia / Procedimentos Teóricos ou Experimentais; 3. Resultados e Discussão (inclusão de figuras nítidas e/ou tabelas sintetizadas); 4. Considerações Finais / Conclusões; Agradecimentos (menção às agências de fomento como FUNCAP, CNPq, CAPES ou à UFCA); Referências Bibliográficas (normas ABNT ou padrão numérico internacional consistente).", size="2", color="#CBD5E1", line_height="1.6"),
                            spacing="2",
                            width="100%",
                            padding_left="0.5rem",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),

                # 4. Diretrizes para Apresentação em Banner / Pôster
                _secao_card(
                    "4. Diretrizes para Apresentação em Banner / Pôster",
                    rx.vstack(
                        rx.heading("4.1 Dimensões e Características Físicas do Banner", size="3", weight="bold", color="white"),
                        rx.vstack(
                            rx.text("• Dimensões Padrão Recomendadas: 90 cm de largura por 120 cm de altura (padrão tradicional de feiras e congressos científicos) ou Padrão A0 retrato (84,1 cm × 118,9 cm).", size="2", color="#CBD5E1"),
                            rx.text("• Orientação: Estritamente Vertical (Retrato). Não serão aceitos banners em formato paisagem (horizontal).", size="2", color="#CBD5E1", weight="medium"),
                            rx.text("• Acabamento: O banner deve possuir canaleta de plástico/madeira superior e inferior com cordão de sustentação para fixação nos tripés e painéis do evento.", size="2", color="#CBD5E1"),
                            spacing="1",
                            width="100%",
                            padding_left="0.5rem",
                        ),
                        rx.heading("4.2 Organização Visual e Legibilidade", size="3", weight="bold", color="white", margin_top="0.8rem"),
                        rx.vstack(
                            rx.text("• Visibilidade a Distância: O banner deve ser legível com conforto a uma distância mínima de 1,5 a 2,0 metros.", size="2", color="#CBD5E1"),
                            rx.text("• Cabeçalho: Deve conter em destaque:", size="2", color="#CBD5E1"),
                            rx.box(
                                rx.vstack(
                                    rx.text("– Logomarca da UFCA à esquerda, título centralizado e Logomarca do IV EFAC à direita (com citação de apoio à FUNCAP no rodapé).", size="2", color="#CBD5E1"),
                                    rx.text("– Título em tamanho generoso (60 a 80 pt), em caixa alta/baixa legível.", size="2", color="#CBD5E1"),
                                    rx.text("– Nomes dos autores (32 a 42 pt) com sublinhado no nome do apresentador.", size="2", color="#CBD5E1"),
                                    rx.text("– Filiações e e-mails (24 a 30 pt).", size="2", color="#CBD5E1"),
                                    spacing="1",
                                ),
                                padding_left="1.2rem",
                            ),
                            rx.text("• Corpo do Pôster:", size="2", color="#CBD5E1"),
                            rx.box(
                                rx.vstack(
                                    rx.text("– Títulos de seções: 40 a 50 pt (em negrito e cores institucionais).", size="2", color="#CBD5E1"),
                                    rx.text("– Texto corrido: 22 a 28 pt (nunca inferior a 20 pt).", size="2", color="#CBD5E1"),
                                    rx.text("– Utilize gráficos de boa resolução (mínimo 300 DPI), esquemas visuais e tabelas autoexplicativas. Evite blocos extensos de texto contínuo.", size="2", color="#CBD5E1"),
                                    spacing="1",
                                ),
                                padding_left="1.2rem",
                            ),
                            rx.text("• Template Oficial: A organização disponibiliza um modelo de banner tanto em PowerPoint (.pptx) quanto em LaTeX Beamerposter (.tex).", size="2", color="#CBD5E1"),
                            spacing="1",
                            width="100%",
                            padding_left="0.5rem",
                        ),
                        rx.heading('4.3 Dinâmica da Sessão de Pôsteres ("Apresentação dos Meninos")', size="3", weight="bold", color="white", margin_top="0.8rem"),
                        rx.vstack(
                            rx.text("• Data e Horário: Quinta-feira, 12 de novembro de 2026, das 15:00 às 17:30.", size="2", color="#CBD5E1", weight="bold"),
                            rx.text("• Local: Hall Principal e Foyer do Campus Brejo Santo – UFCA.", size="2", color="#CBD5E1"),
                            rx.text("• Fixação e Retirada: A fixação deve ocorrer das 13:30 às 14:00 (antes da Mesa-Redonda). A retirada ocorrerá após as 17:30.", size="2", color="#CBD5E1"),
                            rx.text("• Avaliação Presencial: O apresentador cadastrado deve permanecer junto ao seu pôster durante toda a sessão para receber a comissão avaliadora e interagir com o público.", size="2", color="#CBD5E1"),
                            spacing="1",
                            width="100%",
                            padding_left="0.5rem",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                ),

                # 5. Diretrizes para Apresentação Oral
                _secao_card(
                    "5. Diretrizes para Apresentação Oral",
                    rx.vstack(
                        rx.text("• Tempo de Duração: 15 minutos no total, distribuídos em:", size="2", color="#CBD5E1"),
                        rx.box(
                            rx.vstack(
                                rx.text("– 10 a 12 minutos de exposição pelo autor;", size="2", color="#CBD5E1"),
                                rx.text("– 3 a 5 minutos para perguntas da banca avaliadora e do público.", size="2", color="#CBD5E1"),
                                spacing="1",
                            ),
                            padding_left="1.2rem",
                        ),
                        rx.text("• Formato dos Slides: Padrão 16:9 (Widescreen), em formato PowerPoint (.pptx) ou PDF gerado via LaTeX Beamer.", size="2", color="#CBD5E1"),
                        rx.text("• Template Oficial: Recomenda-se utilizar o template oficial de slides fornecido pelo IV EFAC.", size="2", color="#CBD5E1"),
                        rx.text("• Entrega Prévia dos Arquivos: O apresentador deverá entregar o arquivo em pendrive na sala de apoio técnico da monitoria com no mínimo 30 minutos de antecedência da sua sessão.", size="2", color="#CBD5E1"),
                        spacing="2",
                        width="100%",
                        padding_left="0.5rem",
                    ),
                ),

                # 6. Avaliação, Pareceres e Certificação
                _secao_card(
                    "6. Avaliação, Pareceres e Certificação",
                    rx.vstack(
                        rx.text("• Comitê Avaliador: Todos os trabalhos serão avaliados por professores e pesquisadores do comitê científico.", size="2", color="#CBD5E1"),
                        rx.text("• Critérios de Julgamento:", size="2", color="#CBD5E1"),
                        rx.box(
                            rx.vstack(
                                rx.text("1. Relevância do problema científico e originalidade;", size="2", color="#CBD5E1"),
                                rx.text("2. Coerência e rigor metodológico;", size="2", color="#CBD5E1"),
                                rx.text("3. Consistência na análise dos resultados e conclusões;", size="2", color="#CBD5E1"),
                                rx.text("4. Qualidade da redação acadêmica e respeito estrito às normas (máximo 2 páginas).", size="2", color="#CBD5E1"),
                                spacing="1",
                            ),
                            padding_left="1.2rem",
                        ),
                        rx.text("• Resultado: Os trabalhos serão classificados como: Aprovado para Apresentação Oral, Aprovado para Apresentação em Pôster, Aprovado com Ressalvas ou Recusado. A comissão reserva-se o direito de reenquadrar a modalidade pretendida em função da capacidade das salas.", size="2", color="#CBD5E1", line_height="1.6"),
                        rx.text("• Certificação Oficial: Todos os autores e apresentadores com trabalhos aprovados e devidamente apresentados no evento (nas modalidades Oral ou Pôster) receberão certificados oficiais emitidos pela Universidade Federal do Cariri (UFCA).", size="2", color="#CBD5E1", line_height="1.6"),
                        spacing="2",
                        width="100%",
                        padding_left="0.5rem",
                    ),
                ),

                # 7. Cronograma Oficial de Submissões
                _secao_card(
                    "7. Cronograma Oficial de Submissões",
                    rx.vstack(
                        rx.table.root(
                            rx.table.header(
                                rx.table.row(
                                    rx.table.column_header_cell("Etapa do Processo", color=COLOR_CYAN_LIGHT),
                                    rx.table.column_header_cell("Data Limite / Período", color=COLOR_CYAN_LIGHT),
                                )
                            ),
                            rx.table.body(
                                rx.table.row(
                                    rx.table.cell("Lançamento do Portal Web e Abertura das Submissões"),
                                    rx.table.cell("05 de outubro de 2026"),
                                ),
                                rx.table.row(
                                    rx.table.cell("Prazo Final para Submissão de Trabalhos"),
                                    rx.table.cell(rx.text.strong("08 de novembro de 2026 (às 23h59)", color="#F59E0B")),
                                ),
                                rx.table.row(
                                    rx.table.cell("Divulgação dos Trabalhos Aprovados e Ensalamento"),
                                    rx.table.cell("10 de novembro de 2026"),
                                ),
                                rx.table.row(
                                    rx.table.cell("Credenciamento e Início do Evento"),
                                    rx.table.cell("11 de novembro de 2026 (quarta-feira)"),
                                ),
                                rx.table.row(
                                    rx.table.cell("Sessão de Apresentações Orais e Pôsteres"),
                                    rx.table.cell(rx.text.strong("12 de novembro de 2026 (quinta-feira, 15h00 às 17h30)", color=COLOR_CYAN)),
                                ),
                            ),
                            width="100%",
                            variant="surface",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),

                # Assinaturas e Rodapé Institucional
                rx.card(
                    rx.vstack(
                        rx.text(
                            "Prof. Dr. Edson Otoniel da Silva • Prof. Dr. André Flávio Gonçalves Silva",
                            size="3",
                            weight="bold",
                            color="white",
                            text_align="center",
                        ),
                        rx.text(
                            "Coordenação Geral e Científica do IV EFAC 2026",
                            size="2",
                            color=COLOR_CYAN_LIGHT,
                            text_align="center",
                        ),
                        rx.text(
                            "Universidade Federal do Cariri – IFE / Campus Brejo Santo",
                            size="2",
                            color="#CBD5E1",
                            text_align="center",
                        ),
                        rx.divider(color_scheme="gray", opacity="0.2", margin_y="0.5rem"),
                        rx.hstack(
                            rx.badge("Apoio: FUNCAP (Edital 03/2026)", color_scheme="indigo", variant="soft", size="2"),
                            rx.link(
                                rx.button(
                                    rx.hstack(
                                        rx.icon(tag="download", size=14),
                                        rx.text("Baixar PDF Original das Normas"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    size="2",
                                    variant="outline",
                                    color_scheme="cyan",
                                    style=STYLE_BUTTON_CHIP,
                                ),
                                href="/normas_submissao_iv_efac.pdf",
                                is_external=True,
                            ),
                            spacing="3",
                            align="center",
                            justify="center",
                            wrap="wrap",
                            width="100%",
                        ),
                        spacing="2",
                        align="center",
                        width="100%",
                    ),
                    padding=rx.breakpoints(initial="1.5rem", sm="2rem"),
                    border_radius="16px",
                    background="rgba(15, 23, 42, 0.7)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    width="100%",
                ),

                # Botão Inferior de Retorno
                rx.box(
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="arrow-left", size=16),
                                rx.text("Voltar ao Espaço do Usuário / Inscrição", weight="bold"),
                                spacing="2",
                                align="center",
                            ),
                            size="3",
                            radius="full",
                            variant="surface",
                            color_scheme="cyan",
                            padding_x="2rem",
                            style=STYLE_BUTTON_CHIP,
                        ),
                        href="/inscricao",
                    ),
                    margin_top="1rem",
                    margin_bottom="2rem",
                ),

                spacing="5",
                align="center",
                max_width="1000px",
                margin="0 auto",
                padding=rx.breakpoints(initial="1.5rem 1rem 3rem 1rem", sm="2.5rem 1.5rem 4rem 1.5rem"),
                width="100%",
            ),
            width="100%",
            flex="1",
            position="relative",
            z_index="2",
        ),

        footer(),

        display="flex",
        flex_direction="column",
        min_height="100vh",
        background=COLOR_BG,
        color="white",
        position="relative",
    )
