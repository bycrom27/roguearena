#import modules
from random import randint
from click import clear
import sys,tty,os,termios
import pickle
import json

#global variables
keylogging = False
action = ""
player_stats = {
    "playername": "Steven",
    "weaponname": "dagger",
    "armorname": "clothes",
    "magicweaponname": "nothing",
    "charmname": "copper ring",
    "attack": 1,
    "defense": 1,
    "agility": 1,
    "magic": 1,
    "heritage": "human",
    "playerclass": "warrior",
    "classlevel": 0,
    "effectivelevel": 0,
    "weapon": 1,
    "armor": 1,
    "magicweapon": 0,
    "charm": 1,
    "spellslot1": "       ",
    "spellslot2": "       ",
    "spellslot3": "       ",
    "spellslot4": "       ",
    "health": 100,
    "experience": 0,
    "gold": 50,
    "freshweapons": True,
    "fresharmor": True,
    "freshmagicweapons": True,
    "freshcharms": True,
    "freshspells": True
}
item_values = {
    "weaponvalue1": 1,
    "weaponvalue2": 2,
    "weaponvalue3": 3,
    "weaponvalue4": 4,
    "weaponvalue5": 5,
    "weaponvalue6": 6,
    "armorvalue1": 1,
    "armorvalue2": 2,
    "armorvalue3": 3,
    "armorvalue4": 4,
    "armorvalue5": 5,
    "armorvalue6": 6,
    "mweaponvalue1": 1,
    "mweaponvalue2": 2,
    "mweaponvalue3": 3,
    "mweaponvalue4": 4,
    "mweaponvalue5": 5,
    "mweaponvalue6": 6,
    "charmvalue1": 1,
    "charmvalue2": 2,
    "charmvalue3": 3,
    "charmvalue4": 4,
    "charmvalue5": 5,
    "charmvalue6": 6,
    "spellvalue1": 1,
    "spellvalue2": 2,
    "spellvalue3": 3,
    "spellvalue4": 4,
    "spellvalue5": 5,
    "spellvalue6": 6
}

enemy_stats = {
    "enemyname": "mook",
    "enemybreath": False,
    "enemycancast": False,
    "enemycanheal": False,
    "enemyattack": 1,
    "enemydefense": 1,
    "enemyagility": 1,
    "enemymagic": 1,
    "enemyweapon": 0,
    "enemyarmor": 0,
    "enemymagic"]weapon": 0,
    "enemycharm": 0,
    "enemyhealth": 20,
    "enemylevel": 1,
    "xpdrop": 10,
    "golddrop": 10,
    "enemysleepcounter": 0,
    "enemywound": ""
}

combat_variables = {
    "firstturn": True,
    "playerturn": False,
    "sneak": False,
    "woundpenalty": 0,
    "incombat": False,
    "magicmenu": False
}

shop_variables = {
    "purchaseitem": "rubber chicken",
    "itemvalue": 333,
    "itembonus": 3,
    "itemtype": "gag",
    "totalassets": 0,
    "resellitem": "cosmic hammer",
    "resellvalue": 5
}

slotchosen = 1
savegameslot = "1"

