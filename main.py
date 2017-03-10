from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random


# Create Black Magic
fire = Spell('Fire', 10, 100, "Black")
thunder = Spell("Thunder", 10, 100, "Black")
blizzard = Spell("Blizzard", 10, 100, "Black")
meteor = Spell("Meteor", 20, 200, "Black")
quake = Spell("Quake", 14, 140, "Black")

# Create White Magic
cure = Spell("Cure", 12, 120, "White")
cura = Spell("Cura", 18, 200, "White")

# Create Items
potion = Item("Potion", "potion", "Heals 50HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 500HP", 500)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP of one party member", 9999)
megaelixir = Item("Mega Elixir", "elixir", "Fully restores HP/MP of party", 9999 )
grenade = Item("Grenade", 'attack', 'Deals 500 damage', 500)


player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{"item": potion, "quantity": 15}, {"item": hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item": elixir, "quantity": 5},
                {"item": megaelixir, "quantity": 5}, {"item": grenade, "quantity": 8}]

# Instantiate People
# HP / MP / ATK / DEF / Spells
player1 = Person("Valos", 125, 25, 50, 20, player_spells, player_items)
player2 = Person("Nick ", 80, 58, 15, 10, player_spells, player_items)
player3 = Person("Robot", 200, 1, 32, 30, player_spells, player_items)

enemy1 = Person("Slime", 300, 100, 20, 10, [blizzard], [])
enemy2 = Person("Skeleton", 350, 100, 45, 5, [fire], [])
enemy3 = Person("Wisp", 100, 500, 5, 1, [fire], [])
running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

while running:
    print('====================')
    print('\n\n')
    print("NAME                     HP                                    MP")

    for player in players:
        player.get_stats()

    for enemy in enemies:
        enemy.get_enemy_stats()

    print('\n')

    for player in players:
        player.choose_action()
        choice = input("    Choose action: ")
        index = int(choice) - 1

        ##  This is the section for the basic attack and usage of it    ##
        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + ' for', dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        ##  This is the section for magic commands and usage            ##
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("    Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'White':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == 'Black':
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name, 'deals', str(magic_dmg), 'points of damage to', enemies[enemy].name.replace(" ", "") + bcolors.ENDC )

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died.")
                del enemies[enemy]

        ##  This is the section for item commands and usage             ##
        elif index == 2:
            player.choose_item()
            item_choice = int(input("    Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]['item']

            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + '\n' + 'None left of this item' + bcolors.ENDC)
                continue

            player.items[item_choice]['quantity'] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + ' heals for', str(item.prop), "HP" + bcolors.ENDC )
            elif item.type == "elixir":
                if item.name == "MegaElixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + "\n" + item.name, "full restores HP/MP" + bcolors.ENDC)
            elif item.type == 'attack':
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + '\n' + item.name, "deals", str(item.prop), "points of damage to", enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]

    #   Check if battle is over
    defeated_players = 0
    defeated_enemies = 0

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    # Check if Player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
        running = False

    # Check if Enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "Your team has been defeated!" + bcolors.ENDC)
        running = False

    # Enemy attack phase
    for enemy in enemies:
        print('\n')
        enemy_choice = random.randrange(0,2)

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ",""),"attacks", players[target].name.replace(" ",""), "for", enemy_dmg, "points of damage")

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'White':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals", enemy.name.replace(" ", ""),"for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == 'Black':

                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)

                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + "'s", spell.name + " deals", str(magic_dmg), "damage to", players[target].name.replace(" ", "") + bcolors.ENDC )

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(" ", ""), "has died.")
                    del players[target]

            # print("Enemy chose", spell, "damage is", magic_dmg)