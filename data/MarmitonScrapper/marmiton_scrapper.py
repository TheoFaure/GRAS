from lxml import html
import requests
import re
import json

recipes_nb = 3  # 66970
recipes_per_iter = 3;
links_file = "links_to_marmiton_recipes.json"
json_file = "marmiton_recipes.json"

def get_recipes():
    recipes = [] # Url, dishType, isVegetarian
    for i in range(1, recipes_nb, recipes_per_iter):
        json_str = requests.get('http://m.marmiton.org/webservices/json.svc/GetRecipeSearch?SiteId' +
                            '=1&SearchType=0&ItemsPerPage=10&StartIndex=' + str(i))
        json_obj = json_str.json()
        for j in range(recipes_per_iter):
            new = []
            new.append(json_obj['data']['items'][j]['recipeUrl'])
            new.append(json_obj['data']['items'][j]['dishType']['token'])
            new.append(json_obj['data']['items'][j]['isVegetarian'])
            recipes.append(new)

    print(len(recipes))
    with open(links_file, 'w') as f:
        json.dump(recipes, f, ensure_ascii=False)
    f.closed

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
    # recipes = []
    # recipes.append(["http://www.marmiton.org/recettes/recette_delice-au-saumon-fume-roquette-et-asperges-vertes_325759.aspx", "PlatPrincipal", "True"])
    recipes = []

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
        print(recipe)

    json_recipes = json.dumps(recipes)

    with open(json_file, 'w') as f:
        json.dump(recipes, f, ensure_ascii=False)
    f.closed
