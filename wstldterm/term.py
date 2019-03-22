from asciimatics.screen import Screen
from math import ceil

import os
import keys

HEADER = """ROBCO INDUSTRIES UNIFIED OPERATING SYSTEM
COPYRIGHT 2075-2077 ROBCO INDUSTRIES

"""
def header(screen):
    for i, text in enumerate(HEADER.split('\n')):
        screen.centre(text, i, screen.COLOUR_GREEN, screen.A_BOLD)

def wrap_text(text, screen):
    text = str(text)

    for i in range(ceil(len(text)/screen.width)):
        screen.print_at(text[i*screen.width-1:(i+1)*screen.width-1], 0, 4+i, screen.COLOUR_GREEN)

def context_manager(screen, context, cur, vars, ev):
    if context == 'menu':
        return menu(screen, cur, vars, ev)
    else:
        return None, None

def menu(screen, path, vars, ev):
    if ev == 13:
        screen.clear()
        header(screen)
        dirname, dirs, files = next(os.walk(path))

        listing = ['..']
        listing.extend(dirs)
        listing.extend(files)
        selected = f'{path}/{listing[vars["choice"]]}'
        print(selected)
        if os.path.isdir(selected):
            vars['choice'] = 0
            path = selected
        else:
            pass

    dirname, dirs, files = next(os.walk(path))

    listing = ['..']
    listing.extend(dirs)
    listing.extend(files)
    length = len(listing)

    if ev == -204:
        vars['choice'] = max(vars['choice'] - 1, 0)
    elif ev == -206:
        vars['choice'] = min(vars['choice'] + 1, length - 1)

    title = os.path.abspath(path)
    screen.print_at(title, 1, 4, screen.COLOUR_GREEN)
    screen.print_at("-"*len(title), 1, 5, screen.COLOUR_GREEN)

    for i, file in enumerate(listing):
        if i == vars['choice']:
            screen.print_at(f'> {file}', 1, 6+i, screen.COLOUR_GREEN, screen.A_REVERSE)
        else:
            screen.print_at(f'> {file}', 1, 6+i, screen.COLOUR_GREEN)
    return 'menu', os.path.abspath(path), True

def main(screen):
    updated = True
    context = 'menu'
    path = './'
    ev = None
    vars = {'choice': 0}

    screen.clear()
    screen.set_title("RIUOS")
    header(screen)
    while True:
        if updated:
            context, path, refresh = context_manager(screen, context, path, vars, ev)
            if refresh:
                screen.refresh()
            updated = False
            
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        else:
            updated = keys.handle(ev, vars)


Screen.wrapper(main)