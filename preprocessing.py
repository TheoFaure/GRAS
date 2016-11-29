import json
import nltk
import re
from nltk.stem import SnowballStemmer


dict_ingred = {}


stop_words_ingredients = ["", "de", "d", "l", "le", "la", "au", "a", "à", "des", "les", "grosse", "grosses", "bien", "cuillères"]

unit_words = re.compile("^(g|kg|mg|ml|l|cl|dl|paquet|verre)$")
# unit_words = "( g | kg | mg | ml | l | cl | dl | cuillère à café | cuillère | cuillère à soupe " \
#              "| noix de (?!cajou|coco|macadamia|saint-jacques|pécan|grenoble)| noisette de | paquet | verre )"

nb_files = 2
json_file = "data/preprocessed_recipes.json"


def load_recipes():
    list_recipes = []
    for i in range(1, nb_files+1):
        file_name = "data/MarmitonScrapper/marmiton_recipes" + str(i) + ".json"
        with open(file_name, 'r') as f:
            recipes_in_file = json.load(f)
            for recipe in recipes_in_file:
                list_recipes.append(recipe)
        f.closed
    return list_recipes


def remove_stop_words(word):
    words = word.split('\'')
    for w in words:
        if w not in stop_words_ingredients:
            return w
    return ""


def get_qty_name_unit(ingredient):
    ingredient = ingredient.lower()
    words = ingredient.split()
    qty = 0
    name = ""
    unit = ""
    qty_found = False
    for w in words:
        if any(char.isdigit() for char in w) and not qty_found:
            if w.isdigit():
                qty = int(w)
            elif w[0].isdigit():
                qty = int(w[0])
            else:
                qty=0
            qty_found = True
        elif unit_words.match(w):
            unit = w
        else:
            w_filtered = remove_stop_words(w)
            name = " ".join([name, w_filtered])

    name_std = get_standard_ingredient(name)
    print("In: %s, Out: %i, %s, %s"%(ingredient, qty, unit, name_std))
    return qty, name_std, unit


# def get_qty_name_unit(ingredient):
#     ingredient = ingredient.lower()
#     words = ingredient.split()
#     qty = 0
#     name = ""
#     unit = "qty"
#     qty_found = False
#     unit_found = True
#     for i, w in enumerate(words):
#         print(w)
#         if re.match("^[0-9]*(\/)*[0-9]*", w) and not qty_found:
#             if re.match("^[0-9]*(\/)[0-9]*", w):
#                 nb = w.split('/')
#                 while not nb[0].isdigit() and nb[0] is not "":
#                     nb[0] = nb[0][:-1]
#                 while not nb[1].isdigit() and nb[1] is not "":
#                     nb[1] = nb[1][:-1]
#                 if nb[0] is "" or nb[1] is "":
#                     qty = 0
#                 else:
#                     qty = float(nb[0]) / float(nb[1])
#             else:
#                 while not w.isdigit() and w is not "":
#                     w = w[:-1]
#                 if w is "":
#                     qty = 0
#                 else:
#                     qty = int(w)
#             qty_found = True
#             print("qty: %i"%qty)
#
#         if re.match(unit_words, w) and not unit_found:
#             unit = w
#             unit_found = True
#
#         if not re.match("^[0-9]*(\/)*[0-9]*", w) and not re.match(unit_words, w):
#             w_filtered = remove_stop_words(w)
#             " ".join([name, w_filtered])
#
#     return qty, name, unit


def stem_ingred_list():
    stemmer = SnowballStemmer("french", ignore_stopwords=True)
    with open("data/marmiton_ingredients_list.txt", 'r') as f:
        for line in f:
            l_key = line[:-1]
            l = l_key.lower()
            l_split = l.split()
            # next line we create a string with the stemmed words, without stop words of the list.
            dict_ingred[l_key] = " ".join([stemmer.stem(remove_stop_words(w)) for w in l_split])
    f.closed


def get_standard_ingredient(ingredient):
    ing_array = ingredient.split()
    stemmer = SnowballStemmer("french", ignore_stopwords=True)
    ingr_stem = " ".join([stemmer.stem(i) for i in ing_array])
    standard_ing = find_closest_ing(ingr_stem, ingredient)
    return standard_ing


def find_closest_ing(ingr_stem, ingr_norm):
    for i in sorted(dict_ingred, key=lambda j : len(dict_ingred[j]), reverse=True):
        if ingr_norm == dict_ingred[i]:
            return i

    for i in sorted(dict_ingred, key=lambda j : len(dict_ingred[j]), reverse=True):
        if ingr_stem == dict_ingred[i]:
            return i

    dist_min = 10000
    i_min = ""

    for i in sorted(dict_ingred, key=lambda j : len(dict_ingred[j]), reverse=True):
        dist = distance_ingr(ingr_stem, dict_ingred[i])
        if dist == 0:
            return i
        elif dist < dist_min:
            i_min = i

    print(ingr_stem, dict_ingred[i_min])
    return i_min


def distance_ingr(my_ing, std_ing):
    if std_ing in my_ing:
        return 0
    else:
        return 1


if __name__ == "__main__":
    recipes = load_recipes()
    stem_ingred_list()
    recipes_modified = []
    for r in recipes:
        recipe_mod = {}
        recipe_mod['link'] = r['link']
        recipe_mod['dishType'] = r['dishType']
        recipe_mod['isVegetarian'] = r['isVegetarian']
        recipe_mod['title'] = r['title'][0].lower()

        recipe_mod['ingredients'] = []
        for i in r['ingredients']:
            ingredient = {}
            ingredient['qty'], ingredient['name'], ingredient['unit'] = get_qty_name_unit(i)
            recipe_mod['ingredients'].append(ingredient)

        recipe_mod['instructions'] = []
        for s in r['instructions']:
            recipe_mod['instructions'].append(s)

        recipes_modified.append(recipe_mod)

    with open(json_file, 'w') as f:
        json.dump(recipes_modified, f, ensure_ascii=False)
    f.closed
