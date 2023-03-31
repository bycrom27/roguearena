#import modules
from random import randint
from click import clear
import sys,tty,os,termios
import pickle
import json

#global variables
keylogging = False
action = ""
attack = 1
defense = 1
agility = 1
magic = 1
heritage = "heritage"
playerclass = "class"
playername = "Steven"
classlevel = 0
effectivelevel = 0
weaponname = "dagger"
weapon = 1
armorname = "clothes"
armor = 1
magicweaponname = "nothing"
magicweapon = 0
charmname = "copper ring"
charm = 1
spellslot1 = "       "
spellslot2 = "       "
spellslot3 = "       "
spellslot4 = "       "
health = 20
enemyname = "mook"
enemybreath = False
enemycancast = False
enemycanheal = False
enemyattack = 1
enemydefense = 1
enemyagility = 1
enemymagic = 1
enemyweapon = 0
enemyarmor = 0
enemymagicweapon = 0
enemycharm = 0
enemyhealth = 20
enemylevel = 1
xpdrop = 10
golddrop = 10
experience = 0
firstturn = True
playerturn = False
sneak = False
woundpenalty = 0
enemywound = ""
incombat = False
magicmenu = False
enemysleepcounter = 0
freshweapons = True
fresharmor = True
freshmagicweapons = True
freshcharms = True
freshspells = True
gold = 50
purchaseitem = "rubber chicken"
itemvalue = 333
itembonus = 3
itemtype = "gag"
totalassets = 0
resellitem = "cosmic hammer"
resellvalue = 5
weaponvalue1 = 1
weaponvalue2 = 2
weaponvalue3 = 3
weaponvalue4 = 4
weaponvalue5 = 5
weaponvalue6 = 6
armorvalue1 = 1
armorvalue2 = 2
armorvalue3 = 3
armorvalue4 = 4
armorvalue5 = 5
armorvalue6 = 6
mweaponvalue1 = 1
mweaponvalue2 = 2
mweaponvalue3 = 3
mweaponvalue4 = 4
mweaponvalue5 = 5
mweaponvalue6 = 6
charmvalue1 = 1
charmvalue2 = 2
charmvalue3 = 3
charmvalue4 = 4
charmvalue5 = 5
charmvalue6 = 6
spellvalue1 = 1
spellvalue2 = 2
spellvalue3 = 3
spellvalue4 = 4
spellvalue5 = 5
spellvalue6 = 6
slotchosen = 1
savegameslot = "1"
freshgame = True

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

def save_game(state):
    global savegameslot
    if savegameslot == "1":
        with open("savegame.txt", "w") as save_file:
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
    if savegameslot == "1":
        try:
            with open("savegame.txt", "r") as save_file:
                state = json.load(save_file)
                return state
        except FileNotFoundError:
            return None
    elif savegameslot == "2":
        try:
            with open("savegame2.txt", "r") as save_file:
                state = json.load(save_file)
                return state
        except FileNotFoundError:
            return None
    elif savegameslot == "3":
        try:
            with open("savegame3.txt", "r") as save_file:
                state = json.load(save_file)
                return state
        except FileNotFoundError:
            return None   
    else:
        print("Invalid save file!\n")
        input()
        gamestart()
    print("File loaded!\n")
    input()
    filemenu(state)
           
def filemenu(game_state=None):
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
    global experience
    global freshweapons
    global fresharmor
    global freshmagicweapons
    global freshcharms
    global freshspells
    global gold
    global weaponvalue1
    global weaponvalue2
    global weaponvalue3
    global weaponvalue4
    global weaponvalue5
    global weaponvalue6
    global armorvalue1
    global armorvalue2
    global armorvalue3
    global armorvalue4
    global armorvalue5
    global armorvalue6
    global mweaponvalue1
    global mweaponvalue2
    global mweaponvalue3
    global mweaponvalue4
    global mweaponvalue5
    global mweaponvalue6
    global charmvalue1
    global charmvalue2
    global charmvalue3
    global charmvalue4
    global charmvalue5
    global charmvalue6
    global spellvalue1
    global spellvalue2
    global spellvalue3
    global spellvalue4
    global spellvalue5
    global spellvalue6 
    attack = game_state.get("attack", 0) if game_state else 0
    defense = game_state.get("defense", 0) if game_state else 0
    agility = game_state.get("agility", 0) if game_state else 0
    magic = game_state.get("magic", 0) if game_state else 0
    heritage = game_state.get("heritage", 0) if game_state else 0
    playerclass = game_state.get("playerclass", 0) if game_state else 0
    playername = game_state.get("playername", 0) if game_state else 0
    classlevel = game_state.get("classlevel", 0) if game_state else 0
    effectivelevel = game_state.get("effectivelevel", 0) if game_state else 0
    weaponname = game_state.get("weaponname", 0) if game_state else 0
    weapon = game_state.get("weapon", 0) if game_state else 0
    armorname = game_state.get("armorname", 0) if game_state else 0
    armor = game_state.get("armor", 0) if game_state else 0
    magicweaponname = game_state.get("magicweaponname", 0) if game_state else 0
    magicweapon = game_state.get("magicweapon", 0) if game_state else 0
    charmname = game_state.get("charmname", 0) if game_state else 0
    charm = game_state.get("charm", 0) if game_state else 0
    spellslot1 = game_state.get("spellslot1", 0) if game_state else 0
    spellslot2 = game_state.get("spellslot2", 0) if game_state else 0
    spellslot3 = game_state.get("spellslot3", 0) if game_state else 0
    spellslot4 = game_state.get("spellslot4", 0) if game_state else 0
    experience = game_state.get("experience", 0) if game_state else 0
    freshweapons = game_state.get("freshweapons", 0) if game_state else 0
    fresharmor = game_state.get("fresharmor", 0) if game_state else 0
    freshmagicweapons = game_state.get("freshmagicweapons", 0) if game_state else 0
    freshcharms = game_state.get("freshcharms", 0) if game_state else 0
    freshspells = game_state.get("freshspells", 0) if game_state else 0
    gold = game_state.get("gold", 0) if game_state else 0
    weaponvalue1 = game_state.get("weaponvalue1", 0) if game_state else 0
    weaponvalue2 = game_state.get("weaponvalue2", 0) if game_state else 0
    weaponvalue3 = game_state.get("weaponvalue3", 0) if game_state else 0
    weaponvalue4 = game_state.get("weaponvalue4", 0) if game_state else 0
    weaponvalue5 = game_state.get("weaponvalue5", 0) if game_state else 0
    weaponvalue6 = game_state.get("weaponvalue6", 0) if game_state else 0
    armorvalue1 = game_state.get("armorvalue1", 0) if game_state else 0
    armorvalue2 = game_state.get("armorvalue2", 0) if game_state else 0
    armorvalue3 = game_state.get("armorvalue3", 0) if game_state else 0
    armorvalue4 = game_state.get("armorvalue4", 0) if game_state else 0
    armorvalue5 = game_state.get("armorvalue5", 0) if game_state else 0
    armorvalue6 = game_state.get("armorvalue6", 0) if game_state else 0
    mweaponvalue1 = game_state.get("mweaponvalue1", 0) if game_state else 0
    mweaponvalue2 = game_state.get("mweaponvalue2", 0) if game_state else 0
    mweaponvalue3 = game_state.get("mweaponvalue3", 0) if game_state else 0
    mweaponvalue4 = game_state.get("mweaponvalue4", 0) if game_state else 0
    mweaponvalue5 = game_state.get("mweaponvalue5", 0) if game_state else 0
    mweaponvalue6 = game_state.get("mweaponvalue6", 0) if game_state else 0
    charmvalue1 = game_state.get("charmvalue1", 0) if game_state else 0
    charmvalue2 = game_state.get("charmvalue2", 0) if game_state else 0
    charmvalue3 = game_state.get("charmvalue3", 0) if game_state else 0
    charmvalue4 = game_state.get("charmvalue4", 0) if game_state else 0
    charmvalue5 = game_state.get("charmvalue5", 0) if game_state else 0
    charmvalue6 = game_state.get("charmvalue6", 0) if game_state else 0
    spellvalue1 = game_state.get("spellvalue1", 0) if game_state else 0
    spellvalue2 = game_state.get("spellvalue2", 0) if game_state else 0
    spellvalue3 = game_state.get("spellvalue3", 0) if game_state else 0
    spellvalue4 = game_state.get("spellvalue4", 0) if game_state else 0
    spellvalue5 = game_state.get("spellvalue5", 0) if game_state else 0
    spellvalue6 = game_state.get("spellvalue6", 0) if game_state else 0  
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
        if state:
            filemenu(state)
        else:
            print("Error loading game!\n")
            input()
            gamestart()
    elif choice == "n" or choice == "N" or choice == "new":
        rolldice()
    else:
        gamestart()
    
