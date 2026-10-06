"""Modal de Edição de Perfil, Segurança de Senha e Confirmação de E-mail."""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.styles.theme import (
    COLOR_CYAN,
    COLOR_SURFACE_GLASS,
    STYLE_BUTTON_CHIP,
    STYLE_TEXT_RESPONSIVE,
)


def modal_meu_perfil() -> rx.Component:
    """Modal central de gerenciamento de dados cadastrais, credenciais e e-mail."""
    return rx.cond(
        EventoState.modal_perfil_aberto,
        rx.box(
            # Fundo escuro com backdrop blur
            rx.box(
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                background="rgba(2, 6, 23, 0.75)",
                backdrop_filter="blur(8px)",
                z_index="1000",
                on_click=EventoState.fechar_modal_perfil,
            ),
            # Conteúdo do Modal
            rx.box(
                rx.vstack(
                    # Cabeçalho do Modal
                    rx.hstack(
                        rx.hstack(
                            rx.icon(tag="user-cog", size=22, color=COLOR_CYAN),
                            rx.vstack(
                                rx.heading("Meu Perfil & Segurança", size="4", weight="bold", color="white"),
                                rx.text(
                                    f"{EventoState.user_nome} • {EventoState.user_codigo}",
                                    size="1",
                                    color="var(--gray-9)",
                                ),
                                spacing="0",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="x", size=18),
                            variant="ghost",
                            color_scheme="gray",
                            size="1",
                            on_click=EventoState.fechar_modal_perfil,
                            cursor="pointer",
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.divider(color_scheme="gray", opacity="0.2"),
                    # Abas de Configuração
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="user", size=15),
                                    rx.text("Dados Pessoais", size="2"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="dados",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="key-round", size=15),
                                    rx.text("Troca de Senha", size="2"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="senha",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="mail-check", size=15),
                                    rx.text("Confirmação de E-mail", size="2"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="email",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="id-card", size=15),
                                    rx.text("Carteirinha", size="2"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="carteirinha",
                            ),
                            size="2",
                        ),
                        # Aba 1: Dados Pessoais
                        rx.tabs.content(
                            rx.vstack(
                                rx.vstack(
                                    rx.text("Nome Completo", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Seu nome completo",
                                        value=EventoState.perfil_nome_input,
                                        on_change=EventoState.set_perfil_nome,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Instituição de Ensino / Polo", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Ex: Universidade Federal do Cariri (UFCA)",
                                        value=EventoState.perfil_instituicao_input,
                                        on_change=EventoState.set_perfil_instituicao,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Modalidade de Participação", size="1", weight="bold", color="white"),
                                    rx.hstack(
                                        rx.button(
                                            "Presencial (Brejo Santo)",
                                            variant=rx.cond(EventoState.perfil_modalidade_input == "Presencial", "solid", "outline"),
                                            color_scheme="cyan",
                                            size="2",
                                            on_click=EventoState.set_perfil_modalidade("Presencial"),
                                        ),
                                        rx.button(
                                            "Online (Transmissão)",
                                            variant=rx.cond(EventoState.perfil_modalidade_input == "Online", "solid", "outline"),
                                            color_scheme="indigo",
                                            size="2",
                                            on_click=EventoState.set_perfil_modalidade("Online"),
                                        ),
                                        spacing="2",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.hstack(
                                    rx.spacer(),
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="save", size=15),
                                            rx.text("Salvar Alterações"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="2",
                                        color_scheme="cyan",
                                        on_click=EventoState.salvar_meu_perfil,
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    width="100%",
                                    padding_top="0.8rem",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            value="dados",
                            padding_top="1rem",
                        ),
                        # Aba 2: Troca de Senha Segura
                        rx.tabs.content(
                            rx.vstack(
                                rx.text(
                                    "Para proteger sua conta, informe sua senha atual antes de cadastrar uma nova credencial.",
                                    size="2",
                                    color="var(--gray-10)",
                                    style=STYLE_TEXT_RESPONSIVE,
                                ),
                                rx.vstack(
                                    rx.text("Senha Atual", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Digite sua senha atual",
                                        type="password",
                                        value=EventoState.minha_senha_atual_input,
                                        on_change=EventoState.set_minha_senha_atual,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Nova Senha (Mínimo 6 caracteres)", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Digite a nova senha",
                                        type="password",
                                        value=EventoState.minha_nova_senha_input,
                                        on_change=EventoState.set_minha_nova_senha,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Confirme a Nova Senha", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Repita a nova senha",
                                        type="password",
                                        value=EventoState.minha_nova_senha_confirm,
                                        on_change=EventoState.set_minha_nova_senha_confirm,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.hstack(
                                    rx.spacer(),
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="lock", size=15),
                                            rx.text("Atualizar Senha"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="2",
                                        color_scheme="green",
                                        on_click=EventoState.salvar_minha_nova_senha,
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    width="100%",
                                    padding_top="0.8rem",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            value="senha",
                            padding_top="1rem",
                        ),
                        # Aba 3: Confirmação de E-mail com Aviso Anti-Spam
                        rx.tabs.content(
                            rx.vstack(
                                rx.cond(
                                    EventoState.usuario_logado_email_confirmado,
                                    rx.card(
                                        rx.vstack(
                                            rx.hstack(
                                                rx.icon(tag="shield-check", size=24, color="#10b981"),
                                                rx.badge("E-MAIL CONFIRMADO E AUTENTICADO", color_scheme="green", variant="solid", size="2"),
                                                spacing="2",
                                                align="center",
                                            ),
                                            rx.text(
                                                f"O endereço {EventoState.user_email} está verificado com sucesso no sistema do IV EFAC 2026.",
                                                size="2",
                                                color="white",
                                            ),
                                            rx.text(
                                                "✅ Submissão de trabalhos científicos liberada nos Anais do evento.",
                                                size="2",
                                                color="#34d399",
                                            ),
                                            spacing="2",
                                            align="start",
                                        ),
                                        background="rgba(6, 78, 59, 0.4)",
                                        border="1px solid rgba(16, 185, 129, 0.4)",
                                        width="100%",
                                    ),
                                    rx.vstack(
                                        rx.badge("Confirmação de E-mail Pendente", color_scheme="amber", variant="solid", size="2"),
                                        rx.text(
                                            f"Para enviar resumos e receber comunicados oficiais, confirme seu e-mail cadastrado ({EventoState.user_email}).",
                                            size="2",
                                            color="var(--gray-11)",
                                        ),
                                        # Box de Orientação Amigável Anti-Lixo/Spam
                                        rx.box(
                                            rx.vstack(
                                                rx.hstack(
                                                    rx.icon(tag="alert-triangle", size=18, color="#f59e0b"),
                                                    rx.text("Atenção sobre sua Caixa de Entrada:", size="2", weight="bold", color="#fbbf24"),
                                                    spacing="2",
                                                    align="center",
                                                ),
                                                rx.text(
                                                    "Ao receber a mensagem de confirmação ou notificações sobre seus artigos, verifique sempre a pasta de SPAM ou LIXO ELETRÔNICO do seu e-mail.",
                                                    size="1",
                                                    color="white",
                                                ),
                                                rx.text(
                                                    "🛡️ Recomendação de Proteção: Adicione o remetente oficial aos seus contatos e marque como 'Não é Spam' para garantir o recebimento dos pareceres da Comissão Científica.",
                                                    size="1",
                                                    color="var(--gray-10)",
                                                ),
                                                spacing="1",
                                                align="start",
                                            ),
                                            padding="0.85rem 1rem",
                                            border_radius="10px",
                                            background="rgba(120, 53, 15, 0.35)",
                                            border="1px solid rgba(245, 158, 11, 0.4)",
                                            width="100%",
                                        ),
                                        rx.hstack(
                                            rx.button(
                                                rx.hstack(
                                                    rx.icon(tag="send", size=15),
                                                    rx.text("Solicitar Código de Confirmação"),
                                                    spacing="1",
                                                    align="center",
                                                ),
                                                size="2",
                                                variant="outline",
                                                color_scheme="cyan",
                                                on_click=EventoState.solicitar_codigo_email,
                                            ),
                                            rx.button(
                                                rx.hstack(
                                                    rx.icon(tag="check-circle", size=15),
                                                    rx.text("Confirmar E-mail Agora"),
                                                    spacing="1",
                                                    align="center",
                                                ),
                                                size="2",
                                                color_scheme="green",
                                                on_click=EventoState.confirmar_email_direto,
                                            ),
                                            spacing="2",
                                            wrap="wrap",
                                            width="100%",
                                        ),
                                        # Campo para código de confirmação
                                        rx.hstack(
                                            rx.input(
                                                placeholder="Digite o código de 6 dígitos...",
                                                value=EventoState.codigo_email_input,
                                                on_change=EventoState.set_codigo_email,
                                                size="2",
                                                flex="1",
                                            ),
                                            rx.button(
                                                "Validar Código",
                                                size="2",
                                                color_scheme="cyan",
                                                on_click=EventoState.confirmar_email_codigo,
                                            ),
                                            width="100%",
                                        ),
                                        spacing="3",
                                        width="100%",
                                    ),
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            value="email",
                            padding_top="1rem",
                        ),
                        # Aba 4: Download da Carteirinha
                        rx.tabs.content(
                            rx.vstack(
                                rx.text(
                                    "Baixe a sua carteirinha oficial em alta resolução com o Soldadinho-do-Araripe e arte do Cariri Cósmico.",
                                    size="2",
                                    color="var(--gray-10)",
                                ),
                                rx.button(
                                    rx.hstack(
                                        rx.icon(tag="download", size=16),
                                        rx.text("Baixar Carteirinha (PNG)"),
                                        spacing="2",
                                        align="center",
                                    ),
                                    size="3",
                                    color_scheme="cyan",
                                    on_click=EventoState.baixar_minha_carteirinha_png,
                                    style=STYLE_BUTTON_CHIP,
                                    width="100%",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            value="carteirinha",
                            padding_top="1rem",
                        ),
                        default_value="dados",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="1001",
                width="92%",
                max_width="620px",
                max_height="90vh",
                overflow_y="auto",
                background="rgba(15, 23, 42, 0.98)",
                border="1.5px solid rgba(0, 173, 181, 0.4)",
                box_shadow="0 25px 60px rgba(0, 0, 0, 0.85)",
                border_radius="16px",
                padding="1.5rem",
            ),
        ),
        rx.fragment(),
    )
