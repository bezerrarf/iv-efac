"""Configuração da engine do banco de dados SQLite, migrações e sessões."""

from sqlmodel import Session, SQLModel, create_engine, select
from projeto_web.core.config import DATABASE_URL
from projeto_web.models.usuario import Usuario
from projeto_web.models.atividade import AtividadeModel
from projeto_web.models.configuracao import ConfiguracaoModel
from projeto_web.core.security import PBKDF2PasswordHasher

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def _exec_migration(engine_instance):
    """Executa migrações não-destrutivas de schema no SQLite."""
    with engine_instance.connect() as conn:
        try:
            cursor = conn.exec_driver_sql("PRAGMA table_info(usuario);")
            cols = [row[1] for row in cursor.fetchall()]
            if cols:
                if "role" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN role VARCHAR DEFAULT 'participante';")
                if "foto_url" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN foto_url VARCHAR;")
                if "presenca_confirmada" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN presenca_confirmada BOOLEAN DEFAULT 0;")
                if "presenca_dia1" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN presenca_dia1 BOOLEAN DEFAULT 0;")
                if "presenca_dia2" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN presenca_dia2 BOOLEAN DEFAULT 0;")
                if "email_confirmado" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN email_confirmado BOOLEAN DEFAULT 0;")
                if "codigo_confirmacao" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN codigo_confirmacao VARCHAR;")
                if "codigo_confirmacao_hash" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN codigo_confirmacao_hash VARCHAR;")
                if "codigo_expira_em" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN codigo_expira_em TIMESTAMP;")
                if "codigo_tentativas" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN codigo_tentativas INTEGER DEFAULT 0;")
                if "codigo_enviado_em" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN codigo_enviado_em TIMESTAMP;")
                if "email_confirmado_em" not in cols:
                    conn.exec_driver_sql("ALTER TABLE usuario ADD COLUMN email_confirmado_em TIMESTAMP;")
        except Exception:
            pass


def _seed_admin_and_schedule():
    """Garante a existência do usuário administrador padrão e da grade de programação inicial."""
    hasher = PBKDF2PasswordHasher()
    with Session(engine) as session:
        # 1. Admin Único do Evento
        admin_email = "admin@ufca.edu.br"
        stmt_admin = select(Usuario).where(Usuario.email == admin_email)
        admin = session.exec(stmt_admin).first()
        if not admin:
            novo_admin = Usuario(
                nome="Coordenação Geral IV EFAC",
                email=admin_email,
                instituicao="Universidade Federal do Cariri (UFCA)",
                modalidade="Presencial",
                area="Comissão Organizadora",
                senha_hash=hasher.hash("Admin_IVEFAC_2026!"),
                codigo_inscricao="ADMIN-001",
                role="admin",
                presenca_confirmada=True,
                presenca_dia1=True,
                presenca_dia2=True,
                email_confirmado=True,
            )
            session.add(novo_admin)
            session.commit()
        else:
            changed = False
            if admin.role != "admin":
                admin.role = "admin"
                changed = True
            if not getattr(admin, "email_confirmado", False):
                admin.email_confirmado = True
                changed = True
            if changed:
                session.add(admin)
                session.commit()

        # 2. Grade de Programação Inicial
        stmt_ativ = select(AtividadeModel)
        total_ativ = len(session.exec(stmt_ativ).all())
        if total_ativ == 0:
            from projeto_web.controllers.evento_controller import EventoController
            ordem_counter = 1
            for dia in ["Dia 1", "Dia 2"]:
                itens = EventoController.obter_programacao_padrao(dia)
                for item in itens:
                    at_model = AtividadeModel(
                        dia=dia,
                        horario=item.horario,
                        titulo=item.titulo,
                        palestrante=item.palestrante,
                        local=item.local,
                        tipo=item.tipo,
                        descricao=item.descricao,
                        tipo_color=item.tipo_color,
                        ordem=ordem_counter,
                    )
                    session.add(at_model)
                    ordem_counter += 1
            session.commit()

        # 3. Links Oficiais dos Modelos de Submissão
        links_oficiais = {
            "link_modelo_resumo": "https://docs.google.com/document/d/1tp2I660zIwhE8SpjEmeSdNa4aGOx5TAN/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true",
            "link_modelo_slides": "https://docs.google.com/presentation/d/1iUEyNN3E_IglPo508DiXv8wOgi9emzqJ/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true",
            "link_modelo_poster": "https://docs.google.com/presentation/d/1p12rVh3LbCWgHostLjOYgxG1Z0tpk1qc/edit?usp=drive_link&ouid=107036139512820297420&rtpof=true&sd=true",
        }
        placeholder_antigo = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
        for chave, url_oficial in links_oficiais.items():
            cfg = session.get(ConfiguracaoModel, chave)
            if not cfg:
                session.add(ConfiguracaoModel(chave=chave, valor=url_oficial))
            elif placeholder_antigo in cfg.valor or not cfg.valor.strip():
                cfg.valor = url_oficial
                session.add(cfg)
        session.commit()


def init_db():
    """Cria tabelas, habilita o modo WAL no SQLite e executa migrações/seeds."""
    SQLModel.metadata.create_all(engine)
    if "sqlite" in DATABASE_URL:
        with engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
            conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")
        _exec_migration(engine)
    _seed_admin_and_schedule()


def get_session() -> Session:
    """Retorna uma nova sessão do banco de dados."""
    return Session(engine)