# key logging function
def getkey():
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b)
            key_mapping = {
                127: 'backspace',
                10: 'return',
                32: 'space',
                9: 'tab',
                27: 'esc',
                65: 'up',
                66: 'down',
                67: 'right',
                68: 'left'
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def save_game(state, savegameslot):
    if savegameslot == "1":
        with open("savegame1.txt", "w") as save_file:
            json.dump(state, save_file) 
    elif savegameslot == "2":
        with open("savegame2.txt", "w") as save_file:
            json.dump(state, save_file) 
    elif savegameslot == "3":
        with open("savegame3.txt", "w") as save_file:
            json.dump(state, save_file) 
    else:
        print("Invalid save slot!\n")
        input()
        town()
    print("Game saved!\n")
    input()
    town()
        
def load_game():
    global savegameslot
    filename = f"savegame{savegameslot}.txt"
    try:
        with open(filename, "r") as save_file:
            state = json.load(save_file)
            print("File loaded!\n")
            input()
            filemenu(state)
    except FileNotFoundError:
        print("Invalid save file!\n")
        input()
        gamestart()
           
def filemenu(game_state=None):
    if game_state is not None:
        player_stats.update(game_state.get("player_stats", {}))
        item_values.update(game_state.get("item_values", {}))
    town()

def temple():
    clear()
    print("The priestess asks if you'd like your deeds recorded on the holy register.")
    print("Choose a file to save the game (1-3) or press enter to exit.")
    savegameslot = input()
    if savegameslot in ["1", "2", "3"]:
        game_state = {
            "player_stats": player_stats,
            "item_values": item_values,
        }
        save_game(game_state, savegameslot)
    else:
        print("'My services are always here if you should ever need them,' the priestess tells you.\n")
        input()
    town()
    
def gamestart():
    global savegameslot
    clear()
    print("Would you like to (L)oad an old game or start a (N)ew one?\n")
    choice = input()
    if choice == "l" or choice == "load" or choice == "L":
        clear()
        print("""Choose a game file to load.

Save Game (1)

Save Game (2)

Save Game (3)

""")
        savegameslot = input()
        state = load_game()
        if state is not None:
            filemenu(state)
        else:
            print("Error loading game!\n")
            input()
            gamestart()
    elif choice == "n" or choice == "N" or choice == "new":
        rolldice()  # or any valid function call to start a new game
    else:
        gamestart()
    
#this begins character creation and sets character's stats
def rolldice(): 
    for i in range(0, 5000):
        clear()
        die1 = randint(1, 6)
        die2 = randint(1, 6)
        die3 = randint(1, 6)
        die4 = randint(1, 6)
        print(f"""
Rolling stats...         


           ---
Attack:   | {die1} |
           ---
           
           ---
Defense:  | {die2} |
           ---

           ---
Agility:  | {die3} |
           ---
           
           ---
Magic:    | {die4} |
           ---

""")
    choice = input("Would you like to keep this character? y/n\n\n")
    if choice == "y" or choice == "yes":
        player_stats["attack"] = die1
        player_stats["defense"] = die2
        player_stats["agility"] = die3
        player_stats["magic"] = die4
        chooseheritage()
    if choice == "n" or choice == "no":
        rolldice()

# the player may now choose a heritage which gives certain bonuses and penalties
def chooseheritage():
    clear()
    print(f"""
Please choose a heritage.          (human) Humans are good at many different things.


           ---            
Attack:   | {player_stats["attack"]} |                    (orc) Orcs are very strong and make fierce warriors.
           ---
           
           ---            
Defense:  | {player_stats["defense"]} |                    (dwarf) Dwarves are strong, sturdy folk.
           ---

           ---            
Agility:  | {player_stats["agility"]} |                    (goblin) Goblins are sneaky and make good rogues.
           ---
           
           ---            
Magic:    | {player_stats["magic"]} |                    (elf) Elves are nimble and gifted with magic.
           ---

""")    
    playerchoice = input("Type the heritage of your choice.\n\n")
    if playerchoice == "orc" or playerchoice == "o":
        player_stats["heritage"] = "orc"
        player_stats["attack"] += 2
        player_stats["magic"] -= 1
    elif playerchoice == "dwarf" or playerchoice == "d":
        player_stats["heritage"] = "dwarf"
        player_stats["attack"] += 1
        player_stats["defense"] += 1
        player_stats["agility"] -= 1
    elif playerchoice == "goblin" or playerchoice == "g":
        player_stats["heritage"] = "goblin"
        player_stats["agility"] += 2
        player_stats["attack"] -= 1
    elif playerchoice == "elf" or playerchoice == "e":
        player_stats["heritage"] = "elf"
        player_stats["agility"] += 1
        player_stats["magic"] += 1
        player_stats["defense"] -= 1        
    elif playerchoice == "debug6":
        player_stats["heritage"] = "cheater"
        player_stats["attack"] = 6
        player_stats["defense"] = 6
        player_stats["agility"] = 6    
        player_stats["magic"] = 6        
    else:
        player_stats["heritage"] = "human"
        for x in range(2):
            humanbonus = randint(1,4)
            if humanbonus == 1:
                player_stats["attack"] += 1
            elif humanbonus == 2:
                player_stats["defense"] += 1
            elif humanbonus == 3:
                player_stats["agility"] += 1
            else:
                player_stats["magic"] += 1        
    chooseclass()   
    
# now the player chooses a class, which further increases stats and grants starting equipment, level-ups, and special abilities
def chooseclass():
    clear()
    print(f"""
Now choose a class.                (warrior) Warriors are the best at fighting.


           ---            
Attack:   | {player_stats["attack"]} |                    (rogue) Rogues are very stealthy.
           ---
           
           ---            
Defense:  | {player_stats["defense"]} |                    (mage) Mages are masters of magic.
           ---

           ---            
Agility:  | {player_stats["agility"]} |                    (cleric) Clerics are tough magic users.
           ---
           
           ---            
Magic:    | {player_stats["magic"]} |                    (bard) Bards are knowledgable about many things.
           ---

""")    
    playerchoice = input("Type the class of your choice.\n\n")
    if playerchoice == "rogue" or playerchoice == "r":
        player_stats["playerclass"] = "rogue"
        player_stats["attack"] += 1
        player_stats["agility"] += 1
    elif playerchoice == "mage" or playerchoice == "m":
        player_stats["playerclass"] = "mage"
        player_stats["magic"] += 2
    elif playerchoice == "cleric" or playerchoice == "c":
        player_stats["playerclass"] = "cleric"
        player_stats["defense"] += 1
        player_stats["magic"] += 1  
    elif playerchoice == "bard" or playerchoice == "b":
        player_stats["playerclass"] = "bard"
        player_stats["agility"] += 1
        player_stats["magic"] += 1
    else:
        player_stats["playerclass"] = "warrior"
        player_stats["attack"] += 1
        player_stats["defense"] += 1
    confirmcharacter()
        
# the player now chooses to keep or discard the character they rolled
def confirmcharacter():
    clear()
    print(f"""
Heritage: {player_stats["heritage"]} 
Class: {player_stats["playerclass"]}          


           ---            
Attack:   | {player_stats["attack"]} |                    
           ---
           
           ---            
Defense:  | {player_stats["defense"]} |                    
           ---

           ---            
Agility:  | {player_stats["agility"]} |                    
           ---
           
           ---            
Magic:    | {player_stats["magic"]} |                    
           ---

""")    
    playerchoice = input("Keep this character?\n\n")
    if playerchoice == "yes" or playerchoice == "y":
        namecharacter()
    else:
        rolldice()

# the player now names their character
def namecharacter():
    clear()
    playername = input("\nName your character.\n\n")
    player_stats["playername"] = playername
    clear()
    print(f"""
Name: {player_stats["playername"]}
Heritage: {player_stats["heritage"]} 
Class: {player_stats["playerclass"]}          


           ---            
Attack:   | {player_stats["attack"]} |                    
           ---
           
           ---            
Defense:  | {player_stats["defense"]} |                    
           ---

           ---            
Agility:  | {player_stats["agility"]} |                    
           ---
           
           ---            
Magic:    | {player_stats["magic"]} |                    
           ---

Welcome! And good luck! """)        
        
    finalizecharacter()  

# this function mostly serves to finalize the character before the game begins
def finalizecharacter():
    if player_stats["playerclass"] == "warrior":
        player_stats["weaponname"] = "short sword"
        player_stats["weapon"] = 2
    elif player_stats["playerclass"] == "rogue":
        player_stats["weaponname"] = "short sword"
        player_stats["weapon"] = 2
    elif player_stats["playerclass"] == "mage":
        player_stats["magicweaponname"] = "training wand"
        player_stats["magicweapon"] = 1
        player_stats["spellslot1"] = "~blaze~"
    elif player_stats["playerclass"] == "cleric":
        player_stats["charmname"] = "holy symbol"
        player_stats["charm"] = 2
        player_stats["spellslot1"] = "restore"
    elif player_stats["playerclass"] == "bard":
        player_stats["magicweaponname"] = "lute"
        player_stats["magicweapon"] = 1
        player_stats["spellslot1"] = "~sleep~"
    else:
        player_stats["weaponname"] = "stick"
        player_stats["weapon"] = 1
        # this code should never kick in so it is only for debugging
    player_stats["health"] = 100
    totalstats = player_stats["attack"] + player_stats["defense"] + player_stats["agility"] + player_stats["magic"]
    player_stats["effectivelevel"] = totalstats // 2
    town()

def resolveactions():
    global combat_variables["magicmenu"]
    global combat_variables["incombat"]
    if combat_variables["magicmenu"]:
        battlemagic()
    elif combat_variables["incombat"]:
        combat()
    
def town():   
    global combat_variables["firstturn"]
    global keylogging    

    combat_variables["firstturn"] = True
    keylogging = False
    player_stats["health"] = 100
    clear()
    print("""You are in the city of Mirstone. What would you like to do?
    
    (1) Visit the temple of Xola, Goddess of Justice
    
    (2) Go to the marketplace
    
    (3) Enter the arena
    
    (4) Check your stats

    """)

    choice = input()
    if choice == "1":
        temple()
    elif choice == "2":
        shop()
    elif choice == "3":
        arena()
    elif choice == "4":
        stats()
        
def stats():    
    clear()
    print(f"""Name:          {player_stats["playername"]}
Heritage:      {player_stats["heritage"]}
Class:         {player_stats["playerclass"]}
Level:         {player_stats["classlevel"]} 
Experience:    {player_stats["experience"]}
Gold:          {player_stats["gold"]}

Attack:        {player_stats["attack"]}
Defense:       {player_stats["defense"]}
Agility:       {player_stats["agility"]}
Magic:         {player_stats["magic"]}

Weapon:        {player_stats["weaponname"]} ({player_stats["weapon"]})
Armor:         {player_stats["armorname"]} ({player_stats["armor"]})
Magic Focus:   {player_stats["magicweaponname"]} ({player_stats["magicweapon"]})
Magic Charm:   {player_stats["charmname"]} ({player_stats["charm"]})

Spells known:  
{player_stats["spellslot1"]} {player_stats["spellslot2"]} 
{player_stats["spellslot3"]} {player_stats["spellslot4"]}

Press (enter) to continue""")  
    input()
    town()
        
def arena():
    clear()
    print("""You are at the arena. Fighters from all over the world have come here to prove their mettle.
    
    Which league would you like to enter?
    
    (1) Copper League
    
    (2) Silver League
    
    (3) Gold League
    
    (4) Platinum League
    
    (5) Leave

    """)
    choice = input()
    if choice == "1":
        copperleague()
    elif choice == "2":
        silverleague()
    elif choice == "3":
        goldleague()
    elif choice == "4":
        platinumleague()
    elif choice == "5":
        town()
    
def copperleague():
    global enemy_stats["enemyname"] 
    global enemy_stats["enemybreath"] 
    global enemy_stats["enemycancast"] 
    global enemy_stats["enemyattack"] 
    global enemy_stats["enemydefense"] 
    global enemy_stats["enemyagility"] 
    global enemy_stats["enemymagic"] 
    global enemy_stats["enemyweapon"] 
    global enemy_stats["enemyarmor"] 
    global enemy_stats["enemymagic"]weapon 
    global enemy_stats["enemycharm"] 
    global enemy_stats["enemyhealth"] 
    global enemy_stats["enemylevel"] 
    global enemy_stats["xpdrop"] 
    global enemy_stats["golddrop"] 
    clear()
    print("""The Copper League is where most amateurs begin their fighting career. The easiest enemies can be found here.
    
    What would you like to fight?
    
    (1) Giant Bat
    
    (2) Giant Rat
    
    (3) Kobold
    
    (4) Goblin
    
    (5) Orc
    
    (6) Leave

    """)    
    
    choice = input()
    if choice == "1":
        enemy_stats["enemyname"] = "giant bat"
        enemy_stats["enemyattack"] = 1
        enemy_stats["enemydefense"] = 1
        enemy_stats["enemyagility"] = 3
        enemy_stats["enemymagic"] = 1
        enemy_stats["enemyweapon"] = 1
        enemy_stats["enemyarmor"] = 1
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 1
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 3
        enemy_stats["xpdrop"] = 30
        enemy_stats["golddrop"] = 3
    elif choice == "2":
        enemy_stats["enemyname"] = "giant rat"
        enemy_stats["enemyattack"] = 2
        enemy_stats["enemydefense"] = 2
        enemy_stats["enemyagility"] = 3
        enemy_stats["enemymagic"] = 1
        enemy_stats["enemyweapon"] = 1
        enemy_stats["enemyarmor"] = 1
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 1
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 4
        enemy_stats["xpdrop"] = 40 
        enemy_stats["golddrop"] = 4
    elif choice == "3":
        enemy_stats["enemyname"] = "kobold"
        enemy_stats["enemyattack"] = 2
        enemy_stats["enemydefense"] = 3
        enemy_stats["enemyagility"] = 3
        enemy_stats["enemymagic"] = 2
        enemy_stats["enemyweapon"] = 2
        enemy_stats["enemyarmor"] = 2
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 2
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 5
        enemy_stats["xpdrop"] = 50
        enemy_stats["golddrop"] = 10
    elif choice == "4":
        enemy_stats["enemyname"] = "goblin"
        enemy_stats["enemyattack"] = 3
        enemy_stats["enemydefense"] = 3
        enemy_stats["enemyagility"] = 3
        enemy_stats["enemymagic"] = 3
        enemy_stats["enemyweapon"] = 2
        enemy_stats["enemyarmor"] = 2
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 2
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 6
        enemy_stats["xpdrop"] = 60
        enemy_stats["golddrop"] = 12
    elif choice == "5":
        enemy_stats["enemyname"] = "orc"
        enemy_stats["enemyattack"] = 4
        enemy_stats["enemydefense"] = 4
        enemy_stats["enemyagility"] = 3
        enemy_stats["enemymagic"] = 3
        enemy_stats["enemyweapon"] = 4
        enemy_stats["enemyarmor"] = 4
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 4
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 7
        enemy_stats["xpdrop"] = 70
        enemy_stats["golddrop"] = 56
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        copperleague()
    combat_variables["firstturn"] = True
    combat()        
        
def silverleague():
    global enemy_stats["enemyname"] 
    global enemy_stats["enemybreath"] 
    global enemy_stats["enemycancast"] 
    global enemy_stats["enemyattack"] 
    global enemy_stats["enemydefense"] 
    global enemy_stats["enemyagility"] 
    global enemy_stats["enemymagic"] 
    global enemy_stats["enemyweapon"] 
    global enemy_stats["enemyarmor"] 
    global enemy_stats["enemymagic"]weapon 
    global enemy_stats["enemycharm"] 
    global enemy_stats["enemyhealth"] 
    global enemy_stats["enemylevel"] 
    global enemy_stats["xpdrop"] 
    global enemy_stats["golddrop"]
    clear()
    print("""The Silver League is for veterans who have started to earn a reputation in the arena. 
The enemies here are a little more difficult than those found in the Copper League.
    
    What would you like to fight?
    
    (1) Slime
    
    (2) Dark Acolyte
    
    (3) Ogre
    
    (4) Hellhound
    
    (5) Dark Dwarf
    
    (6) Leave

    """)   
    choice = input()        
    if choice == "1":
        enemy_stats["enemyname"] = "slime"
        enemy_stats["enemyattack"] = 6
        enemy_stats["enemydefense"] = 6
        enemy_stats["enemyagility"] = 2
        enemy_stats["enemymagic"] = 2
        enemy_stats["enemyweapon"] = 4
        enemy_stats["enemyarmor"] = 4
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 4
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 8
        enemy_stats["xpdrop"] = 80
        enemy_stats["golddrop"] = 64
    elif choice == "2":
        enemy_stats["enemyname"] = "dark acolyte"
        enemy_stats["enemycancast"] = True
        enemy_stats["enemyattack"] = 3
        enemy_stats["enemydefense"] = 3
        enemy_stats["enemyagility"] = 6
        enemy_stats["enemymagic"] = 6
        enemy_stats["enemyweapon"] = 4
        enemy_stats["enemyarmor"] = 4
        enemy_stats["enemymagic"]weapon = 4
        enemy_stats["enemycharm"] = 4
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 9
        enemy_stats["xpdrop"] = 90
        enemy_stats["golddrop"] = 72
    elif choice == "3":
        enemy_stats["enemyname"] = "ogre"
        enemy_stats["enemyattack"] = 9
        enemy_stats["enemydefense"] = 9
        enemy_stats["enemyagility"] = 1
        enemy_stats["enemymagic"] = 1
        enemy_stats["enemyweapon"] = 4
        enemy_stats["enemyarmor"] = 4
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 4
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 10
        enemy_stats["xpdrop"] = 100
        enemy_stats["golddrop"] = 80
    elif choice == "4":
        enemy_stats["enemyname"] = "hellhound"
        enemy_stats["enemybreath"] = True
        enemy_stats["enemyattack"] = 6
        enemy_stats["enemydefense"] = 5
        enemy_stats["enemyagility"] = 6
        enemy_stats["enemymagic"] = 5
        enemy_stats["enemyweapon"] = 4
        enemy_stats["enemyarmor"] = 4
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 4
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 11
        enemy_stats["xpdrop"] = 110
        enemy_stats["golddrop"] = 88
    elif choice == "5":
        enemy_stats["enemyname"] = "dark dwarf"
        enemy_stats["enemyattack"] = 8
        enemy_stats["enemydefense"] = 8
        enemy_stats["enemyagility"] = 4
        enemy_stats["enemymagic"] = 4
        enemy_stats["enemyweapon"] = 6
        enemy_stats["enemyarmor"] = 6
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 6
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 12
        enemy_stats["xpdrop"] = 120
        enemy_stats["golddrop"] = 216
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        silverleague()
    combat_variables["firstturn"] = True
    combat()

def goldleague():
    global enemy_stats["enemyname"] 
    global enemy_stats["enemybreath"] 
    global enemy_stats["enemycancast"] 
    global enemy_stats["enemyattack"] 
    global enemy_stats["enemydefense"] 
    global enemy_stats["enemyagility"] 
    global enemy_stats["enemymagic"] 
    global enemy_stats["enemyweapon"] 
    global enemy_stats["enemyarmor"] 
    global enemy_stats["enemymagic"]weapon 
    global enemy_stats["enemycharm"] 
    global enemy_stats["enemyhealth"] 
    global enemy_stats["enemylevel"] 
    global enemy_stats["xpdrop"] 
    global enemy_stats["golddrop"]
    clear()
    print("""The Gold League is for champions who are cunning enough or strong enough to survive the lower
leagues. It is a truly dangerous place to compete.
    
    What would you like to fight?
    
    (1) Dark Elf
    
    (2) Dark Mage
    
    (3) Chimera
    
    (4) Wraith
    
    (5) Giant
    
    (6) Leave

    """)   
    choice = input()        
    if choice == "1":
        enemy_stats["enemyname"] = "dark elf"
        enemy_stats["enemyattack"] = 6
        enemy_stats["enemydefense"] = 6
        enemy_stats["enemyagility"] = 8
        enemy_stats["enemymagic"] = 6
        enemy_stats["enemyweapon"] = 6
        enemy_stats["enemyarmor"] = 6
        enemy_stats["enemymagic"]weapon = 6
        enemy_stats["enemycharm"] = 6
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 13
        enemy_stats["xpdrop"] = 130
        enemy_stats["golddrop"] = 234
    elif choice == "2":
        enemy_stats["enemyname"] = "dark mage"
        enemy_stats["enemycancast"] = True
        enemy_stats["enemyattack"] = 4
        enemy_stats["enemydefense"] = 5
        enemy_stats["enemyagility"] = 9
        enemy_stats["enemymagic"] = 10
        enemy_stats["enemyweapon"] = 6
        enemy_stats["enemyarmor"] = 6
        enemy_stats["enemymagic"]weapon = 6
        enemy_stats["enemycharm"] = 6
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 14
        enemy_stats["xpdrop"] = 140
        enemy_stats["golddrop"] = 252
    elif choice == "3":
        enemy_stats["enemyname"] = "chimera"
        enemy_stats["enemybreath"] = True
        enemy_stats["enemyattack"] = 8
        enemy_stats["enemydefense"] = 8
        enemy_stats["enemyagility"] = 7
        enemy_stats["enemymagic"] = 7
        enemy_stats["enemyweapon"] = 6
        enemy_stats["enemyarmor"] = 6
        enemy_stats["enemymagic"]weapon = 6
        enemy_stats["enemycharm"] = 6
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 15
        enemy_stats["xpdrop"] = 150
        enemy_stats["golddrop"] = 270
    elif choice == "4":
        enemy_stats["enemyname"] = "wraith"
        enemy_stats["enemyattack"] = 9
        enemy_stats["enemydefense"] = 9
        enemy_stats["enemyagility"] = 8
        enemy_stats["enemymagic"] = 6
        enemy_stats["enemyweapon"] = 6
        enemy_stats["enemyarmor"] = 6
        enemy_stats["enemymagic"]weapon = 6
        enemy_stats["enemycharm"] = 6
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 16
        enemy_stats["xpdrop"] = 160
        enemy_stats["golddrop"] = 288
    elif choice == "5":
        enemy_stats["enemyname"] = "giant"
        enemy_stats["enemyattack"] = 11
        enemy_stats["enemydefense"] = 11
        enemy_stats["enemyagility"] = 6
        enemy_stats["enemymagic"] = 6
        enemy_stats["enemyweapon"] = 8
        enemy_stats["enemyarmor"] = 8
        enemy_stats["enemymagic"]weapon = 0
        enemy_stats["enemycharm"] = 8
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 17
        enemy_stats["xpdrop"] = 170
        enemy_stats["golddrop"] = 680
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        goldleague()
    combat_variables["firstturn"] = True
    combat()    

def platinumleague():
    global enemy_stats["enemyname"] 
    global enemy_stats["enemybreath"] 
    global enemy_stats["enemycancast"] 
    global enemy_stats["enemycanheal"]
    global enemy_stats["enemyattack"] 
    global enemy_stats["enemydefense"] 
    global enemy_stats["enemyagility"] 
    global enemy_stats["enemymagic"] 
    global enemy_stats["enemyweapon"] 
    global enemy_stats["enemyarmor"] 
    global enemy_stats["enemymagic"]weapon 
    global enemy_stats["enemycharm"] 
    global enemy_stats["enemyhealth"] 
    global enemy_stats["enemylevel"] 
    global enemy_stats["xpdrop"] 
    global enemy_stats["golddrop"]
    clear()
    print("""The Platinum League is for champions who are cunning enough or strong enough to survive the lower leagues. It is a truly dangerous place to compete.
    
    What would you like to fight?
    
    (1) Dark Priest
    
    (2) Vampire
    
    (3) Death Knight
    
    (4) Demon
    
    (5) Dragon
    
    (6) Leave

    """)   
    choice = input()        
    if choice == "1":
        enemy_stats["enemyname"] = "dark priest"
        enemy_stats["enemycanheal"] = True
        enemy_stats["enemyattack"] = 9
        enemy_stats["enemydefense"] = 9
        enemy_stats["enemyagility"] = 8
        enemy_stats["enemymagic"] = 10
        enemy_stats["enemyweapon"] = 8
        enemy_stats["enemyarmor"] = 8
        enemy_stats["enemymagic"]weapon = 8
        enemy_stats["enemycharm"] = 8
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 18
        enemy_stats["xpdrop"] = 180
        enemy_stats["golddrop"] = 720
    elif choice == "2":
        enemy_stats["enemyname"] = "vampire"
        enemy_stats["enemyattack"] = 9
        enemy_stats["enemydefense"] = 9
        enemy_stats["enemyagility"] = 10
        enemy_stats["enemymagic"] = 10
        enemy_stats["enemyweapon"] = 8
        enemy_stats["enemyarmor"] = 8
        enemy_stats["enemymagic"]weapon = 8
        enemy_stats["enemycharm"] = 8
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 19
        enemy_stats["xpdrop"] = 190
        enemy_stats["golddrop"] = 760
    elif choice == "3":
        enemy_stats["enemyname"] = "death knight"
        enemy_stats["enemyattack"] = 11
        enemy_stats["enemydefense"] = 11
        enemy_stats["enemyagility"] = 8
        enemy_stats["enemymagic"] = 10
        enemy_stats["enemyweapon"] = 8
        enemy_stats["enemyarmor"] = 8
        enemy_stats["enemymagic"]weapon = 8
        enemy_stats["enemycharm"] = 8
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 20
        enemy_stats["xpdrop"] = 200
        enemy_stats["golddrop"] = 800
    elif choice == "4":
        enemy_stats["enemyname"] = "demon"
        enemy_stats["enemycancast"] = True
        enemy_stats["enemyattack"] = 10
        enemy_stats["enemydefense"] = 10
        enemy_stats["enemyagility"] = 8
        enemy_stats["enemymagic"] = 12
        enemy_stats["enemyweapon"] = 8
        enemy_stats["enemyarmor"] = 8
        enemy_stats["enemymagic"]weapon = 8
        enemy_stats["enemycharm"] = 8
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 21
        enemy_stats["xpdrop"] = 210
        enemy_stats["golddrop"] = 840
    elif choice == "5":
        enemy_stats["enemyname"] = "dragon"
        enemy_stats["enemybreath"] = True
        enemy_stats["enemyattack"] = 11
        enemy_stats["enemydefense"] = 11
        enemy_stats["enemyagility"] = 10
        enemy_stats["enemymagic"] = 10
        enemy_stats["enemyweapon"] = 10
        enemy_stats["enemyarmor"] = 10
        enemy_stats["enemymagic"]weapon = 10
        enemy_stats["enemycharm"] = 10
        enemy_stats["enemyhealth"] = 100
        enemy_stats["enemylevel"] = 22
        enemy_stats["xpdrop"] = 220
        enemy_stats["golddrop"] = 2200
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        platinumleague()
    combat_variables["firstturn"] = True
    combat()        
    
def shop():
    clear()
    print("""Welcome to my shop!

What would you like to buy?

1) Weapon

2) Armor

3) Magic Focus

4) Protection Charm

5) Spell Scrolls

6) Leave

""")
    choice = input()
    if choice == "1":
        weaponshop()
    elif choice == "2":
        armorshop()
    elif choice == "3":
        focusshop()
    elif choice == "4":
        charmshop()
    elif choice == "5":
        spellshop()
    else:
        town()

# the weapon shop has up to six items for sale for a pseudo-random price. only one is available at the beginning of the game but more are unlocked as the player gains levels.        
def weaponshop():
    global freshweapons
    global weapon
    global weaponname
    global gold
    global purchaseitem
    global itemvalue
    global itembonus
    global itemtype  
    global totalassets
    global resellitem
    global resellvalue
    global weaponvalue1
    global weaponvalue2
    global weaponvalue3
    global weaponvalue4
    global weaponvalue5
    global weaponvalue6
    global playerclass
    clear()
# players may get some many back when they sell their current weapon to purchase a new one

    if player_stats["weapon"] == 1:
        shop_variables["resellvalue"] = 5
    elif player_stats["weapon"] == 2:
        shop_variables["resellvalue"] = 25
    elif player_stats["weapon"] == 4:
        shop_variables["resellvalue"] = 125
    elif player_stats["weapon"] == 6:
        shop_variables["resellvalue"] = 750
    elif player_stats["weapon"] == 8:
        shop_variables["resellvalue"] = 2250
    elif player_stats["weapon"] == 10:
        shop_variables["resellvalue"] = 6000
    elif player_stats["weapon"] == 12:
        shop_variables["resellvalue"] = 15000
    else:
        shop_variables["resellvalue"] = 0
# players can actually trade in their old weapon to gain enough cash to buy the new weapon

    shop_variables["totalassets"] = shop_variables["resellvalue"] = + player_stats["gold"]
    shop_variables["resellitem"] = player_stats["weaponname"]
    print("What would you like to buy?\n")    
# the first time the player visits the store and at each level that is a multiple of 4, the prices for each available weapon are randomized

    if player_stats["freshweapons"]:
        player_stats["freshweapons"] = False
        item_values["weaponvalue1"] = randint(5,10)
        item_values["weaponvalue1"] = item_values["weaponvalue1"] * 5
        if player_stats["classlevel"] >= 4:
            item_values["weaponvalue2"] = randint(75,125)
            item_values["weaponvalue2"] = item_values["weaponvalue2"] // 2
            item_values["weaponvalue2"] = item_values["weaponvalue2"] * 5
        if player_stats["classlevel"] >= 8:
            item_values["weaponvalue3"] = randint(75,125)
            item_values["weaponvalue3"] = item_values["weaponvalue3"] // 2
            item_values["weaponvalue3"] = item_values["weaponvalue3"] * 15
        if player_stats["classlevel"] >= 12:            
            item_values["weaponvalue4"] = randint(75,125)
            item_values["weaponvalue4"] = item_values["weaponvalue4"] // 2
            item_values["weaponvalue4"] = item_values["weaponvalue4"] * 45
        if player_stats["classlevel"] >= 16:
            item_values["weaponvalue5"] = randint(75,125)
            item_values["weaponvalue5"] = item_values["weaponvalue5"] // 2
            item_values["weaponvalue5"] = item_values["weaponvalue5"] * 120
        if player_stats["classlevel"] >= 20:
            item_values["weaponvalue6"] = randint(75,125)
            item_values["weaponvalue6"] = item_values["weaponvalue6"] // 2
            item_values["weaponvalue6"] = item_values["weaponvalue6"] * 350
# the default weapons
    player_stats["weaponslot1"] = "short sword"
    player_stats["weaponslot2"] = "long sword"    
    player_stats["weaponslot3"] = "broad sword"
    player_stats["weaponslot4"] = "great sword"
    player_stats["weaponslot5"] = "mithril sword"
    player_stats["weaponslot6"] = "rune blade"
# some classes have their weapons "re-skinned" to fit their style
    if player_stats["playerclass"] == "rogue":
        player_stats["weaponslot3"] = "scimitar"
        player_stats["weaponslot4"] = "twin-blade"
        player_stats["weaponslot5"] = "ninja blade"
    if player_stats["playerclass"] == "bard" or player_stats["playerclass"] == "mage":
        player_stats["weaponslot3"] = "elven blade"
        player_stats["weaponslot4"] = "ancient sword"
    if player_stats["playerclass"] == "cleric":
        player_stats["weaponslot1"] = "mace"
        player_stats["weaponslot2"] = "warhammer"
        player_stats["weaponslot3"] = "flail"
        player_stats["weaponslot4"] = "great hammer"
        player_stats["weaponslot5"] = "mithril mace"
        player_stats["weaponslot6"] = "lawbringer"        
# the store displays the weapons that are currently available and how much they cost
    print(f'1) {player_stats["weaponslot1"]} {item_values["weaponvalue1"]} gold')
    if player_stats["classlevel"] >= 4:
        print(f'2) {player_stats["weaponslot2"]} {item_values["weaponvalue2"]} gold')
    if player_stats["classlevel"] >= 8:
        print(f'3) {player_stats["weaponslot3"]} {item_values["weaponvalue3"]} gold')
    if player_stats["classlevel"] >= 12:
        print(f'4) {player_stats["weaponslot4"]} {item_values["weaponvalue4"]} gold')
    if player_stats["classlevel"] >= 16:
        print(f'5) {player_stats["weaponslot5"]} {item_values["weaponvalue5"]} gold')
    if player_stats["classlevel"] >= 20:
        print(f'6) {player_stats["weaponslot6"]} {item_values["weaponvalue6"]} gold')
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    shop_variables["itemtype"] = "weapon"
    if choice == "1":
        shop_variables["purchaseitem"] = player_stats["weaponslot1"]
        shop_variables["itemvalue"] = item_values["weaponvalue1"]
        shop_variables["itembonus"] = 2                
# [and] statements prevent the game from crashing
    elif choice == "2" and player_stats["classlevel"] >= 4:
        shop_variables["purchaseitem"] = player_stats["weaponslot2"]
        shop_variables["itemvalue"] = item_values["weaponvalue2"]
        shop_variables["itembonus"] = 4
    elif choice == "3" and player_stats["classlevel"] >= 8:
        shop_variables["purchaseitem"] = player_stats["weaponslot3"]
        shop_variables["itemvalue"] = item_values["weaponvalue3"]
        shop_variables["itembonus"] = 6
    elif choice == "4" and player_stats["classlevel"] >= 12:
        shop_variables["purchaseitem"] = player_stats["weaponslot4"]
        shop_variables["itemvalue"] = item_values["weaponvalue4"]
        shop_variables["itembonus"] = 8
    elif choice == "5" and player_stats["classlevel"] >= 16:
        shop_variables["purchaseitem"] = player_stats["weaponslot5"]
        shop_variables["itemvalue"] = item_values["weaponvalue5"]
        shop_variables["itembonus"] = 10
    elif choice == "6" and player_stats["classlevel"] >= 20:
        shop_variables["purchaseitem"] = player_stats["weaponslot6"]
        shop_variables["itemvalue"] = item_values["weaponvalue6"]
        shop_variables["itembonus"] = 12
    else:
        shop()
    confirmpurchase()

# the armor shop uses pretty well the same code as the weapon shop with some different variables    
def armorshop():
    global fresharmor
    global armor
    global armorname
    global gold
    global purchaseitem
    global itemvalue
    global itembonus
    global itemtype  
    global totalassets
    global resellitem
    global resellvalue
    global armorvalue1
    global item_values["armorvalue2"]
    global item_values["armorvalue3"]
    global item_values["armorvalue4"]
    global item_values["armorvalue5"]
    global item_values["armorvalue6"]
    global playerclass
    clear()
    if player_stats["armor"] == 1:
        shop_variables["resellvalue"] = 5
    elif player_stats["armor"] == 2:
        shop_variables["resellvalue"] = 25
    elif player_stats["armor"] == 4:
        shop_variables["resellvalue"] = 125
    elif player_stats["armor"] == 6:
        shop_variables["resellvalue"] = 750
    elif player_stats["armor"] == 8:
        shop_variables["resellvalue"] = 2250
    elif player_stats["armor"] == 10:
        shop_variables["resellvalue"] = 6000
    elif player_stats["armor"] == 12:
        shop_variables["resellvalue"] = 15000
    else:
        shop_variables["resellvalue"] = 0
    shop_variables["totalassets"] = shop_variables["resellvalue"] + player_stats["gold"]
    shop_variables["resellitem"] = player_stats["armorname"]
    print("What would you like to buy?\n")    
    if player_stats["fresharmor"]:
        player_stats["fresharmor"] = False
        item_values["armorvalue1"] = randint(5,10)
        item_values["armorvalue1"] = item_values["armorvalue1"] * 5
        if player_stats["classlevel"] >= 4:
            item_values["armorvalue2"] = randint(75,125)
            item_values["armorvalue2"] = item_values["armorvalue2"] // 2
            item_values["armorvalue2"] = item_values["armorvalue2"] * 5
        if player_stats["classlevel"] >= 8:
            item_values["armorvalue3"] = randint(75,125)
            item_values["armorvalue3"] = item_values["armorvalue3"] // 2
            item_values["armorvalue3"] = item_values["armorvalue3"] * 15
        if player_stats["classlevel"] >= 12:            
            item_values["armorvalue4"] = randint(75,125)
            item_values["armorvalue4"] = item_values["armorvalue4"] // 2
            item_values["armorvalue4"] = item_values["armorvalue4"] * 45
        if player_stats["classlevel"] >= 16:
            item_values["armorvalue5"] = randint(75,125)
            item_values["armorvalue5"] = item_values["armorvalue5"] // 2
            item_values["armorvalue5"] = item_values["armorvalue5"] * 120
        if player_stats["classlevel"] >= 20:
            item_values["armorvalue6"] = randint(75,125)
            item_values["armorvalue6"] = item_values["armorvalue6"] // 2
            item_values["armorvalue6"] = item_values["armorvalue6"] * 350
    armorslot1 = "leather"
    armorslot2 = "ring mail"    
    armorslot3 = "chain mail"
    armorslot4 = "plate mail"
    armorslot5 = "mithril"
    armorslot6 = "dragon scale"
    if player_stats["playerclass"] == "rogue":
        armorslot2 = "studded leather"
        armorslot3 = "elven cloak"
        armorslot4 = "magic cloak"
        armorslot5 = "ninja"
        armorslot6 = "shadow cloak"
    if player_stats["playerclass"] == "bard" or player_stats["playerclass"] == "mage":
        armorslot4 = "elven chain mail"
        armorslot5 = "mithril vest"
        armorslot6 = "dragon scale cape"
    if player_stats["playerclass"] == "mage":
        armorslot1 = "apprentice robe"
        armorslot2 = "heavy robe"
        armorslot3 = "wizard robe"
        armorslot4 = "magic robe"
        armorslot5 = "sage robe"
        armorslot6 = "aegis robe"        
    print(f"1) {armorslot1} {item_values["armorvalue1"]} gold")
    if player_stats["classlevel"] >= 4:
        print(f"2) {armorslot2} {item_values["armorvalue2"]} gold")
    if player_stats["classlevel"] >= 8:
        print(f"3) {armorslot3} {item_values["armorvalue3"]} gold")
    if player_stats["classlevel"] >= 12:
        print(f"4) {armorslot4} {item_values["armorvalue4"]} gold")
    if player_stats["classlevel"] >= 16:
        print(f"5) {armorslot5} {item_values["armorvalue5"]} gold")
    if player_stats["classlevel"] >= 20:
        print(f"6) {armorslot6} {item_values["armorvalue6"]} gold")
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    shop_variables["itemtype"] = "armor"
    if choice == "1":
        shop_variables["purchaseitem"] = armorslot1
        shop_variables["itemvalue"] = item_values["armorvalue1"]
        shop_variables["itembonus"] = 2                
    elif choice == "2" and player_stats["classlevel"] >= 4:
        shop_variables["purchaseitem"] = armorslot2
        shop_variables["itemvalue"] = item_values["armorvalue2"]
        shop_variables["itembonus"] = 4
    elif choice == "3" and player_stats["classlevel"] >= 8:
        shop_variables["purchaseitem"] = armorslot3
        shop_variables["itemvalue"] = item_values["armorvalue3"]
        shop_variables["itembonus"] = 6
    elif choice == "4" and player_stats["classlevel"] >= 12:
        shop_variables["purchaseitem"] = armorslot4
        shop_variables["itemvalue"] = item_values["armorvalue4"]
        shop_variables["itembonus"] = 8
    elif choice == "5" and player_stats["classlevel"] >= 16:
        shop_variables["purchaseitem"] = armorslot5
        shop_variables["itemvalue"] = item_values["armorvalue5"]
        shop_variables["itembonus"] = 10
    elif choice == "6" and player_stats["classlevel"] >= 20:
        shop_variables["purchaseitem"] = armorslot6
        shop_variables["itemvalue"] = item_values["armorvalue6"]
        shop_variables["itembonus"] = 12
    else:
        shop()
    confirmpurchase()    
    
# the magic weapon shop uses pretty well the same code as the weapon shop with some different variables    
def focusshop():
    global freshmagicweapons
    global magicweapon
    global magicweaponname
    global gold
    global purchaseitem
    global itemvalue
    global shop_variables["itembonus"]
    global shop_variables["itemtype"]  
    global shop_variables["totalassets"]
    global shop_variables["resellitem"]
    global shop_variables["resellvalue"]
    global item_values["mweaponvalue1"]
    global item_values["mweaponvalue2"]
    global item_values["mweaponvalue3"]
    global item_values["mweaponvalue4"]
    global item_values["mweaponvalue5"]
    global item_values["mweaponvalue6"]
    global playerclass
    clear()
    if player_stats["magicweapon"] == 1:
        shop_variables["resellvalue"] = 5
    elif player_stats["magicweapon"] == 2:
        shop_variables["resellvalue"] = 25
    elif player_stats["magicweapon"] == 4:
        shop_variables["resellvalue"] = 125
    elif player_stats["magicweapon"] == 6:
        shop_variables["resellvalue"] = 750
    elif player_stats["magicweapon"] == 8:
        shop_variables["resellvalue"] = 2250
    elif player_stats["magicweapon"] == 10:
        shop_variables["resellvalue"] = 6000
    elif player_stats["magicweapon"] == 12:
        shop_variables["resellvalue"] = 15000
    else:
        shop_variables["resellvalue"] = 0
    shop_variables["totalassets"] = shop_variables["resellvalue"] + player_stats["gold"]
    shop_variables["resellitem"] = player_stats["magicweaponname"]
    print("What would you like to buy?\n")    
    if player_stats["freshmagicweapons"]:
        player_stats["freshmagicweapons"] = False
        item_values["mweaponvalue1"] = randint(5,10)
        item_values["mweaponvalue1"] = item_values["mweaponvalue1"] * 5
        if player_stats["classlevel"] >= 4:
            item_values["mweaponvalue2"] = randint(75,125)
            item_values["mweaponvalue2"] = item_values["mweaponvalue2"] // 2
            item_values["mweaponvalue2"] = item_values["mweaponvalue2"] * 5
        if player_stats["classlevel"] >= 8:
            item_values["mweaponvalue3"] = randint(75,125)
            item_values["mweaponvalue3"] = item_values["mweaponvalue3"] // 2
            item_values["mweaponvalue3"] = item_values["mweaponvalue3"] * 15
        if player_stats["classlevel"] >= 12:            
            item_values["mweaponvalue4"] = randint(75,125)
            item_values["mweaponvalue4"] = item_values["mweaponvalue4"] // 2
            item_values["mweaponvalue4"] = item_values["mweaponvalue4"] * 45
        if player_stats["classlevel"] >= 16:
            item_values["mweaponvalue5"] = randint(75,125)
            item_values["mweaponvalue5"] = item_values["mweaponvalue5"] // 2
            item_values["mweaponvalue5"] = item_values["mweaponvalue5"] * 120
        if player_stats["classlevel"] >= 20:
            item_values["mweaponvalue6"] = randint(75,125)
            item_values["mweaponvalue6"] = item_values["mweaponvalue6"] // 2
            item_values["mweaponvalue6"] = item_values["mweaponvalue6"] * 350
    mweaponslot1 = "oak wand"
    mweaponslot2 = "rowan wand"    
    mweaponslot3 = "ash wand"
    mweaponslot4 = "crystal wand"
    mweaponslot5 = "master wand"
    mweaponslot6 = "elder wand"
    if player_stats["playerclass"] == "cleric":
        mweaponslot1 = "oak staff"
        mweaponslot2 = "rowan staff"    
        mweaponslot3 = "holy staff"
        mweaponslot4 = "sage staff"
        mweaponslot5 = "blessed staff"
        mweaponslot6 = "staff of light" 
    if player_stats["playerclass"] == "mage":
        mweaponslot1 = "oak staff"
        mweaponslot2 = "rowan staff"    
        mweaponslot3 = "wizard staff"
        mweaponslot4 = "sage staff"
        mweaponslot5 = "staff of the magus"
        mweaponslot6 = "starlight staff"       
# the store displays the weapons that are currently available and how much they cost
    print(f"1) {mweaponslot1} {item_values["mweaponvalue1"]} gold")
    if player_stats["classlevel"] >= 4:
        print(f"2) {mweaponslot2} {item_values["mweaponvalue2"]} gold")
    if player_stats["classlevel"] >= 8:
        print(f"3) {mweaponslot3} {item_values["mweaponvalue3"]} gold")
    if player_stats["classlevel"] >= 12:
        print(f"4) {mweaponslot4} {item_values["mweaponvalue4"]} gold")
    if player_stats["classlevel"] >= 16:
        print(f"5) {mweaponslot5} {item_values["mweaponvalue5"]} gold")
    if player_stats["classlevel"] >= 20:
        print(f"6) {mweaponslot6} {item_values["mweaponvalue6"]} gold")
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    shop_variables["itemtype"] = "mweapon"
    if choice == "1":
        shop_variables["purchaseitem"] = mweaponslot1
        shop_variables["itemvalue"] = item_values["mweaponvalue1"]
        shop_variables["itembonus"] = 2                
    elif choice == "2" and player_stats["classlevel"] >= 4:
        shop_variables["purchaseitem"] = mweaponslot2
        shop_variables["itemvalue"] = item_values["mweaponvalue2"]
        shop_variables["itembonus"] = 4
    elif choice == "3" and player_stats["classlevel"] >= 8:
        shop_variables["purchaseitem"] = mweaponslot3
        shop_variables["itemvalue"] = item_values["mweaponvalue3"]
        shop_variables["itembonus"] = 6
    elif choice == "4" and player_stats["classlevel"] >= 12:
        shop_variables["purchaseitem"] = mweaponslot4
        shop_variables["itemvalue"] = item_values["mweaponvalue4"]
        shop_variables["itembonus"] = 8
    elif choice == "5" and player_stats["classlevel"] >= 16:
        shop_variables["purchaseitem"] = mweaponslot5
        shop_variables["itemvalue"] = item_values["mweaponvalue5"]
        shop_variables["itembonus"] = 10
    elif choice == "6" and player_stats["classlevel"] >= 20:
        shop_variables["purchaseitem"] = mweaponslot6
        shop_variables["itemvalue"] = item_values["mweaponvalue6"]
        shop_variables["itembonus"] = 12
    else:
        shop()
    confirmpurchase()    

def charmshop():
    global freshcharms
    global charm
    global charmname
    global gold
    global purchaseitem
    global itemvalue
    global shop_variables["itembonus"]
    global shop_variables["itemtype"]  
    global shop_variables["totalassets"]
    global shop_variables["resellitem"]
    global shop_variables["resellvalue"]
    global item_values["charmvalue1"]
    global item_values["charmvalue2"]
    global item_values["charmvalue3"]
    global item_values["charmvalue4"]
    global item_values["charmvalue5"]
    global item_values["charmvalue6"]
    global playerclass
    clear()
    if player_stats["charm"] == 1:
        shop_variables["resellvalue"] = 5
    elif player_stats["charm"] == 2:
        shop_variables["resellvalue"] = 25
    elif player_stats["charm"] == 4:
        shop_variables["resellvalue"] = 125
    elif player_stats["charm"] == 6:
        shop_variables["resellvalue"] = 750
    elif player_stats["charm"] == 8:
        shop_variables["resellvalue"] = 2250
    elif player_stats["charm"] == 10:
        shop_variables["resellvalue"] = 6000
    elif player_stats["charm"] == 12:
        shop_variables["resellvalue"] = 15000
    else:
        shop_variables["resellvalue"] = 0
    shop_variables["totalassets"] = shop_variables["resellvalue"] + player_stats["gold"]
    shop_variables["resellitem"] = player_stats["magicweaponname"]
    print("What would you like to buy?\n")    
    if player_stats["freshcharms"]:
        player_stats["freshcharms"] = False
        item_values["charmvalue1"] = randint(5,10)
        item_values["charmvalue1"] = item_values["charmvalue1"] * 5
        if player_stats["classlevel"] >= 4:
            item_values["charmvalue2"] = randint(75,125)
            item_values["charmvalue2"] = item_values["charmvalue2"] // 2
            item_values["charmvalue2"] = item_values["charmvalue2"] * 5
        if player_stats["classlevel"] >= 8:
            item_values["charmvalue3"] = randint(75,125)
            item_values["charmvalue3"] = item_values["charmvalue3"] // 2
            item_values["charmvalue3"] = item_values["charmvalue3"] * 15
        if player_stats["classlevel"] >= 12:            
            item_values["charmvalue4"] = randint(75,125)
            item_values["charmvalue4"] = item_values["charmvalue4"] // 2
            item_values["charmvalue4"] = item_values["charmvalue4"] * 45
        if player_stats["classlevel"] >= 16:
            item_values["charmvalue5"] = randint(75,125)
            item_values["charmvalue5"] = item_values["charmvalue5"] // 2
            item_values["charmvalue5"] = item_values["charmvalue5"] * 120
        if player_stats["classlevel"] >= 20:
            item_values["charmvalue6"] = randint(75,125)
            item_values["charmvalue6"] = item_values["charmvalue6"] // 2
            item_values["charmvalue6"] = item_values["charmvalue6"] * 350
    charmslot1 = "copper ring"
    charmslot2 = "iron ring"    
    charmslot3 = "sapphire ring"
    charmslot4 = "garnet ring"
    charmslot5 = "opal ring"
    charmslot6 = "jade ring"
    if player_stats["playerclass"] == "cleric" or player_stats["playerclass"] == "mage":
        charmslot1 = "amulet of protection"
        charmslot2 = "talisman"    
        charmslot3 = "sapphire pendant"
        charmslot4 = "garnet pendant"
        charmslot5 = "opal pendant"
        charmslot6 = "jade pendant" 
    print(f"1) {charmslot1} {item_values["charmvalue1"]} gold")
    if player_stats["classlevel"] >= 4:
        print(f"2) {charmslot2} {item_values["charmvalue2"]} gold")
    if player_stats["classlevel"] >= 8:
        print(f"3) {charmslot3} {item_values["charmvalue3"]} gold")
    if player_stats["classlevel"] >= 12:
        print(f"4) {charmslot4} {item_values["charmvalue4"]} gold")
    if player_stats["classlevel"] >= 16:
        print(f"5) {charmslot5} {item_values["charmvalue5"]} gold")
    if player_stats["classlevel"] >= 20:
        print(f"6) {charmslot6} {item_values["charmvalue6"]} gold")
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    shop_variables["itemtype"] = "charm"
    if choice == "1":
        shop_variables["purchaseitem"] = charmslot1
        shop_variables["itemvalue"] = item_values["charmvalue1"]
        shop_variables["itembonus"] = 2                
    elif choice == "2" and player_stats["classlevel"] >= 4:
        shop_variables["purchaseitem"] = charmslot2
        shop_variables["itemvalue"] = item_values["charmvalue2"]
        shop_variables["itembonus"] = 4
    elif choice == "3" and player_stats["classlevel"] >= 8:
        shop_variables["purchaseitem"] = charmslot3
        shop_variables["itemvalue"] = item_values["charmvalue3"]
        shop_variables["itembonus"] = 6
    elif choice == "4" and player_stats["classlevel"] >= 12:
        shop_variables["purchaseitem"] = charmslot4
        shop_variables["itemvalue"] = item_values["charmvalue4"]
        shop_variables["itembonus"] = 8
    elif choice == "5" and player_stats["classlevel"] >= 16:
        shop_variables["purchaseitem"] = charmslot5
        shop_variables["itemvalue"] = item_values["charmvalue5"]
        shop_variables["itembonus"] = 10
    elif choice == "6" and player_stats["classlevel"] >= 20:
        shop_variables["purchaseitem"] = charmslot6
        shop_variables["itemvalue"] = item_values["charmvalue6"]
        shop_variables["itembonus"] = 12
    else:
        shop()
    confirmpurchase()     

def spellshop():
    clear()
    print("This is placeholder text. The spell shop is not done yet!\n")
    input()
    shop()
    
# this function resolves purchases from the weapon, armor, magic weapon, and charm stores, which is why it has so many global variables    
def confirmpurchase():
    global slotchosen 
    if shop_variables["itemvalue"] > shop_variables["totalassets"]:
        print("You don't have enough gold!\n")
        input()
        shop()
    else:
        if shop_variables["resellvalue"] > 0:
            print(f'The {shop_variables["purchaseitem"]}? Then I will buy your {shop_variables["resellitem"]} for {shop_variables["resellvalue"]} gold.\n')
            print("Deal?\n")
        else:
            print(f'The {shop_variables["purchaseitem"]}? Are you sure?\n')            
        choice = input()
        clear()
        if choice == "y" or choice == "yes":
            if shop_variables["itemtype"] == "weapon":
                player_stats["weaponname"] = shop_variables["purchaseitem"]
                player_stats["weapon"] = shop_variables["itembonus"]
                player_stats["gold"] -= shop_variables["itemvalue"]
                player_stats["gold"] += shop_variables["resellvalue"]
            elif shop_variables["itemtype"] == "armor":
                player_stats["armorname"] = shop_variables["purchaseitem"]
                player_stats["armor"] = shop_variables["itembonus"]
                player_stats["gold"] -= shop_variables["itemvalue"]
                player_stats["gold"] += shop_variables["resellvalue"]
            elif shop_variables["itemtype"] == "mweapon":
                player_stats["magicweaponname"] = shop_variables["purchaseitem"]
                player_stats["magicweapon"] = shop_variables["itembonus"]
                player_stats["gold"] -= shop_variables["itemvalue"]
                player_stats["gold"] += shop_variables["resellvalue"]
            elif shop_variables["itemtype"] == "charm":
                player_stats["charmname"] = shop_variables["purchaseitem"]
                player_stats["charm"] = shop_variables["itembonus"]
                player_stats["gold"] -= shop_variables["itemvalue"]
                player_stats["gold"] += shop_variables["resellvalue"]
            elif shop_variables["itemtype"] == "spell":
                if slotchosen == 1:
                    player_stats["spellslot1"] = shop_variables["purchaseitem"]
                elif slotchosen == 2:
                    player_stats["spellslot2"] = shop_variables["purchaseitem"]
                elif slotchosen == 3:
                    player_stats["spellslot3"] = shop_variables["purchaseitem"]
                elif slotchosen == 4:
                    player_stats["spellslot4"] = shop_variables["purchaseitem"]
                player_stats["gold"] -= shop_variables["itemvalue"]
                player_stats["gold"] += shop_variables["resellvalue"]
            print("Thank you! Please shop here again.\n")
            print("Press (enter) to continue\n")
            input()
            town()                             
        else:
            print("That's too bad! Come back when you are ready to make this purchase.\n")
            print("Press (enter) to continue\n")
            input()
            town()    
        
def combat():
    global attack
    global defense
    global agility
    global magic
    global heritage
    global playerclass
    global playername
    global classlevel
    global effectivelevel
    global weaponname
    global weapon
    global armorname
    global armor
    global magicweaponname
    global magicweapon
    global charmname
    global charm
    global spellslot1
    global spellslot2
    global spellslot3
    global spellslot4
    global health
    global enemy_stats["enemyname"]
    global enemy_stats["enemybreath"]
    global enemy_stats["enemycancast"]
    global enemy_stats["enemycanheal"]
    global enemy_stats["enemyattack"] 
    global enemy_stats["enemydefense"] 
    global enemy_stats["enemyagility"] 
    global enemy_stats["enemymagic"] 
    global enemy_stats["enemyweapon"] 
    global enemy_stats["enemyarmor"] 
    global enemy_stats["enemyhealth"] 
    global enemy_stats["enemylevel"] 
    global enemy_stats["xpdrop"]    
    global enemy_stats["golddrop"]
    global combat_variables["firstturn"]
    global action
    global combat_variables["playerturn"]
    global sneak
    global keylogging
    global combat_variables["woundpenalty"]
    global enemy_stats["enemywound"]
    global combat_variables["magicmenu"]
    global combat_variables["incombat"]
    global enemy_stats["enemysleepcounter"]
    keylogging = True
    combat_variables["incombat"] = True
    # see who goes first
    if combat_variables["firstturn"]:
        enemy_stats["enemysleepcounter"] = 0
        clear()
        print(f"A {enemy_stats["enemyname"]} appears!\n")
        combat_variables["firstturn"] = False
        initiative = randint(1,20)
        if player_stats["playerclass"] == "rogue":
            if initiative <= 2:
                initiative = randint(1,20)
                print("Rogue reroll!")
        initiative += player_stats["agility"]
        enemyinitiative = 10
        enemyinitiative += enemy_stats["enemyagility"]
        if initiative < enemyinitiative:
            print(f"The {enemy_stats["enemyname"]} attacks before you are ready!\n")
            combat_variables["playerturn"] = False
            combat()
        elif initiative <= enemyinitiative + 5:
            print(f"You strike first before the {enemy_stats["enemyname"]}!\n")
            combat_variables["playerturn"] = True
            input("Press (enter) to continue\n")
            combat()
        else:
            print(f"You sneak up on the {enemy_stats["enemyname"]}!\n")
            combat_variables["playerturn"] = True
            combat_variables["sneak"] = True
            input("Press (enter) to continue\n")
            combat()
# player's turn starts here        
    if combat_variables["playerturn"]:
        if enemy_stats["enemyhealth"] < 30:
            enemy_stats["enemywound"] = "severely "
        elif enemy_stats["enemyhealth"] < 55:
            enemy_stats["enemywound"] = ""
        elif enemy_stats["enemyhealth"] < 80:
            enemy_stats["enemywound"] = "somewhat "
        elif enemy_stats["enemyhealth"] < 100:
            enemy_stats["enemywound"] = "barely "
        else:
            enemy_stats["enemywound"] = "not "
        if player_stats["health"] < 30:
            combat_variables["woundpenalty"] = 3
        elif player_stats["health"] < 55:
            combat_variables["woundpenalty"] = 2
        elif player_stats["health"] < 80:
            combat_variables["woundpenalty"] = 1
        else:
            combat_variables["woundpenalty"] = 0
        clear()
        print(f"""{player_stats["playername"]} the {player_stats["heritage"]} {player_stats["playerclass"]} (Lvl: {player_stats["classlevel"]})
Health: {player_stats["health"]}%

You are fighting a {enemy_stats["enemyname"]}. It is {enemy_stats["enemywound"]}wounded.

             ^
           Fight
        
<Magic    Command?    Item> 
         
            Run
             v
        """)
        print("It's your turn. Choose a command.\n")  
# player chooses attack        
        if action == "N":
            action = ""
            combat_variables["playerturn"] = False 
            keylogging = False
            print(f"You attack the {enemy_stats["enemyname"]}!")
            attackroll = randint(1,20)
            if combat_variables["sneak"] or enemy_stats["enemysleepcounter"] >= 1:
                attackroll2 = randint(1,20)
                if attackroll2 > attackroll:
                    attackroll = attackroll2 
                combat_variables["sneak"] = False
                if enemy_stats["enemysleepcounter"] >= 1:
                    enemy_stats["enemysleepcounter"] = 1
            if player_stats["playerclass"] == "warrior":
                if attackroll <= 2:
                    attackroll = randint(1,20)
                    print("Warrior reroll!")
            attackroll += player_stats["attack"]
            attackroll += player_stats["weapon"]
            attackroll -= combat_variables["woundpenalty"]
            combatdefense = 10
            combatdefense += enemy_stats["enemydefense"]
            combatdefense += enemy_stats["enemyarmor"]
            if attackroll < combatdefense:
                print(f"You roll a {attackroll} to hit {combatdefense}. A miss!\n")
                combat_variables["playerturn"] = False
                combat()
            else:
                damage = attackroll - combatdefense + 1
                damage = damage * 5
                print(f"You roll a {attackroll} to hit {combatdefense}, hitting for {damage}% damage!\n")
                enemy_stats["enemyhealth"] -= damage
                if enemy_stats["enemyhealth"] <= 0:
                    print(f"You have killed the {enemy_stats["enemyname"]}!\n")
                    input("Press (enter) to continue\n")
                    checkxp()            
                else:
                    combat_variables["playerturn"] = False
                    combat()

# player chooses magic                    
        elif action == "W":
            action = ""  
            combat_variables["magicmenu"] = True
            combat_variables["playerturn"] = False
            battlemagic()
                    
# enemy's turn                    
    if not combat_variables["playerturn"] and not combat_variables["magicmenu"]:
        combat_variables["playerturn"] = True
        keylogging = False
        if enemy_stats["enemyhealth"] < 30:
            combat_variables["woundpenalty"] = 3
        elif enemy_stats["enemyhealth"] < 55:
            combat_variables["woundpenalty"] = 2
        elif enemy_stats["enemyhealth"] < 80:
            combat_variables["woundpenalty"] = 1
        else:
            combat_variables["woundpenalty"] = 0

        # check to see if enemy is asleep
        if enemy_stats["enemysleepcounter"] >= 1:
            enemy_stats["enemysleepcounter"] -= 1
            if enemy_stats["enemysleepcounter"] <= 0:
                print(f"The {enemy_stats["enemyname"]} wakes up!")
            else: 
                print(f"The {enemy_stats["enemyname"]} is still asleep!")
            input("\nPress (enter) to continue\n")
            combat()

        # some enemies will heal themselves when they are badly wounded    
        elif enemy_stats["enemycanheal"]:
            castchance = randint(1,2)
            if castchance == 2 and enemy_stats["enemyhealth"] <= 50:                
                print(f"The {enemy_stats["enemyname"]} casts a healing spell!")
                attackroll = randint(1,20)
                attackroll += enemy_stats["enemymagic"]
                attackroll += enemy_stats["enemycharm"]
                attackroll -= combat_variables["woundpenalty"]
                combatdefense = 10
                combatdefense += player_stats["magic"]
                combatdefense += player_stats["charm"]
                if attackroll < combatdefense:
                    print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} against a target of {combatdefense}. The spell doesn't work!\n")
                    input("Press (enter) to continue\n")
                    combat()
                else:
                    damage = attackroll - combatdefense + 1
                    damage = damage * 5
                    print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} against a target of {combatdefense}. The spell heals {damage}% damage!\n")
                    enemy_stats["enemyhealth"] += damage
                    if enemy_stats["enemyhealth"] > 100:
                        enemy_stats["enemyhealth"] = 100
                    input("Press (enter) to continue\n")
                    combat()  
            
        # some enemies use magic to attack           
        elif enemy_stats["enemycancast"]:
            castchance = randint(1,5)
            if castchance <= 4:                
                print(f"The {enemy_stats["enemyname"]} casts a spell on you!")
                attackroll = randint(1,20)
                # clerics have a defense bonus against attacks of a magical nature
                if player_stats["playerclass"] == "cleric":
                    if attackroll >= 19:
                        attackroll = randint(1,20)
                        print("Cleric reroll!")  
                attackroll += enemy_stats["enemymagic"]
                attackroll += enemy_stats["enemymagic"]weapon
                attackroll -= combat_variables["woundpenalty"]
                combatdefense = 10
                combatdefense += player_stats["magic"]
                combatdefense += player_stats["charm"]
                if attackroll < combatdefense:
                    print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} to hit {combatdefense}. You resist the spell!\n")
                    input("Press (enter) to continue\n")
                    combat()
                else:
                    damage = attackroll - combatdefense + 1
                    damage = damage * 5
                    print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} to hit {combatdefense}. The spell causes {damage}% damage!\n")
                    player_stats["health"] -= damage
                    if player_stats["health"] <= 0:
                        print(f"You were killed by the {enemy_stats["enemyname"]}!\n")
                        quit()
                    else:
                        input("Press (enter) to continue\n")
                        combat()                   
            else:
                enemyphysicalattack()
   
        # certain enemies breathe fire
        elif enemy_stats["enemybreath"]:
            breathchance = randint(1,2)
            if breathchance == 1:
                print(f"The {enemy_stats["enemyname"]} uses its breath attack on you!")
                attackroll = randint(1,20)
                # clerics have a defense bonus against attacks of a magical nature
                if player_stats["playerclass"] == "cleric":
                    if attackroll >= 19:
                        attackroll = randint(1,20)
                        print("Cleric reroll!")  
                attackroll += enemy_stats["enemyattack"]
                attackroll += enemy_stats["enemyweapon"]
                attackroll -= combat_variables["woundpenalty"]
                combatdefense = 10
                combatdefense += player_stats["magic"]
                combatdefense += player_stats["charm"]
                if attackroll < combatdefense:
                    print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} to hit {combatdefense}. You dodge its breath attack!\n")
                    combat_variables["playerturn"] = True
                    input("Press (enter) to continue\n")
                    combat()
                else:
                    damage = attackroll - combatdefense + 1
                    damage = damage * 5
                    print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} to hit {combatdefense}. You are hit for {damage}% damage!\n")
                    player_stats["health"] -= damage
                    if player_stats["health"] <= 0:
                        print(f"You were killed by the {enemy_stats["enemyname"]}!\n")
                        quit()
                    else:
                        input("Press (enter) to continue\n")
                        combat()                   
            else:
                enemyphysicalattack()
        else:
            enemyphysicalattack()
            
