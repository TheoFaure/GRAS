import sys, getopt
import json

recipes = []
nb_recipes = 0
ingredients = []


def prob_iIC(i, I, C, list_proba):
    # P(i|I,C)
    # I is an array of all the given ingredients
    if list_proba == 0:
        return 0
    else:
        return prob_IC([i]+I, C) / list_proba

def prob_IC(I, C):
    #P(I, C)
    prob = 0
    global recipes
    global nb_recipes
    for recipe in recipes:
        if recipe['dishType'] in C:
            if not False in [(Ik in [i['name'] for i in recipe['ingredients']]) for Ik in I]:
                prob += 1
    prob /= nb_recipes
    return prob

def load_recipes():
    file_name = "data/preprocessed_recipes.json"
    global recipes
    global nb_recipes
    with open(file_name, 'r') as f:
        recipes = json.load(f)
    f.closed

    nb = 0
    for recipe in recipes:
        nb += 1
    nb_recipes = nb


def load_ing():
    with open("data/marmiton_ingredients_list.txt", 'r') as f:
        global ingredients
        for line in f:
            ingredients.append(line[:-1])
    f.closed


def mean_nb_ing(ing_list, C):
    nb_ing = 0
    nb_of_class = 0
    global recipes
    global nb_recipes
    for recipe in recipes:
        if recipe['dishType'] in C:
            nb_of_class += 1
            if not False in [(Ik in [i['name'] for i in recipe['ingredients']]) for Ik in ing_list]:
                nb_ing += len([i for i in recipe['ingredients']])
    nb_ing /= nb_of_class
    return nb_ing


def generate_ing_list(list_ing, list_classes):
    nb_out_ing = mean_nb_ing(list_ing, list_classes)
    print("Recipe with %i ingredients"%nb_out_ing)
    for i in range(int(nb_out_ing+3)):
        max_prob = 0
        max_prob_ing = ""
        for new_ing in ingredients:
            if new_ing not in list_ing:
                list_proba = prob_IC(list_ing, list_classes)
                proba_new = prob_iIC(new_ing, list_ing, list_classes, list_proba)
                if proba_new > max_prob:
                    max_prob_ing = new_ing
                    max_prob = proba_new
        list_ing.append(max_prob_ing)
    return list_ing


if __name__ == "__main__":
    param_ing = ""
    param_class = ""
    print(sys.argv)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:c:", ["ingredients=", "classes="])
    except getopt.GetoptError:
        print('generate_recipes_bayes.py -i "<ingredients1>,<ingredient2>,<ingredientN>" -c "<class1>,<class2>,<classN>"')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generate_recipes_bayes.py -i "<ingredients1>,<ingredient2>,<ingredientN>" -c "<class1>,<class2>,<classN>"')
            sys.exit()
        elif opt in ("-i", "--ingredients"):
            param_ing = arg
        elif opt in ("-c", "--classes"):
            param_class = arg

    if param_ing == "":
        print("Give at least 1 ingredient")
        print('generate_recipes_bayes.py -i "<ingredients1>,<ingredient2>,<ingredientN>" -c "<class1>,<class2>,<classN>"')
        sys.exit(2)
    else:
        list_ing = param_ing.split(',')

    if param_class == "":
        list_classes = ['PlatPrincipal', 'Entree', 'Dessert', 'Sauce', 'Boisson', 'AmuseGueule', 'Confiserie', 'Accompagnement']
    else:
        list_classes = param_class.split(',')

    load_ing()
    load_recipes()

    print(ingredients)

    print(list_ing, list_classes)
    list_ing = generate_ing_list(list_ing, list_classes)

    print("Your new fucking recipe is composed of: %s"%', '.join(list_ing))