"""Native CSV boss designs. No executable patch or invented engine effects."""
VERSION = '1.1.0'

def create_bosses(monsters, base, skill, set_skill, clear_passives):
    bosses=[]
    def add(source,index,name,cn,asset,region,cards,hp,mechanics,counter,tip,origin):
        b=base(source,index,name,tip,region)
        x=b['data']; clear_passives(x)
        for i in range(1,4): set_skill(x,i,{})
        x.update({'asset':asset,'musicAsset':'','Visible Cards':str(cards),'Hidden Cards':'0',
                  'Modifier 1 Name':'modifyHp','m1p1':str(hp),
                  'backgroundAsset':monsters[source]['backgroundAsset'],
                  'class1':'attack','class2':'timed','class3':''})
        b.update({'cn':cn,'mechanics':mechanics,'counter':counter,'origin':origin,'hpMultiplier':hp})
        bosses.append(b)
        return x
    def use(x,slot,source,source_slot,**changes):
        s=skill(source,source_slot)
        # Probability columns are refreshed by the builder. Reusability and
        # hidden inherited effects are cleared before the new design is added.
        s={k:v for k,v in s.items() if k not in ('Effect1','Effect2','Effect3')
           and not k.startswith(('mod','m1p','m2p','e1','e2','e3'))}
        s.update(changes)
        set_skill(x,slot,s)
    def attack(mult): return {'Effect1':'attack','e1f1':'MBD*e1p1','e1p1':str(mult)}
    def lightning(mult):
        return {'Effect1':'lightning','e1f1':'MBD*e1p1*lightningMultiplier',
                'e1f2':'MBD*e1p1','e1p1':str(mult)}
    def cooldown(n): return {'mod1':'cooldown','m1p1':str(n)}
    def vulnerable(effect=2): return {f'Effect{effect}':'vulnerable',f'e{effect}f1':'1',f'e{effect}f2':'self'}

    x=add('Phoenix',1,'Ashwing','灰烬之翼','phoenix','plains',4,.5,
          '受击令装备燃烧；复活一次\n四红牌：攻击并治疗\n主技能冷却，治疗最多两次',
          '减少低伤连击；复活前留好资源。主技能冷却期间进攻。',
          'Revives once at half base HP. Hits Enflame your items. Royal Flare has a cooldown and two uses.', 'active-monster')
    x.update({'Modifier 2 Name':'revive','m2p1':'1','Modifier 3 Name':'onGetHit',
              'm3description':'Enflame All [m3f2], when hit','m3f1':'enflameAll','m3f2':'[m3p1]*EPL','m3p1':'0.006'})
    use(x,1,'Phoenix',1,name='Royal Flare',query='4 red cards',queryparams='',
        desc='Attack [e1f1].;Heal [e2f1].;Cooldown [cooldown].;2 uses per combat.',
        **attack(.4),Effect2='heal',e2f1='EPD*e2p1',e2p1='.15',
        **cooldown(1),mod2='numUsesPerCombat',m2p1='2')
    use(x,2,'Red Dragon',3,name='Cinder Talons',query='3 black cards',queryparams='',desc='Attack [e1f1].',**attack(.25))

    x=add('Tanglewood',2,'Old Thorn','老荆棘','tanglewood','swamp',4,1,
          '周期魅惑一个装备\n总和 30 重击、40 治疗\n治疗最多两次且有冷却',
          '留意被魅惑装备送出的牌；小牌可减少帮助敌方凑总和的风险。',
          'Charm transfers your used cards. One item is targeted at a time; healing is limited to two uses.', 'dormant-boss')
    use(x,1,'Tanglewood',1,name='Tribute of Thorns',
        desc='Charm [e1f1], to [e1f2] arbitrary hero items.;Cooldown [cooldown].',
        Effect1='charm',e1f1='1',e1f2='1',e1f3='enemy',e1p2='noDuplicates',**cooldown(1))
    use(x,2,'Tanglewood',2,name='Root Renewal',query='at least 40',queryparams='',
        desc='Heal [e1f1].;Cooldown [cooldown].;2 uses per combat.',
        Effect1='heal',e1f1='EPD*e1p1',e1p1='.25',**cooldown(2),mod2='numUsesPerCombat',m2p1='2')
    use(x,3,'Count Spade',2,name='Crown Strike',query='at least 30',queryparams='',desc='Attack [e1f1].',**attack(.5))

    x=add('Hydra',3,'Three Kings','三王','hydra','desert',5,.95,
          'K：毒与易燃\nQ：燃烧与共享雷击机会\nJ：雷击与贫血；各有冷却',
          '敌方全部明牌；优先破坏能形成连续状态联动的王室牌。',
          'K/Q/J retain their identities. All cards are visible; each head has a cooldown.', 'active-monster')
    for i in range(1,4):
        s=skill('Hydra',i); s.update(cooldown(1));
        s['desc'] += ';Cooldown [cooldown].'
        s['e1p1']=['.08','.018','.32'][i-1]
        set_skill(x,i,s)

    x=add('Leviathan',4,'River Serpent','河牌巨蛇','leviathan','sea',4,1,
          '对子：后续明牌抽牌 +2\n四条：吞噬并抽牌 -4\n吞噬后易伤，成长带冷却',
          '抽牌增加是危险信号；留防御应对吞噬，再利用易伤反击。',
          'Pairs grow visible draw. Devour consumes that growth and makes the boss Vulnerable.', 'active-monster')
    use(x,1,'Leviathan',1,name='Devour',desc='Attack [e1f1].;Draw -4 visible.;Become Vulnerable 1.;Cooldown [cooldown].',
        **attack(1),Effect2='increaseDraw',e2f1='-4',e2f2='self',e2f3='visible',**vulnerable(3),**cooldown(1))
    use(x,2,'Leviathan',2,name='Rising Tide',desc='Draw +2 visible.;Cooldown [cooldown].',
        Effect1='increaseDraw',e1f1='2',e1f2='self',e1f3='visible',**cooldown(1))
    use(x,3,'Knight of Clubs',1,name='Undertow',query='2 black cards',queryparams='',desc='Attack [e1f1].',**attack(.18))

    x=add('Storm Titan',5,'Thunder Giant','雷霆巨人','storm_titan','mountains',5,.95,
          '周期提供共享 Ionize 2\n三红牌雷击，黑牌防御\n雷击和护盾均有冷却',
          '雷击装备能争夺满功率机会；其他构筑可用防御、控制和抢攻应对。',
          'Storm Pact gives two shared full-power Lightning strikes. Defense and Lightning have cooldowns.', 'active-monster')
    use(x,1,'Storm Titan',2,name='Verdict of Thunder',desc='Lightning [e1f1];(Max [e1f2]).;Cooldown [cooldown].',**lightning(.5),**cooldown(1))
    use(x,2,'Sergeant Toad',1,name='Stone Ward',query='2 black cards',queryparams='',
        desc='Block [e1f1].;Cooldown [cooldown].',Effect1='block',e1f1='EPD*e1p1',e1p1='.2',**cooldown(1))
    use(x,3,'Storm Titan',1,name='Storm Pact',query='*None*',queryparams='',
        desc='Ionize [e1f1].;Both sides can use these full-power lightning strikes.;Cooldown [cooldown].',
        Effect1='ionize',e1f1='2',e1f2='self',**cooldown(2),mod2='showLightningStatus')

    x=add('Lady Blackheart',6,'Black Sail','黑帆','lady_blackheart','sea',5,1,
          '对子：诅咒两件装备并返牌\n两对：眩晕后自身易伤\n两项控制都有两回合冷却',
          '返牌使同回合仍有危险；控制冷却与眩晕后的易伤是反击窗口。',
          'Curse returns its cards. Stun makes the boss Vulnerable; both control actions have cooldown 2.', 'dormant-boss')
    use(x,1,'Lady Blackheart',1,name='Black Sail Oath',
        desc='Curse [e1f1], up to [e1f2] distinct hero items.;Return all cards to your hand.;Cooldown [cooldown].',
        Effect1='curse',e1f1='MBD*e1p1',e1f2='2',e1p1='.055',e1p2='noDuplicates',Effect3='return',e3f1='all',**cooldown(2))
    use(x,2,'Lady Blackheart',2,name='Stun Cannon',desc='Stun.;Become Vulnerable 1.;Cooldown [cooldown].',
        Effect1='discard',e1f1='all',e1f2='enemy',**vulnerable(),**cooldown(2))
    use(x,3,'Red Dragon',3,name='Broadside',query='3 red cards',queryparams='',desc='Attack [e1f1].',**attack(.35))

    x=add('Storm Titan',7,'Storm Sovereign','风暴领主','the_storm_lord','mountains',4,1,
          '无耗牌蓄势：后续明牌 +1\n总和 40：雷暴并抽牌 -4\n雷暴后自身易伤',
          '观察明牌总和与冷却；准备承受爆发，在脱力窗口集中输出。',
          'Gathering Storm grows visible draw. Tempest needs rank sum 40, reduces draw by four and causes Vulnerable.', 'unfinished-definition')
    use(x,1,'Leviathan',2,name='Gathering Storm',query='*None*',queryparams='',
        desc='Draw +1 visible.;Cooldown [cooldown].',Effect1='increaseDraw',e1f1='1',e1f2='self',e1f3='visible',**cooldown(1))
    use(x,2,'Storm Titan',2,name='Tempest Break',query='at least 40',queryparams='',
        desc='Lightning [e1f1];(Max [e1f2]).;Draw -4 visible.;Become Vulnerable 1.;Cooldown [cooldown].',
        **lightning(.8),Effect2='increaseDraw',e2f1='-4',e2f2='self',e2f3='visible',**vulnerable(3),**cooldown(1))
    use(x,3,'Sergeant Toad',1,name='Wind Barrier',query='2 black cards',queryparams='',
        desc='Block [e1f1].;Cooldown [cooldown].',Effect1='block',e1f1='EPD*e1p1',e1p1='.2',**cooldown(1))

    x=add('Titan Lord',8,'Crowned Titan','泰坦领主','titan_lord','mountains',4,.95,
          '每次受击立即抽一张牌\n四连顺：重击后自身易伤\n三黑牌冻结两件装备，有冷却',
          '减少低伤连击，防止帮它凑顺子；冻结空窗和重击后的易伤可用来反击。',
          'Every hit draws one card. A four-card Straight enables a heavy attack, followed by Vulnerable.', 'dormant-region-boss')
    x.update({'Modifier 2 Name':'onGetHit','m2description':'Draw 1 card when hit','m2p1':'drawCard','m2p2':'1'})
    use(x,1,'Titan Lord',1,name='Royal Cleave',desc='Attack [e1f1].;Become Vulnerable 1.;Cooldown [cooldown].',**attack(.7),**vulnerable(),**cooldown(1))
    use(x,2,'The Frost Lord',1,name='Winter Grip',query='3 black cards',queryparams='',
        desc='Freeze [e1f1] to [e1f2] arbitrary hero items.;Cooldown [cooldown].',
        Effect1='freeze',e1f1='EPC*e1p1',e1f2='2',e1p1='.45',**cooldown(2))
    use(x,3,'Sergeant Toad',1,name='Crown Ward',query='at least 30',queryparams='',
        desc='Block [e1f1].',Effect1='block',e1f1='EPD*e1p1',e1p1='.25')

    x=add('The Underqueen',9,'Underqueen','地下女王','the_underqueen','swamp',4,.95,
          '两黑牌：Hex 一件装备\n两红牌：攻击并燃烧一件装备\n低牌冻结后自身易伤',
          '根据敌方红黑牌调整装备使用；冻结带冷却且会暴露女王。',
          'Black cards Hex one item; red cards attack and Enflame one item. Freezing makes the queen Vulnerable.', 'dormant-boss')
    use(x,1,'The Underqueen',1,name='Royal Edict',query='2 black cards',queryparams='',
        desc='Hex [e1f1], to [e1f2] arbitrary hero items.;Cooldown [cooldown].',
        Effect1='hex',e1f1='1',e1f2='1',e1f3='enemy',e1p2='noDuplicates',**cooldown(2))
    use(x,2,'The Underqueen',2,name='Crimson Decree',query='2 red cards',queryparams='',
        desc='Attack [e1f1].;Enflame [e2f1] a random hero item.',
        **attack(.25),Effect2='enflame',e2f1='EPL*e2p1',e2f2='1',e2p1='.015')
    use(x,3,'The Underqueen',3,name='Frozen Audience',query="two 7's or lower",queryparams='',
        desc='Freeze [e1f1] a random hero item.;Become Vulnerable 1.;Cooldown [cooldown].',
        Effect1='freeze',e1f1='EPC*e1p1',e1f2='1',e1p1='.55',**vulnerable(),**cooldown(1))

    x=add('Storm Titan',10,'Azure Dragon','蓝龙','blue_dragon','sea',5,1,
          '两黑牌：共享雷击机会 +1\n蓄势提高后续明牌 +2\n同花雷息后抽牌 -2、自身易伤',
          '可以争夺雷击机会，也能用防御接雷息；随后利用易伤反击。',
          'Static adds one shared Ionize and two visible draw. A three-card Flush releases breath, reduces draw and causes Vulnerable.', 'portrait-only')
    use(x,1,'Storm Titan',1,name='Gather Static',query='2 black cards',queryparams='',
        desc='Ionize [e1f1].;Draw +2 visible.;Cooldown [cooldown].',
        Effect1='ionize',e1f1='1',e1f2='self',Effect2='increaseDraw',e2f1='2',e2f2='self',e2f3='visible',**cooldown(2),mod2='showLightningStatus')
    use(x,2,'Storm Titan',2,name='Arc Breath',query='3-card Flush',queryparams='',
        desc='Lightning [e1f1];(Max [e1f2]).;Draw -2 visible.;Become Vulnerable 1.;Cooldown [cooldown].',
        **lightning(.75),Effect2='increaseDraw',e2f1='-2',e2f2='self',e2f3='visible',**vulnerable(3),**cooldown(1))
    use(x,3,'Red Dragon',3,name='Tail Sweep',query='2 red cards',queryparams='',desc='Attack [e1f1].',**attack(.22))

    x=add('Phoenix',11,'The Reassembled','弗兰肯斯坦怪物','frankensteins_monster','swamp',4,.5,
          '半份基础血量，复活一次\n对子：重组治疗，最多两次\n重组后易伤、重击后虚弱',
          '重组有次数上限，不用强求秒杀；在它易伤或虚弱时交换伤害。',
          'Revives once at half base HP. Reassembly has two uses and causes Vulnerable; heavy attacks cause Weak.', 'portrait-only')
    x.update({'Modifier 2 Name':'revive','m2p1':'1','backgroundAsset':'attack'})
    use(x,1,'Troll',2,name='Reassembly',desc='Heal [e1f1].;Become Vulnerable 1.;2 uses per combat.',
        Effect1='heal',e1f1='EPD*e1p1',e1p1='.18',**vulnerable(),mod1='numUsesPerCombat',m1p1='2')
    use(x,2,'Red Dragon',3,name='Overloaded Slam',query='3 red cards',queryparams='',
        desc='Attack [e1f1].;Become Weak 1.;Cooldown [cooldown].',
        **attack(.65),Effect2='weak',e2f1='1',e2f2='self',**cooldown(1))
    use(x,3,'Knight of Clubs',1,name='Stitched Fist',query='2 black cards',queryparams='',desc='Attack [e1f1].',**attack(.18))

    x=add('Sergeant Toad',12,'Queen of Clubs','梅花王后','queen_of_clubs','plains',5,1,
          '两张梅花：进攻后自身易伤\n一张梅花：防御\n红牌可发动普通攻击',
          '看敌方梅花数量安排攻防；王后豪赌之后易伤，普通构筑也能反击。',
          'Two Clubs enable Royal Gambit but cause Vulnerable. The same Clubs are needed for defense.', 'portrait-only')
    use(x,1,'Knight of Clubs',1,name='Royal Gambit',query='2 [suit]',queryparams='clubs',
        desc='Attack [e1f1].;Become Vulnerable 1.;Cooldown [cooldown].',**attack(.55),**vulnerable(),**cooldown(1))
    use(x,2,'Knight of Clubs',2,name='Club Guard',query='1 [suit]',queryparams='clubs',
        desc='Block [e1f1].',Effect1='block',e1f1='EPD*e1p1',e1p1='.35')
    use(x,3,'Sergeant Toad',2,name='Court Strike',query='2 red cards',queryparams='',desc='Attack [e1f1].',**attack(.2))

    x=add('Count Spade',13,'Obsidian Smith','邪恶矮人','evil_dwarf','desert',4,1,
          '黑牌：护盾与强壮\n红牌：重击后自身易伤\n对子：诅咒与毒，有冷却',
          '锻造后的强化攻击更危险；护盾冷却和重击后的易伤是输出窗口。',
          'Black cards forge Block and Strong. Red-card heavy attacks cause Vulnerable; Curse and Poison have cooldown 2.', 'portrait-only')
    use(x,1,'Sergeant Toad',1,name='Obsidian Furnace',query='2 black cards',queryparams='',
        desc='Block [e1f1].;Become Strong 1.;Cooldown [cooldown].',
        Effect1='block',e1f1='EPD*e1p1',e1p1='.4',Effect2='strong',e2f1='1',e2f2='self',**cooldown(1))
    use(x,2,'Count Spade',2,name='Slag Hammer',query='2 red cards',queryparams='',
        desc='Attack [e1f1].;Become Vulnerable 1.;Cooldown [cooldown].',**attack(.42),**vulnerable(),**cooldown(1))
    use(x,3,'Crazed Witch',2,name='Debt Rune',query='Pair',queryparams='',
        desc='Curse [e1f1] a random hero item.;Poison [e2f1].;Cooldown [cooldown].',
        Effect1='curse',e1f1='MBD*e1p1',e1f2='1',e1p1='.1',Effect2='poison',e2f1='MBD*e2p1',e2p1='.035',**cooldown(2))
    return bosses