def enemyphysicalattack():
    global defense
    global armor
    global health
    global enemy_stats["enemyname"]
    global enemy_stats["enemyattack"] 
    global enemy_stats["enemyweapon"] 
    global action
    global combat_variables["playerturn"]    
    print(f"The {enemy_stats["enemyname"]} attacks!\n")
    attackroll = randint(1,20)
    # bards have a defense bonus for being lucky
    if player_stats["playerclass"] == "bard":
        if attackroll >= 19:
            attackroll = randint(1,20)
            print("Bard reroll!")  
    attackroll += enemy_stats["enemyattack"]
    attackroll += enemy_stats["enemyweapon"]
    attackroll -= combat_variables["woundpenalty"]
    combatdefense = 10
    combatdefense += player_stats["defense"]
    combatdefense += player_stats["armor"]
    if attackroll < combatdefense:
        print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} to hit {combatdefense}. A miss!\n")
        input("Press (enter) to continue\n")
        combat()
    else:
        damage = attackroll - combatdefense + 1
        damage = damage * 5
        print(f"The {enemy_stats["enemyname"]} rolls a {attackroll} to hit {combatdefense}, hitting for {damage}% damage!\n")
        player_stats["health"] -= damage
        if player_stats["health"] <= 0:
            print(f"You were killed by the {enemy_stats["enemyname"]}!\n")
            quit()
        else:
            input("Press (enter) to continue\n")
            combat() 

