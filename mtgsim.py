import random
import math
from pprint import pprint

c_art_slot = [('signed', 5), ('non-signed', 95)]
c_land_slot = [('foil', 15), ('non-foil', 85)]
c_connected_slot = [
        ({'U': 6, 'C': 0}, 2),
        ({'U': 5, 'C': 1}, 3.5),
        ({'U': 4, 'C': 2}, 7),
        ({'U': 3, 'C': 3}, 12.5),
        ({'U': 2, 'C': 4}, 40),
        ({'U': 1, 'C': 5}, 35)
]
c_showcase_slot = [('uncommon', 58.82), ('common', 41.18)]
c_wildcard_slot = [
        ({'RM': (2, None), 'U': 0, 'C': 0, 'R': 0, 'M': 0}, 1.6),
        ({'RM': (1, None), 'U': 1, 'C': 0, 'R': 0, 'M': 0}, 4.3),
        ({'RM': (0, None), 'U': 2, 'C': 0, 'R': 0, 'M': 0}, 3.1),
        ({'RM': (1, None), 'U': 0, 'C': 1, 'R': 0, 'M': 0}, 17.5),
        ({'RM': (0, None), 'U': 1, 'C': 1, 'R': 0, 'M': 0}, 24.5),
        ({'RM': (0, None), 'U': 0, 'C': 2, 'R': 0, 'M': 0}, 49)
]
c_rare_slot = [('mythic', 13.5), ('rare', 86.5)]
c_foil_slot = [('mythic', 1), ('rare', 6.2), ('uncommon', 21.4), ('common', 71.4)]
c_token_slot = [('list', 25), ('token', 75)]


def simulate_pack():
    pack = dict()
    pack = {
            'art_slot' : random.choices(c_art_slot, cum_weights=(c_art_slot[0][1], c_art_slot[1][1]), k=1),
            'land_slot' : random.choices(c_land_slot, cum_weights=(c_land_slot[0][1], c_land_slot[1][1]), k=1),
            'connected_slot' : random.choices(c_connected_slot, cum_weights=(
                    c_connected_slot[0][1],
                    c_connected_slot[1][1],
                    c_connected_slot[2][1],
                    c_connected_slot[3][1],
                    c_connected_slot[4][1],
                    c_connected_slot[5][1]
                ),
                k=1
            ),
            'showcase_slot' : random.choices(c_showcase_slot, cum_weights=(
                    c_showcase_slot[0][1],
                    c_showcase_slot[1][1]
                ),
                k=1
            ),
            'wildcard_slot': random.choices(c_wildcard_slot, cum_weights=(
                    c_wildcard_slot[0][1],
                    c_wildcard_slot[1][1],
                    c_wildcard_slot[2][1],
                    c_wildcard_slot[3][1],
                    c_wildcard_slot[4][1],
                    c_wildcard_slot[5][1],
            ),
                k=1
            ),
            'rare_slot': random.choices(c_rare_slot, cum_weights=(c_rare_slot[0][1], c_rare_slot[1][1]), k=1),
            'foil_slot': random.choices(c_foil_slot, cum_weights=(
                    c_foil_slot[0][1],
                    c_foil_slot[1][1],
                    c_foil_slot[2][1],
                    c_foil_slot[3][1]
                ),
                k=1
            ),
            'token_slot': random.choices(c_token_slot, cum_weights=(c_token_slot[0][1], c_rare_slot[1][1]), k=1)
    }
    # pprint(pack)
    if pack['wildcard_slot'][0][0]['RM'][0] and (pack['wildcard_slot'][0][1] == 1.6 or pack['wildcard_slot'][0][1] == 4.3 or pack['wildcard_slot'][0][1] == 17.5):
        rare_mythic = random.choices(c_rare_slot,
                                     cum_weights=(c_rare_slot[0][1], c_rare_slot[1][1]),
                                     k=pack['wildcard_slot'][0][0]['RM'][0])
        pack['wildcard_slot'][0][0]['R'] = list()
        pack['wildcard_slot'][0][0]['M'] = list()
        for card in rare_mythic:
            if card[0] == 'rare':
                pack['wildcard_slot'][0][0]['R'].append(c_rare_slot[1])
            if card[0] == 'mythic':
                pack['wildcard_slot'][0][0]['M'].append(c_rare_slot[0])
        pack = calc_wildcard_slot(pack)




        # print(f'Rares: {num_rares} {[round(rare_perm_chance, 2) if rare_perm_chance else ""][0]}%')
        # print(f'Mythics: {num_mythics} {[round(mythic_perm_chance, 2) if mythic_perm_chance else ""][0]}%\n')


        # rare_count_prob = (((c_rare_slot[1][1]/100)**len(pack['wildcard_slot'][0][0]['R']))*(pack['wildcard_slot'][0][1]/100))*100
        # print(round(rare_count_prob,2))

        # pprint(pack)
    return pack

