import requests

hero_names = ['Hulk', 'Captain America', 'Thanos']


def smartest_hero(hero_list):
    result = {}
    for name in hero_list:
        response_by_hero = requests.get(f'https://superheroapi.com/api/2619421814940190/search/{name}')
        list_of_heroes = response_by_hero.json()['results']
        for hero in list_of_heroes:
            if hero['name'] == name:
                result[name] = int(int(hero['powerstats']['intelligence']))
    return max(result)


print(smartest_hero(hero_names))