def battlemagic():
    global playername
    global heritage
    global playerclass
    global classlevel
    global health
    global enemy_stats["enemyhealth"]
    global spellslot1
    global spellslot2
    global spellslot3
    global spellslot4
    global magic
    global magicweapon
    global enemy_stats["enemyname"]
    global enemy_stats["enemymagic"]
    global enemy_stats["enemycharm"]
    global combat_variables["woundpenalty"]
    global enemy_stats["enemywound"]
    global action
    global combat_variables["playerturn"]
    global keylogging
    global combat_variables["magicmenu"]
    keylogging = True
    if combat_variables["magicmenu"]:
        clear()
        print(f"""{player_stats["playername"]} the {player_stats["heritage"]} {player_stats["playerclass"]} (Lvl: {player_stats["classlevel"]})
Health: {player_stats["health"]}%

You are fighting a {enemy_stats["enemyname"]}. It is {enemy_stats["enemywound"]}wounded.

                ^
             {player_stats["spellslot1"]}

<{player_stats["spellslot2"]}     Spell ?    {player_stats["spellslot3"]}> 

             {player_stats["spellslot4"]}
                v
        """)
        print("Press (enter) to cancel.\n")  
    # player tries to cast the spell in slot 1        
        if action == "N":
            action = ""
            combat_variables["magicmenu"] = False
            castspellslot1()
            
        elif action == "RETURN":
            combat_variables["playerturn"] = True
            combat_variables["magicmenu"] = False
            combat()
    else:
        combat_variables["playerturn"] = True
        combat()
        
