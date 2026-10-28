"""Controller responsável pelas informações e dados do IV EFAC (2026).
Encontro de Física e Astronomia do Cariri - UFCA / IFE.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any


@dataclass
class Atividade:
    horario: str
    titulo: str
    palestrante: str
    local: str
    tipo: str
    descricao: str
    tipo_color: str = "indigo"
    id: Optional[int] = None
    dia: str = "Dia 1"
    ordem: int = 0


@dataclass
class Palestrante:
    nome: str
    cargo: str
    instituicao: str
    especialidade: str
    topico: str = ""
    foto_placeholder: str = ""
    foto: str = ""


@dataclass
class EixoTematico:
    numero: int
    titulo: str
    subtitulo: str
    descricao: str
    cor: str
    icone: str
    tags: List[str] = field(default_factory=list)


@dataclass
class NormaSubmissao:
    modalidade: str
    duracao: str
    formato: str
    paginas: str
    publicacao: str
    criterios: List[str]


class EventoController:
    """Fornece dados e programações estruturadas para o IV EFAC."""

    INFO_EVENTO: Dict[str, str] = {
        "sigla": "IV EFAC",
        "nome": "IV Encontro de Física e Astronomia do Cariri",
        "tema": "Fronteiras da Física Contemporânea, Formação Científica e Integração Regional",
        "data_inicio": "2026-11-11",
        "data_fim": "2026-11-12",
        "datas_legiveis": "11 e 12 de Novembro de 2026",
        "dias_semana": "quarta e quinta-feira",
        "iso_inicio": "2026-11-11T08:00:00-03:00",
        "instituicao": "Universidade Federal do Cariri (UFCA)",
        "unidade": "Instituto de Formação de Educadores – IFE",
        "campus": "Campus Brejo Santo",
        "endereco": "Rua Olegário Emídio de Araújo, s/n - Centro, Brejo Santo - CE",
        "cidade": "Brejo Santo",
        "state": "CE",
        "fomento": "Fomento FUNCAP (Processo: CER-0264-00190.01.00/26)",
        "coordenacao_geral": "Prof. Dr. Edson Otoniel da Silva e Prof. Dr. André Flávio Gonçalves Silva",
        "coordenador": "Prof. Dr. Edson Otoniel da Silva e Prof. Dr. André Flávio Gonçalves Silva",
        "email_contato": "edson.otoniel@ufca.edu.br",
    }

    STATS = [
        {"valor": "2", "rotulo": "Dias de Imersão"},
        {"valor": "9", "rotulo": "Conferencistas Convidados"},
        {"valor": "100+", "rotulo": "Participantes Esperados"},
        {"valor": "Apresentações", "rotulo": "Orais e Painéis"},
    ]

    _cache_programacao: Dict[str, Tuple[float, List[Atividade]]] = {}
    CACHE_TTL_SEGUNDOS: float = 60.0  # 1 minuto de cache

    @classmethod
    def invalidar_cache_programacao(cls):
        """Invalida o cache em memória da programação oficial."""
        cls._cache_programacao.clear()

    @staticmethod
    def obter_programacao_padrao(dia: str) -> List[Atividade]:
        """Grade oficial padrão do IV EFAC com dados 100% fiéis aos banners oficiais."""
        programacoes = {
            "Dia 1": [
                Atividade(
                    horario="08:00 – 09:00",
                    titulo="Credenciamento de Participantes e Acolhimento",
                    palestrante="Comissão Organizadora e Recepção Acadêmica",
                    local="Hall de Entrada - Campus Brejo Santo",
                    tipo="Acolhimento",
                    descricao="Recepção presencial dos congressistas, entrega de credenciais e materiais do simpósio.",
                    tipo_color="violet",
                    dia="Dia 1",
                    ordem=1,
                ),
                Atividade(
                    horario="09:00 – 09:30",
                    titulo="Cerimônia Oficial de Abertura",
                    palestrante="UFCA / IFE / Comitê Científico",
                    local="Auditório Central - Campus Brejo Santo",
                    tipo="Sessão Solene",
                    descricao="Abertura oficial com a direção do IFE, coordenação do IV EFAC e representantes da FUNCAP.",
                    tipo_color="indigo",
                    dia="Dia 1",
                    ordem=2,
                ),
                Atividade(
                    horario="09:30 – 10:45",
                    titulo="Palestra Convidada: Da licenciatura à sala de aula: como dar continuidade à formação docente?",
                    palestrante="Profa. Dra. Eliane Angela Veit (UFRGS)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="A formação de professores pensada além de cursos com início e fim. Aborda a Teoria Social da Aprendizagem de Etienne Wenger, comunidades de prática e a articulação entre escola e universidade.",
                    tipo_color="cyan",
                    dia="Dia 1",
                    ordem=3,
                ),
                Atividade(
                    horario="10:45 – 11:30",
                    titulo="Coffee Break, Acolhimento e Sessão de Networking",
                    palestrante="Integração Acadêmica",
                    local="Espaço de Convivência IFE",
                    tipo="Intervalo Técnico",
                    descricao="Momento de conexão e articulação científica entre estudantes, professores e conferencistas convidados.",
                    tipo_color="gray",
                    dia="Dia 1",
                    ordem=4,
                ),
                Atividade(
                    horario="11:30 – 12:45",
                    titulo="Palestra Convidada: Sondando a gravidade quântica com astrofísica multimensageira e experimentos de bancada",
                    palestrante="Prof. Dr. Iarley Pereira Lobo (UFPB)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Aborda o problema da gravidade quântica, tentativas de detecção experimental de sua assinatura através de observáveis astrofísicos, física de altas energias e sistemas quânticos a baixas energias.",
                    tipo_color="sky",
                    dia="Dia 1",
                    ordem=5,
                ),
                Atividade(
                    horario="12:45 – 14:00",
                    titulo="Intervalo de Almoço",
                    palestrante="Livre",
                    local="Praça de Alimentação / Cidade Universitária",
                    tipo="Intervalo",
                    descricao="Pausa para refeição e descanso dos congressistas.",
                    tipo_color="gray",
                    dia="Dia 1",
                    ordem=6,
                ),
                Atividade(
                    horario="14:00 – 17:00",
                    titulo="Minicurso Oficial: Entre ondas e partículas: história, controvérsias e a construção da Física Quântica",
                    palestrante="Prof. Marcos Antonio Barros (UEPB)",
                    local="Salas Temáticas / Laboratório",
                    tipo="Minicurso",
                    descricao="Construção histórica da dualidade onda-partícula, quantização da luz em Einstein, ondas de De Broglie, complementaridade de Bohr, interferômetro de Mach-Zehnder e epistemologia para o ensino.",
                    tipo_color="teal",
                    dia="Dia 1",
                    ordem=7,
                ),
                Atividade(
                    horario="14:00 – 17:30",
                    titulo="Sessões Orais dos Inscritos (Bloco A): Apresentações de Trabalhos Submetidos",
                    palestrante="Pesquisadores e Estudantes Autores",
                    local="Salas Temáticas A1, A2 e A3",
                    tipo="Sessão Técnica",
                    descricao="Apresentação oral (15 minutos) de resumos expandidos submetidos e aprovados pelos comitês avaliadores.",
                    tipo_color="teal",
                    dia="Dia 1",
                    ordem=8,
                ),
                Atividade(
                    horario="17:30 – 18:00",
                    titulo="Intervalo Técnico",
                    palestrante="Livre",
                    local="Espaço IFE",
                    tipo="Intervalo Técnico",
                    descricao="Pausa para ajuste de áudio e recepção da conferência magna do dia.",
                    tipo_color="gray",
                    dia="Dia 1",
                    ordem=9,
                ),
                Atividade(
                    horario="18:00 – 19:30",
                    titulo="Palestra Convidada: A mecânica quântica e o nosso dia a dia: aspectos históricos e desenvolvimento tecnológico",
                    palestrante="Prof. Dr. César Lenzi (ITA)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Como a mecânica quântica faz parte de nosso cotidiano e interfere em diversos aspectos em nossa vida, revisitando a história, conceitos e tecnologias derivadas desta teoria fundamental.",
                    tipo_color="indigo",
                    dia="Dia 1",
                    ordem=10,
                ),
            ],
            "Dia 2": [
                Atividade(
                    horario="08:30 – 09:30",
                    titulo="Palestra Convidada: Da equação de Dirac à linha de 21 cm: um percurso didático da teoria relativística à radioastronomia",
                    palestrante="Prof. Dr. José Crisanto (UECE)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Percurso didático que conecta a equação de Dirac à linha de 21 cm do hidrogênio neutro, interação hiperfina e radioastronomia para investigar a distribuição do hidrogênio na Via Láctea.",
                    tipo_color="cyan",
                    dia="Dia 2",
                    ordem=11,
                ),
                Atividade(
                    horario="09:30 – 10:30",
                    titulo="Palestra Convidada: Do grafeno curvo aos Qubits: Um caminho para a computação quântica",
                    palestrante="Prof. Dr. Job Saraiva Furtado (UFCA)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Uso da curvatura no grafeno como recurso para a computação quântica: nanotorus de grafeno sob campos externos, ripples gaussianos e controle coerente de portas lógicas de dois qubits.",
                    tipo_color="teal",
                    dia="Dia 2",
                    ordem=12,
                ),
                Atividade(
                    horario="10:30 – 11:30",
                    titulo="Palestra Convidada: Buracos de Minhoca de Casca Fina: da Estabilidade às Assinaturas Ópticas",
                    palestrante="Prof. Jonathan A. Rebouças (IFCE)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Construção, estabilidade e propriedades ópticas de wormholes de casca fina em diferentes modelos de matéria e geometrias simétricas e assimétricas, com destaque para assinaturas observacionais.",
                    tipo_color="sky",
                    dia="Dia 2",
                    ordem=13,
                ),
                Atividade(
                    horario="11:30 – 12:30",
                    titulo="Palestra Convidada: Buracos negros coloridos na teoria de Yang-Mills logarítmica: soluções, termodinâmica e estrutura interna",
                    palestrante="Prof. Célio R. Muniz (UECE)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Buracos negros coloridos com cabelos não abelianos acoplados à teoria de Yang-Mills logarítmica com grupo SU(2), termodinâmica de Hawking e análise da estrutura interna.",
                    tipo_color="violet",
                    dia="Dia 2",
                    ordem=14,
                ),
                Atividade(
                    horario="12:30 – 14:00",
                    titulo="Intervalo de Almoço",
                    palestrante="Livre",
                    local="Praça de Alimentação",
                    tipo="Intervalo",
                    descricao="Pausa para almoço, descanso e recomposição dos participantes.",
                    tipo_color="gray",
                    dia="Dia 2",
                    ordem=15,
                ),
                Atividade(
                    horario="14:00 – 17:30",
                    titulo="Sessão Especial dos Estudantes: Exposição de Pôsteres Científicos e Apresentações Orais",
                    palestrante="Estudantes de Iniciação Científica e Pós-Graduação",
                    local="Hall Principal e Salas de Banca",
                    tipo="Sessão Especial",
                    descricao="Exposição de Pôsteres Científicos no Hall Principal e Sessão Oral de Iniciação Científica/Mestrado com Banca Avaliadora e premiação.",
                    tipo_color="indigo",
                    dia="Dia 2",
                    ordem=16,
                ),
                Atividade(
                    horario="17:30 – 18:00",
                    titulo="Intervalo Técnico",
                    palestrante="Livre",
                    local="Espaço IFE",
                    tipo="Intervalo Técnico",
                    descricao="Preparação técnica e recepção para a conferência magna de encerramento.",
                    tipo_color="gray",
                    dia="Dia 2",
                    ordem=17,
                ),
                Atividade(
                    horario="18:00 – 19:30",
                    titulo="Conferência Magna de Encerramento: Inteligência Artificial na Astrofísica: Modelagem Física e Inferência Bayesiana",
                    palestrante="Dr. Ronaldo Vieira Lobato (CBPF)",
                    local="Auditório Central",
                    tipo="Conferência Magna",
                    descricao="Redes neurais e machine learning em problemas atuais de astrofísica: matéria nuclear densa, estrelas de nêutrons, anãs brancas, pulsares, magnetares e quantificação de incertezas bayesianas.",
                    tipo_color="cyan",
                    dia="Dia 2",
                    ordem=18,
                ),
                Atividade(
                    horario="19:30 – 20:00",
                    titulo="Premiação de Melhores Trabalhos e Cerimônia Oficial de Encerramento",
                    palestrante="Coordenação Geral IV EFAC / UFCA",
                    local="Auditório Central",
                    tipo="Encerramento",
                    descricao="Divulgação dos trabalhos premiados, homenagens acadêmicas e encerramento oficial do simpósio.",
                    tipo_color="amber",
                    dia="Dia 2",
                    ordem=19,
                ),
            ],
        }
        return programacoes.get(dia, programacoes["Dia 1"])

    @classmethod
    def obter_programacao(cls, dia: str) -> List[Atividade]:
        """Busca programação do SQLite persistente via CQRS Query Repository com cache inteligente de 1 minuto."""
        now = time.time()
        if dia in cls._cache_programacao:
            ts, dados = cls._cache_programacao[dia]
            if now - ts < cls.CACHE_TTL_SEGUNDOS:
                return dados

        resultado = None
        try:
            from projeto_web.repositories.queries.atividade_queries import SQLiteAtividadeQueryRepository
            query_repo = SQLiteAtividadeQueryRepository()
            itens = query_repo.find_by_dia(dia)
            if itens:
                resultado = [
                    Atividade(
                        id=r.id,
                        dia=r.dia,
                        horario=r.horario,
                        titulo=r.titulo,
                        palestrante=r.palestrante,
                        local=r.local,
                        tipo=r.tipo,
                        descricao=r.descricao,
                        tipo_color=r.tipo_color,
                        ordem=r.ordem,
                    )
                    for r in itens
                ]
        except Exception:
            pass

        if not resultado:
            resultado = cls.obter_programacao_padrao(dia)

        cls._cache_programacao[dia] = (now, resultado)
        return resultado

    @staticmethod
    def obter_todas_atividades() -> List[Atividade]:
        """Retorna todas as atividades de todos os dias persistidas no banco via CQRS Query."""
        todas = []
        for dia in ["Dia 1", "Dia 2"]:
            todas.extend(EventoController.obter_programacao(dia))
        return todas

    @classmethod
    def atualizar_atividade(
        cls,
        id: int,
        dia: str,
        horario: str,
        titulo: str,
        palestrante: str,
        local: str,
        tipo: str,
        descricao: str,
    ) -> bool:
        """Permite ao administrador alterar datas, horários e temas diretamente no banco via CQRS Command."""
        try:
            from projeto_web.repositories.commands.atividade_commands import SQLiteAtividadeCommandRepository
            cmd_repo = SQLiteAtividadeCommandRepository()
            ok = cmd_repo.update_by_fields(
                id=id,
                dia=dia,
                horario=horario,
                titulo=titulo,
                palestrante=palestrante,
                local=local,
                tipo=tipo,
                descricao=descricao,
            )
            if ok:
                cls.invalidar_cache_programacao()
            return ok
        except Exception:
            return False

    @classmethod
    def adicionar_atividade(
        cls,
        dia: str,
        horario: str,
        titulo: str,
        palestrante: str,
        local: str,
        tipo: str,
        descricao: str,
    ) -> bool:
        """Permite ao administrador criar uma nova atividade via CQRS Command."""
        try:
            from projeto_web.models.atividade import AtividadeModel
            from projeto_web.repositories.commands.atividade_commands import SQLiteAtividadeCommandRepository
            from projeto_web.repositories.queries.atividade_queries import SQLiteAtividadeQueryRepository

            query_repo = SQLiteAtividadeQueryRepository()
            cmd_repo = SQLiteAtividadeCommandRepository()

            atividades_dia = query_repo.find_by_dia(dia)
            total_dia = len(atividades_dia)

            nova = AtividadeModel(
                dia=dia,
                horario=horario,
                titulo=titulo,
                palestrante=palestrante,
                local=local,
                tipo=tipo,
                descricao=descricao,
                ordem=total_dia + 1,
            )
            cmd_repo.create(nova)
            cls.invalidar_cache_programacao()
            return True
        except Exception:
            return False

    @classmethod
    def excluir_atividade(cls, id: int) -> bool:
        """Permite ao administrador excluir uma atividade da grade via CQRS Command."""
        try:
            from projeto_web.repositories.commands.atividade_commands import SQLiteAtividadeCommandRepository
            cmd_repo = SQLiteAtividadeCommandRepository()
            ok = cmd_repo.delete(id)
            if ok:
                cls.invalidar_cache_programacao()
            return ok
        except Exception:
            return False

    @classmethod
    def restaurar_programacao_padrao(cls) -> bool:
        """Restaura a grade de atividades para os valores originais via CQRS Command."""
        try:
            from projeto_web.models.atividade import AtividadeModel
            from projeto_web.repositories.commands.atividade_commands import SQLiteAtividadeCommandRepository

            cmd_repo = SQLiteAtividadeCommandRepository()
            cmd_repo.clear_all()

            ordem_counter = 1
            for dia in ["Dia 1", "Dia 2"]:
                padrao = cls.obter_programacao_padrao(dia)
                for p in padrao:
                    at = AtividadeModel(
                        dia=dia,
                        horario=p.horario,
                        titulo=p.titulo,
                        palestrante=p.palestrante,
                        local=p.local,
                        tipo=p.tipo,
                        descricao=p.descricao,
                        tipo_color=p.tipo_color,
                        ordem=ordem_counter,
                    )
                    cmd_repo.create(at)
                    ordem_counter += 1
            cls.invalidar_cache_programacao()
            return True
        except Exception:
            return False

    @staticmethod
    def obter_palestrantes() -> List[Palestrante]:
        return [
            Palestrante(
                nome="Prof. Dr. César Lenzi",
                cargo="Docente e Pesquisador Titular",
                instituicao="Instituto Tecnológico de Aeronáutica (ITA)",
                especialidade="A mecânica quântica e o nosso dia a dia",
                topico="Palestra Convidada (11/11 às 18:00) • A mecânica quântica e o nosso dia a dia: aspectos históricos e desenvolvimento tecnológico",
                foto="/participantes/cesar_lenzi.webp",
            ),
            Palestrante(
                nome="Dr. Ronaldo Vieira Lobato",
                cargo="Pesquisador Titular",
                instituicao="Centro Brasileiro de Pesquisas Físicas (CBPF)",
                especialidade="Inteligência Artificial na Astrofísica",
                topico="Conferência Magna (12/11 às 18:00) • Inteligência Artificial na Astrofísica: Modelagem Física e Inferência Bayesiana",
                foto="/participantes/ronaldo_lobato.webp",
            ),
            Palestrante(
                nome="Profa. Dra. Eliane Angela Veit",
                cargo="Docente e Pesquisadora Titular",
                instituicao="Universidade Federal do Rio Grande do Sul (UFRGS)",
                especialidade="Formação Docente e Ensino de Ciências",
                topico="Palestra Convidada (11/11 às 09:30) • Da licenciatura à sala de aula: como dar continuidade à formação docente?",
                foto="/participantes/eliane_angela.webp",
            ),
            Palestrante(
                nome="Prof. Dr. Iarley Pereira Lobo",
                cargo="Docente e Pesquisador",
                instituicao="Universidade Federal da Paraíba (UFPB)",
                especialidade="Gravidade Quântica e Astrofísica Multimensageira",
                topico="Palestra Convidada (11/11 às 11:30) • Sondando a gravidade quântica com astrofísica multimensageira e experimentos de bancada",
                foto="/participantes/iarley_lobo.webp",
            ),
            Palestrante(
                nome="Prof. Dr. José Crisanto",
                cargo="Docente e Pesquisador",
                instituicao="Universidade Estadual do Ceará (UECE)",
                especialidade="Teoria Relativística e Radioastronomia",
                topico="Palestra Convidada (12/11 às 08:30) • Da equação de Dirac à linha de 21 cm: um percurso didático da teoria relativística à radioastronomia",
                foto="/participantes/jose_crisanto.webp",
            ),
            Palestrante(
                nome="Prof. Dr. Job Saraiva Furtado",
                cargo="Docente e Pesquisador",
                instituicao="Universidade Federal do Cariri (UFCA)",
                especialidade="Grafeno Curvo e Computação Quântica",
                topico="Palestra Convidada (12/11 às 09:30) • Do grafeno curvo aos Qubits: Um caminho para a computação quântica",
                foto="/participantes/job_saraiva.webp",
            ),
            Palestrante(
                nome="Prof. Jonathan A. Rebouças",
                cargo="Docente e Pesquisador",
                instituicao="Instituto Federal do Ceará (IFCE)",
                especialidade="Buracos de Minhoca e Geometria Relativística",
                topico="Palestra Convidada (12/11 às 10:30) • Buracos de Minhoca de Casca Fina: da Estabilidade às Assinaturas Ópticas",
                foto="/participantes/jonathan_reboucas.webp",
            ),
            Palestrante(
                nome="Prof. Célio R. Muniz",
                cargo="Docente e Bolsista de Produtividade PQ-CNPq",
                instituicao="Universidade Estadual do Ceará (UECE)",
                especialidade="Gravitação, Buracos Negros e Yang-Mills",
                topico="Palestra Convidada (12/11 às 11:30) • Buracos negros coloridos na teoria de Yang-Mills logarítmica: soluções, termodinâmica e estrutura interna",
                foto="/participantes/celio_muniz.webp",
            ),
            Palestrante(
                nome="Prof. Marcos Antonio Barros",
                cargo="Docente e Pesquisador Titular",
                instituicao="Universidade Estadual da Paraíba (UEPB)",
                especialidade="História e Epistemologia da Física Quântica",
                topico="Minicurso Oficial (11/11 às 14:00) • Entre ondas e partículas: história, controvérsias e a construção da Física Quântica",
                foto="/participantes/marcos_barros.webp",
            ),
        ]

    @staticmethod
    def obter_eixos_tematicos() -> List[EixoTematico]:
        return [
            EixoTematico(
                numero=1,
                titulo="Astrofísica",
                subtitulo="Objetos Compactos e Cosmologia",
                descricao="Investigação da matéria sob densidades e pressões extremas, evolução estelar, pulsares, estrelas de nêutrons e anãs brancas.",
                cor="#103460",
                icone="disc",
                tags=["Astrofísica", "Pulsares", "Cosmologia"],
            ),
            EixoTematico(
                numero=2,
                titulo="Física Computacional",
                subtitulo="Simulações e Ciência de Dados",
                descricao="Aplicações de algoritmos de aprendizado de máquina, simulações numéricas avançadas e processamento de grandes levantamentos científicos.",
                cor="#2563EB",
                icone="cpu",
                tags=["Computação Científica", "Simulações", "Machine Learning"],
            ),
            EixoTematico(
                numero=3,
                titulo="Relatividade e Gravitação",
                subtitulo="Campos Fortes e Espaço-Tempo",
                descricao="Estudos de gravitação em regimes de campo forte, ondas gravitacionais, termodinâmica de buracos negros e geometria relativística.",
                cor="#00ADB5",
                icone="orbit",
                tags=["Relatividade", "Buracos Negros", "Gravitação"],
            ),
            EixoTematico(
                numero=4,
                titulo="Física Quântica",
                subtitulo="Fundamentos e Tecnologias Quânticas",
                descricao="Mecânica quântica fundamental, estados quânticos, grafeno curvo, qubits e tecnologias emergentes de computação quântica.",
                cor="#818CF8",
                icone="atom",
                tags=["Física Quântica", "Qubits", "Grafeno"],
            ),
            EixoTematico(
                numero=5,
                titulo="Ensino e Divulgação Científica",
                subtitulo="Formação Docente e Interiorização",
                descricao="Metodologias inovadoras de ensino, formação continuada de professores e popularização da astronomia em parceria com o Observatório Kariri.",
                cor="#059669",
                icone="graduation-cap",
                tags=["Ensino", "Divulgação", "Observatório Kariri"],
            ),
        ]

    # Alias de compatibilidade com testes anteriores
    @staticmethod
    def obter_dimensoes():
        eixos = EventoController.obter_eixos_tematicos()
        return [
            type(
                "DimensaoCompat",
                (),
                {
                    "slug": f"eixo-{e.numero}",
                    "nome": e.titulo,
                    "cor": e.cor,
                    "descricao": e.descricao,
                    "icone": e.icone,
                    "link": "/#eixos",
                    "badge_texto": "Saiba Mais",
                },
            )()
            for e in eixos
        ]

    @staticmethod
    def obter_normas_submissao() -> NormaSubmissao:
        return NormaSubmissao(
            modalidade="Apresentação Oral (15 minutos) ou Apresentação em Pôster/Painel",
            duracao="15 minutos (oral) ou 1 hora (sessão de painéis)",
            formato="Resumo Expandido em PDF",
            paginas="Até 2 páginas (incluindo introdução, metodologia, resultados, conclusões e referências)",
            publicacao="Anais do IV EFAC (Publicação oficial digital com registro ISBN/ISSN institucional)",
            criterios=[
                "Aderência temática aos eixos do evento",
                "Coerência metodológica e fundamentação teórica",
                "Rigor conceitual e precisão analítica",
                "Originalidade e contribuição científica ou pedagógica",
                "Clareza e conformidade da redação científica",
            ],
        )

    @staticmethod
    def obter_comite_institucional() -> Dict[str, Any]:
        return {
            "coordenacao_geral": "Prof. Dr. Edson Otoniel da Silva (UFCA) e Prof. Dr. André Flávio Gonçalves Silva (UFCA)",
            "comite_cientifico": [
                "Prof. Dr. Edson Otoniel da Silva (UFCA)",
                "Prof. Dr. Gilson Francisco de Oliveira Junior (UFCA)",
                "Prof. Dr. Tharcisyo Sá e Sousa Duarte (UFCA)",
            ],
            "instituicao_executora": "Universidade Federal do Cariri – UFCA (Instituto de Formação de Educadores – IFE)",
            "fomento": "Fundação Cearense de Apoio ao Desenvolvimento Científico e Tecnológico – Fomento FUNCAP / Governo do Estado do Ceará (Processo: CER-0264-00190.01.00/26)",
            "parceiros": [
                "ITA (Instituto Tecnológico de Aeronáutica)",
                "CBPF (Centro Brasileiro de Pesquisas Físicas)",
                "UFRGS (Universidade Federal do Rio Grande do Sul)",
                "UFPB (Universidade Federal da Paraíba)",
                "IFCE (Instituto Federal do Ceará)",
                "UECE (Universidade Estadual do Ceará)",
                "URCA (Universidade Regional do Cariri)",
                "Observatório Kariri",
            ],
        }
