from lxml import html
import requests
import re
import json

recipe_start_index = 62601
recipes_nb = 4000# 66970
recipes_per_iter = 20;
links_file = "links_to_marmiton_recipes40.json"
json_file = "marmiton_recipes40.json"

def get_recipes():
    print("Beginning the scrapping of recipes from " + str(recipe_start_index) + " and of " + str(recipes_nb) + " recipes.")
    recipes = [] # Url, dishType, isVegetarian
    for i in range(recipe_start_index, recipe_start_index + recipes_nb, recipes_per_iter):
        json_str = requests.get('http://m.marmiton.org/webservices/json.svc/GetRecipeSearch?SiteId' +
                            '=1&SearchType=0&ItemsPerPage=' + str(recipes_per_iter) + '&StartIndex=' + str(i))
        json_obj = json_str.json()
        for j in range(recipes_per_iter):
            new = []
            new.append(json_obj['data']['items'][j]['recipeUrl'])
            new.append(json_obj['data']['items'][j]['dishType']['token'])
            new.append(json_obj['data']['items'][j]['isVegetarian'])
            recipes.append(new)
            if len(recipes)%50 == 0:
                print(str(len(recipes)) + " links scrapped...")

    print("All links scrapped. Write links save file...")
    print(len(recipes))
    with open(links_file, 'w') as f:
        json.dump(recipes, f, ensure_ascii=False)
    f.closed
    print("File saved.")

    return recipes


def process_str(string):
    string_processed = []
    for s in string:
        s = s.strip().replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("- ", "")
        s = " ".join(s.split())
        if s != '' and "Préparation de la recette" not in s and "Ingrédients" not in s:
            string_processed.append(s)
    return string_processed


def create_json(title, ingredients, instructions, link, dishType, veggie):
    recipe = {}
    recipe['link'] = link
    recipe['dishType'] = dishType
    recipe['isVegetarian'] = veggie
    recipe['title'] = title

    recipe['ingredients'] = []
    for s in ingredients:
        recipe['ingredients'].append(s)

    recipe['instructions'] = []
    for s in instructions:
        recipe['instructions'].append(s)

    return recipe


if __name__ == "__main__":
    recipes_infos = get_recipes()
    # with open(links_file, 'r') as f:
    #     recipes_infos = json.load(f)
    # f.closed
    recipes = []
    print("Beginning the scrapping of the recipes.")
    for link, dishType, veggie in recipes_infos:
        page = requests.get(link)

        #process on the html page
        page_str = str(page.text)
        page_str = re.sub('<[\/]?a[^>]*>', '', page_str)

        tree = html.fromstring(page_str)

        title = tree.xpath('//h1[contains(@class, m_title) and contains(@class, fn)]/span/span/text()')
        ingredients = tree.xpath('//*[@id="m_content"]/div[2]/div[2]/div[4]/div[2]/div[1]//text()')
        instructions = tree.xpath('//*[@id="m_content"]/div[2]/div[2]/div[4]/div[2]/div[3]//text()')

        ingredients = process_str(ingredients)
        instructions = process_str(instructions)

        recipe = create_json(title, ingredients, instructions, link, dishType, veggie)
        recipes.append(recipe)
        if len(recipes) % 20 == 0:
            print(str(len(recipes)) + " recipes scrapped...")

    json_recipes = json.dumps(recipes)
    print("All recipes scrapped. Writing recipes save file...")

    with open(json_file, 'w') as f:
        json.dump(recipes, f, ensure_ascii=False)
    f.closed
    print("Terminated. :)")
