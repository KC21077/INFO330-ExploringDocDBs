
# import sqlite3, sys, and pymongo
import sqlite3

from pymongo import MongoClient

#Connect to MongoDB
mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']

#Connect to sqlite3 database
connection = sqlite3.connect('pokemon.sqlite')
cursor = connection.cursor()

# The General Query For Pokemon
num = " SELECT COUNT(*) FROM pokemon "
p_num = cursor.execute(num).fetchall()
x = p_num[0][0]

for i in range(1,x+1):

    poke = """SELECT pokemon.name,pokemon.pokedex_number, pokemon_types_view.type1, 
        pokemon_types_view.type2, pokemon.hp, pokemon.attack, pokemon.defense, pokemon.speed, 
        pokemon.sp_attack, pokemon.sp_defense FROM pokemon JOIN pokemon_types_view 
        ON pokemon.name = pokemon_types_view.name WHERE pokemon.pokedex_number= """ + str(i)
    p_poke = cursor.execute(poke).fetchall()
    general = p_poke[0]

#Extarct each property from p_poke
    name = general[0]
    pokedex_number = general[1]
    type1 = general[2]
    type2 = general[3]
    hp = general[4]
    attack = general[5]
    defense = general[6]
    speed = general[7]
    sp_attack = general[8]
    sp_defense = general[9]



#The Ability Query
    ab = """ SELECT ability.name
            FROM pokemon_abilities
            JOIN ability ON ability.id = pokemon_abilities.ability_id
            JOIN pokemon ON pokemon.pokedex_number = pokemon_abilities.pokemon_id
            WHERE pokemon.pokedex_number=""" + str(i)
    p_ab = cursor.execute(ab).fetchall()
    p_ab = [item[0] for item in p_ab]

# Create the JSON List
    poke_list = {
            "name": name,
            "pokedex_number": pokedex_number,
            "types": type1 + ',' + type2,
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "speed": speed,
            "sp_attack": sp_attack,
            "sp_defense": sp_defense,
            "abilities": p_ab
    }
    pokemonColl.insert_one(poke_list)

