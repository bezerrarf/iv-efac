# Registro de Automação, Comandos e Processo do Sistema

Este documento foi gerado automaticamente pela suíte de auditoria baseada em **Playwright**, inspecionando todo o ecossistema do **IV EFAC 2026**.

## 1. Linhas de Comando Utilizadas

```bash
# 1. Instalação do Playwright e Navegador Chromium no WSL2
uv add playwright
uv run playwright install chromium

# 2. Execução da Automação de Varredura e Auditoria E2E
uv run python .automacao/varredura_playwright.py

# 3. Inspeção do Log de Execução em Tempo Real
cat .automacao/processo_execucao.log

# 4. Consulta ao Relatório Estruturado de Auditoria
cat .automacao/relatorio_auditoria.json
```

## 2. Etapas do Processo de Varredura

1. **Varredura de Rotas e Telas Reativas:**
   - `GET /`: Status 200 (Home com Canvas dinâmico e telemetria).
   - Seções inspecionadas: Eixos, Palestrantes, Programação, Submissões, Local e Sobre.
   - `GET /cronograma`: Status 200 (Grade horária expandida de 2 dias).

2. **Criação de Conta / Cadastro de Teste:**
   - Geração de participante com carimbo de tempo único.
   - Envio do formulário via WebSocket / Reflex State.
   - Criptografia de senha com salt PBKDF2 e código gerado `ASTRO-XXXXXX`.

3. **Autenticação / Login:**
   - Login realizado na aba 'Já sou Inscrito'.
   - Renderização da Credencial Digital Oficial com código de check-in.

4. **Auditoria de Banco de Dados:**
   - Arquivo: `evento.db` em modo WAL (`journal_mode=WAL`).
   - Total de Inscritos: 12 registros recentes validados.

## 3. Screenshots Geradas na Varredura

- `.automacao/screenshots/01_home_inicio.png`
- `.automacao/screenshots/02_home_eixos.png`
- `.automacao/screenshots/03_home_palestrantes.png`
- `.automacao/screenshots/04_home_programacao.png`
- `.automacao/screenshots/05_home_submissoes.png`
- `.automacao/screenshots/06_home_local.png`
- `.automacao/screenshots/07_home_sobre.png`
- `.automacao/screenshots/08_cronograma_expandido.png`
- `.automacao/screenshots/09_portal_inscricao.png`
- `.automacao/screenshots/10_formulario_preenchido.png`
- `.automacao/screenshots/11_pos_cadastro.png`
- `.automacao/screenshots/13_modalidade_alternada.png`
