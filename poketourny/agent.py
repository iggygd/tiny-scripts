import random

class Agent():
    '''
    State:
       Agent_Pokeset: Poke1, Poke2, Poke3, Poke4, Poke5, Poke6
       Agent_Pokemon: HP, Attack, Defense, Special Attack, Special Defense, Speed
    Opponent_Pokemon: HP, Attack, Defense, Special Attack, Special Defense, Speed

    Rewards:
        (1) = (Agent_Pokemon_Health_T2 - Agent_Pokemon_Health_T1) + (Opponent_Pokemon_Health_T1 - Opponent_Pokemon_Health_T2)
        (Alt) = ((Opponent_Pokemon_Health_T1 - Opponent_Pokemon_Health_T2)/Opponent_PokemonMaxHealth) - ((Agent_Pokemon_Health_T2 - Agent_Pokemon_Health_T1)/Agent_Pokemon_MaxHealth)
        eg.
        T1:
        Pikachu: 110hp -> Tackle
        Bulbasaur: 120hp -> Tackle
        T2:                              #Alternate:                    #
        Pikachu: 88 (110-22)             #Pikachu: 88                   #Pikachu: 97 (110-13)
        Bulbasaur: 99 (120-21)           #Bulbasaur: 99                 #Chansey: 271 (325-54)
        Reward= (88 - 110) + (120 - 99)  #Reward= (110/88) - (120/99)   #Reward = (54/325) - (13/110) #= (97-110) + (325-271)
              = -1 (-22 + 21)            #      = -0.04 (1.25 - 1.21)   #       = 0.06 (1.17 - 1.12)   #= 41 (-13 + 54)
    '''
    def __init__(self):
        pass

    def action(self, state):
        raise NotImplementedError

class RandomAgent(Agent):
    def __init__(self):
        pass

    def action(self, state, actionspace):
        return random.randint(0, len(actionspace))

class UserAgent(Agent):
    def __init__(self):
        pass

class SmartAgent(Agent):
    def __init__(self):
        pass

class MachineAgent(Agent):
    def __init__(self):
        pass

class MCAgent(Agent):
    def __init__(self):
        pass
    