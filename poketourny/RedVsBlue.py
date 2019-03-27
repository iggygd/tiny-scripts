import battle
import data
import glob
import os

#trainers = glob.glob('trainers/*')
pokemons, moves = data.load()
Red = battle.Trainer('Red', pokemons, moves, )
Blue = battle.Trainer('Blue', pokemons, moves)

RedVsBlue = battle.Battle(Red, Blue)