#this begins character creation and sets character's stats
def rolldice(): 
    global attack
    global defense
    global agility
    global magic
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
        attack = die1
        defense = die2
        agility = die3
        magic = die4
        chooseheritage()
    if choice == "n" or choice == "no":
        rolldice()

# the player may now choose a heritage which gives certain bonuses and penalties
def chooseheritage():
    global attack
    global defense
    global agility
    global magic
    global heritage
    clear()
    print(f"""
Please choose a heritage.          (human) Humans are good at many different things.


           ---            
Attack:   | {attack} |                    (orc) Orcs are very strong and make fierce warriors.
           ---
           
           ---            
Defense:  | {defense} |                    (dwarf) Dwarves are strong, sturdy folk.
           ---

           ---            
Agility:  | {agility} |                    (goblin) Goblins are sneaky and make good rogues.
           ---
           
           ---            
Magic:    | {magic} |                    (elf) Elves are nimble and gifted with magic.
           ---

""")    
    playerchoice = input("Type the heritage of your choice.\n\n")
    if playerchoice == "orc" or playerchoice == "o":
        heritage = "orc"
        attack += 2
        magic -= 1
    elif playerchoice == "dwarf" or playerchoice == "d":
        heritage = "dwarf"
        attack += 1
        defense += 1
        agility -= 1
    elif playerchoice == "goblin" or playerchoice == "g":
        heritage = "goblin"
        agility += 2
        attack -= 1
    elif playerchoice == "elf" or playerchoice == "e":
        heritage = "elf"
        agility += 1
        magic += 1
        defense -= 1
    elif playerchoice == "debug6":
        heritage = "cheater"
        attack = 6
        defense = 6
        agility = 6
        magic = 6        
    elif playerchoice == "debug9":
        heritage = "big fat cheater"
        attack = 9
        defense = 9
        agility = 9
        magic = 9
    else:
        heritage = "human"
        for x in range(2):
            humanbonus = randint(1,4)
            if humanbonus == 1:
                attack += 1
            elif humanbonus == 2:
                defense += 1
            elif humanbonus == 3:
                agility += 1
            else:
                magic += 1        
    chooseclass()   
    
# now the player chooses a class, which further increases stats and grants starting equipment, level-ups, and special abilities
def chooseclass():
    global attack
    global defense
    global agility
    global magic
    global heritage
    global playerclass
    clear()
    print(f"""
Now choose a class.                (warrior) Warriors are the best at fighting.


           ---            
Attack:   | {attack} |                    (rogue) Rogues are very stealthy.
           ---
           
           ---            
Defense:  | {defense} |                    (mage) Mages are masters of magic.
           ---

           ---            
Agility:  | {agility} |                    (cleric) Clerics are tough magic users.
           ---
           
           ---            
Magic:    | {magic} |                    (bard) Bards are knowledgable about many things.
           ---

""")    
    playerchoice = input("Type the class of your choice.\n\n")
    if playerchoice == "warrior" or playerchoice == "w":
        playerclass = "warrior"
        attack += 1
        defense += 1
    elif playerchoice == "rogue" or playerchoice == "r":
        playerclass = "rogue"
        attack += 1
        agility += 1
    elif playerchoice == "mage" or playerchoice == "m":
        playerclass = "mage"
        magic += 2
    elif playerchoice == "cleric" or playerchoice == "c":
        playerclass = "cleric"
        defense += 1
        magic += 1    
    elif playerchoice == "bard" or playerchoice == "b":
        playerclass = "bard"
        agility += 1
        magic += 1   
    else:
        playerclass = "peasant"
    confirmcharacter()
        
# the player now chooses to keep or discard the character they rolled
def confirmcharacter():
    global attack
    global defense
    global agility
    global magic
    global heritage
    global playerclass
    clear()
    print(f"""
You are a/an {heritage} {playerclass}.          


           ---            
Attack:   | {attack} |                    
           ---
           
           ---            
Defense:  | {defense} |                    
           ---

           ---            
Agility:  | {agility} |                    
           ---
           
           ---            
Magic:    | {magic} |                    
           ---

""")    
    playerchoice = input("Keep this character?\n\n")
    if playerchoice == "yes" or playerchoice == "y":
        namecharacter()
    else:
        rolldice()

# the player now names their character
def namecharacter():
    global attack
    global defense
    global agility
    global magic
    global heritage
    global playerclass
    global playername
    global classlevel
    clear()
    playername = input("\nName your character.\n\n")
    clear()
    print(f"""
You are {playername} the {classlevel}-level {heritage} {playerclass}.          


           ---            
Attack:   | {attack} |                    
           ---
           
           ---            
Defense:  | {defense} |                    
           ---

           ---            
Agility:  | {agility} |                    
           ---
           
           ---            
Magic:    | {magic} |                    
           ---

Welcome! And good luck! {playername}!""")        
        
    finalizecharacter()  

# this function mostly serves to finalize the character before the game begins
def finalizecharacter():
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
    if playerclass == "warrior":
        weaponname = "short sword"
        weapon = 2
    elif playerclass == "rogue":
        weaponname = "short sword"
        weapon = 2
    elif playerclass == "mage":
        magicweaponname = "training wand"
        magicweapon = 1
        spellslot1 = "~blaze~"
    elif playerclass == "cleric":
        charmname = "holy symbol"
        charm = 2
        spellslot1 = "restore"
    elif playerclass == "bard":
        magicweaponname = "lute"
        magicweapon = 1
        spellslot1 = "~sleep~"
    else:
        weaponname = "stick"
        weapon = 1
    health = 100
    totalstats = attack + defense + agility + magic
    effectivelevel = totalstats // 2
    town()

def resolveactions():
    global magicmenu
    global incombat
    if magicmenu:
        battlemagic()
    elif incombat:
        combat()
    
def town():
    global health
    global enemyname
    global enemybreath
    global enemycancast
    global enemyattack 
    global enemydefense 
    global enemyagility 
    global enemymagic 
    global enemyweapon 
    global enemyarmor 
    global enemymagicweapon
    global enemycharm
    global enemyhealth 
    global enemylevel 
    global xpdrop    
    global firstturn
    global keylogging    
    global gold
    firstturn = True
    keylogging = False
    health = 100
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

def temple():
    global savegameslot
    clear()
    print("""The priestess asks you if you would like your deeds recorded on the holy register.

Choose a file:


Save Game (1)

Save Game (2)

Save Game (3)


(or press enter to exit)

""")
    savegameslot = input()
    if savegameslot == "1" or savegameslot == "2" or savegameslot == "3":
        game_state = {"attack": attack, "defense": defense, "agility": agility, "magic": magic, "heritage": heritage, "playerclass": playerclass, "playername": playername, "classlevel": classlevel, "effectivelevel": effectivelevel, "weaponname": weaponname, "weapon": weapon, "armorname": armorname, "armor": armor, "magicweaponname": magicweaponname, "magicweapon": magicweapon, "charmname": charmname, "charm": charm, "spellslot1": spellslot1, "spellslot2": spellslot2, "spellslot3": spellslot3, "spellslot4": spellslot4, "experience": experience, "freshweapons": freshweapons, "fresharmor": fresharmor, "freshmagicweapons": freshmagicweapons, "freshcharms": freshcharms, "freshspells": freshspells, "gold": gold, "weaponvalue1": weaponvalue1, "weaponvalue2": weaponvalue2, "weaponvalue3": weaponvalue3, "weaponvalue4": weaponvalue4, "weaponvalue5": weaponvalue5, "weaponvalue6": weaponvalue6, "armorvalue1": armorvalue1, "armorvalue2": armorvalue2, "armorvalue3": armorvalue3, "armorvalue4": armorvalue4, "armorvalue5": armorvalue5, "armorvalue6": armorvalue6, "mweaponvalue1": mweaponvalue1, "mweaponvalue2": mweaponvalue2, "mweaponvalue3": mweaponvalue3, "mweaponvalue4": mweaponvalue4, "mweaponvalue5": mweaponvalue5, "mweaponvalue": mweaponvalue6, "charmvalue1": charmvalue1, "charmvalue2": charmvalue2, "charmvalue3": charmvalue3, "charmvalue4": charmvalue4, "charmvalue5": charmvalue5, "charmvalue6": charmvalue6, "spellvalue1": spellvalue1, "spellvalue2": spellvalue2, "spellvalue3": spellvalue3, "spellvalue4": spellvalue4, "spellvalue5": spellvalue5, "spellvalue6": spellvalue6}
        save_game(game_state)
    else:
        print("'My services are always here if you should ever need them,' the priestess tells you.\n")
        input()        
    town()
        
