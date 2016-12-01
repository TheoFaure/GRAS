import math
import json
import numpy as np


def loss_rmse(r, list_ing, nb_ing):
    rmse = 0
    for index, ing in enumerate(r):
        rmse += (list_ing[index] - ing)**2

    rmse /= nb_ing
    rmse = math.sqrt(rmse)
    return rmse


def load_ing():
    ingredients = []
    with open("data/marmiton_ingredients_list.txt", 'r') as f:
        for line in f:
            ingredients.append(line[:-1])
    f.closed
    ingredients.append("")

    ing_indices = dict((c, i) for i, c in enumerate(ingredients))
    indices_ing = dict((i, c) for i, c in enumerate(ingredients))

    return ing_indices, indices_ing


def load_recipes():
    file_name = "data/preprocessed_recipes.json"
    with open(file_name, 'r') as f:
        recipes = json.load(f)
    f.closed

    ing_indices, indices_ing = load_ing()

    dish_indices = {'PlatPrincipal':0, 'Entree':1, 'Dessert':2, 'Sauce':3, 'Boisson':4, 'AmuseGueule':5,
                    'Confiserie':6, 'Accompagnement':7, 'Conseil':8}
    indices_dish = {0:'PlatPrincipal', 1:'Entree', 2:'Dessert', 3:'Sauce', 4:'Boisson', 5:'AmuseGueule',
                    6:'Confiserie', 7:'Accompagnement', 8:'Conseil'}

    ing_recipes = np.zeros((len(recipes), len(ing_indices)))
    print(ing_recipes.shape)
    nb_ing = ing_recipes.shape[1]
    dish_types = []
    for index, r in enumerate(recipes):
        ingred = []
        for i in r['ingredients']:
            ing_recipes[index, ing_indices[i['name']]] = 1
        # ing_recipes[index] = ingred
        dish_types.append(dish_indices[r['dishType']])

    return nb_ing, ing_recipes, dish_types, ing_indices, indices_ing, dish_indices, indices_dish



nb_ing, ing_recipes, dish_types, ing_indices, indices_ing, dish_indices, indices_dish = load_recipes()

test_ing = ["Boeuf", "Farine", "Beurre", "Bouillon", "Tomate", "Pinot noir", "Madère", "Bouquet garni", "Pomme",
            "Oignon", "Carotte", "Ail", "Chocolat"]
# test_ing = ["Chocolat", "Beurre"]

test_ing_indices = np.zeros((len(ing_indices)))
for i in test_ing:
    test_ing_indices[ing_indices[i]] = 1


min_rmse = 10000
for r in ing_recipes:
    rmse = loss_rmse(r, test_ing_indices, nb_ing)
    if rmse < min_rmse:
        min_rmse = rmse

print(min_rmse)