def castspellslot1():
    global spellslot1
    global enemy_stats["enemyname"]
    global sneak
    global playerclass
    global magic
    global magicweapon
    global enemy_stats["enemymagic"]
    global enemy_stats["enemycharm"]
    global enemy_stats["enemyhealth"]
    global charm
    global health
    global enemy_stats["enemysleepcounter"]
    if player_stats["spellslot1"] == "~blaze~":
        action = ""
        combat_variables["playerturn"] = False 
        keylogging = False
        print(f"You cast {player_stats["spellslot1"]} on the {enemy_stats["enemyname"]}!")
        attackroll = randint(1,20)
        if combat_variables["sneak"] or enemy_stats["enemysleepcounter"] >= 1:
            attackroll2 = randint(1,20)
            if attackroll2 > attackroll:
                attackroll = attackroll2 
            combat_variables["sneak"] = False
            enemy_stats["enemysleepcounter"] = 1
        if player_stats["playerclass"] == "mage":
            if attackroll <= 2:
                attackroll = randint(1,20)
                print("Mage reroll!")
        attackroll += player_stats["magic"]
        attackroll += player_stats["magicweapon"]
        attackroll -= combat_variables["woundpenalty"]
        combatdefense = 10
        combatdefense += enemy_stats["enemymagic"]
        combatdefense += enemy_stats["enemycharm"]
        if attackroll < combatdefense:
            print(f"You roll a {attackroll} to hit {combatdefense}. Your spell does not work!\n")
            combat_variables["playerturn"] = False
            combat()
        else:
            damage = attackroll - combatdefense + 1
            damage = damage * 5
            print(f"You roll a {attackroll} to hit {combatdefense}. The spell hits for {damage}% damage!\n")
            enemy_stats["enemyhealth"] -= damage
            if enemy_stats["enemyhealth"] <= 0:
                print(f"You have killed the {enemy_stats["enemyname"]}!\n")
                input("Press (enter) to continue\n")
                checkxp()            
            else:
                combat_variables["playerturn"] = False
                combat()
        
    elif player_stats["spellslot1"] == "restore":
        action = ""
        combat_variables["playerturn"] = False 
        keylogging = False
        print(f"You cast {player_stats["spellslot1"]} on yourself!")
        attackroll = randint(1,20)
        
        if combat_variables["sneak"]: 
            combat_variables["sneak"] = False
        if player_stats["playerclass"] == "cleric":
            attackroll2 = randint(1,20)
            if attackroll < attackroll2:
                attackroll = attackroll2
                print("Cleric bonus kicks in!")
        attackroll += player_stats["magic"]
        attackroll += player_stats["charm"]
        attackroll -= combat_variables["woundpenalty"]
        combatdefense = 10
        combatdefense += enemy_stats["enemymagic"]
        combatdefense += enemy_stats["enemycharm"]
        if attackroll < combatdefense:
            print(f"You roll a {attackroll} against a spell difficulty of {combatdefense}. Your spell does not work!\n")
            combat_variables["playerturn"] = False
            combat()
        else:
            damage = attackroll - combatdefense + 1
            damage = damage * 5
            print(f"You roll a {attackroll} against a spell difficulty of {combatdefense}. You are healed by {damage}%\n")
            player_stats["health"] += damage
            if player_stats["health"] > 100:
                player_stats["health"] = 100           
            combat_variables["playerturn"] = False
            combat()        

    elif player_stats["spellslot1"] == "~sleep~":
        action = ""
        combat_variables["playerturn"] = False 
        keylogging = False
        print(f"You cast {player_stats["spellslot1"]} on the {enemy_stats["enemyname"]}!")
        attackroll = randint(1,20)        
        if combat_variables["sneak"]:
            attackroll2 = randint(1,20)
            if attackroll2 > attackroll:
                attackroll = attackroll2 
            combat_variables["sneak"] = False
        if player_stats["playerclass"] == "bard":
            if attackroll <= 2:
                attackroll = randint(1,20)
                print("Bard bonus kicks in!")
        attackroll += player_stats["magic"]
        attackroll += player_stats["magicweapon"]
        attackroll -= combat_variables["woundpenalty"]
        combatdefense = 10
        combatdefense += enemy_stats["enemymagic"]
        combatdefense += enemy_stats["enemycharm"]
        if attackroll < combatdefense:
            print(f"You roll a {attackroll} against your target's resistance of {combatdefense}. Your spell does not work!\n")
            combat_variables["playerturn"] = False
            combat()
        else:
            damage = attackroll - combatdefense + 1
            damage = damage // 4
            if damage < 2:
                damage = 2
            if damage > 5:
                damage = 5
            print(f"You roll a {attackroll} against your target's resistance of {combatdefense}. The {enemy_stats["enemyname"]} falls asleep for {damage} turns.\n")
            enemy_stats["enemysleepcounter"] = damage         
            combat_variables["playerturn"] = False
            combat()                  
        
    else:
        print("There is no spell in that slot!")
        input("Press (enter) to continue\n")
        combat_variables["playerturn"] = True
        combat() 
            
