# 🪐 AstroData 2026 • Simpósio Brasileiro de Astronomia & Ciência de Dados

Aplicação web full-stack desenvolvida em **Python puro** com **Reflex**, estruturada segundo a arquitetura **MVC (Model-View-Controller)**, com estrita observância aos princípios **SOLID**, persistência em **SQLite (modo WAL)** e suíte de testes unitários e de integração desenvolvidos via **TDD**.

---

## 🏛️ Arquitetura do Projeto (MVC + SOLID)

```
projeto-web/
├── pyproject.toml                     # Dependências e configuração do uv e pytest
├── rxconfig.py                        # Configurações do Reflex e temas Radix
├── evento.db                          # Banco de dados SQLite com WAL mode
│
├── tests/                             # Suíte de Testes (TDD)
│   ├── conftest.py                    # Fixtures e InMemoryUsuarioRepository (LSP/DIP)
│   ├── unit/
│   │   ├── test_security.py           # Testes do serviço de hash de senhas
│   │   ├── test_repository.py         # Testes do contrato de repositório
│   │   └── test_usuario_controller.py # Testes do Controller com injeção de dependência
│   └── integration/
│       └── test_sqlite_integration.py # Testes com SQLite real e transações concorrentes
│
└── projeto_web/
    ├── projeto_web.py                 # Ponto de entrada (registro de rotas e metadata)
    │
    ├── core/                          # Serviços de Infraestrutura Transversal
    │   ├── config.py                  # Constantes e URLs de configuração
    │   └── security.py                # Contrato e implementação PBKDF2 (SRP / DIP)
    │
    ├── models/                        # [M] MODEL: Entidades de Domínio
    │   └── usuario.py                 # Entidade Usuario (SQLModel / Pydantic)
    │
    ├── repositories/                  # Camada de Acesso a Dados (DAO / Repository)
    │   ├── base.py                    # Protocolo abstrato UsuarioRepositoryProtocol (ISP / DIP)
    │   ├── database.py                # Engine SQLite e ativação do modo WAL
    │   └── sqlite_usuario.py          # Implementação concreta do repositório SQLite (LSP)
    │
    ├── controllers/                   # [C] CONTROLLER: Casos de Uso e Regras de Negócio
    │   ├── usuario_controller.py      # Orquestração de cadastro, login e modalidade (SRP / DIP)
    │   └── evento_controller.py       # Programação, trilhas e palestrantes
    │
    ├── state/                         # Adaptador Reativo para o Reflex
    │   └── evento_state.py            # Consome os Controllers e sincroniza o estado da UI
    │
    └── views/                         # [V] VIEW: Apresentação e Componentes Visuais
        ├── components/
        │   ├── navbar.py              # Barra de navegação cósmica com glassmorphism
        │   └── footer.py              # Rodapé institucional
        └── pages/
            ├── home.py                # Página Inicial (Hero, estatísticas, tópicos)
            ├── cronograma.py          # Grade de atividades com filtro por dia
            └── inscricao.py           # Inscrição, Login e Credencial do Participante
```

---

## 🎯 Aplicação dos Princípios SOLID

1. **S - Single Responsibility Principle (SRP):**
   - Cada módulo possui um foco exclusivo: `security.py` lida apenas com criptografia; `sqlite_usuario.py` lida apenas com SQL; `usuario_controller.py` lida exclusivamente com regras de validação e negócios; `views` cuidam unicamente da apresentação.
2. **O - Open/Closed Principle (OCP):**
   - O repositório e o serviço de hash de senhas são desacoplados por `Protocols`. Para migrar de SQLite para PostgreSQL ou Turso, nenhuma linha do `UsuarioController` precisa ser alterada.
3. **L - Liskov Substitution Principle (LSP):**
   - O `InMemoryUsuarioRepository` usado nos testes unitários e o `SQLiteUsuarioRepository` usado em produção implementam o mesmo contrato e são intercambiáveis sem quebrar o sistema.
4. **I - Interface Segregation Principle (ISP):**
   - Contratos coesos e segregados (`UsuarioRepositoryProtocol`, `PasswordHasherProtocol`), evitando interfaces infladas com métodos desnecessários.
5. **D - Dependency Inversion Principle (DIP):**
   - O `UsuarioController` recebe suas dependências via construtor (`__init__`), dependendo exclusivamente de abstrações e não de implementações concretas de baixo nível.

---

## 🚀 Como Executar

### 1. Rodar os Testes Automatizados (TDD)
```powershell
uv run pytest tests/ -v
```

### 2. Iniciar o Servidor Web Local (Preview / Produção)
```powershell
uv run reflex run --env preview
```
Acesse: 👉 **http://localhost:3000**
