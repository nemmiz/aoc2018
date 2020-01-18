#!/usr/bin/python3

import re
from copy import deepcopy
from itertools import zip_longest, chain


GROUP_REGEX = r'^(\d+) units each with (\d+) hit points.*with an attack that does (\d+) (\w+) damage at initiative (\d+)\s*$'
WEAKNESS_IMMUNITY_REGEX = r'.*hit points \((.*)\) with an.*'


class UnitGroup:
    def __init__(self, description, uid):
        m = re.match(GROUP_REGEX, description)
        assert m, 'Group description does not match regex'
        self.uid = uid
        self.units = int(m.group(1))
        self.hp = int(m.group(2))
        self.dmg = int(m.group(3))
        self.dmg_type = m.group(4)
        self.initiative = int(m.group(5))
        self.weaknesses = []
        self.immunities = []
        m = re.match(WEAKNESS_IMMUNITY_REGEX, description)
        if m:
            for info in m.group(1).split('; '):
                if info.startswith('weak to '):
                    self.weaknesses = info[8:].split(', ')
                elif info.startswith('immune to '):
                    self.immunities = info[10:].split(', ')
    def effective_power(self):
        return self.dmg * self.units
    def __repr__(self):
        return str(self.uid)


def selection_order(army1, army2):
    combined = list(chain(zip_longest(army1, [], fillvalue=army2), zip_longest(army2, [], fillvalue=army1)))
    combined.sort(key=lambda x: (x[0].effective_power(), x[0].initiative), reverse=True)
    for x in combined:
        yield x


def attack_order(army1, army2):
    combined = army1 + army2
    combined.sort(key=lambda group: group.initiative, reverse=True)
    for x in combined:
        yield x


def calculate_damage(attacking_group, defending_group):
    if attacking_group.dmg_type in defending_group.immunities:
        damage = 0
    else:
        damage = attacking_group.effective_power()
        if attacking_group.dmg_type in defending_group.weaknesses:
            damage *= 2
    return damage
        

def fight(imm_army, inf_army):
    attacked_by = {}
    will_attack = {}
    total_units_lost = 0
    
    for group, targets in selection_order(imm_army, inf_army):
        potential_targets = [target for target in targets if target.uid not in attacked_by]
        if potential_targets:
            potential_targets.sort(key=lambda t: (calculate_damage(group, t), t.effective_power(), t.initiative))
            target = potential_targets[-1]
            damage = calculate_damage(group, target)
            if damage > 0:
                will_attack[group.uid] = target
                attacked_by[target.uid] = group

    for group in attack_order(imm_army, inf_army):
        if group.units > 0:
            target = will_attack.get(group.uid)
            if target:
                damage = calculate_damage(group, target)
                units_lost = min(damage // target.hp, target.units)
                total_units_lost += units_lost
                target.units -= units_lost

    return total_units_lost == 0


def do_battle(imm_army, inf_army, attack_boost):
    imm_army = deepcopy(imm_army)
    inf_army = deepcopy(inf_army)

    if attack_boost > 0:
        for group in imm_army:
            group.dmg += attack_boost

    while imm_army and inf_army:
        stalemate = fight(imm_army, inf_army)
        if stalemate:
            return (None, None)
        imm_army = [group for group in imm_army if group.units > 0]
        inf_army = [group for group in inf_army if group.units > 0]

    if imm_army:
        return ('Immune System', sum((group.units for group in imm_army)))
    else:
        return ('Infection', sum((group.units for group in inf_army)))


def battle_until_immune_system_wins(imm_army, inf_army):
    result = (None, None)
    attack_boost = 0
    while result[0] != 'Immune System':
        result = do_battle(imm_army, inf_army, attack_boost)
        attack_boost += 1
    return result


def main():
    immune_system = []
    infection = []

    with open('../input/24.txt') as infile:
        current_army = None
        for line in infile:
            if line.startswith('Immune System:'):
                current_army = immune_system
            elif line.startswith('Infection:'):
                current_army = infection
            elif line.isspace():
                continue
            else:
                current_army.append(UnitGroup(line, len(immune_system)+len(infection)))

    print(do_battle(immune_system, infection, 0)[1])
    print(battle_until_immune_system_wins(immune_system, infection)[1])


if __name__ == "__main__":
    main()
