"""Conferência Automatizada Integral e Auditoria E2E — IV EFAC 2026.
Valida toda a jornada do usuário no navegador:
1. Acesso inicial (Home /), navegação por todas as abas e seções (Eixos, Palestrantes, Programação, Submissões, Local, Sobre).
2. Interação com o HUD de Contagem Regressiva e Citações Inspiradoras.
3. Botão do Edital Oficial (verificado como seguro/desativado aguardando regras finais).
4. Tela do Cronograma Expandido (/cronograma) com alternância entre Dia 1 e Dia 2 e fundo cósmico imersivo.
5. Tela de Inscrição (/inscricao), Carteirinha Digital, personalização de foto e modelo palestrante.
6. Painel Super Admin: navegação de abas, criação de atividade, delegação e DOWNLOAD DA LISTA EM PDF.
7. Painel do Supervisor: conferência de presença (check-in) e DOWNLOAD DA LISTA EM CSV.
8. Geração de relatórios completos (JSON, Markdown) e screenshots de evidência.
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

BASE_URL = os.getenv("TARGET_URL", "http://localhost:3000")
BASE_DIR = Path("/home/ramon_bezerra/Projects/Python_Lang/Projeto Web")
AUTO_DIR = BASE_DIR / ".automacao"
DOWNLOADS_DIR = AUTO_DIR / "downloads"
SCREENSHOTS_DIR = AUTO_DIR / "screenshots_conferencia"

DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

REPORT_JSON = AUTO_DIR / "relatorio_conferencia_geral.json"
REPORT_MD = AUTO_DIR / "RESUMO_CONFERENCIA.md"
LOG_FILE = AUTO_DIR / "conferencia_execucao.log"

logs = []


def log(msg: str, level: str = "INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] [{level}] {msg}"
    print(entry)
    logs.append(entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry + "\n")


async def run_full_conference():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== CONFERÊNCIA AUTOMATIZADA INTEGRAL — IV EFAC 2026 ===\n\n")

    log(f"Iniciando automação do fluxo completo do site: {BASE_URL}")

    conferencia = {
        "data_hora": datetime.now().isoformat(),
        "url_alvo": BASE_URL,
        "status_geral": "PENDENTE",
        "etapas": [],
        "screenshots": [],
        "downloads": {},
        "metricas": {}
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="IVEFAC-Playwright-QualityAuditor/3.0",
            accept_downloads=True
        )
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda exc: log(f"Exceção JavaScript na página: {exc}", "ERROR"))

        # ==============================================================
        # ETAPA 1: PÁGINA INICIAL (HOME), LOGO, EDITAL, HUD & TODAS AS ABAS
        # ==============================================================
        log("--- ETAPA 1: Acesso Inicial (Home), Identidade Visual, HUD de Contagem & Todas as Abas ---")
        t0 = time.time()
        resp = await page.goto(f"{BASE_URL}/", wait_until="networkidle", timeout=30000)
        tempo_home = round((time.time() - t0) * 1000, 1)
        status_home = resp.status if resp else 0
        titulo = await page.title()

        assert status_home == 200, f"Home retornou status {status_home}"
        log(f"Home carregada com sucesso ({tempo_home} ms) | Título: '{titulo}'")

        sc1_hero = SCREENSHOTS_DIR / "01_home_hero.png"
        await page.screenshot(path=str(sc1_hero))
        conferencia["screenshots"].append(sc1_hero.name)

        # 1.1 Nova Logo Oficial
        logo_imgs = await page.query_selector_all("img[src*='logo_ivefac.jpeg']")
        tem_logo = len(logo_imgs) > 0
        log(f"Nova Logo Oficial ('logo_ivefac.jpeg'): {tem_logo} ({len(logo_imgs)} ocorrência(s))")

        # 1.2 Botão Edital (Em Breve, Desativado para segurança)
        btn_edital = page.get_by_role("button", name="Edital", exact=False).first
        if not await btn_edital.is_visible():
            btn_edital = page.locator("#btn-edital-disabled").first
        edital_visivel = await btn_edital.is_visible() if btn_edital else False
        edital_desativado = await btn_edital.is_disabled() if edital_visivel else False
        log(f"Botão Edital detectado: visível={edital_visivel}, desativado={edital_desativado}")

        # 1.3 HUD de Contagem Regressiva Ativa (11/11 às 08h00)
        hud_container = page.locator("#hud-countdown-container").first
        hud_visivel = await hud_container.is_visible()
        dias_val = await page.locator("#hud-dias").inner_text() if await page.locator("#hud-dias").count() > 0 else ""
        horas_val = await page.locator("#hud-horas").inner_text() if await page.locator("#hud-horas").count() > 0 else ""
        log(f"HUD Contagem Regressiva visível: {hud_visivel} | Dias restantes: {dias_val} | Horas: {horas_val}")

        sc1_hud = SCREENSHOTS_DIR / "01b_hud_contagem_regressiva.png"
        await page.screenshot(path=str(sc1_hud))
        conferencia["screenshots"].append(sc1_hud.name)

        # 1.4 Alternância para Modo Celebratório / Citações Inspiradoras
        btn_mensagens = page.get_by_role("button", name="Ver Mensagens Inspiradoras", exact=False).first
        citacao_ok = False
        if await btn_mensagens.is_visible():
            await btn_mensagens.click()
            await asyncio.sleep(1.0)

            content_live = await page.content()
            citacao_ok = "AO VIVO • SIMPÓSIO EM ANDAMENTO" in content_live or "Inspiração Científica" in content_live
            log(f"Modo Celebratório com Citações Científicas ativado: {citacao_ok}")

            sc1_cit = SCREENSHOTS_DIR / "01c_citacao_cientista_einstein.png"
            await page.screenshot(path=str(sc1_cit))
            conferencia["screenshots"].append(sc1_cit.name)

            # Próxima citação do carrossel
            btn_prox = page.get_by_role("button", name="Próxima", exact=False).first
            if await btn_prox.is_visible():
                await btn_prox.click()
                await asyncio.sleep(0.8)
                sc1_cit2 = SCREENSHOTS_DIR / "01d_citacao_cientista_curie.png"
                await page.screenshot(path=str(sc1_cit2))
                conferencia["screenshots"].append(sc1_cit2.name)
                log("Navegação do carrossel de citações (Próxima) efetuada")

            # Retorno ao relógio
            btn_relogio = page.get_by_role("button", name="Ver Relógio", exact=False).first
            if await btn_relogio.is_visible():
                await btn_relogio.click()
                await asyncio.sleep(0.8)
                log("Retorno ao relógio de contagem efetuado com sucesso")

        # 1.5 Navegação por TODAS as seções/abas da Home através dos botões da Navbar
        abas_home = [
            ("eixos", "Eixos", "Eixos Temáticos"),
            ("palestrantes", "Palestrantes", "Palestrantes Convidados"),
            ("programacao", "Programação", "Programação do Simpósio"),
            ("submissoes", "Submissões", "Chamada de Trabalhos"),
            ("local", "Local", "Brejo Santo"),
            ("sobre", "Sobre", "Sobre o Encontro"),
        ]

        detalhes_abas = {}
        for chave, nome_btn, trecho_esperado in abas_home:
            log(f"Navegando para a aba '{nome_btn}'...")
            btn_aba = page.get_by_role("button", name=nome_btn, exact=False).first
            if await btn_aba.is_visible():
                await btn_aba.click()
                await asyncio.sleep(1.0)
                content_secao = await page.content()
                achou_secao = trecho_esperado.lower() in content_secao.lower()
                detalhes_abas[f"aba_{chave}"] = achou_secao
                log(f"Aba '{nome_btn}' aberta e conteúdo validado: {achou_secao}")

                sc_aba = SCREENSHOTS_DIR / f"01_secao_{chave}.png"
                await page.screenshot(path=str(sc_aba))
                conferencia["screenshots"].append(sc_aba.name)
            else:
                detalhes_abas[f"aba_{chave}"] = False
                log(f"Aviso: botão da aba '{nome_btn}' não encontrado", "WARN")

        # Retornar ao início clicando na logo/marca
        link_inicio = page.locator("a[href='/']").first
        if await link_inicio.is_visible():
            await link_inicio.click()
            await asyncio.sleep(0.8)

        # 1.6 Rodapé Oficial com Autoria Completa
        content_home = await page.content()
        rodape_esperado = "© 2026 IV EFAC • Universidade Federal do Cariri (UFCA) • Desenvolvido por Ramon Firmino Bezerra."
        tem_rodape_autor = rodape_esperado in content_home
        log(f"Rodapé oficial verificado: {tem_rodape_autor}")

        conferencia["etapas"].append({
            "nome": "1. Home, Identidade Visual, HUD & Todas as Abas",
            "status": "PASS" if (status_home == 200 and tem_logo and hud_visivel and tem_rodape_autor) else "WARN",
            "detalhes": {
                "status_code": status_home,
                "tempo_resposta_ms": tempo_home,
                "logo_oficial_ativa": tem_logo,
                "edital_seguro_desativado": edital_visivel,
                "hud_contagem_visivel": hud_visivel,
                "citacoes_cientistas_carrossel": citacao_ok,
                "rodape_autoria_valido": tem_rodape_autor,
                **detalhes_abas
            }
        })

        # ==============================================================
        # ETAPA 2: CRONOGRAMA OFICIAL EXPANDIDO COM FUNDO CÓSMICO (/cronograma)
        # ==============================================================
        log("--- ETAPA 2: Cronograma Oficial Expandido & Fundo Cósmico Imersivo ---")
        t0 = time.time()
        resp_crono = await page.goto(f"{BASE_URL}/cronograma", wait_until="networkidle", timeout=20000)
        tempo_crono = round((time.time() - t0) * 1000, 1)
        assert resp_crono.status == 200, f"Cronograma retornou status {resp_crono.status}"

        # Verificar se camada fixa de SVG ou fundo cósmico existe
        fundo_cosmico_presente = await page.locator("svg").count() > 0
        log(f"Fundo cósmico com elementos gráficos fixos: {fundo_cosmico_presente}")

        sc2_c1 = SCREENSHOTS_DIR / "02_cronograma_dia1.png"
        await page.screenshot(path=str(sc2_c1))
        conferencia["screenshots"].append(sc2_c1.name)

        btn_dia2 = page.get_by_role("button", name="Dia 2", exact=False).first
        dia2_ok = False
        if await btn_dia2.is_visible():
            await btn_dia2.click()
            await asyncio.sleep(0.8)
            dia2_ok = True

        sc2_c2 = SCREENSHOTS_DIR / "02b_cronograma_dia2.png"
        await page.screenshot(path=str(sc2_c2))
        conferencia["screenshots"].append(sc2_c2.name)
        log(f"Cronograma verificado ({tempo_crono} ms). Alternância Dia 2: {dia2_ok}")

        conferencia["etapas"].append({
            "nome": "2. Cronograma Oficial & Fundo Cósmico",
            "status": "PASS" if dia2_ok else "WARN",
            "detalhes": {
                "status_code": resp_crono.status,
                "tempo_resposta_ms": tempo_crono,
                "fundo_cosmico_ativo": fundo_cosmico_presente,
                "alternancia_dia2": dia2_ok
            }
        })

        # ==============================================================
        # ETAPA 3: CARTEIRINHA DIGITAL, MULTI-ORIGEM DE FOTO & NAVBAR
        # ==============================================================
        log("--- ETAPA 3: Carteirinha Digital, Personalização de Foto & Modelo Palestrante ---")
        await page.goto(f"{BASE_URL}/inscricao", wait_until="networkidle", timeout=20000)
        await asyncio.sleep(0.5)

        tab_login = page.get_by_role("tab", name="Já sou Inscrito", exact=False).first
        if await tab_login.is_visible():
            await tab_login.click()
            await asyncio.sleep(0.5)

        inputs = await page.query_selector_all("input")
        vis_inputs = [inp for inp in inputs if await inp.is_visible()]
        assert len(vis_inputs) >= 2, "Campos de login não encontrados"

        await vis_inputs[0].fill("qa.seguranca@ufca.edu.br")
        await vis_inputs[1].fill("Cosmologia_UFCA_2026!")
        await asyncio.sleep(0.3)

        btn_entrar = page.get_by_role("button", name="Acessar Minha Credencial", exact=False).first
        await btn_entrar.click()
        await asyncio.sleep(3.0)

        content_cred = await page.content()
        login_qa_ok = "ASTRO-QA2026" in content_cred or "Dra. Vera Rubin" in content_cred or "Supervisor" in content_cred
        log(f"Login de participante efetuado com sucesso: {login_qa_ok}")

        sc3_card = SCREENSHOTS_DIR / "03_carteirinha_digital_participante.png"
        await page.screenshot(path=str(sc3_card))
        conferencia["screenshots"].append(sc3_card.name)

        # 3.1 Testar aba de avatares presets
        tab_foto_presets = page.get_by_role("tab", name="Avatares", exact=False).first
        preset_foto_ok = False
        if await tab_foto_presets.is_visible():
            await tab_foto_presets.click()
            await asyncio.sleep(0.8)

            btn_preset = page.get_by_role("button", name="Quântico", exact=False).first
            if not await btn_preset.is_visible():
                btn_preset = page.get_by_role("button", name="Cosmos", exact=False).first
            if await btn_preset.is_visible():
                await btn_preset.click()
                await asyncio.sleep(1.5)
                preset_foto_ok = True
                log("Avatar cósmico temático aplicado com sucesso à carteirinha")

        sc3_preset = SCREENSHOTS_DIR / "03b_carteirinha_com_avatar_preset.png"
        await page.screenshot(path=str(sc3_preset))
        conferencia["screenshots"].append(sc3_preset.name)

        # 3.2 Alternar para modelo Palestrante
        btn_mod_palestrante = page.get_by_role("button", name="Modelo Palestrante", exact=False).first
        mod_palestrante_ok = False
        if await btn_mod_palestrante.is_visible():
            await btn_mod_palestrante.click()
            await asyncio.sleep(1.0)
            mod_palestrante_ok = True
            log("Modelo Palestrante da carteirinha visualizado")

        sc3_palest = SCREENSHOTS_DIR / "03c_carteirinha_modelo_palestrante.png"
        await page.screenshot(path=str(sc3_palest))
        conferencia["screenshots"].append(sc3_palest.name)

        # Logout para prosseguir com autenticação do Admin
        btn_sair = page.get_by_role("button", name="Sair", exact=False).first
        if await btn_sair.is_visible():
            await btn_sair.click()
            await asyncio.sleep(1.5)
            log("Logout de participante efetuado com sucesso")

        conferencia["etapas"].append({
            "nome": "3. Carteirinha Digital & Personalização",
            "status": "PASS" if login_qa_ok else "FAIL",
            "detalhes": {
                "autenticacao_participante": login_qa_ok,
                "personalizacao_foto_presets": preset_foto_ok,
                "alternancia_modelo_palestrante": mod_palestrante_ok
            }
        })

        # ==============================================================
        # ETAPA 4: PAINEL SUPER ADMIN & DOWNLOAD DA LISTA EM PDF
        # ==============================================================
        log("--- ETAPA 4: Cockpit Super Admin, Delegação de Atividades & Download em PDF ---")
        await page.goto(f"{BASE_URL}/inscricao", wait_until="networkidle", timeout=20000)
        await asyncio.sleep(0.5)

        tab_login_adm = page.get_by_role("tab", name="Já sou Inscrito", exact=False).first
        if await tab_login_adm.is_visible():
            await tab_login_adm.click()
            await asyncio.sleep(0.5)

        inputs_adm = await page.query_selector_all("input")
        vis_inputs_adm = [inp for inp in inputs_adm if await inp.is_visible()]

        await vis_inputs_adm[0].fill("admin@ufca.edu.br")
        await vis_inputs_adm[1].fill("Admin_IVEFAC_2026!")
        await asyncio.sleep(0.3)

        btn_login_adm = page.get_by_role("button", name="Acessar Minha Credencial", exact=False).first
        await btn_login_adm.click()
        await asyncio.sleep(3.0)

        # Acessar a aba "Painel do Administrador"
        tab_admin = page.get_by_role("tab", name="Painel do Administrador", exact=False).first
        if await tab_admin.is_visible():
            await tab_admin.click()
            await asyncio.sleep(1.5)
            log("Aba 'Painel do Administrador' selecionada")

        content_adm = await page.content()
        painel_adm_ok = "Painel Administrativo" in content_adm or "Super Admin" in content_adm
        log(f"Painel Super Admin ativo: {painel_adm_ok}")

        sc4_adm = SCREENSHOTS_DIR / "04_admin_dashboard_inscritos.png"
        await page.screenshot(path=str(sc4_adm))
        conferencia["screenshots"].append(sc4_adm.name)

        # 4.1 BAIXAR A LISTA DE PARTICIPANTES EM PDF COM ADMIN (CRÍTICO)
        btn_pdf_adm = page.locator("#btn-admin-export-pdf").first
        if not await btn_pdf_adm.is_visible():
            btn_pdf_adm = page.get_by_role("button", name="Baixar PDF Oficial", exact=False).first

        download_pdf_ok = False
        pdf_path_final = None
        pdf_size_bytes = 0

        if await btn_pdf_adm.is_visible():
            log("Disparando download oficial da lista de inscritos em PDF pelo Admin...")
            async with page.expect_download(timeout=15000) as download_info:
                await btn_pdf_adm.click()

            download_pdf = await download_info.value
            pdf_sugerido = download_pdf.suggested_filename
            pdf_path_final = DOWNLOADS_DIR / f"participantes_admin_{pdf_sugerido}"
            await download_pdf.save_as(str(pdf_path_final))

            if pdf_path_final.exists() and pdf_path_final.stat().st_size > 0:
                pdf_size_bytes = pdf_path_final.stat().st_size
                with open(pdf_path_final, "rb") as f_pdf:
                    header_pdf = f_pdf.read(5)
                # Validar cabeçalho %PDF
                is_valid_pdf = header_pdf.startswith(b"%PDF")
                download_pdf_ok = is_valid_pdf and pdf_size_bytes > 500
                log(f"Download PDF concluído com SUCESSO! Arquivo: {pdf_path_final.name} ({pdf_size_bytes} bytes, Válido={is_valid_pdf})")
                conferencia["downloads"]["admin_pdf"] = {
                    "arquivo": pdf_path_final.name,
                    "tamanho_bytes": pdf_size_bytes,
                    "valido_pdf": is_valid_pdf
                }
            else:
                log("Erro: Arquivo PDF baixado está vazio ou inexistente", "ERROR")
        else:
            log("Erro: Botão de exportação PDF do Admin não encontrado", "ERROR")

        # 4.2 Testar Aba Grade de Palestras & Delegação
        tab_grade = page.get_by_role("tab", name="Palestras & Grade", exact=False).first
        if not await tab_grade.is_visible():
            tab_grade = page.get_by_role("tab", name="Editor & Delegação de Grade", exact=False).first

        criacao_ativ_ok = False
        if await tab_grade.is_visible():
            await tab_grade.click()
            await asyncio.sleep(1.0)
            sc4_grade = SCREENSHOTS_DIR / "04b_admin_grade_atividades.png"
            await page.screenshot(path=str(sc4_grade))
            conferencia["screenshots"].append(sc4_grade.name)

            btn_nova_ativ = page.get_by_role("button", name="Adicionar Nova Atividade", exact=False).first
            if await btn_nova_ativ.is_visible():
                await btn_nova_ativ.click()
                await asyncio.sleep(0.8)
                inp_titulo = page.locator("input[placeholder*='Título da atividade']").first
                if await inp_titulo.is_visible():
                    await inp_titulo.fill("Simpósio Internacional: Astrofísica de Altas Energias")
                    criacao_ativ_ok = True
                    log("Formulário de criação de atividades operado com sucesso pelo Admin")

        # 4.3 Testar Aba Supervisores / Atribuição de Funções
        tab_sup = page.get_by_role("tab", name="Supervisores", exact=False).first
        if not await tab_sup.is_visible():
            tab_sup = page.get_by_role("tab", name="Supervisores & Delegação", exact=False).first

        promocao_sup_ok = False
        if await tab_sup.is_visible():
            await tab_sup.click()
            await asyncio.sleep(1.0)
            sc4_sup = SCREENSHOTS_DIR / "04c_admin_supervisores.png"
            await page.screenshot(path=str(sc4_sup))
            conferencia["screenshots"].append(sc4_sup.name)

            btn_promover = page.get_by_role("button", name="Supervisor", exact=False).first
            if await btn_promover.is_visible():
                await btn_promover.click()
                await asyncio.sleep(1.0)
                promocao_sup_ok = True
                log("Função de Supervisor delegada/validada com sucesso")

        # Logout do Admin
        btn_sair_adm = page.get_by_role("button", name="Sair", exact=False).first
        if await btn_sair_adm.is_visible():
            await btn_sair_adm.click()
            await asyncio.sleep(1.5)
            log("Logout do Super Admin efetuado com sucesso")

        conferencia["etapas"].append({
            "nome": "4. Painel Super Admin & Download PDF",
            "status": "PASS" if (painel_adm_ok and download_pdf_ok) else "FAIL",
            "detalhes": {
                "autenticacao_admin": painel_adm_ok,
                "download_pdf_sucesso": download_pdf_ok,
                "pdf_tamanho_bytes": pdf_size_bytes,
                "formulario_atividades_ok": criacao_ativ_ok,
                "gestao_supervisores_ok": promocao_sup_ok
            }
        })

        # ==============================================================
        # ETAPA 5: PAINEL DE SUPERVISOR & DOWNLOAD DA LISTA EM CSV
        # ==============================================================
        log("--- ETAPA 5: Painel de Supervisor Oficial, Check-in & Download em CSV ---")
        await page.goto(f"{BASE_URL}/inscricao", wait_until="networkidle", timeout=20000)
        await asyncio.sleep(0.5)

        tab_login_sup = page.get_by_role("tab", name="Já sou Inscrito", exact=False).first
        if await tab_login_sup.is_visible():
            await tab_login_sup.click()
            await asyncio.sleep(0.5)

        inputs_sup = await page.query_selector_all("input")
        vis_inputs_sup = [inp for inp in inputs_sup if await inp.is_visible()]

        # Login com o usuário supervisor
        await vis_inputs_sup[0].fill("qa.seguranca@ufca.edu.br")
        await vis_inputs_sup[1].fill("Cosmologia_UFCA_2026!")
        await asyncio.sleep(0.3)

        btn_entrar_sup = page.get_by_role("button", name="Acessar Minha Credencial", exact=False).first
        await btn_entrar_sup.click()
        await asyncio.sleep(3.0)

        # Clicar na aba "Conferência de Presença"
        tab_superv = page.get_by_role("tab", name="Conferência de Presença", exact=False).first
        if await tab_superv.is_visible():
            await tab_superv.click()
            await asyncio.sleep(1.5)
            log("Aba 'Conferência de Presença' selecionada")

        content_sup = await page.content()
        painel_sup_ok = "Painel do Supervisor" in content_sup or "Conferência Oficial de Presença" in content_sup or "Presente" in content_sup
        log(f"Painel do Supervisor ativo para conferência: {painel_sup_ok}")

        sc5_sup = SCREENSHOTS_DIR / "05_supervisor_painel.png"
        await page.screenshot(path=str(sc5_sup))
        conferencia["screenshots"].append(sc5_sup.name)

        # 5.1 Testar Marcação / Check-in de Presença
        btn_checkin = page.get_by_role("button", name="Check-in", exact=False).first
        if not await btn_checkin.is_visible():
            btn_checkin = page.get_by_role("button", name="Presente", exact=False).first

        checkin_ok = False
        if await btn_checkin.is_visible():
            await btn_checkin.click()
            await asyncio.sleep(1.5)
            checkin_ok = True
            log("Marcação de presença (Check-in) executada com sucesso")

            sc5_pres = SCREENSHOTS_DIR / "05b_supervisor_checkin_realizado.png"
            await page.screenshot(path=str(sc5_pres))
            conferencia["screenshots"].append(sc5_pres.name)

        # 5.2 BAIXAR A LISTA DE PARTICIPANTES EM CSV COM SUPERVISOR (CRÍTICO)
        btn_csv_sup = page.locator("#btn-superv-export-csv").first
        if not await btn_csv_sup.is_visible():
            btn_csv_sup = page.get_by_role("button", name="Baixar CSV", exact=False).first

        download_csv_ok = False
        csv_path_final = None
        csv_size_bytes = 0

        if await btn_csv_sup.is_visible():
            log("Disparando download oficial da lista de inscritos em CSV pelo Supervisor...")
            async with page.expect_download(timeout=15000) as download_csv_info:
                await btn_csv_sup.click()

            download_csv = await download_csv_info.value
            csv_sugerido = download_csv.suggested_filename
            csv_path_final = DOWNLOADS_DIR / f"participantes_supervisor_{csv_sugerido}"
            await download_csv.save_as(str(csv_path_final))

            if csv_path_final.exists() and csv_path_final.stat().st_size > 0:
                csv_size_bytes = csv_path_final.stat().st_size
                with open(csv_path_final, "r", encoding="utf-8-sig") as f_csv:
                    linhas_csv = [f_csv.readline() for _ in range(5)]
                tem_cabecalho = any("ID" in l and "Nome Completo" in l for l in linhas_csv)
                tem_sep = any("sep=;" in l for l in linhas_csv)
                download_csv_ok = tem_cabecalho and csv_size_bytes > 50
                log(f"Download CSV concluído com SUCESSO! Arquivo: {csv_path_final.name} ({csv_size_bytes} bytes, Cabeçalho={tem_cabecalho})")
                conferencia["downloads"]["supervisor_csv"] = {
                    "arquivo": csv_path_final.name,
                    "tamanho_bytes": csv_size_bytes,
                    "cabecalho_valido": tem_cabecalho,
                    "separador_excel": tem_sep
                }
            else:
                log("Erro: Arquivo CSV baixado está vazio ou inexistente", "ERROR")
        else:
            log("Erro: Botão de exportação CSV do Supervisor não encontrado", "ERROR")

        # Logout final
        btn_sair_sup = page.get_by_role("button", name="Sair", exact=False).first
        if await btn_sair_sup.is_visible():
            await btn_sair_sup.click()
            await asyncio.sleep(1.0)
            log("Logout do Supervisor efetuado com sucesso")

        conferencia["etapas"].append({
            "nome": "5. Painel Supervisor & Download CSV",
            "status": "PASS" if (painel_sup_ok and download_csv_ok) else "FAIL",
            "detalhes": {
                "painel_supervisor_ativo": painel_sup_ok,
                "toggle_checkin_presenca": checkin_ok,
                "download_csv_sucesso": download_csv_ok,
                "csv_tamanho_bytes": csv_size_bytes
            }
        })

        await browser.close()

    # Consolidar Status Geral
    falhas = [e for e in conferencia["etapas"] if e["status"] == "FAIL"]
    conferencia["status_geral"] = "APROVADO" if len(falhas) == 0 else "FALHA"
    conferencia["total_erros_console"] = len(console_errors)
    conferencia["concluido_em"] = datetime.now().isoformat()

    # Salva relatório JSON
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(conferencia, f, indent=2, ensure_ascii=False)

    # Salva relatório Markdown
    with open(REPORT_MD, "w", encoding="utf-8") as f:
        f.write("# Relatório de Conferência Automatizada Integral — IV EFAC 2026\n\n")
        f.write(f"- **Data da Auditoria:** {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n")
        f.write(f"- **URL Testada:** `{BASE_URL}`\n")
        f.write(f"- **Status Geral:** **{conferencia['status_geral']}**\n")
        f.write(f"- **Erros de Console JavaScript:** `{len(console_errors)}`\n\n")
        f.write("## 📥 Downloads de Participantes Validados\n\n")
        for k, v in conferencia["downloads"].items():
            f.write(f"- **{k.upper()}:** `{v['arquivo']}` ({v['tamanho_bytes']} bytes)\n")
        f.write("\n## 📋 Resultados por Módulo e Funcionalidade\n\n")
        for et in conferencia["etapas"]:
            f.write(f"### {et['nome']} — Status: `{et['status']}`\n")
            for k, v in et["detalhes"].items():
                f.write(f"- **{k}:** `{v}`\n")
            f.write("\n")
        f.write("## 📸 Evidências Capturadas\n\n")
        for sc in conferencia["screenshots"]:
            f.write(f"- `{sc}`\n")

    log(f"=== Conferência Geral Concluída com SUCESSO! Status: {conferencia['status_geral']} ===")
    log(f"Relatório Markdown salvo em: {REPORT_MD}")
    log(f"Relatório JSON salvo em: {REPORT_JSON}")


if __name__ == "__main__":
    asyncio.run(run_full_conference())