def checkxp():
    global experience
    global enemy_stats["xpdrop"]
    global gold
    global enemy_stats["golddrop"]
    global enemy_stats["enemyname"]
    global enemy_stats["enemylevel"]
    global classlevel
    global effectivelevel    
    global enemy_stats["enemycanheal"]
    global combat_variables["incombat"]
    clear()
    combat_variables["incombat"] = False
    enemy_stats["enemycanheal"] = False
    enemy_stats["enemycancast"] = False
    enemy_stats["enemybreath"] = False
# next line exists for debug purposes, comment it out when not debugging
#    print(f"xp drop: {enemy_stats["xpdrop"]}")
    xpmod = 0
    totallevel = player_stats["classlevel"] + player_stats["effectivelevel"]
# enemies weaker than the player drop less xp, enemies stronger drop extra
    quarterlevel = enemy_stats["enemylevel"] * 4
    thirdlevel = enemy_stats["enemylevel"] * 3
    halflevel = enemy_stats["enemylevel"] * 2
    if totallevel >= quarterlevel:
        xpmod = enemy_stats["xpdrop"] * .75
        xpmod = round(xpmod)
        enemy_stats["xpdrop"] -= xpmod
    elif totallevel >= thirdlevel:
        xpmod = enemy_stats["xpdrop"] * .66
        xpmod = round(xpmod)
        enemy_stats["xpdrop"] -= xpmod
    elif totallevel >= halflevel:
        xpmod = enemy_stats["xpdrop"] * .5
        xpmod = round(xpmod)
        enemy_stats["xpdrop"] -= xpmod
    elif totallevel < enemy_stats["enemylevel"]:
        xpmod = enemy_stats["xpdrop"] * 1.5
        xpmod = round(xpmod)
        enemy_stats["xpdrop"] = xpmod
    else:
        xpmod = 0
    player_stats["experience"] += enemy_stats["xpdrop"]
    player_stats["gold"] += enemy_stats["golddrop"]
    print(f"For defeating the {enemy_stats["enemyname"]} you have gained {enemy_stats["xpdrop"]} xp and {enemy_stats["golddrop"]} gold.\n")
