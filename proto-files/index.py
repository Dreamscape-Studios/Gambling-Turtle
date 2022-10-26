## index.py
## Contributors : Ben

from enum import Enum
from time import sleep
from tokenize import String
from random import randint

roll_range = (1, 3)
attack_range = (2, 6)
block_cost = 2

game_running : bool = True
player_turn : bool = True

class Actions(Enum):
    ROLL = 0
    ATTACK = 1
    BLOCK = 2

class Entity:
    def __init__(self, name : String) -> None:
        self.name = name
        self.max_pool = 20
        self.pool = self.max_pool
        self.blocking = False

    def act(self, target, action):
        print("")
        match action:
            case Actions.ROLL.value:
                rolled_pool = randint(roll_range[0], roll_range[1])
                self.add_pool(rolled_pool)
                print(f" | {self.name.capitalize()} Rolled for {rolled_pool} and added it to their Pool")
                print(f" | {self.name.capitalize()} now has {self.pool} Pool")
            case Actions.ATTACK.value:
                rolled_attack = randint(attack_range[0], attack_range[1])
                self.sub_pool(4)

                # Lost round check because this action takes pool
                if not self.lost_round():
                    print(f" | {self.name.capitalize()} Attacked for {rolled_attack} and lost 4 Pool")
                    print(f" | {self.name.capitalize()} now has {self.pool} Pool")

                    # Blocking logic
                    if not target.blocking:
                        target.sub_pool(rolled_attack)
                        print(f" | Succesfully removed {rolled_attack} from {target.name.capitalize()}'s Pool!")
                    else:
                        print(f" | Failed to remove Pool. {target.name.capitalize()} blocked the attack!")
            case Actions.BLOCK.value:
                self.sub_pool(2)

                # Lost round check because this action takes pool
                if not self.lost_round():
                    print(f"| {self.name.capitalize()} readies themselves for an attack!")
                    self.blocking = True
                    print(f"| {self.name.capitalize()} now has {self.pool} Pool")
            case _:
                print(" | Invalid action; Turn skipped")
            
    
    def enact_turn(self, target):
        # Allows access of `player_turn` (for those who don't understand `global` and why it's used)
        global player_turn

        # Simple lost round check 
        if target.lost_round() or self.lost_round(): 
            return

        # Allows matching an enemy with any name
        match self.name:
            case "player":
                action = -1
                while action != 0 or action != 1 or action != 2:
                    print(f"\nPlayer Turn; Pool: {self.pool}")
                    print(f"{Actions.ROLL.value}; Roll: Roll a dice between {roll_range[0]}-{roll_range[1]} and gain that amount of Pool")
                    print(f"{Actions.ATTACK.value}; Attack: Expend 3 Pool and Roll a dice between {attack_range[0]}-{attack_range[1]} and damage your enemy's Pool with that amount of Damage")
                    print(f"{Actions.BLOCK.value}; Block: Expend 2 Pool to Defend against the next attack")
                    action = input("Choose your Action: ")
                    try:
                        action = int(action)
                    except:
                        print("Invalid action; Turn skipped")
                    finally:
                        self.act(target, action)
                        break
            case _:
                ## Enemy AI! :D
                # If the player has less health and the enemy can attack without dying -
                if target.pool < self.pool and self.pool > 4:
                    action = Actions.ATTACK.value
                # If the enemy has less health than the player, play defensive -
                elif target.pool > self.pool:
                    if randint(0,1) == 0:
                        action = Actions.BLOCK.value
                    else:
                        action = Actions.ROLL.value
                # Otherwise do random stuff and hope not to die
                else:
                    action = randint(0,2)
                
                sleep(0.5)
                print(f"\nEnemy Turn; Pool: {self.pool}")
                self.act(target, action)
                
                        
        # Cycle turns
        player_turn = not player_turn

        # Blocking only lasts one turn
        target.blocking = False
    
    def add_pool(self, amt):
        self.pool += amt
        if self.pool > self.max_pool:
            self.pool = self.max_pool
    
    def sub_pool(self, amt):
        global game_running
        self.pool -= amt
        if self.pool <= 0:
            self.pool = 0
            return
    
    def lost_round(self):
        global game_running
        if self.pool <= 0:
            print(f"\n{str(self.name).capitalize()} Has Lost!")
            game_running = False
        return self.pool <= 0

enemy : Entity = Entity("enemy")
player : Entity = Entity("player")

## Game Loop
def _process():
    if player_turn:
        Entity.enact_turn(player, enemy)
    else:
        Entity.enact_turn(enemy, player)

while game_running:
    _process()