def print_pack(in_pack):

    mythic_chance = ""
    mythic_count = 0
    rare_chance = ""
    rare_count = 0
    total_wildcard_rarity = None
    wildcard_chance = ""

    # pprint(in_pack)
    # print([x for x in in_pack['wildcard_slot'][0][0]['M'] if x[0] == 'total'])
    # print([x for x in in_pack['wildcard_slot'][0][0]['R'] if x[0] == 'total'])

    if in_pack['wildcard_slot'][0][0]['RM'][0]:
        mythic_count = sum([1 for x in in_pack['wildcard_slot'][0][0]['M'] if x[0] == 'mythic'])
        rare_count = sum([1 for x in in_pack['wildcard_slot'][0][0]['R'] if x[0] == 'rare'])

        if not [x for x in in_pack['wildcard_slot'][0][0]['M'] if x[0] == 'total'] and not [x for x in in_pack['wildcard_slot'][0][0]['R'] if x[0] == 'total']:
            in_pack = calc_wildcard_slot(in_pack)

        # pprint(in_pack['wildcard_slot'][0][0]['M'] + in_pack['wildcard_slot'][0][0]['R'])
        total_rm_rarities = [x[1]/100 for x in in_pack['wildcard_slot'][0][0]['M'] + in_pack['wildcard_slot'][0][0]['R'] if x[0] != 'total']
        total_wildcard_rarity = round(((math.prod(total_rm_rarities)*(in_pack['wildcard_slot'][0][1]/100))*100), 2)
        wildcard_chance = "Total: "+str(total_wildcard_rarity)+"%"
        # print(total_wildcard_rarity)

        # pprint(in_pack)
        if [x[1] for x in in_pack['wildcard_slot'][0][0]['M'] if x[0] == 'total'][0]:
            mythic_chance = [x[1] for x in in_pack['wildcard_slot'][0][0]['M'] if x[0] == 'total'][0]
            mythic_chance = f'{mythic_chance}%'
        if [x[1] for x in in_pack['wildcard_slot'][0][0]['R'] if x[0] == 'total'][0]:
            rare_chance = [x[1] for x in in_pack['wildcard_slot'][0][0]['R'] if x[0] == 'total'][0]
            rare_chance = f'{rare_chance}%'

    # if total_wildcard_rarity < 0.19:
    print(f'Art Slot: {in_pack["art_slot"][0][0]} {in_pack["art_slot"][0][1]}%')
    print(f'Land Slot: {in_pack["land_slot"][0][0]} {in_pack["land_slot"][0][1]}%')
    print('Connected Slots: {}%\n  Uncommons: {} \n  Commons: {}'.format(
        in_pack['connected_slot'][0][1],
        in_pack['connected_slot'][0][0]['U'],
        in_pack['connected_slot'][0][0]['C'],
    )
    )
    print(f'Showcase Slot: {in_pack["showcase_slot"][0][0]} {in_pack["showcase_slot"][0][1]}%')
    print('Wildcard Slots: {}% {}\n  Mythic: {} {}\n  Rare: {} {}\n  Uncommons: {}\n  Commons: {}'.format(
        in_pack['wildcard_slot'][0][1],
        wildcard_chance,
        mythic_count,
        mythic_chance,
        rare_count,
        rare_chance,
        in_pack['wildcard_slot'][0][0]['U'],
        in_pack['wildcard_slot'][0][0]['C']
    )
    )
    print(f'Rare Slot: {in_pack["rare_slot"][0][0]} {in_pack["rare_slot"][0][1]}%')
    print(f'Foil Slot: {in_pack["foil_slot"][0][0]} {in_pack["foil_slot"][0][1]}%')
    print(f'Token Slot: {in_pack["token_slot"][0][0]} {in_pack["token_slot"][0][1]}%')

    if not total_wildcard_rarity:
        total_wildcard_rarity = in_pack['wildcard_slot'][0][1]
    total_pack_rarity = get_total_rarity(in_pack, total_wildcard_rarity)
    print(f'Total: {total_pack_rarity:.7f}%')

    # print(f'Total Pack Rarity: {total_pack_rarity}%')


