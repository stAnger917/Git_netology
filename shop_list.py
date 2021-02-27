from files_homework import get_cook_book
import pprint

dishes = get_cook_book()

# This func will get list of dishes from da cook_book

def get_dish_list(dish_cook_book):
    dish_list = list(dish_cook_book.keys())
    return dish_list


dish_lst = get_dish_list(dishes)


def get_shop_list_by_dishes(dish, persons):
    result = {}
    for i in range(len(dish)):
        a = dishes.get(dish[i])
        for k in range(len(a)):
            ingr = a[k].get('ingredient_name')
            measure = a[k].get("measure")
            quantity = (int(a[k].get("quantity"))) * persons
            if ingr not in result:
                result[ingr] = {"measure": measure, "quantity": quantity}
            else:
                existed_ingr = result.get(ingr)
                tmp = existed_ingr.get('quantity') + quantity
                result[ingr] = {"measure": measure, "quantity": tmp}
    return result


pprint.pprint(get_shop_list_by_dishes(dish_lst, 3))
