#!../env/bin/python3

from asciimatics.screen import Screen
from math import ceil
from pathlib import Path

import os
import keys

HEADER = """ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES
-LOCAL-
"""
def header(screen):
    for i, text in enumerate(HEADER.split('\n')):
        screen.centre(text, i, screen.COLOUR_GREEN, screen.A_BOLD)

def wrap_text(screen, text):
    text = str(text)

    for i in range(ceil(len(text)/screen.width)):
        screen.print_at(text[i*screen.width-1:(i+1)*screen.width-1], 0, 4+i, screen.COLOUR_GREEN)

def context_manager(screen, context, cur, vars_, ev):
    if context == 'menu':
        return menu(screen, cur, vars_, ev)
    elif context == 'file':
        return file_(screen, cur, vars_, ev)
    else:
        return None, None

def file_(screen, path, vars_, ev=None):
    if ev == -300:
        screen.clear()
        header(screen)
        menu(screen, path.parent, vars_)
        return 'menu', path.parent, True
    elif ev == -204:
        screen.clear()
        header(screen)
        vars_['choice'] = max(vars_['choice'] - 4, 0)
    elif ev == -206:
        screen.clear()
        header(screen)
        length = len(vars_['loaded'])
        vars_['choice'] = min(vars_['choice'] + 4, length - screen.height + 5)

    if vars_['new_file']:
        with open(path, 'r') as file:
            vars_['loaded'] = tuple(tuple(line) for line in file.read().split('\n'))
    
    i = 0
    for j, line in enumerate(vars_['loaded']):
        if j < vars_['choice']:
            continue
        elif i >= screen.height-5:
            vars_['new_file'] = False
            return 'file', path, True
        screen.print_at(line, 1, 4+i, screen.COLOUR_GREEN)
        i += 1

    vars_['new_file'] = False
    return 'file', path, True

def menu(screen, path, vars_, ev=None):
    if ev == 13 or ev == 10:
        screen.clear()
        header(screen)
        dirname, dirs, files = next(os.walk(path))

        listing = ['..']
        listing.extend(dirs)
        listing.extend(files)
        selected = path / listing[vars_["choice"]]
        if os.path.isdir(selected):
            vars_['choice'] = 0
            path = selected
        else:
            vars_['choice'] = 0
            vars_['new_file'] = True
            file_(screen, selected, vars_)
            return 'file', selected, True

    dirname, dirs, files = next(os.walk(path))

    listing = ['..']
    listing.extend(dirs)
    listing.extend(files)
    length = len(listing)

    if ev == -204:
        vars_['choice'] = max(vars_['choice'] - 1, 0)
    elif ev == -206:
        vars_['choice'] = min(vars_['choice'] + 1, length - 1)

    title = str(path.resolve())
    screen.print_at(title, 1, 4, screen.COLOUR_GREEN)
    screen.print_at("-"*len(title), 1, 5, screen.COLOUR_GREEN)

    for i, file in enumerate(listing):
        if i == vars_['choice']:
            screen.print_at(f'> {file}', 1, 6+i, screen.COLOUR_GREEN, screen.A_REVERSE)
        else:
            screen.print_at(f'> {file}', 1, 6+i, screen.COLOUR_GREEN)
    return 'menu', path.resolve(), True

def main(screen):
    updated = True
    context = 'menu'
    path = Path('.')
    ev = None
    vars_ = {'choice': 0}

    screen.clear()
    #screen.set_title("RIUOS")
    header(screen)
    while True:
        if updated:
            context, path, refresh = context_manager(screen, context, path, vars_, ev)
            if refresh:
                screen.refresh()
            updated = False
            
        ev = screen.get_event()
        updated = keys.handle(ev, vars_)
        ev = updated
        if ev in (ord('Q'), ord('q')):
            return
        

Screen.wrapper(main)