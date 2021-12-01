import numpy as np


def main(input_lines):
    foods = parse_input(input_lines)
    allergen_to_ingredient, all_ingredients = match_allergen_to_ingredient(foods)
    inert_ingredients = find_inert_ingredients(all_ingredients, allergen_to_ingredient)

    part1_answer = 0
    for ingredients, _ in foods:
        for ingredient in ingredients:
            if ingredient in inert_ingredients:
                part1_answer += 1

    sorted_allergen_ingredients = []
    for allergen in sorted(allergen_to_ingredient.keys()):
        sorted_allergen_ingredients.append(allergen_to_ingredient[allergen])
    part2_answer = ','.join(sorted_allergen_ingredients)

    return part1_answer, part2_answer


def parse_input(input_lines):
    foods = []
    for input_line in input_lines:
        ingredients_raw, allergens_raw = input_line.split('contains')
        ingredients = ingredients_raw[:-2].split(' ')
        allergens = allergens_raw[1:-2].split(', ')
        foods.append((ingredients, allergens))
    return foods


def match_allergen_to_ingredient(foods):
    all_ingredients = set()
    allergen_to_ingredient_hypothesis = {}
    for ingredients, allergens in foods:
        for allergen in allergens:
            if allergen not in allergen_to_ingredient_hypothesis:
                allergen_to_ingredient_hypothesis[allergen] = set(ingredients)
            else:
                allergen_to_ingredient_hypothesis[allergen] = allergen_to_ingredient_hypothesis[allergen].intersection(ingredients)
        all_ingredients = all_ingredients.union(ingredients)

    all_allergens = list(allergen_to_ingredient_hypothesis.keys())
    confirmed_allergens = np.full((len(all_allergens),), False)
    while not np.all(confirmed_allergens):
        for i, allergen in enumerate(all_allergens):
            if confirmed_allergens[i]:
                continue
            ingredients = allergen_to_ingredient_hypothesis[allergen]
            if len(ingredients) == 1:
                ingredient = list(ingredients)[0]
                allergen_to_ingredient_hypothesis[allergen] = ingredient
                confirmed_allergens[i] = True
                for j, other_allergen in enumerate(all_allergens):
                    if confirmed_allergens[j]:
                        continue
                    allergen_to_ingredient_hypothesis[other_allergen].discard(ingredient)

    return allergen_to_ingredient_hypothesis, all_ingredients


def find_inert_ingredients(all_ingredients, allergen_to_ingredient):
    allergen_ingredients = set(allergen_to_ingredient.values())
    inert_ingredients = all_ingredients.difference(allergen_ingredients)
    return inert_ingredients