# these lines exist for debug purposes, comment them out when not debugging    
#    print(f"""enemy level: {enemy_stats["enemylevel"]}
#class level: {player_stats["classlevel"]}
#effective level: {player_stats["effectivelevel"]}
#total level: {totallevel}
#xp modifier: {xpmod}
#xp gained: {enemy_stats["xpdrop"]}
#    """)
    input("Press (enter) to continue\n")
# check for level up
    xpneeded = totallevel * 10
    if player_stats["experience"] >= xpneeded:
        player_stats["experience"] -= xpneeded
        levelup()
    else:
        town()
    
def levelup():
    global classlevel  
    global attack
    global defense
    global agility
    global magic
    global playerclass
    global freshweapons
    global fresharmor
    global freshmagicweapons
    global freshcharms
    global freshspells
    player_stats["classlevel"] += 1
    print(f"Your level has increased to {player_stats["classlevel"]}!\n")
# warriors always gain either attack or defense and the game tries to balance those two abilities
    if player_stats["playerclass"] == "warrior":
        if player_stats["attack"] < player_stats["defense"]:
            player_stats["attack"] += 1
            print(f"Attack increased to {player_stats["attack"]}!\n")
            increasedstat = "attack"
        elif player_stats["defense"] < player_stats["attack"]:
            player_stats["defense"] += 1
            print(f"Defense increased to {player_stats["defense"]}!\n")
            increasedstat = "defense"
        else:
            randomability = randint(1,2)
            if randomability == 1:
                player_stats["attack"] += 1
                print(f"Attack increased to {player_stats["attack"]}!\n")
                increasedstat = "attack"
            else:
                player_stats["defense"] += 1
                print(f"Defense increased to {player_stats["defense"]}!\n")
                increasedstat = "defense"