def get_total_rarity(calc_pack, wildcard_rm):
    # print(wildcard_rm)
    art = calc_pack["art_slot"][0][1]/100
    land = calc_pack["land_slot"][0][1]/100
    connected = calc_pack['connected_slot'][0][1]/100
    showcase = calc_pack["showcase_slot"][0][1]/100
    wildcard = wildcard_rm/100
    rare = calc_pack["rare_slot"][0][1]/100
    foil = calc_pack["foil_slot"][0][1]/100
    token = calc_pack["token_slot"][0][1]/100
    # print([art, land, connected, showcase, wildcard, rare, foil, token])
    total_rarity = math.prod([art, land, connected, showcase, wildcard, rare, foil, token])*100
    # print(total_rarity)
    return total_rarity


def calc_wildcard_slot(pack):
    num_rares = len(pack['wildcard_slot'][0][0]['R'])
    num_mythics = len(pack['wildcard_slot'][0][0]['M'])
    rare_perm_chance = None
    mythic_perm_chance = None
    if num_rares:
        rare_chance = (c_rare_slot[1][1]/100)**num_rares
        wildcard_chance = pack['wildcard_slot'][0][1]/100
        rare_perm_chance = round((rare_chance*wildcard_chance)*100, 2)
    pack['wildcard_slot'][0][0]['R'].append(('total', rare_perm_chance))

    if num_mythics:
        mythic_chance = (c_rare_slot[0][1]/100)**num_mythics
        wildcard_chance = pack['wildcard_slot'][0][1]/100
        mythic_perm_chance = round((mythic_chance*wildcard_chance)*100, 2)
    pack['wildcard_slot'][0][0]['M'].append(('total', mythic_perm_chance))

    return pack


# test_pack = {'art_slot': [('non-signed', 95)],
#              'connected_slot': [({'C': 4, 'U': 2}, 40)],
#              'foil_slot': [('mythic', 1)],
#              'land_slot': [('non-foil', 85)],
#              'rare_slot': [('mythic', 13.5)],
#              'showcase_slot': [('uncommon', 58.82)],
#              'token_slot': [('token', 75)],
#              'wildcard_slot': [({'C': 0,
#                                  'M': [('mythic', 13.5), ('mythic', 13.5)],
#                                  'R': [],
#                                  'RM': (2, None),
#                                  'U': 0},
#                                 1.6)]}
# #
# #
# print_pack(test_pack)
for x in range(1):
    s_pack = None
    s_pack = simulate_pack()
    # if s_pack['wildcard_slot'][0][1] == 1.6:
    print(f'Pack: {x}')
    # pprint(s_pack)
    print_pack(s_pack)


