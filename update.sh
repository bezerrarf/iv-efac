#!/usr/bin/env bash
# ==============================================================================
# Script de Atualização Contínua com Testes Automatizados e Auto-Rollback
# Simpósio IV EFAC 2026 - Universidade Federal do Cariri (UFCA)
# ==============================================================================
# Funcionamento:
# 1. Executa a cada 24h (via cron) ou sob demanda.
# 2. Busca alterações no GitHub (origin/main) sem alterar a versão em produção.
# 3. Se for a mesma versão já em produção: encerra sem reiniciar nada.
# 4. Se houver nova versão:
#    - Executa backup preventivo do SQLite local.
#    - Aplica os novos commits temporariamente.
#    - Roda todos os testes automatizados (uv run pytest).
#    - Se todos passarem (100% green): efetiva a atualização e reinicia o serviço.
#    - Se algum teste falhar: desfaz imediatamente (rollback) e mantém a versão estável no ar.
# ==============================================================================

set -o pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRANCH="main"
LOG_FILE="${PROJECT_DIR}/update.log"
SERVICE_NAME="efac"

# Carrega ambiente do usuário (garante uv e python no PATH ao rodar pelo cron)
export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$msg"
    echo "$msg" >> "$LOG_FILE"
}

instalar_cron_24h() {
    local cron_cmd="0 3 * * * /bin/bash ${PROJECT_DIR}/update.sh >> ${LOG_FILE} 2>&1"
    
    # Verifica se já está instalado no crontab
    if crontab -l 2>/dev/null | grep -F "${PROJECT_DIR}/update.sh" > /dev/null; then
        echo "O agendamento automático de 24h já está ativo no crontab."
        crontab -l | grep -F "${PROJECT_DIR}/update.sh"
    else
        (crontab -l 2>/dev/null; echo "$cron_cmd") | crontab -
        echo "Agendamento automático de 24h instalado com sucesso!"
        echo "Execução diária programada para as 03:00 da madrugada:"
        echo "  $cron_cmd"
    fi
    exit 0
}

# Tratamento de flags
if [[ "${1:-}" == "--install-cron" ]]; then
    instalar_cron_24h
fi

cd "$PROJECT_DIR" || exit 1

log "======================================================================"
log "Iniciando verificação de versão do IV EFAC em: $PROJECT_DIR"

# 1. Busca alterações remotas
if ! git fetch origin "$BRANCH" --quiet; then
    log "[ERRO] Não foi possível conectar ao repositório remoto no GitHub."
    exit 1
fi

LOCAL_HASH=$(git rev-parse HEAD)
REMOTE_HASH=$(git rev-parse "origin/$BRANCH")

# 2. Compara se é a mesma versão de produção ou se há novidades
if [[ "$LOCAL_HASH" == "$REMOTE_HASH" ]]; then
    log "[INFO] A versão em produção já é a mais recente ($LOCAL_HASH)."
    log "[INFO] Nenhuma alteração detectada no GitHub. Nenhuma reinicialização necessária."
    exit 0
fi

log "[NOVIDADE] Nova versão detectada no GitHub!"
log "  -> Versão atual em produção: $LOCAL_HASH"
log "  -> Nova versão disponível:   $REMOTE_HASH"

# 3. Backup de segurança do banco de dados local antes de atualizar
if [[ -f "${PROJECT_DIR}/evento.db" ]]; then
    BACKUP_FILE="${PROJECT_DIR}/evento.db.bak_$(date +%Y%m%d_%H%M%S)"
    cp "${PROJECT_DIR}/evento.db" "$BACKUP_FILE"
    log "[BACKUP] Backup preventivo do banco criado: $(basename "$BACKUP_FILE")"
fi

# 4. Atualiza o código para testar a nova versão
PREV_COMMIT="$LOCAL_HASH"
if ! git merge --ff-only "origin/$BRANCH"; then
    log "[AVISO] Merge fast-forward direto não foi possível. Tentando pull padrão..."
    if ! git pull origin "$BRANCH" --no-rebase; then
        log "[ERRO CRÍTICO] Falha ao mesclar novos commits do GitHub. Abortando."
        exit 1
    fi
fi

# 5. Sincroniza dependências com uv
log "[SYNC] Sincronizando dependências com uv sync..."
if ! uv sync --quiet; then
    log "[ERRO] Falha ao sincronizar dependências da nova versão."
    git reset --hard "$PREV_COMMIT"
    exit 1
fi

# 6. BATERIA DE TESTES AUTOMATIZADOS PRÉ-REINICIALIZAÇÃO
log "[TESTES] Executando suíte completa de testes automatizados (pytest)..."
if uv run pytest; then
    log "------------------------------------------------------------------"
    log "[SUCESSO] Todos os testes passaram na nova versão!"
    log "[ATUALIZAÇÃO] Sistema atualizado com sucesso para: $REMOTE_HASH"

    # Reinicia o serviço se estiver rodando via systemd
    if command -v systemctl >/dev/null 2>&1 && systemctl is-active --quiet "$SERVICE_NAME"; then
        log "[RESTART] Reiniciando serviço $SERVICE_NAME via systemd..."
        sudo systemctl restart "$SERVICE_NAME"
        log "[RESTART] Serviço $SERVICE_NAME reiniciado com sucesso!"
    else
        log "[INFO] Serviço systemd '$SERVICE_NAME' não detectado ou inativo. Processo atualizado em disco."
    fi
    log "=================================================================="
    exit 0
else
    # 7. ROLLBACK IMEDIATO EM CASO DE FALHA DE QUALQUER TESTE
    log "------------------------------------------------------------------"
    log "[ALERTA CRÍTICO] A nova versão FALHOU nos testes automatizados!"
    log "[ROLLBACK] Revertendo imediatamente para o commit estável anterior ($PREV_COMMIT)..."
    
    git reset --hard "$PREV_COMMIT"
    uv sync --quiet
    
    log "[PROTEÇÃO] Rollback concluído. A produção continua rodando na versão estável anterior sem interrupções."
    log "=================================================================="
    exit 1
fi