# warriors then get one more ability upgrade, favoring agility over magic
        randomability = randint(1,3)
        if randomability == 1:
            player_stats["magic"] += 1
            print(f"Magic increased to {player_stats["magic"]}!\n")
        if randomability == 2:
            player_stats["agility"] += 1
            print(f"Agility increased to {player_stats["agility"]}!\n")
        else:
            if increasedstat == "attack":
                player_stats["defense"] += 1
                print(f"Defense increased to {player_stats["defense"]}!\n")
            else:
                player_stats["attack"] += 1
                print(f"Attack increased to {player_stats["attack"]}!\n")
            
# rogues always get a point of agility
    elif player_stats["playerclass"] == "rogue":
        player_stats["agility"] += 1
        print(f"Agility increased to {player_stats["agility"]}!\n")  
        
# rogues then get one more ability upgrade, favoring attack over defense or magic
        randomability = randint(1,4)
        if randomability == 1:
            player_stats["magic"] += 1
            print(f"Magic increased to {player_stats["magic"]}!\n")
        elif randomability == 2:
            player_stats["defense"] += 1
            print(f"Defense increased to {player_stats["defense"]}!\n")
        else:
            player_stats["attack"] += 1
            print(f"Attack increased to {player_stats["attack"]}!\n")            

# mages always get a point of magic
    elif player_stats["playerclass"] == "mage":
        player_stats["magic"] += 1
        print(f"Magic increased to {player_stats["magic"]}!\n")  
        
# mages then get one more ability upgrade, favoring agility over attack or defense
        randomability = randint(1,4)
        if randomability == 1:
            player_stats["attack"] += 1
            print(f"Attack increased to {player_stats["attack"]}!\n")
        elif randomability == 2:
            player_stats["defense"] += 1
            print(f"Defense increased to {player_stats["defense"]}!\n")
        else:
            player_stats["agility"] += 1
            print(f"Agility increased to {player_stats["agility"]}!\n")             

# clerics always gain either defense or magic and the game tries to balance those two abilities
    elif player_stats["playerclass"] == "cleric":
        if player_stats["magic"] < player_stats["defense"]:
            player_stats["magic"] += 1
            print(f"Magic increased to {player_stats["magic"]}!\n")
            increasedstat = "magic"
        elif player_stats["defense"] < player_stats["magic"]:
            player_stats["defense"] += 1
            print(f"Defense increased to {player_stats["defense"]}!\n")
            increasedstat = "defense"
        else:
            randomability = randint(1,2)
            if randomability == 1:
                player_stats["magic"] += 1
                print(f"Magic increased to {player_stats["magic"]}!\n")
                increasedstat = "magic"
            else:
                player_stats["defense"] += 1
                print(f"Defense increased to {player_stats["defense"]}!\n")
                increasedstat = "defense"
# clerics then get one more ability upgrade
        randomability = randint(1,3)
        if randomability == 1:
            player_stats["attack"] += 1
            print(f"Attack increased to {player_stats["attack"]}!\n")
        elif randomability == 2:
            player_stats["agility"] += 1
            print(f"Agility increased to {player_stats["agility"]}!\n")  
        else:
            if increasedstat == "magic":
                player_stats["defense"] += 1
                print(f"Defense increased to {player_stats["defense"]}!\n")
            else:
                player_stats["magic"] += 1
                print(f"Magic increased to {player_stats["magic"]}!\n")

    # a bard's growth balances magic and agility             
    elif player_stats["playerclass"] == "bard":
        if player_stats["magic"] < player_stats["agility"]:
            player_stats["magic"] += 1
            print(f"Magic increased to {player_stats["magic"]}!\n")
        elif player_stats["agility"] < player_stats["magic"]:
            player_stats["agility"] += 1
            print(f"Agility increased to {player_stats["agility"]}!\n")
        else:
            randomability = randint(1,2)
            if randomability == 1:
                player_stats["magic"] += 1
                print(f"Magic increased to {player_stats["magic"]}!\n")
            else:
                player_stats["agility"] += 1
                print(f"Agility increased to {player_stats["agility"]}!\n")             
    # a bard's growth also balances attack and defense
        if player_stats["defense"] < player_stats["attack"]:
            player_stats["defense"] += 1
            print(f"Defense increased to {player_stats["defense"]}!\n")
        elif player_stats["attack"] < player_stats["defense"]:
            player_stats["attack"] += 1
            print(f"Attack increased to {player_stats["attack"]}!\n")
        else:
            randomability = randint(1,2)
            if randomability == 1:
                player_stats["defense"] += 1
                print(f"Defense increased to {player_stats["defense"]}!\n")
            else:
                player_stats["attack"] += 1
                print(f"Attack increased to {player_stats["attack"]}!\n") 
                
    input("Press (enter) to continue\n")
    if player_stats["classlevel"] == 4 or player_stats["classlevel"] == 8 or player_stats["classlevel"] == 12 or player_stats["classlevel"] == 16 or player_stats["classlevel"] == 20:
        player_stats["freshweapons"] = True
        player_stats["fresharmor"] = True
        player_stats["freshmagicweapons"] = True
        player_stats["freshcharms"] = True
        player_stats["freshspells"] = True
    town()

gamestart()

while keylogging:
    k = getkey()
    if k == 'esc':
        quit()
    elif k == 'up':
        action = "N"
        msg = ""
        resolveactions()
    elif k == 'down':
        action = "S"
        msg = ""
        resolveactions()
    elif k == 'right':
        action = "E"
        msg = ""
        resolveactions()
    elif k == 'left':
        action = "W"
        msg = ""
        resolveactions()
    elif k == 'return':
        action = "RETURN"
        resolveactions()
    else:
        action = ""
        resolveactions()
