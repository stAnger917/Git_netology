def get_cook_book():
    with open('recipes.txt', 'r', encoding="utf-8") as f:
        tmp = f.read()

    cook_book = {}
    load_lst = tmp.split('\n\n')

    for item in load_lst:
        dish = item.split('\n')
        dish_name = dish.pop(0)
        dish.pop(0)
        dish_recipe_tmp = []
        for i in dish:
            tmp_string = str(i)
            tmp_ingridient = (tmp_string.split("|"))

            dish_ingridient = {"ingredient_name": tmp_ingridient[0].strip(), 'quantity': tmp_ingridient[1].strip(),
                               'measure': tmp_ingridient[2].strip()}
            print(dish_ingridient)
            dish_recipe_tmp.append(dish_ingridient)
            cook_book[dish_name] = dish_recipe_tmp

    return cook_book