def stats():
    global attack
    global defense
    global agility
    global magic
    global heritage
    global playerclass
    global classlevel
    global playername
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
    global experience
    global gold     
    clear()
    print(f"""Name:          {playername}
Heritage:      {heritage}
Class:         {playerclass}
Level:         {classlevel} 
Experience:    {experience}
Gold:          {gold}

Attack:        {attack}
Defense:       {defense}
Agility:       {agility}
Magic:         {magic}

Weapon:        {weaponname} ({weapon})
Armor:         {armorname} ({armor})
Magic Focus:   {magicweaponname} ({magicweapon})
Magic Charm:   {charmname} ({charm})

Spells known:  
{spellslot1} {spellslot2} 
{spellslot3} {spellslot4}

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
    global enemyname 
    global enemybreath 
    global enemycancast 
    global enemyattack 
    global enemydefense 
    global enemyagility 
    global enemymagic 
    global enemyweapon 
    global enemyarmor 
    global enemymagicweapon 
    global enemycharm 
    global enemyhealth 
    global enemylevel 
    global xpdrop 
    global golddrop 
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
        enemyname = "giant bat"
        enemyattack = 1
        enemydefense = 1
        enemyagility = 3
        enemymagic = 1
        enemyweapon = 1
        enemyarmor = 1
        enemymagicweapon = 0
        enemycharm = 1
        enemyhealth = 100
        enemylevel = 3
        xpdrop = 30
        golddrop = 3
    elif choice == "2":
        enemyname = "giant rat"
        enemyattack = 2
        enemydefense = 2
        enemyagility = 3
        enemymagic = 1
        enemyweapon = 1
        enemyarmor = 1
        enemymagicweapon = 0
        enemycharm = 1
        enemyhealth = 100
        enemylevel = 4
        xpdrop = 40 
        golddrop = 4
    elif choice == "3":
        enemyname = "kobold"
        enemyattack = 2
        enemydefense = 3
        enemyagility = 3
        enemymagic = 2
        enemyweapon = 2
        enemyarmor = 2
        enemymagicweapon = 0
        enemycharm = 2
        enemyhealth = 100
        enemylevel = 5
        xpdrop = 50
        golddrop = 10
    elif choice == "4":
        enemyname = "goblin"
        enemyattack = 3
        enemydefense = 3
        enemyagility = 3
        enemymagic = 3
        enemyweapon = 2
        enemyarmor = 2
        enemymagicweapon = 0
        enemycharm = 2
        enemyhealth = 100
        enemylevel = 6
        xpdrop = 60
        golddrop = 12
    elif choice == "5":
        enemyname = "orc"
        enemyattack = 4
        enemydefense = 4
        enemyagility = 3
        enemymagic = 3
        enemyweapon = 4
        enemyarmor = 4
        enemymagicweapon = 0
        enemycharm = 4
        enemyhealth = 100
        enemylevel = 7
        xpdrop = 70
        golddrop = 56
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        copperleague()
    firstturn = True
    combat()        
        
def silverleague():
    global enemyname 
    global enemybreath 
    global enemycancast 
    global enemyattack 
    global enemydefense 
    global enemyagility 
    global enemymagic 
    global enemyweapon 
    global enemyarmor 
    global enemymagicweapon 
    global enemycharm 
    global enemyhealth 
    global enemylevel 
    global xpdrop 
    global golddrop
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
        enemyname = "slime"
        enemyattack = 6
        enemydefense = 6
        enemyagility = 2
        enemymagic = 2
        enemyweapon = 4
        enemyarmor = 4
        enemymagicweapon = 0
        enemycharm = 4
        enemyhealth = 100
        enemylevel = 8
        xpdrop = 80
        golddrop = 64
    elif choice == "2":
        enemyname = "dark acolyte"
        enemycancast = True
        enemyattack = 3
        enemydefense = 3
        enemyagility = 6
        enemymagic = 6
        enemyweapon = 4
        enemyarmor = 4
        enemymagicweapon = 4
        enemycharm = 4
        enemyhealth = 100
        enemylevel = 9
        xpdrop = 90
        golddrop = 72
    elif choice == "3":
        enemyname = "ogre"
        enemyattack = 9
        enemydefense = 9
        enemyagility = 1
        enemymagic = 1
        enemyweapon = 4
        enemyarmor = 4
        enemymagicweapon = 0
        enemycharm = 4
        enemyhealth = 100
        enemylevel = 10
        xpdrop = 100
        golddrop = 80
    elif choice == "4":
        enemyname = "hellhound"
        enemybreath = True
        enemyattack = 6
        enemydefense = 5
        enemyagility = 6
        enemymagic = 5
        enemyweapon = 4
        enemyarmor = 4
        enemymagicweapon = 0
        enemycharm = 4
        enemyhealth = 100
        enemylevel = 11
        xpdrop = 110
        golddrop = 88
    elif choice == "5":
        enemyname = "dark dwarf"
        enemyattack = 8
        enemydefense = 8
        enemyagility = 4
        enemymagic = 4
        enemyweapon = 6
        enemyarmor = 6
        enemymagicweapon = 0
        enemycharm = 6
        enemyhealth = 100
        enemylevel = 12
        xpdrop = 120
        golddrop = 216
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        silverleague()
    firstturn = True
    combat()

def goldleague():
    global enemyname 
    global enemybreath 
    global enemycancast 
    global enemyattack 
    global enemydefense 
    global enemyagility 
    global enemymagic 
    global enemyweapon 
    global enemyarmor 
    global enemymagicweapon 
    global enemycharm 
    global enemyhealth 
    global enemylevel 
    global xpdrop 
    global golddrop
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
        enemyname = "dark elf"
        enemyattack = 6
        enemydefense = 6
        enemyagility = 8
        enemymagic = 6
        enemyweapon = 6
        enemyarmor = 6
        enemymagicweapon = 6
        enemycharm = 6
        enemyhealth = 100
        enemylevel = 13
        xpdrop = 130
        golddrop = 234
    elif choice == "2":
        enemyname = "dark mage"
        enemycancast = True
        enemyattack = 4
        enemydefense = 5
        enemyagility = 9
        enemymagic = 10
        enemyweapon = 6
        enemyarmor = 6
        enemymagicweapon = 6
        enemycharm = 6
        enemyhealth = 100
        enemylevel = 14
        xpdrop = 140
        golddrop = 252
    elif choice == "3":
        enemyname = "chimera"
        enemybreath = True
        enemyattack = 8
        enemydefense = 8
        enemyagility = 7
        enemymagic = 7
        enemyweapon = 6
        enemyarmor = 6
        enemymagicweapon = 6
        enemycharm = 6
        enemyhealth = 100
        enemylevel = 15
        xpdrop = 150
        golddrop = 270
    elif choice == "4":
        enemyname = "wraith"
        enemyattack = 9
        enemydefense = 9
        enemyagility = 8
        enemymagic = 6
        enemyweapon = 6
        enemyarmor = 6
        enemymagicweapon = 6
        enemycharm = 6
        enemyhealth = 100
        enemylevel = 16
        xpdrop = 160
        golddrop = 288
    elif choice == "5":
        enemyname = "giant"
        enemyattack = 11
        enemydefense = 11
        enemyagility = 6
        enemymagic = 6
        enemyweapon = 8
        enemyarmor = 8
        enemymagicweapon = 0
        enemycharm = 8
        enemyhealth = 100
        enemylevel = 17
        xpdrop = 170
        golddrop = 680
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        goldleague()
    firstturn = True
    combat()    

def platinumleague():
    global enemyname 
    global enemybreath 
    global enemycancast 
    global enemycanheal
    global enemyattack 
    global enemydefense 
    global enemyagility 
    global enemymagic 
    global enemyweapon 
    global enemyarmor 
    global enemymagicweapon 
    global enemycharm 
    global enemyhealth 
    global enemylevel 
    global xpdrop 
    global golddrop
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
        enemyname = "dark priest"
        enemycanheal = True
        enemyattack = 9
        enemydefense = 9
        enemyagility = 8
        enemymagic = 10
        enemyweapon = 8
        enemyarmor = 8
        enemymagicweapon = 8
        enemycharm = 8
        enemyhealth = 100
        enemylevel = 18
        xpdrop = 180
        golddrop = 720
    elif choice == "2":
        enemyname = "vampire"
        enemyattack = 9
        enemydefense = 9
        enemyagility = 10
        enemymagic = 10
        enemyweapon = 8
        enemyarmor = 8
        enemymagicweapon = 8
        enemycharm = 8
        enemyhealth = 100
        enemylevel = 19
        xpdrop = 190
        golddrop = 760
    elif choice == "3":
        enemyname = "death knight"
        enemyattack = 11
        enemydefense = 11
        enemyagility = 8
        enemymagic = 10
        enemyweapon = 8
        enemyarmor = 8
        enemymagicweapon = 8
        enemycharm = 8
        enemyhealth = 100
        enemylevel = 20
        xpdrop = 200
        golddrop = 800
    elif choice == "4":
        enemyname = "demon"
        enemycancast = True
        enemyattack = 10
        enemydefense = 10
        enemyagility = 8
        enemymagic = 12
        enemyweapon = 8
        enemyarmor = 8
        enemymagicweapon = 8
        enemycharm = 8
        enemyhealth = 100
        enemylevel = 21
        xpdrop = 210
        golddrop = 840
    elif choice == "5":
        enemyname = "dragon"
        enemybreath = True
        enemyattack = 11
        enemydefense = 11
        enemyagility = 10
        enemymagic = 10
        enemyweapon = 10
        enemyarmor = 10
        enemymagicweapon = 10
        enemycharm = 10
        enemyhealth = 100
        enemylevel = 22
        xpdrop = 220
        golddrop = 2200
    elif choice == "6":
        town()
    else:
        print("\nPlease make a valid choice!\n")
        input()
        platinumleague()
    firstturn = True
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
    if weapon == 1:
        resellvalue = 5
    elif weapon == 2:
        resellvalue = 25
    elif weapon == 4:
        resellvalue = 125
    elif weapon == 6:
        resellvalue = 750
    elif weapon == 8:
        resellvalue = 2250
    elif weapon == 10:
        resellvalue = 6000
    elif weapon == 12:
        resellvalue = 15000
    else:
        resellvalue = 0
# players can actually trade in their old weapon to gain enough cash to buy the new weapon
    totalassets = resellvalue + gold
    resellitem = weaponname
    print("What would you like to buy?\n")    
# the first time the player visits the store and at each level that is a multiple of 4, the prices for each available weapon are randomized
    if freshweapons:
        freshweapons = False
        weaponvalue1 = randint(5,10)
        weaponvalue1 = weaponvalue1 * 5
        if classlevel >= 4:
            weaponvalue2 = randint(75,125)
            weaponvalue2 = weaponvalue2 // 2
            weaponvalue2 = weaponvalue2 * 5
        if classlevel >= 8:
            weaponvalue3 = randint(75,125)
            weaponvalue3 = weaponvalue3 // 2
            weaponvalue3 = weaponvalue3 * 15
        if classlevel >= 12:            
            weaponvalue4 = randint(75,125)
            weaponvalue4 = weaponvalue4 // 2
            weaponvalue4 = weaponvalue4 * 45
        if classlevel >= 16:
            weaponvalue5 = randint(75,125)
            weaponvalue5 = weaponvalue5 // 2
            weaponvalue5 = weaponvalue5 * 120
        if classlevel >= 20:
            weaponvalue6 = randint(75,125)
            weaponvalue6 = weaponvalue6 // 2
            weaponvalue6 = weaponvalue6 * 350
# the default weapons
    weaponslot1 = "short sword"
    weaponslot2 = "long sword"    
    weaponslot3 = "broad sword"
    weaponslot4 = "great sword"
    weaponslot5 = "mithril sword"
    weaponslot6 = "rune blade"
# some classes have their weapons "re-skinned" to fit their style
    if playerclass == "rogue":
        weaponslot3 = "scimitar"
        weaponslot4 = "twin-blade"
        weaponslot5 = "ninja blade"
    if playerclass == "bard" or playerclass == "mage":
        weaponslot3 = "elven blade"
        weaponslot4 = "ancient sword"
    if playerclass == "cleric":
        weaponslot1 = "mace"
        weaponslot2 = "warhammer"
        weaponslot3 = "flail"
        weaponslot4 = "great hammer"
        weaponslot5 = "mithril mace"
        weaponslot6 = "lawbringer"        
# the store displays the weapons that are currently available and how much they cost
    print(f"1) {weaponslot1} {weaponvalue1} gold")
    if classlevel >= 4:
        print(f"2) {weaponslot2} {weaponvalue2} gold")
    if classlevel >= 8:
        print(f"3) {weaponslot3} {weaponvalue3} gold")
    if classlevel >= 12:
        print(f"4) {weaponslot4} {weaponvalue4} gold")
    if classlevel >= 16:
        print(f"5) {weaponslot5} {weaponvalue5} gold")
    if classlevel >= 20:
        print(f"6) {weaponslot6} {weaponvalue6} gold")
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    itemtype = "weapon"
    if choice == "1":
        purchaseitem = weaponslot1
        itemvalue = weaponvalue1
        itembonus = 2                
# [and] statements prevent the game from crashing
    elif choice == "2" and classlevel >= 4:
        purchaseitem = weaponslot2
        itemvalue = weaponvalue2
        itembonus = 4
    elif choice == "3" and classlevel >= 8:
        purchaseitem = weaponslot3
        itemvalue = weaponvalue3
        itembonus = 6
    elif choice == "4" and classlevel >= 12:
        purchaseitem = weaponslot4
        itemvalue = weaponvalue4
        itembonus = 8
    elif choice == "5" and classlevel >= 16:
        purchaseitem = weaponslot5
        itemvalue = weaponvalue5
        itembonus = 10
    elif choice == "6" and classlevel >= 20:
        purchaseitem = weaponslot6
        itemvalue = weaponvalue6
        itembonus = 12
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
    global armorvalue2
    global armorvalue3
    global armorvalue4
    global armorvalue5
    global armorvalue6
    global playerclass
    clear()
    if armor == 1:
        resellvalue = 5
    elif armor == 2:
        resellvalue = 25
    elif armor == 4:
        resellvalue = 125
    elif armor == 6:
        resellvalue = 750
    elif armor == 8:
        resellvalue = 2250
    elif armor == 10:
        resellvalue = 6000
    elif armor == 12:
        resellvalue = 15000
    else:
        resellvalue = 0
    totalassets = resellvalue + gold
    resellitem = armorname
    print("What would you like to buy?\n")    
    if fresharmor:
        fresharmor = False
        armorvalue1 = randint(5,10)
        armorvalue1 = armorvalue1 * 5
        if classlevel >= 4:
            armorvalue2 = randint(75,125)
            armorvalue2 = armorvalue2 // 2
            armorvalue2 = armorvalue2 * 5
        if classlevel >= 8:
            armorvalue3 = randint(75,125)
            armorvalue3 = armorvalue3 // 2
            armorvalue3 = armorvalue3 * 15
        if classlevel >= 12:            
            armorvalue4 = randint(75,125)
            armorvalue4 = armorvalue4 // 2
            armorvalue4 = armorvalue4 * 45
        if classlevel >= 16:
            armorvalue5 = randint(75,125)
            armorvalue5 = armorvalue5 // 2
            armorvalue5 = armorvalue5 * 120
        if classlevel >= 20:
            armorvalue6 = randint(75,125)
            armorvalue6 = armorvalue6 // 2
            armorvalue6 = armorvalue6 * 350
    armorslot1 = "leather"
    armorslot2 = "ring mail"    
    armorslot3 = "chain mail"
    armorslot4 = "plate mail"
    armorslot5 = "mithril"
    armorslot6 = "dragon scale"
    if playerclass == "rogue":
        armorslot2 = "studded leather"
        armorslot3 = "elven cloak"
        armorslot4 = "magic cloak"
        armorslot5 = "ninja"
        armorslot6 = "shadow cloak"
    if playerclass == "bard" or playerclass == "mage":
        armorslot4 = "elven chain mail"
        armorslot5 = "mithril vest"
        armorslot6 = "dragon scale cape"
    if playerclass == "mage":
        armorslot1 = "apprentice robe"
        armorslot2 = "heavy robe"
        armorslot3 = "wizard robe"
        armorslot4 = "magic robe"
        armorslot5 = "sage robe"
        armorslot6 = "aegis robe"        
    print(f"1) {armorslot1} {armorvalue1} gold")
    if classlevel >= 4:
        print(f"2) {armorslot2} {armorvalue2} gold")
    if classlevel >= 8:
        print(f"3) {armorslot3} {armorvalue3} gold")
    if classlevel >= 12:
        print(f"4) {armorslot4} {armorvalue4} gold")
    if classlevel >= 16:
        print(f"5) {armorslot5} {armorvalue5} gold")
    if classlevel >= 20:
        print(f"6) {armorslot6} {armorvalue6} gold")
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    itemtype = "armor"
    if choice == "1":
        purchaseitem = armorslot1
        itemvalue = armorvalue1
        itembonus = 2                
    elif choice == "2" and classlevel >= 4:
        purchaseitem = armorslot2
        itemvalue = armorvalue2
        itembonus = 4
    elif choice == "3" and classlevel >= 8:
        purchaseitem = armorslot3
        itemvalue = armorvalue3
        itembonus = 6
    elif choice == "4" and classlevel >= 12:
        purchaseitem = armorslot4
        itemvalue = armorvalue4
        itembonus = 8
    elif choice == "5" and classlevel >= 16:
        purchaseitem = armorslot5
        itemvalue = armorvalue5
        itembonus = 10
    elif choice == "6" and classlevel >= 20:
        purchaseitem = armorslot6
        itemvalue = armorvalue6
        itembonus = 12
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
    global itembonus
    global itemtype  
    global totalassets
    global resellitem
    global resellvalue
    global mweaponvalue1
    global mweaponvalue2
    global mweaponvalue3
    global mweaponvalue4
    global mweaponvalue5
    global mweaponvalue6
    global playerclass
    clear()
    if magicweapon == 1:
        resellvalue = 5
    elif magicweapon == 2:
        resellvalue = 25
    elif magicweapon == 4:
        resellvalue = 125
    elif magicweapon == 6:
        resellvalue = 750
    elif magicweapon == 8:
        resellvalue = 2250
    elif magicweapon == 10:
        resellvalue = 6000
    elif magicweapon == 12:
        resellvalue = 15000
    else:
        resellvalue = 0
    totalassets = resellvalue + gold
    resellitem = magicweaponname
    print("What would you like to buy?\n")    
    if freshmagicweapons:
        freshmagicweapons = False
        mweaponvalue1 = randint(5,10)
        mweaponvalue1 = mweaponvalue1 * 5
        if classlevel >= 4:
            mweaponvalue2 = randint(75,125)
            mweaponvalue2 = mweaponvalue2 // 2
            mweaponvalue2 = mweaponvalue2 * 5
        if classlevel >= 8:
            mweaponvalue3 = randint(75,125)
            mweaponvalue3 = mweaponvalue3 // 2
            mweaponvalue3 = mweaponvalue3 * 15
        if classlevel >= 12:            
            mweaponvalue4 = randint(75,125)
            mweaponvalue4 = mweaponvalue4 // 2
            mweaponvalue4 = mweaponvalue4 * 45
        if classlevel >= 16:
            mweaponvalue5 = randint(75,125)
            mweaponvalue5 = mweaponvalue5 // 2
            mweaponvalue5 = mweaponvalue5 * 120
        if classlevel >= 20:
            mweaponvalue6 = randint(75,125)
            mweaponvalue6 = mweaponvalue6 // 2
            mweaponvalue6 = mweaponvalue6 * 350
    mweaponslot1 = "oak wand"
    mweaponslot2 = "rowan wand"    
    mweaponslot3 = "ash wand"
    mweaponslot4 = "crystal wand"
    mweaponslot5 = "master wand"
    mweaponslot6 = "elder wand"
    if playerclass == "cleric":
        mweaponslot1 = "oak staff"
        mweaponslot2 = "rowan staff"    
        mweaponslot3 = "holy staff"
        mweaponslot4 = "sage staff"
        mweaponslot5 = "blessed staff"
        mweaponslot6 = "staff of light" 
    if playerclass == "mage":
        mweaponslot1 = "oak staff"
        mweaponslot2 = "rowan staff"    
        mweaponslot3 = "wizard staff"
        mweaponslot4 = "sage staff"
        mweaponslot5 = "staff of the magus"
        mweaponslot6 = "starlight staff"       
# the store displays the weapons that are currently available and how much they cost
    print(f"1) {mweaponslot1} {mweaponvalue1} gold")
    if classlevel >= 4:
        print(f"2) {mweaponslot2} {mweaponvalue2} gold")
    if classlevel >= 8:
        print(f"3) {mweaponslot3} {mweaponvalue3} gold")
    if classlevel >= 12:
        print(f"4) {mweaponslot4} {mweaponvalue4} gold")
    if classlevel >= 16:
        print(f"5) {mweaponslot5} {mweaponvalue5} gold")
    if classlevel >= 20:
        print(f"6) {mweaponslot6} {mweaponvalue6} gold")
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    itemtype = "mweapon"
    if choice == "1":
        purchaseitem = mweaponslot1
        itemvalue = mweaponvalue1
        itembonus = 2                
    elif choice == "2" and classlevel >= 4:
        purchaseitem = mweaponslot2
        itemvalue = mweaponvalue2
        itembonus = 4
    elif choice == "3" and classlevel >= 8:
        purchaseitem = mweaponslot3
        itemvalue = mweaponvalue3
        itembonus = 6
    elif choice == "4" and classlevel >= 12:
        purchaseitem = mweaponslot4
        itemvalue = mweaponvalue4
        itembonus = 8
    elif choice == "5" and classlevel >= 16:
        purchaseitem = mweaponslot5
        itemvalue = mweaponvalue5
        itembonus = 10
    elif choice == "6" and classlevel >= 20:
        purchaseitem = mweaponslot6
        itemvalue = mweaponvalue6
        itembonus = 12
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
    global itembonus
    global itemtype  
    global totalassets
    global resellitem
    global resellvalue
    global charmvalue1
    global charmvalue2
    global charmvalue3
    global charmvalue4
    global charmvalue5
    global charmvalue6
    global playerclass
    clear()
    if charm == 1:
        resellvalue = 5
    elif charm == 2:
        resellvalue = 25
    elif charm == 4:
        resellvalue = 125
    elif charm == 6:
        resellvalue = 750
    elif charm == 8:
        resellvalue = 2250
    elif charm == 10:
        resellvalue = 6000
    elif charm == 12:
        resellvalue = 15000
    else:
        resellvalue = 0
    totalassets = resellvalue + gold
    resellitem = magicweaponname
    print("What would you like to buy?\n")    
    if freshcharms:
        freshcharms = False
        charmvalue1 = randint(5,10)
        charmvalue1 = charmvalue1 * 5
        if classlevel >= 4:
            charmvalue2 = randint(75,125)
            charmvalue2 = charmvalue2 // 2
            charmvalue2 = charmvalue2 * 5
        if classlevel >= 8:
            charmvalue3 = randint(75,125)
            charmvalue3 = charmvalue3 // 2
            charmvalue3 = charmvalue3 * 15
        if classlevel >= 12:            
            charmvalue4 = randint(75,125)
            charmvalue4 = charmvalue4 // 2
            charmvalue4 = charmvalue4 * 45
        if classlevel >= 16:
            charmvalue5 = randint(75,125)
            charmvalue5 = charmvalue5 // 2
            charmvalue5 = charmvalue5 * 120
        if classlevel >= 20:
            charmvalue6 = randint(75,125)
            charmvalue6 = charmvalue6 // 2
            charmvalue6 = charmvalue6 * 350
    charmslot1 = "copper ring"
    charmslot2 = "iron ring"    
    charmslot3 = "sapphire ring"
    charmslot4 = "garnet ring"
    charmslot5 = "opal ring"
    charmslot6 = "jade ring"
    if playerclass == "cleric" or playerclass == "mage":
        charmslot1 = "amulet of protection"
        charmslot2 = "talisman"    
        charmslot3 = "sapphire pendant"
        charmslot4 = "garnet pendant"
        charmslot5 = "opal pendant"
        charmslot6 = "jade pendant" 
    print(f"1) {charmslot1} {charmvalue1} gold")
    if classlevel >= 4:
        print(f"2) {charmslot2} {charmvalue2} gold")
    if classlevel >= 8:
        print(f"3) {charmslot3} {charmvalue3} gold")
    if classlevel >= 12:
        print(f"4) {charmslot4} {charmvalue4} gold")
    if classlevel >= 16:
        print(f"5) {charmslot5} {charmvalue5} gold")
    if classlevel >= 20:
        print(f"6) {charmslot6} {charmvalue6} gold")
    print("\nPress (enter) to leave\n")
    choice = input()
    clear()
    itemtype = "charm"
    if choice == "1":
        purchaseitem = charmslot1
        itemvalue = charmvalue1
        itembonus = 2                
    elif choice == "2" and classlevel >= 4:
        purchaseitem = charmslot2
        itemvalue = charmvalue2
        itembonus = 4
    elif choice == "3" and classlevel >= 8:
        purchaseitem = charmslot3
        itemvalue = charmvalue3
        itembonus = 6
    elif choice == "4" and classlevel >= 12:
        purchaseitem = charmslot4
        itemvalue = charmvalue4
        itembonus = 8
    elif choice == "5" and classlevel >= 16:
        purchaseitem = charmslot5
        itemvalue = charmvalue5
        itembonus = 10
    elif choice == "6" and classlevel >= 20:
        purchaseitem = charmslot6
        itemvalue = charmvalue6
        itembonus = 12
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
    global resellitem
    global resellvalue
    global itemtype
    global itemvalue
    global itembonus
    global totalassets
    global purchaseitem
    global resellitem
    global resellvalue
    global weaponname
    global weapon
    global armorname
    global armor
    global magicweaponname
    global magicweapon
    global charmname
    global charm
    global gold
    global slotchosen 
    if itemvalue > totalassets:
        print("You don't have enough gold!\n")
        input()
        shop()
    else:
        if resellvalue > 0:
            print(f"The {purchaseitem}? Then I will buy your {resellitem} for {resellvalue} gold.\n")
            print("Deal?\n")
        else:
            print(f"The {purchaseitem}? Are you sure?\n")            
        choice = input()
        clear()
        if choice == "y" or choice == "yes":
            if itemtype == "weapon":
                weaponname = purchaseitem
                weapon = itembonus
                gold -= itemvalue
                gold += resellvalue
            elif itemtype == "armor":
                armorname = purchaseitem
                armor = itembonus
                gold -= itemvalue
                gold += resellvalue
            elif itemtype == "mweapon":
                magicweaponname = purchaseitem
                magicweapon = itembonus
                gold -= itemvalue
                gold += resellvalue
            elif itemtype == "charm":
                charmname = purchaseitem
                charm = itembonus
                gold -= itemvalue
                gold += resellvalue
            elif itemtype == "spell":
                if slotchosen == 1:
                    spellslot1 = purchaseitem
                elif slotchosen == 2:
                    spellslot2 = purchaseitem
                elif slotchosen == 3:
                    spellslot3 = purchaseitem
                elif slotchosen == 4:
                    spellslot4 = purchaseitem
                gold -= itemvalue
                gold += resellvalue
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
    global enemyname
    global enemybreath
    global enemycancast
    global enemycanheal
    global enemyattack 
    global enemydefense 
    global enemyagility 
    global enemymagic 
    global enemyweapon 
    global enemyarmor 
    global enemyhealth 
    global enemylevel 
    global xpdrop    
    global golddrop
    global firstturn
    global action
    global playerturn
    global sneak
    global keylogging
    global woundpenalty
    global enemywound
    global magicmenu
    global incombat
    global enemysleepcounter
    keylogging = True
    incombat = True
    # see who goes first
    if firstturn:
        enemysleepcounter = 0
        clear()
        print(f"A {enemyname} appears!\n")
        firstturn = False
        initiative = randint(1,20)
        if playerclass == "rogue":
            if initiative <= 2:
                initiative = randint(1,20)
                print("Rogue reroll!")
        initiative += agility
        enemyinitiative = 10
        enemyinitiative += enemyagility
        if initiative < enemyinitiative:
            print(f"The {enemyname} attacks before you are ready!\n")
            playerturn = False
            combat()
        elif initiative <= enemyinitiative + 5:
            print(f"You strike first before the {enemyname}!\n")
            playerturn = True
            input("Press (enter) to continue\n")
            combat()
        else:
            print(f"You sneak up on the {enemyname}!\n")
            playerturn = True
            sneak = True
            input("Press (enter) to continue\n")
            combat()
# player's turn starts here        
    if playerturn:
        if enemyhealth < 30:
            enemywound = "severely "
        elif enemyhealth < 55:
            enemywound = ""
        elif enemyhealth < 80:
            enemywound = "somewhat "
        elif enemyhealth < 100:
            enemywound = "barely "
        else:
            enemywound = "not "
        if health < 30:
            woundpenalty = 3
        elif health < 55:
            woundpenalty = 2
        elif health < 80:
            woundpenalty = 1
        else:
            woundpenalty = 0
        clear()
        print(f"""{playername} the {heritage} {playerclass} (Lvl: {classlevel})
Health: {health}%

You are fighting a {enemyname}. It is {enemywound}wounded.

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
            playerturn = False 
            keylogging = False
            print(f"You attack the {enemyname}!")
            attackroll = randint(1,20)
            if sneak or enemysleepcounter >= 1:
                attackroll2 = randint(1,20)
                if attackroll2 > attackroll:
                    attackroll = attackroll2 
                sneak = False
                if enemysleepcounter >= 1:
                    enemysleepcounter = 1
            if playerclass == "warrior":
                if attackroll <= 2:
                    attackroll = randint(1,20)
                    print("Warrior reroll!")
            attackroll += attack
            attackroll += weapon
            attackroll -= woundpenalty
            combatdefense = 10
            combatdefense += enemydefense
            combatdefense += enemyarmor
            if attackroll < combatdefense:
                print(f"You roll a {attackroll} to hit {combatdefense}. A miss!\n")
                playerturn = False
                combat()
            else:
                damage = attackroll - combatdefense + 1
                damage = damage * 5
                print(f"You roll a {attackroll} to hit {combatdefense}, hitting for {damage}% damage!\n")
                enemyhealth -= damage
                if enemyhealth <= 0:
                    print(f"You have killed the {enemyname}!\n")
                    input("Press (enter) to continue\n")
                    checkxp()            
                else:
                    playerturn = False
                    combat()

# player chooses magic                    
        elif action == "W":
            action = ""  
            magicmenu = True
            playerturn = False
            battlemagic()
                    
# enemy's turn                    
    if not playerturn and not magicmenu:
        playerturn = True
        keylogging = False
        if enemyhealth < 30:
            woundpenalty = 3
        elif enemyhealth < 55:
            woundpenalty = 2
        elif enemyhealth < 80:
            woundpenalty = 1
        else:
            woundpenalty = 0

        # check to see if enemy is asleep
        if enemysleepcounter >= 1:
            enemysleepcounter -= 1
            if enemysleepcounter <= 0:
                print(f"The {enemyname} wakes up!")
            else: 
                print(f"The {enemyname} is still asleep!")
            input("\nPress (enter) to continue\n")
            combat()

        # some enemies will heal themselves when they are badly wounded    
        elif enemycanheal:
            castchance = randint(1,2)
            if castchance == 2 and enemyhealth <= 50:                
                print(f"The {enemyname} casts a healing spell!")
                attackroll = randint(1,20)
                attackroll += enemymagic
                attackroll += enemycharm
                attackroll -= woundpenalty
                combatdefense = 10
                combatdefense += magic
                combatdefense += charm
                if attackroll < combatdefense:
                    print(f"The {enemyname} rolls a {attackroll} against a target of {combatdefense}. The spell doesn't work!\n")
                    input("Press (enter) to continue\n")
                    combat()
                else:
                    damage = attackroll - combatdefense + 1
                    damage = damage * 5
                    print(f"The {enemyname} rolls a {attackroll} against a target of {combatdefense}. The spell heals {damage}% damage!\n")
                    enemyhealth += damage
                    if enemyhealth > 100:
                        enemyhealth = 100
                    input("Press (enter) to continue\n")
                    combat()  
            
        # some enemies use magic to attack           
        elif enemycancast:
            castchance = randint(1,5)
            if castchance <= 4:                
                print(f"The {enemyname} casts a spell on you!")
                attackroll = randint(1,20)
                # clerics have a defense bonus against attacks of a magical nature
                if playerclass == "cleric":
                    if attackroll >= 19:
                        attackroll = randint(1,20)
                        print("Cleric reroll!")  
                attackroll += enemymagic
                attackroll += enemymagicweapon
                attackroll -= woundpenalty
                combatdefense = 10
                combatdefense += magic
                combatdefense += charm
                if attackroll < combatdefense:
                    print(f"The {enemyname} rolls a {attackroll} to hit {combatdefense}. You resist the spell!\n")
                    input("Press (enter) to continue\n")
                    combat()
                else:
                    damage = attackroll - combatdefense + 1
                    damage = damage * 5
                    print(f"The {enemyname} rolls a {attackroll} to hit {combatdefense}. The spell causes {damage}% damage!\n")
                    health -= damage
                    if health <= 0:
                        print(f"You were killed by the {enemyname}!\n")
                        quit()
                    else:
                        input("Press (enter) to continue\n")
                        combat()                   
            else:
                enemyphysicalattack()
   
        # certain enemies breathe fire
        elif enemybreath:
            breathchance = randint(1,2)
            if breathchance == 1:
                print(f"The {enemyname} uses its breath attack on you!")
                attackroll = randint(1,20)
                # clerics have a defense bonus against attacks of a magical nature
                if playerclass == "cleric":
                    if attackroll >= 19:
                        attackroll = randint(1,20)
                        print("Cleric reroll!")  
                attackroll += enemyattack
                attackroll += enemyweapon
                attackroll -= woundpenalty
                combatdefense = 10
                combatdefense += magic
                combatdefense += charm
                if attackroll < combatdefense:
                    print(f"The {enemyname} rolls a {attackroll} to hit {combatdefense}. You dodge its breath attack!\n")
                    playerturn = True
                    input("Press (enter) to continue\n")
                    combat()
                else:
                    damage = attackroll - combatdefense + 1
                    damage = damage * 5
                    print(f"The {enemyname} rolls a {attackroll} to hit {combatdefense}. You are hit for {damage}% damage!\n")
                    health -= damage
                    if health <= 0:
                        print(f"You were killed by the {enemyname}!\n")
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
    global enemyname
    global enemyattack 
    global enemyweapon 
    global action
    global playerturn    
    print(f"The {enemyname} attacks!\n")
    attackroll = randint(1,20)
    # bards have a defense bonus for being lucky
    if playerclass == "bard":
        if attackroll >= 19:
            attackroll = randint(1,20)
            print("Bard reroll!")  
    attackroll += enemyattack
    attackroll += enemyweapon
    attackroll -= woundpenalty
    combatdefense = 10
    combatdefense += defense
    combatdefense += armor
    if attackroll < combatdefense:
        print(f"The {enemyname} rolls a {attackroll} to hit {combatdefense}. A miss!\n")
        input("Press (enter) to continue\n")
        combat()
    else:
        damage = attackroll - combatdefense + 1
        damage = damage * 5
        print(f"The {enemyname} rolls a {attackroll} to hit {combatdefense}, hitting for {damage}% damage!\n")
        health -= damage
        if health <= 0:
            print(f"You were killed by the {enemyname}!\n")
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
    global enemyhealth
    global spellslot1
    global spellslot2
    global spellslot3
    global spellslot4
    global magic
    global magicweapon
    global enemyname
    global enemymagic
    global enemycharm
    global woundpenalty
    global enemywound
    global action
    global playerturn
    global keylogging
    global magicmenu
    keylogging = True
    if magicmenu:
        clear()
        print(f"""{playername} the {heritage} {playerclass} (Lvl: {classlevel})
Health: {health}%

You are fighting a {enemyname}. It is {enemywound}wounded.

                ^
             {spellslot1}

<{spellslot2}     Spell ?    {spellslot3}> 

             {spellslot4}
                v
        """)
        print("Press (enter) to cancel.\n")  
    # player tries to cast the spell in slot 1        
        if action == "N":
            action = ""
            magicmenu = False
            castspellslot1()
            
        elif action == "RETURN":
            playerturn = True
            magicmenu = False
            combat()
    else:
        playerturn = True
        combat()
        
def castspellslot1():
    global spellslot1
    global enemyname
    global sneak
    global playerclass
    global magic
    global magicweapon
    global enemymagic
    global enemycharm
    global enemyhealth
    global charm
    global health
    global enemysleepcounter
    if spellslot1 == "~blaze~":
        action = ""
        playerturn = False 
        keylogging = False
        print(f"You cast {spellslot1} on the {enemyname}!")
        attackroll = randint(1,20)
        if sneak or enemysleepcounter >= 1:
            attackroll2 = randint(1,20)
            if attackroll2 > attackroll:
                attackroll = attackroll2 
            sneak = False
            enemysleepcounter = 1
        if playerclass == "mage":
            if attackroll <= 2:
                attackroll = randint(1,20)
                print("Mage reroll!")
        attackroll += magic
        attackroll += magicweapon
        attackroll -= woundpenalty
        combatdefense = 10
        combatdefense += enemymagic
        combatdefense += enemycharm
        if attackroll < combatdefense:
            print(f"You roll a {attackroll} to hit {combatdefense}. Your spell does not work!\n")
            playerturn = False
            combat()
        else:
            damage = attackroll - combatdefense + 1
            damage = damage * 5
            print(f"You roll a {attackroll} to hit {combatdefense}. The spell hits for {damage}% damage!\n")
            enemyhealth -= damage
            if enemyhealth <= 0:
                print(f"You have killed the {enemyname}!\n")
                input("Press (enter) to continue\n")
                checkxp()            
            else:
                playerturn = False
                combat()
        
    elif spellslot1 == "restore":
        action = ""
        playerturn = False 
        keylogging = False
        print(f"You cast {spellslot1} on yourself!")
        attackroll = randint(1,20)
        
        if sneak: 
            sneak = False
        if playerclass == "cleric":
            attackroll2 = randint(1,20)
            if attackroll < attackroll2:
                attackroll = attackroll2
                print("Cleric bonus kicks in!")
        attackroll += magic
        attackroll += charm
        attackroll -= woundpenalty
        combatdefense = 10
        combatdefense += enemymagic
        combatdefense += enemycharm
        if attackroll < combatdefense:
            print(f"You roll a {attackroll} against a spell difficulty of {combatdefense}. Your spell does not work!\n")
            playerturn = False
            combat()
        else:
            damage = attackroll - combatdefense + 1
            damage = damage * 5
            print(f"You roll a {attackroll} against a spell difficulty of {combatdefense}. You are healed by {damage}%\n")
            health += damage
            if health > 100:
                health = 100           
            playerturn = False
            combat()        

    elif spellslot1 == "~sleep~":
        action = ""
        playerturn = False 
        keylogging = False
        print(f"You cast {spellslot1} on the {enemyname}!")
        attackroll = randint(1,20)        
        if sneak:
            attackroll2 = randint(1,20)
            if attackroll2 > attackroll:
                attackroll = attackroll2 
            sneak = False
        if playerclass == "bard":
            if attackroll <= 2:
                attackroll = randint(1,20)
                print("Bard bonus kicks in!")
        attackroll += magic
        attackroll += magicweapon
        attackroll -= woundpenalty
        combatdefense = 10
        combatdefense += enemymagic
        combatdefense += enemycharm
        if attackroll < combatdefense:
            print(f"You roll a {attackroll} against your target's resistance of {combatdefense}. Your spell does not work!\n")
            playerturn = False
            combat()
        else:
            damage = attackroll - combatdefense + 1
            damage = damage // 4
            if damage < 2:
                damage = 2
            if damage > 5:
                damage = 5
            print(f"You roll a {attackroll} against your target's resistance of {combatdefense}. The {enemyname} falls asleep for {damage} turns.\n")
            enemysleepcounter = damage         
            playerturn = False
            combat()                  
        
    else:
        print("There is no spell in that slot!")
        input("Press (enter) to continue\n")
        playerturn = True
        combat() 
            
def checkxp():
    global experience
    global xpdrop
    global gold
    global golddrop
    global enemyname
    global enemylevel
    global classlevel
    global effectivelevel    
    global enemycanheal
    clear()
    enemycanheal = False
    enemycancast = False
    enemybreath = False
# next line exists for debug purposes, comment it out when not debugging
#    print(f"xp drop: {xpdrop}")
    xpmod = 0
    totallevel = classlevel + effectivelevel
# enemies weaker than the player drop less xp, enemies stronger drop extra
    quarterlevel = enemylevel * 4
    thirdlevel = enemylevel * 3
    halflevel = enemylevel * 2
    if totallevel >= quarterlevel:
        xpmod = xpdrop * .75
        xpmod = round(xpmod)
        xpdrop -= xpmod
    elif totallevel >= thirdlevel:
        xpmod = xpdrop * .66
        xpmod = round(xpmod)
        xpdrop -= xpmod
    elif totallevel >= halflevel:
        xpmod = xpdrop * .5
        xpmod = round(xpmod)
        xpdrop -= xpmod
    elif totallevel < enemylevel:
        xpmod = xpdrop * 1.5
        xpmod = round(xpmod)
        xpdrop = xpmod
    else:
        xpmod = 0
    experience += xpdrop
    gold += golddrop
    print(f"For defeating the {enemyname} you have gained {xpdrop} xp and {golddrop} gold.\n")
# these lines exist for debug purposes, comment them out when not debugging    
#    print(f"""enemy level: {enemylevel}
#class level: {classlevel}
#effective level: {effectivelevel}
#total level: {totallevel}
#xp modifier: {xpmod}
#xp gained: {xpdrop}
#    """)
    input("Press (enter) to continue\n")
# check for level up
    xpneeded = totallevel * 10
    if experience >= xpneeded:
        experience -= xpneeded
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
    classlevel += 1
    print(f"Your level has increased to {classlevel}!\n")
# warriors always gain either attack or defense and the game tries to balance those two abilities
    if playerclass == "warrior":
        if attack < defense:
            attack += 1
            print(f"Attack increased to {attack}!\n")
            increasedstat = "attack"
        elif defense < attack:
            defense += 1
            print(f"Defense increased to {defense}!\n")
            increasedstat = "defense"
        else:
            randomability = randint(1,2)
            if randomability == 1:
                attack += 1
                print(f"Attack increased to {attack}!\n")
                increasedstat = "attack"
            else:
                defense += 1
                print(f"Defense increased to {defense}!\n")
                increasedstat = "defense"
# warriors then get one more ability upgrade, favoring agility over magic
        randomability = randint(1,3)
        if randomability == 1:
            magic += 1
            print(f"Magic increased to {magic}!\n")
        if randomability == 2:
            agility += 1
            print(f"Agility increased to {agility}!\n")
        else:
            if increasedstat == "attack":
                defense += 1
                print(f"Defense increased to {defense}!\n")
            else:
                attack += 1
                print(f"Attack increased to {attack}!\n")
            
# rogues always get a point of agility
    elif playerclass == "rogue":
        agility += 1
        print(f"Agility increased to {agility}!\n")  
        
# rogues then get one more ability upgrade, favoring attack over defense or magic
        randomability = randint(1,4)
        if randomability == 1:
            magic += 1
            print(f"Magic increased to {magic}!\n")
        elif randomability == 2:
            defense += 1
            print(f"Defense increased to {defense}!\n")
        else:
            attack += 1
            print(f"Attack increased to {attack}!\n")            

# mages always get a point of magic
    elif playerclass == "mage":
        magic += 1
        print(f"Magic increased to {magic}!\n")  
        
# mages then get one more ability upgrade, favoring agility over attack or defense
        randomability = randint(1,4)
        if randomability == 1:
            attack += 1
            print(f"Attack increased to {attack}!\n")
        elif randomability == 2:
            defense += 1
            print(f"Defense increased to {defense}!\n")
        else:
            agility += 1
            print(f"Agility increased to {agility}!\n")             

# clerics always gain either defense or magic and the game tries to balance those two abilities
    elif playerclass == "cleric":
        if magic < defense:
            magic += 1
            print(f"Magic increased to {magic}!\n")
            increasedstat = "magic"
        elif defense < magic:
            defense += 1
            print(f"Defense increased to {defense}!\n")
            increasedstat = "defense"
        else:
            randomability = randint(1,2)
            if randomability == 1:
                magic += 1
                print(f"Magic increased to {magic}!\n")
                increasedstat = "magic"
            else:
                defense += 1
                print(f"Defense increased to {defense}!\n")
                increasedstat = "defense"
# clerics then get one more ability upgrade
        randomability = randint(1,3)
        if randomability == 1:
            attack += 1
            print(f"Attack increased to {attack}!\n")
        elif randomability == 2:
            agility += 1
            print(f"Agility increased to {agility}!\n")  
        else:
            if increasedstat == "magic":
                defense += 1
                print(f"Defense increased to {defense}!\n")
            else:
                magic += 1
                print(f"Magic increased to {magic}!\n")

    # a bard's growth balances magic and agility             
    elif playerclass == "bard":
        if magic < agility:
            magic += 1
            print(f"Magic increased to {magic}!\n")
        elif agility < magic:
            agility += 1
            print(f"Agility increased to {agility}!\n")
        else:
            randomability = randint(1,2)
            if randomability == 1:
                magic += 1
                print(f"Magic increased to {magic}!\n")
            else:
                agility += 1
                print(f"Agility increased to {agility}!\n")             
    # a bard's growth also balances attack and defense
        if defense < attack:
            defense += 1
            print(f"Defense increased to {defense}!\n")
        elif attack < defense:
            attack += 1
            print(f"Attack increased to {attack}!\n")
        else:
            randomability = randint(1,2)
            if randomability == 1:
                defense += 1
                print(f"Defense increased to {defense}!\n")
            else:
                attack += 1
                print(f"Attack increased to {attack}!\n") 
                
    input("Press (enter) to continue\n")
    if classlevel == 4 or classlevel == 8 or classlevel == 12 or classlevel == 16 or classlevel == 20:
        freshweapons = True
        fresharmor = True
        freshmagicweapons = True
        freshcharms = True
        freshspells = True
    town()

if freshgame:    
    print("Fresh game was true")
    input()
    freshgame = False
    gamestart()
else:
    print("Fresh game was false")
    input()
    town()

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
