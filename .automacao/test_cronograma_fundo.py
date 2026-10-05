import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

BASE_URL = os.getenv("TARGET_URL", "http://localhost:3000")
BASE_DIR = Path("/home/ramon_bezerra/Projects/Python_Lang/Projeto Web")
SCREENSHOTS_DIR = BASE_DIR / ".automacao" / "screenshots_conferencia"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

async def test_cronograma_background():
    print("=== TESTE DE CONSISTÊNCIA VISUAL DO FUNDO CÓSMICO EM /cronograma ===")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # 1. Acessar /cronograma
        print("1. Acessando /cronograma...")
        resp = await page.goto(f"{BASE_URL}/cronograma", wait_until="networkidle", timeout=30000)
        assert resp.status == 200, f"Status retornado: {resp.status}"

        # 2. Verificar presença do SVG do Fundo Cósmico
        fundo_img = await page.query_selector("svg image[href*='fundo_cosmico.jpeg']")
        assert fundo_img is not None, "Imagem base do fundo cósmico (/fundo_cosmico.jpeg) não foi encontrada no SVG!"
        print("   -> Fundo Cósmico Vetorial ('/fundo_cosmico.jpeg') detectado com sucesso!")

        # 3. Capturar evidência da Grade Dia 1 com Fundo Cósmico
        sc_dia1 = SCREENSHOTS_DIR / "cronograma_dia1_fundo_cosmico.png"
        await page.screenshot(path=str(sc_dia1))
        print(f"   -> Screenshot salvo em: {sc_dia1.name}")

        # 4. Alternar para Dia 2
        print("2. Alternando para Dia 2...")
        btn_dia2 = page.get_by_role("button", name="Dia 2", exact=False).first
        await btn_dia2.click()
        await asyncio.sleep(0.8)

        sc_dia2 = SCREENSHOTS_DIR / "cronograma_dia2_fundo_cosmico.png"
        await page.screenshot(path=str(sc_dia2))
        print(f"   -> Screenshot Dia 2 salvo em: {sc_dia2.name}")

        # 5. Scroll na grade para validar fixação do fundo
        print("3. Validando rolagem suave e permanência fixa do fundo...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(0.5)

        sc_scroll = SCREENSHOTS_DIR / "cronograma_scroll_fundo_fixo.png"
        await page.screenshot(path=str(sc_scroll))
        print(f"   -> Screenshot com rolagem salvo em: {sc_scroll.name}")

        # 6. Testar navegação do Navbar de volta à Home
        print("4. Testando retorno à Home a partir de /cronograma...")
        btn_eixos = page.get_by_role("button", name="Eixos", exact=False).first
        await btn_eixos.click()
        await asyncio.sleep(1.2)
        assert page.url.rstrip("/") == BASE_URL.rstrip("/"), f"URL esperada {BASE_URL}, obtida: {page.url}"
        print("   -> Navegação do Navbar para a Home funcionou com sucesso!")

        await browser.close()

    print("\n✅ TESTE DE CONSISTÊNCIA DO FUNDO CÓSMICO EM /cronograma PASSOU COM 100% DE SUCESSO!")

if __name__ == "__main__":
    asyncio.run(test_cronograma_background())
