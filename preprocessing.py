import json
import nltk
import re

stop_words_ingredients = ["", "de", "d", "l", "le", "la", "au", "a", "gros",
                          "grosse", "petit", "petite", "bien mûr", "bien mûre"]

unit_words = "(g|kg|mg|ml|l|cl|dl|cuillère à café|cuillère|cuillère à soupe|noix de|noisette de|paquet|verre)"

nb_files = 2


def load_recipes():
    recipes = []
    for i in range(1, nb_files+1):
        file_name = "marmiton_recipes" + str(i) + ".json"
        with open(file_name, 'r') as f:
            recipe = json.load(f)
            recipes.append(recipe)
        f.closed
    return recipes


def remove_stop_words(word):
    words = word.split('\'')
    for w in words:
        if w not in stop_words_ingredients:
            return w
    return ""


def get_qty_name_unit(ingredient):
    words = ingredient.split()
    qty = 0
    name = ""
    unit = "qty"
    qty_found = False
    unit_found = True
    for w in words:
        if re.match("^[0-9]*(\/)*[0-9]*", w) and not qty_found:
            if re.match("^[0-9]*(\/)[0-9]*", w):
                nb = w.split('/')
                qty = nb[0] / nb[1]
            else:
                qty = int(w)
            qty_found = True

        if re.match(unit_words, w) and not unit_found:
            unit = w
            unit_found = True

        if not re.match("^[0-9]*(\/)*[0-9]*", w) and not re.match(unit_words, w):
            w_filtered = remove_stop_words(w)
            " ".join([name, w])

    return qty, name, unit


def stemming_ingredients(i, stemmer):
    i = i.lower()
    words = i.split()
    for w in words:
        w = stemmer.stem(w)
        if w[0] == '-':
            w = w[1:]
    i = " ".join(words)
    return i


if __name__ == "__main__":
    recipes = load_recipes()
    recipes_modified = []
    stemmer = nltk.PorterStemmer("french", ignore_stopwords=True)
    for r in recipes:
        recipe_mod = {}
        recipe_mod['link'] = r['link']
        recipe_mod['dishType'] = r['dishType']
        recipe_mod['isVegetarian'] = r['veggie']
        recipe_mod['title'] = r['title'].lower()

        recipe_mod['ingredients'] = []
        for i in r['ingredients']:
            i_stemmed = stemming_ingredients(i, stemmer)
            ingredient = {}
            ingredient['qty'], ingredient['name'], ingredient['unit'] = get_qty_name_unit(i_stemmed)
            recipe_mod['ingredients'].append(ingredient)

        recipe_mod['instructions'] = []
        for s in r['instructions']:
            recipe_mod['instructions'].append(s)
