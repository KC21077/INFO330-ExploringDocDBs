import random
from pymongo import MongoClient

mongoClient = MongoClient("mongodb://localhost/pokemon")
pokemonDB = mongoClient['pokemondb']
pokemonColl = pokemonDB['pokemon_data']

def fetch(pokemonid):
    return pokemonColl.find_one({"pokedex_number":pokemonid})

####Add a scoring system to compare the relative importance of each property
def calculate_score(pokemon):
    points = {
        'hp': 1,
        'attack': 2,
        'defense': 2,
        'speed': 3,
        'sp_attack': 4,
        'sp_defense': 4
    }
####Calculate the total score for the pokemon
    score = sum(pokemon[stat] * points[stat] for stat in points)
    return score

def battle(pokemon1, pokemon2):
    print("Let the Pokemon battle begin! ================")
    print("It's " + pokemon1['name'] + " vs " + pokemon2['name'])
####Show the scores for both pokemon
    pokemon1_score = calculate_score(pokemon1)
    pokemon2_score = calculate_score(pokemon2)

    for stat in ['hp', 'attack', 'defense', 'speed', 'sp_attack', 'sp_defense']:
        if pokemon1[stat] > pokemon2[stat]:
            print(pokemon1['name'] + " has the advantage in " + stat)
        elif pokemon2[stat] > pokemon1[stat]:
            print(pokemon2['name'] + "'s " + stat + " is superior")

    ####Compare the scores of the pokemon to see the winner
    if pokemon1_score > pokemon2_score:
        print(pokemon1['name'] + " wins with a score of " + str(pokemon1_score) + "!")
    elif pokemon2_score > pokemon1_score:
        print(pokemon2['name'] + " wins with a score of " + str(pokemon2_score) + "!")
    else:
        print("It's a tie with a score of " + str(pokemon1_score) + "!")

    winner = random.randrange(2)
    if winner == 0: print("Battle results: " + pokemon1['name'])
    if winner == 1: print("Battle results: " + pokemon2['name'])

def main():
    # Fetch two pokemon from the MongoDB database
    pokemon1 = fetch(random.randrange(801))
    pokemon2 = fetch(random.randrange(801))

    # Pit them against one another
    battle(pokemon1, pokemon2)

main()
