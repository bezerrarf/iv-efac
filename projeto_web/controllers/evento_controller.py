"""Controller responsável pelas informações e dados do IV EFAC (2026).
Encontro de Física e Astronomia do Cariri - UFCA / IFE.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Atividade:
    horario: str
    titulo: str
    palestrante: str
    local: str
    tipo: str
    descricao: str
    tipo_color: str = "indigo"


@dataclass
class Palestrante:
    nome: str
    cargo: str
    instituicao: str
    especialidade: str
    topico: str = ""
    foto_placeholder: str = ""


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
        "fomento": "FUNCAP – Edital 03/2026 (Processo: CER-0264-00190.01.00/26)",
        "coordenacao_geral": "Prof. Dr. Edson Otoniel da Silva e Prof. Dr. André Flávio Gonçalves Silva",
        "coordenador": "Prof. Dr. Edson Otoniel da Silva e Prof. Dr. André Flávio Gonçalves Silva",
        "email_contato": "edson.otoniel@ufca.edu.br",
    }

    STATS = [
        {"valor": "2", "rotulo": "Dias de Imersão"},
        {"valor": "6", "rotulo": "Conferencistas Convidados"},
        {"valor": "100+", "rotulo": "Participantes Esperados"},
        {"valor": "Anais", "rotulo": "Publicação Oficial"},
    ]

    @staticmethod
    def obter_programacao(dia: str) -> List[Atividade]:
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
                ),
                Atividade(
                    horario="09:00 – 09:30",
                    titulo="Cerimônia Oficial de Abertura",
                    palestrante="UFCA / IFE / Comitê Científico",
                    local="Auditório Central - Campus Brejo Santo",
                    tipo="Sessão Solene",
                    descricao="Abertura oficial com a direção do IFE, coordenação do IV EFAC e representantes da FUNCAP.",
                    tipo_color="indigo",
                ),
                Atividade(
                    horario="09:30 – 10:30",
                    titulo="Palestra Convidada 1: Educação Científica e Ensino de Física",
                    palestrante="Profa. Dra. Eliane Angela Veit (UFRGS)",
                    local="Auditório Central",
                    tipo="Palestra de Abertura",
                    descricao="Inovação, epistemologia, metodologias ativas e formação científica de qualidade no ensino contemporâneo.",
                    tipo_color="cyan",
                ),
                Atividade(
                    horario="10:30 – 11:00",
                    titulo="Coffee Break, Acolhimento e Sessão de Networking",
                    palestrante="Integração Acadêmica",
                    local="Espaço de Convivência IFE",
                    tipo="Intervalo Técnico",
                    descricao="Momento de conexão e articulação científica entre estudantes, professores e conferencistas.",
                    tipo_color="gray",
                ),
                Atividade(
                    horario="11:00 – 12:30",
                    titulo="Palestra Convidada 2: Astrofísica Teórica e Objetos Compactos",
                    palestrante="Prof. Dr. Iarley Lobato (UFPB)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Estrutura e física da matéria sob densidades e pressões extremas: evolução estelar, pulsares e estrelas de nêutrons.",
                    tipo_color="sky",
                ),
                Atividade(
                    horario="12:30 – 14:00",
                    titulo="Intervalo de Almoço",
                    palestrante="Livre",
                    local="Praça de Alimentação / Cidade Universitária",
                    tipo="Intervalo",
                    descricao="Pausa para refeição e descanso dos congressistas.",
                    tipo_color="gray",
                ),
                Atividade(
                    horario="14:00 – 17:30",
                    titulo="Sessões Orais dos Inscritos (Bloco A): Apresentações de Trabalhos Submetidos",
                    palestrante="Pesquisadores e Estudantes Autores",
                    local="Salas Temáticas A1, A2 e A3",
                    tipo="Sessão Técnica",
                    descricao="Apresentação oral (15 minutos) de resumos expandidos submetidos e aprovados pelos comitês avaliadores.",
                    tipo_color="teal",
                ),
                Atividade(
                    horario="17:30 – 18:00",
                    titulo="Intervalo Técnico",
                    palestrante="Livre",
                    local="Espaço IFE",
                    tipo="Intervalo Técnico",
                    descricao="Pausa para ajuste de áudio e recepção da conferência magna.",
                    tipo_color="gray",
                ),
                Atividade(
                    horario="18:00 – 19:15",
                    titulo="Plenária Magna do Dia 1: Astrofísica de Altas Energias e Matéria Densa",
                    palestrante="Prof. Dr. Cesar Lenzi (ITA - São José dos Campos)",
                    local="Auditório Central",
                    tipo="Plenária Magna",
                    descricao="Astrofísica de altas energias, objetos ultradensos, processos de radiação e física de fronteira.",
                    tipo_color="indigo",
                ),
            ],
            "Dia 2": [
                Atividade(
                    horario="08:30 – 10:15",
                    titulo="Sessões Orais dos Inscritos (Bloco B): Comunicações Científicas e de Ensino",
                    palestrante="Apresentadores Aprovados",
                    local="Salas Temáticas B1 e B2",
                    tipo="Sessão Técnica",
                    descricao="Comunicações em Ensino de Física, Física Teórica, Astrofísica e Aplicações Computacionais.",
                    tipo_color="cyan",
                ),
                Atividade(
                    horario="10:15 – 10:45",
                    titulo="Coffee Break e Intervalo Técnico",
                    palestrante="Integração Acadêmica",
                    local="Espaço de Convivência IFE",
                    tipo="Intervalo Técnico",
                    descricao="Convivência acadêmica e café da manhã institucional.",
                    tipo_color="gray",
                ),
                Atividade(
                    horario="10:45 – 11:45",
                    titulo="Palestra Convidada 3: Astrofísica e Física Computacional",
                    palestrante="Prof. Dr. Jonathan (IFCE)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Modelagem computacional de sistemas astrofísicos, métodos numéricos e computação científica de alto desempenho.",
                    tipo_color="teal",
                ),
                Atividade(
                    horario="11:45 – 12:45",
                    titulo="Palestra Convidada 4: Gravitação, Cosmologia Quântica e Buracos Negros",
                    palestrante="Prof. Dr. Célio Rodrigues Muniz (UECE / Bolsista PQ-CNPq)",
                    local="Auditório Central",
                    tipo="Palestra Convidada",
                    descricao="Gravitação em regimes de campo forte, termodinâmica de buracos negros e avanços na cosmologia quântica.",
                    tipo_color="sky",
                ),
                Atividade(
                    horario="12:45 – 14:00",
                    titulo="Intervalo de Almoço",
                    palestrante="Livre",
                    local="Praça de Alimentação",
                    tipo="Intervalo",
                    descricao="Pausa para refeição e recomposição.",
                    tipo_color="gray",
                ),
                Atividade(
                    horario="14:00 – 17:30",
                    titulo="Sessão Especial dos Estudantes (Apresentação dos Meninos)",
                    palestrante="Estudantes de Iniciação Científica e Mestrado",
                    local="Hall Principal e Salas de Banca",
                    tipo="Sessão Especial",
                    descricao="Exposição de Pôsteres Científicos no Hall Principal e Sessão Oral de Iniciação Científica/Mestrado com Banca Avaliadora.",
                    tipo_color="indigo",
                ),
                Atividade(
                    horario="17:30 – 18:00",
                    titulo="Intervalo Técnico",
                    palestrante="Livre",
                    local="Espaço IFE",
                    tipo="Intervalo Técnico",
                    descricao="Preparação para a conferência magna de encerramento.",
                    tipo_color="gray",
                ),
                Atividade(
                    horario="18:00 – 19:15",
                    titulo="Conferência Magna de Encerramento: Astrofísica de Partículas e Grandes Levantamentos de Dados",
                    palestrante="Prof. Dr. Ronaldo Vieira Lobato (CBPF - Rio de Janeiro)",
                    local="Auditório Central",
                    tipo="Conferência Magna",
                    descricao="Astrofísica de partículas, processamento de Big Data cósmico, Machine Learning e levantamentos observacionais.",
                    tipo_color="violet",
                ),
                Atividade(
                    horario="19:15 – 19:45",
                    titulo="Premiação dos Trabalhos dos Estudantes, Lançamento dos Anais e Solenidade de Encerramento",
                    palestrante="Coordenação Geral (Prof. Dr. Edson Otoniel e Prof. Dr. André Flávio) & Comitê",
                    local="Auditório Central",
                    tipo="Solenidade de Encerramento",
                    descricao="Premiação dos destaques orais e pôsteres, formalização dos Anais do IV EFAC e encerramento oficial.",
                    tipo_color="indigo",
                ),
            ],
        }
        return programacoes.get(dia, programacoes["Dia 1"])

    @staticmethod
    def obter_palestrantes() -> List[Palestrante]:
        return [
            Palestrante(
                nome="Prof. Dr. Cesar Lenzi",
                cargo="Docente e Pesquisador",
                instituicao="ITA (São José dos Campos)",
                especialidade="Astrofísica de Altas Energias e Matéria Densa",
                topico="Plenária Dia 1 (11/11 às 18:00) • Convidado Principal",
            ),
            Palestrante(
                nome="Prof. Dr. Ronaldo Vieira Lobato",
                cargo="Pesquisador Titular",
                instituicao="CBPF (Rio de Janeiro)",
                especialidade="Astrofísica de Partículas e Big Data",
                topico="Conferência Magna Dia 2 (12/11 às 18:00)",
            ),
            Palestrante(
                nome="Profa. Dra. Eliane Angela Veit",
                cargo="Docente e Pesquisadora Titular",
                instituicao="UFRGS (Porto Alegre)",
                especialidade="Inovação, Epistemologia e Ensino de Física",
                topico="Palestra de Abertura (11/11 às 09:30) • Convidada Principal",
            ),
            Palestrante(
                nome="Prof. Dr. Iarley Lobato",
                cargo="Docente e Pesquisador",
                instituicao="UFPB (João Pessoa)",
                especialidade="Astrofísica Teórica e Objetos Compactos",
                topico="Palestra Convidada (11/11 às 11:00)",
            ),
            Palestrante(
                nome="Prof. Dr. Jonathan",
                cargo="Docente e Pesquisador",
                instituicao="IFCE (Ceará)",
                especialidade="Astrofísica e Física Computacional",
                topico="Palestra Convidada (12/11 às 10:45) • Convidado Regional",
            ),
            Palestrante(
                nome="Prof. Dr. Célio Rodrigues Muniz",
                cargo="Docente e Bolsista PQ-CNPq",
                instituicao="UECE (Ceará)",
                especialidade="Gravitação, Cosmologia Quântica e Buracos Negros",
                topico="Palestra Convidada (12/11 às 11:45) • Convidado Regional",
            ),
        ]

    @staticmethod
    def obter_eixos_tematicos() -> List[EixoTematico]:
        return [
            EixoTematico(
                numero=1,
                titulo="Astrofísica de Objetos Compactos",
                subtitulo="Densidades e Pressões Extremas",
                descricao="Investigação da matéria sob densidades extremas, processos de evolução estelar, pulsares, estrelas de nêutrons e anãs brancas.",
                cor="#103460",
                icone="disc",
                tags=["Pulsares", "Estrelas de Nêutrons", "Anãs Brancas"],
            ),
            EixoTematico(
                numero=2,
                titulo="Relatividade Geral e Gravitação",
                subtitulo="Campos Fortes e Cosmologia",
                descricao="Estudos de gravitação em regimes de campo forte, detecção e teoria de ondas gravitacionais, termodinâmica de buracos negros e modelos cosmológicos.",
                cor="#00ADB5",
                icone="orbit",
                tags=["Ondas Gravitacionais", "Buracos Negros", "Cosmologia"],
            ),
            EixoTematico(
                numero=3,
                titulo="Física Computacional e Ciência de Dados",
                subtitulo="Machine Learning & Big Data Cósmico",
                descricao="Aplicações de algoritmos de aprendizado de máquina, simulações numéricas e processamento de grandes levantamentos astronômicos.",
                cor="#2563EB",
                icone="cpu",
                tags=["Machine Learning", "Big Data", "Simulações"],
            ),
            EixoTematico(
                numero=4,
                titulo="Ensino de Física e Divulgação Científica",
                subtitulo="Interiorização & Formação Docente",
                descricao="Metodologias ativas para sala de aula, formação continuada de educadores, epistemologia e extensão em parceria com o Observatório Kariri.",
                cor="#059669",
                icone="graduation-cap",
                tags=["MNPEF", "Observatório Kariri", "Educação Básica"],
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
            paginas="2 a 4 páginas (incluindo introdução, metodologia, resultados, conclusões e referências)",
            publicacao="Anais do IV EFAC (Publicação oficial digital com registro ISBN/ISSN institucional)",
            criterios=[
                "Aderência temática aos 4 eixos do evento",
                "Coerência metodológica e fundamentação teórica",
                "Rigor conceitual e precisão analítica",
                "Originalidade e contribuição científica ou pedagógica",
                "Clareza e conformidade da redação científica",
            ],
        )

    @staticmethod
    def obter_comite_institucional() -> Dict[str, any]:
        return {
            "coordenacao_geral": "Prof. Dr. Edson Otoniel da Silva (UFCA) e Prof. Dr. André Flávio Gonçalves Silva (UFCA)",
            "comite_cientifico": [
                "Prof. Dr. Edson Otoniel da Silva (UFCA)",
                "Prof. Dr. Gilson Francisco de Oliveira Junior (UFCA)",
                "Prof. Dr. Tharcisyo Sá e Sousa Duarte (UFCA)",
            ],
            "instituicao_executora": "Universidade Federal do Cariri – UFCA (Instituto de Formação de Educadores – IFE)",
            "fomento": "Fundação Cearense de Apoio ao Desenvolvimento Científico e Tecnológico – FUNCAP / Governo do Estado do Ceará (Edital 03/2026 - Processo: CER-0264-00190.01.00/26)",
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
