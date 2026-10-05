import asyncio
import os
import sys
from playwright.async_api import async_playwright

BASE_URL = os.getenv("TARGET_URL", "http://localhost:3000")

async def test_nav_from_inscricao():
    print(f"=== TESTE DE INTERATIVIDADE E NAVEGAÇÃO A PARTIR DE /inscricao ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        console_errors = []
        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda exc: print(f"Page error: {exc}"))

        # 1. Acessar /inscricao diretamente
        print("1. Acessando /inscricao...")
        await page.goto(f"{BASE_URL}/inscricao", wait_until="networkidle", timeout=30000)
        assert "/inscricao" in page.url
        print(f"   URL atual: {page.url}")

        # 2. Testar alternância de abas em /inscricao (Nova Inscrição vs Já sou Inscrito)
        print("2. Testando alternância entre abas de Cadastro e Login...")
        tab_login = page.get_by_role("tab", name="Já sou Inscrito", exact=False).first
        await tab_login.click()
        await asyncio.sleep(0.5)
        btn_login = page.get_by_role("button", name="Acessar Minha Credencial", exact=False).first
        assert await btn_login.is_visible(), "Formulário de login não ficou visível"
        print("   -> Aba 'Já sou Inscrito' ativada com sucesso.")

        tab_cad = page.get_by_role("tab", name="Nova Inscrição", exact=False).first
        await tab_cad.click()
        await asyncio.sleep(0.5)
        btn_cad = page.get_by_role("button", name="Confirmar Inscrição Gratuita", exact=False).first
        assert await btn_cad.is_visible(), "Formulário de cadastro não ficou visível"
        print("   -> Aba 'Nova Inscrição' reativada com sucesso.")

        # 3. Testar clique em 'Eixos' no navbar enquanto em /inscricao
        print("3. Testando clique em 'Eixos' no navbar a partir de /inscricao...")
        btn_eixos = page.get_by_role("button", name="Eixos", exact=False).first
        await btn_eixos.click()
        await asyncio.sleep(1.5)
        print(f"   URL após clique em Eixos: {page.url}")
        content = await page.content()
        assert "Astrofísica de Altas Energias" in content or "Relatividade Geral" in content, "Palco de Eixos não foi renderizado"
        print("   -> Navegação para Eixos a partir de /inscricao funcionou perfeitamente!")

        # 4. Voltar para /inscricao e testar clique em 'Palestrantes'
        print("4. Testando clique em 'Palestrantes' no navbar a partir de /inscricao...")
        await page.goto(f"{BASE_URL}/inscricao", wait_until="networkidle", timeout=20000)
        btn_palestrantes = page.get_by_role("button", name="Palestrantes", exact=False).first
        await btn_palestrantes.click()
        await asyncio.sleep(1.5)
        print(f"   URL após clique em Palestrantes: {page.url}")
        content = await page.content()
        assert "Palestrantes Convidados" in content or "Keynotes" in content, "Palco de Palestrantes não foi renderizado"
        print("   -> Navegação para Palestrantes a partir de /inscricao funcionou perfeitamente!")

        # 5. Voltar para /inscricao e testar clique no Logo IV EFAC
        print("5. Testando clique na Logo IV EFAC a partir de /inscricao...")
        await page.goto(f"{BASE_URL}/inscricao", wait_until="networkidle", timeout=20000)
        logo_link = page.locator("a[href='/']").first
        await logo_link.click()
        await asyncio.sleep(1.5)
        print(f"   URL após clique na Logo: {page.url}")
        content = await page.content()
        assert "CONTAGEM REGRESSIVA PARA ABERTURA" in content or "IV EFAC" in content
        print("   -> Clique na Logo retornou à Home perfeitamente!")

        # 6. Testar login e ações interativas de credencial
        print("6. Testando login e alternâncias no Crachá...")
        await page.goto(f"{BASE_URL}/inscricao", wait_until="networkidle", timeout=20000)
        tab_login = page.get_by_role("tab", name="Já sou Inscrito", exact=False).first
        await tab_login.click()
        await asyncio.sleep(0.5)

        inputs = await page.query_selector_all("input")
        vis_inputs = [inp for inp in inputs if await inp.is_visible()]
        await vis_inputs[0].fill("qa.seguranca@ufca.edu.br")
        await vis_inputs[1].fill("Cosmologia_UFCA_2026!")
        await asyncio.sleep(0.2)

        btn_entrar = page.get_by_role("button", name="Acessar Minha Credencial", exact=False).first
        await btn_entrar.click()
        await asyncio.sleep(2.0)

        content = await page.content()
        assert "ASTRO-QA2026" in content, "Login de participante QA falhou"
        print("   -> Login realizado com sucesso!")

        # Alternar modo palestrante no crachá
        btn_modo_palestrante = page.get_by_role("button", name="Modelo Palestrante", exact=False).first
        if await btn_modo_palestrante.is_visible():
            await btn_modo_palestrante.click()
            await asyncio.sleep(0.8)
            print("   -> Alternância para 'Modelo Palestrante' funcionou perfeitamente!")

        btn_modo_part = page.get_by_role("button", name="Visualizar como Participante", exact=False).first
        if await btn_modo_part.is_visible():
            await btn_modo_part.click()
            await asyncio.sleep(0.8)
            print("   -> Alternância para 'Visualizar como Participante' funcionou perfeitamente!")

        # Logout
        btn_sair = page.get_by_role("button", name="Sair", exact=False).first
        if await btn_sair.is_visible():
            await btn_sair.click()
            await asyncio.sleep(1.0)
            print("   -> Logout executado com sucesso!")

        await browser.close()

    print("\n✅ TODOS OS TESTES DE INTERATIVIDADE E NAVEGAÇÃO PASSARAM COM SUCESSO!")
    if console_errors:
        print(f"Avisos de console: {len(console_errors)}")

if __name__ == "__main__":
    asyncio.run(test_nav_from_inscricao())
