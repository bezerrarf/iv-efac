import os
import re

source_file = '/home/ramon_bezerra/Projects/Python_Lang/Projeto Web/projeto_web/views/pages/home.py'
dest_dir = '/home/ramon_bezerra/Projects/Python_Lang/Projeto Web/projeto_web/views/components/home_sections'

with open(source_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def extract_func(func_name, start_idx, end_idx=None):
    if end_idx is None:
        end_idx = len(lines)
    return ''.join(lines[start_idx:end_idx])

# Imports
base_imports = '''import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip
'''

funcs = [
    ('tela_inicio', 375, 524),
    ('tela_sobre', 524, 640),
    ('tela_eixos', 640, 729),
    ('tela_palestrantes', 729, 815),
    ('tela_programacao', 815, 959),
    ('tela_submissoes', 959, 1055),
    ('tela_local', 1055, 1169)
]

for name, start, end in funcs:
    content = base_imports + '\n\n' + extract_func(name, start, end)
    with open(os.path.join(dest_dir, f'{name}.py'), 'w', encoding='utf-8') as f:
        f.write(content)

print('Split complete.')
