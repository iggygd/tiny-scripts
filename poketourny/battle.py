import pandas as pd

class Battle():
    def __init__(self, trainer_a, trainer_b):
        print(trainer_a.name)
        for pk, move in trainer_a.moves.items():
            print(move)
        print(trainer_b.name)
        for pk, move in trainer_b.moves.items():
            print(move)
        pass

class Trainer():
    def __init__(self, name, stats, moves):
        self.data = pd.read_csv(f'trainers/{name}', header=None)
        self.name = name

        self.pokemons = stats.merge(self.data, left_on='Name', right_on=0).drop([0,1,2,3,4,'Moves','Next Evolution(s)'], axis=1)
        self.moves = {}

        data_T = transpose_moves(self.data)
        for pokemon in self.data[0]:
            self.moves[pokemon] = moves.merge(data_T, left_on='Name', right_on=pokemon).drop(self.data[0], axis=1)
        
    def __repr__(self):
        return str(self.pokemons)

class Pokemon():
    def __init__(self, name, moves):
        pass

def transpose_moves(pokemon):
    df = pokemon.transpose()
    df.columns = df.loc[0]
    df.reindex(df.index.drop(0))
    return df

if __name__ == '__main__':
    import data
    import glob
    import os

    trainers = glob.glob('trainers/*')
    pokemons, moves = data.load()

    participants = [Trainer(os.path.basename(file), pokemons, moves) for file in trainers]
    for participant in participants:
        print(participant.name)