"""Wounded-entry balance pass. Data-only; native CounterAttack remains untouched."""
from boss_design_v12 import create_bosses as previous_design

VERSION = '1.4.0'


def create_bosses(monsters, base, skill, set_skill, clear_passives):
    bosses = previous_design(monsters, base, skill, set_skill, clear_passives)

    def tune(i, hp, fields):
        boss = bosses[i - 1]
        boss['hpMultiplier'] = hp
        boss['data'].update({'m1p1': str(hp), **fields})
        return boss

    # Phoenix's on-hit/all-item fire is replaced with visible, infrequent single-item fire.
    tune(1, .48, {'eq1e1f1': 'MBD*0.26', 'eq2e1f1': 'EPL*0.035',
                 'eq3e1f1': 'MBD*0.30'})
    bosses[0]['mechanics'] = '两条各 48% 基础血量的生命\n每三轮烧一件装备，W1 为 5 点\n低血扑击 18 点，随后自身易伤'

    # A scheduled native attack, NOT the hard-coded 50% immediate CounterAttack status.
    # actorMissingHealth is the equipment owner's missing HP, not player missing HP.
    thorn = tune(2, .70, {
        'Modifier 2 Name': '', 'm2p1': '',
        'eq1name': 'Thorn Reprisal', 'eq1Effect1': 'attack',
        'eq1e1f1': 'min((MBD*0.11),(actorMissingHealth*0.10))',
        'eq1desc': 'EVEN rounds only.;Attack: 10% of own missing life, capped at [MBD*0.11].;Normal Block applies. Not an immediate on-hit counter.',
        'eq1m1p1': 'currentRound % 2 == 0',
        'eq2e1f1': 'MBD*0.22', 'eq3e1f1': 'EPD*0.08',
        'specialTooltip': 'EVEN rounds: one Thorn Reprisal, 10% of own missing life, capped at [MBD*0.11]. ODD rounds: no reprisal. No 50% CounterAttack status.'})
    thorn.update(mechanics='偶数轮一次荆棘反攻：自身已损失血量的 10%\n伤害上限 MBD×11%，W2 为 8 点，可格挡\n奇数轮不反击；低血治疗最多两次',
                 counter='奇数轮集中输出；偶数轮用护盾挡住反攻。多次小伤害不会触发多次反击。',
                 tip=thorn['data']['specialTooltip'])
    for field in ('Asset', 'BgAsset', 'EffectClass'):
        thorn['data']['eq1'+field] = skill('Tanglewood', 3)[field]

    # All native Hydra heads can act; share a hand and each has a recovery turn.
    kings = tune(3, .85, {'Visible Cards': '5',
        'eq1e1f1': 'MBD*0.18', 'eq1e2f1': 'MBD*0.055',
        'eq2e1f1': 'MBD*0.20', 'eq2e2f1': 'EPL*0.025',
        'eq3e1f1': '(MBD*0.32)*lightningMultiplier', 'eq3e1f2': 'MBD*0.32',
        'specialTooltip': 'All three heads are active at any life. K/Q/J share the same hand; each head has Cooldown 1. Jack exposes the boss.'})
    for j in range(1, 4):
        kings['data'][f'eq{j}mod1'] = 'cooldown'
        kings['data'][f'eq{j}m1p1'] = '1'
        kings['data'][f'eq{j}mod2'] = ''
        kings['data'][f'eq{j}m2p1'] = ''
        # Clear the old mutually-exclusive HP requirement text.
        desc = kings['data'][f'eq{j}desc'].split(';', 1)[1]
        kings['data'][f'eq{j}desc'] = desc if 'Cooldown' in desc else desc + ';Cooldown [cooldown].'
    kings.update(mechanics='三头均可行动，K/Q/J 共用手牌\n每个头冷却一轮，降低单头系数\nJ 雷击后自身易伤',
                 counter='观察三种王牌，优先换走关键牌；利用各头冷却和雷击后的易伤。',
                 tip=kings['data']['specialTooltip'])

    tune(4, .90, {'eq1e1f1': 'EPD*0.08', 'eq2e1f1': 'MBD*0.42', 'eq3e1f1': 'MBD*0.20'})
    tune(5, .85, {'eq2e1f1': '(MBD*0.32)*lightningMultiplier',
                 'eq2e1f2': 'MBD*0.32', 'eq3e1f1': 'EPD*0.10'})
    tune(6, .85, {'eq2e1f1': 'MBD*0.38', 'eq3e1f1': 'MBD*0.16'})
    tune(7, .90, {'eq1e1f1': 'MBD*(0.14+(min(numTimesUsed,6)*0.015))', 'eq3e1f1': 'MBD*0.45'})
    tune(8, .85, {'eq1e1f1': 'MBD*0.45', 'eq2e1f1': 'EPD*0.12',
                 'eq3e1f1': 'MBD*0.18'})
    tune(9, .85, {'eq1e2f1': 'MBD*0.08', 'eq2e1f1': 'EPC*0.30',
                 'eq2e2f1': 'MBD*0.08', 'eq3e1f1': 'MBD*0.24'})
    tune(10, .85, {'eq1e1f1': 'EPC*0.30', 'eq1e2f1': 'MBD*0.18',
                  'eq2e1f1': '(MBD*0.32)*lightningMultiplier', 'eq2e1f2': 'MBD*0.32',
                  'eq3e1f1': 'MBD*0.26', 'eq3e2f1': 'EPL*0.035'})
    tune(11, .85, {'eq1e1f1': 'MBD*0.22', 'eq1e2f1': 'MBD*0.040',
                  'eq2e1f1': 'MBD*0.28', 'eq3e1f1': 'MBD*0.40'})
    # Queen's five-card Clubs requirement occurs more often than Toad's four reds.
    tune(12, .90, {'Visible Cards': '4', 'eq1e1f1': 'MBD*0.40',
                  'eq2e1f1': 'EPD*0.12', 'eq3e1f1': 'EPD*0.10'})
    tune(13, .90, {'eq1e1f1': 'EPD*0.10', 'eq1e2f1': 'MBD*0.22', 'eq3e1f1': 'MBD*0.45'})
    for boss in bosses:
        boss['tip'] = boss['data']['specialTooltip']
    return bosses
