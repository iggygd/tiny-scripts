from bs4 import BeautifulSoup
import re
import csv
import glob

def parse(file):
    with open(file, 'r', encoding='UTF-8') as file_:
        data = file_.read()
    						
    types = 'Normal Fire Fighting Water Flying Grass Poison Electric Ground Psychic Rock Ice Bug Dragon Ghost Dark Steel Fairy ???'.split(' ')

    soup = BeautifulSoup(data, "html.parser")
    
    trainers = soup.find_all('table', class_='expandable')
    '''
    A lot of string manipulation required for bulbapedia trainer template
    Name:
    Pokemon: -> Moves:
    '''
    for trainer in trainers:
        body = trainer.find('tbody')
        name, pokemon = body.findChildren("tr" , recursive=False)
        list_ = re.sub('|'.join(['\n', '\xa0']), '', pokemon.text).split('item:')

        name = name.find('tbody').find('tbody').find_all('tr')[1]
        filename = re.sub('|'.join(['\n', '\xa0', ' ']), '', name.text) #FILENAME
        rows = []                                                               #CONTENTS
        print(filename)
        for pkmn in list_[1:]:
            moves = pkmn.replace('Lv.50 ', '--').split('--')
            row = [moves[0].split(' ')[-2].strip('♂/♀')]
            for move in moves[1:5]:
                move = ' '.join(re.sub('|'.join(['     ','    ','   ','  ']), '', move).split(' ')[:-2])
                move = move.replace('ExtremeSpeed', 'Extreme Speed').replace('ThunderPunch', 'Thunder Punch').replace('FeatherDance', 'Feather Dance') #Special Cases hack
                move = move.replace('SolarBeam', 'Solar Beam').replace('AncientPower', 'Ancient Power').replace('DragonBreath', 'Dragon Breath')       #Could be better...
                move = move.replace('DynamicPunch', 'Dynamic Punch')                                                                                   #
                row.append(move)

            rows.append(row)

        write_csv(rows, f'trainers/{filename}')

def write_csv(rows, path):
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(rows)

if __name__ == '__main__':
    files = glob.glob('scraper/data/*.html')
    #file = 'scraper/data/Champions Tournament.html' #test
    for file in files:
        parse(file)
