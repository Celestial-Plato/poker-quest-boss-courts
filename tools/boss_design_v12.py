"""Native skill requirements and deliberate recovery windows; no binary patch."""
from boss_design import create_bosses as previous_design
VERSION='1.3.0'

def create_bosses(monsters,base,skill,set_skill,clear_passives):
    bosses=previous_design(monsters,base,skill,set_skill,clear_passives)
    def reset(i,hp,mechanics,counter,tip):
        b=bosses[i-1]; x=b['data']; clear_passives(x)
        for j in range(1,4): set_skill(x,j,{})
        x.update({'Modifier 1 Name':'modifyHp','m1p1':str(hp),'specialTooltip':tip})
        b.update(hpMultiplier=hp,mechanics=mechanics,counter=counter,tip=tip)
        return x
    def use(x,n,source,s,name,q,desc,eff,req=None,cd=None,uses=None,params=''):
        fields={k:v for k,v in skill(source,s).items() if k in ('Asset','BgAsset','EffectClass')}
        fields.update(name=name,query=q,queryparams=params,desc=desc)
        for i,e in enumerate(eff,1):
            fields[f'Effect{i}']=e[0]
            for j,f in enumerate(e[1:],1): fields[f'e{i}f{j}']=str(f)
        mods=[]
        if req: mods.append(('require',req))
        if cd: mods.append(('cooldown',cd))
        if uses: mods.append(('numUsesPerCombat',uses))
        assert len(mods)<=2
        for j,(mod,p) in enumerate(mods,1): fields[f'mod{j}']=mod;fields[f'm{j}p1']=str(p)
        set_skill(x,n,fields)
    def A(v): return ('attack',f'MBD*{v}')
    def B(v): return ('block',f'EPD*{v}')
    def F(v): return ('enflame',f'EPL*{v}','1')
    def L(v): return ('lightning',f'(MBD*{v})*lightningMultiplier',f'MBD*{v}')
    V=('vulnerable','1','self'); W=('weak','2','self')
    x=reset(1,.5,'半份基础血量，复活一次\n每三轮燃烧一件装备\n低血扑击后自身易伤',
       '留资源应对第二条生命；避免急用燃烧装备，利用扑击后的易伤反攻。',
       'Two half-base-HP lives. No on-hit fire. Cinders every third round; low-life Dive exposes the boss.')
    x.update({'Modifier 2 Name':'revive','m2p1':'1'})
    use(x,1,'Red Dragon',3,'Cinder Talons','3 red cards','Attack [e1f1].',[A(.24)])
    use(x,2,'The Underqueen',2,'Falling Cinders','*None*','Rounds 3/6/9...;Enflame [e1f1] one hero item.',[F(.012)],'currentRound % 3 == 0')
    use(x,3,'Red Dragon',3,'Last Ember Dive','2 black cards','At 40% life or less.;Attack [e1f1].;Become Vulnerable 1.;Cooldown [cooldown].',[A(.34),V],'enemyCurrentLife <= enemyMaxLife * 0.4',1)
    x['eq1Asset']='flare'
    x['eq3Asset']='firestorm'
    x=reset(2,.75,'偶数轮：原生 50% 反击\n奇数轮：撤反击、毒与攻击\n低血治疗，仅两次',
       '偶数轮备好防御与资源；奇数轮集中输出。反击也可能响应非普通攻击伤害。',
       'EVEN rounds: native 50% CounterAttack. ODD rounds: no CounterAttack. Low-life healing has two uses.')
    x.update({'Modifier 2 Name':'applyWorldModifierForCombat','m2p1':'BC Thorn Stance'})
    use(x,1,'Hydra',1,'Bitter Sap','*None*','ODD rounds only.;Poison [e1f1].',[('poison','MBD*0.018')],'currentRound % 2 == 1')
    use(x,2,'Count Spade',2,'Open Crown','2 black cards','ODD rounds only.;Attack [e1f1].',[A(.18)],'currentRound % 2 == 1')
    use(x,3,'Tanglewood',2,'Last Roots','at least 30','At 30% life or less.;Heal [e1f1].;2 uses per combat.',[('heal','EPD*0.12')],'enemyCurrentLife <= enemyMaxLife * 0.3',uses=2)
    x=reset(3,.95,'血量三段：K 毒、Q 火、J 雷\n每段只有对应王牌可行动\nJ 雷击后自身易伤',
       '观察血线和对应 K/Q/J；临近下一段时留防御，也可换走敌方关键王牌。',
       'K above 2/3 life; Q between 1/3 and 2/3; J at 1/3 or less. Only the current head acts.')
    use(x,1,'Hydra',1,'King of Venom','1 card: A','Above 2/3 life.;Attack [e1f1].;Poison [e2f1].',[A(.24),('poison','MBD*0.045')],'enemyCurrentLife > enemyMaxLife * (2 / 3)',params='K')
    use(x,2,'Hydra',2,'Queen of Cinders','1 card: A','Between 1/3 and 2/3 life.;Attack [e1f1].;Enflame [e2f1] one hero item.',[A(.27),F(.02)],'enemyCurrentLife <= enemyMaxLife * (2 / 3) && enemyCurrentLife > enemyMaxLife / 3',params='Q')
    use(x,3,'Hydra',3,'Jack of Storms','1 card: A','At 1/3 life or less.;Lightning [e1f1] (max [e1f2]).;Become Vulnerable 1.',[L(.44),V],'enemyCurrentLife <= enemyMaxLife / 3',params='J')
    x=reset(4,.95,'每两轮获得少量护盾\n第五轮吞噬，第六轮停攻\n吞噬后自身易伤',
       '护盾量随进度缩放；第五轮先防御，下一轮利用停攻和易伤输出。',
       'Tide Block every other round. Devour on rounds 5/10/15; no Undertow on the following round.')
    use(x,1,'Sergeant Toad',1,'Tidal Scales','*None*','Block [e1f1].;Cooldown [cooldown].',[B(.10)],cd=1)
    use(x,2,'Leviathan',1,'Devour','*None*','Rounds 5/10/15...;Attack [e1f1].;Become Vulnerable 1.',[A(.60),V],'currentRound % 5 == 0')
    use(x,3,'Knight of Clubs',1,'Undertow','2 black cards','Not on Devour or the following round.;Attack [e1f1].',[A(.18)],'currentRound % 5 != 0 && currentRound % 5 != 1')
    x=reset(5,.95,'每两轮补充 Ionize 1\n三红牌雷击，黑牌防御\n双方争夺满功率雷击',
       '有雷击装备可抢先消耗共享机会；也可换走红牌，让它花牌防御。',
       'Storm Pact supplies ONE shared full-power lightning strike every other round; no mutual damage.')
    use(x,1,'Storm Titan',1,'Storm Pact','*None*','Ionize [e1f1].;Shared full-power lightning.;Cooldown [cooldown].',[('ionize','1','self')],cd=1)
    use(x,2,'Storm Titan',2,'Thunder Verdict','3 red cards','Lightning [e1f1] (max [e1f2]).;Cooldown [cooldown].',[L(.46)],cd=1)
    use(x,3,'Sergeant Toad',1,'Stone Ward','2 black cards','Block [e1f1].;Cooldown [cooldown].',[B(.16)],cd=1)
    x=reset(6,.95,'对子 Hex 一件装备并返牌\n不再弃掉玩家全部手牌\n炮击后自身虚弱两轮',
       '对子会返还给黑帆继续行动；趁 Hex 冷却或炮击后的虚弱窗口交换伤害。',
       'Pairs Hex ONE item and return the boss cards. No Stun. Broadside makes the boss Weak 2.')
    use(x,1,'Lady Blackheart',1,'Black Sail Oath','Pair','Hex 1 to one hero item.;Return all used cards.;Cooldown [cooldown].',[('hex','1','1','enemy'),('return','all')],cd=2)
    use(x,2,'Red Dragon',3,'Broadside','3 red cards','Attack [e1f1].;Become Weak 2.;Cooldown [cooldown].',[A(.55),W],cd=2)
    use(x,3,'Knight of Clubs',1,'Boarding Party','2 black cards','Attack [e1f1].',[A(.18)])
    x=reset(7,.95,'第二、三轮：攻击逐次增强\n第四轮蓄势，第五轮重击\n第六轮停攻；强化有上限',
       '第 4/9/14 轮备防御；重击后的下一轮集中输出，不宜无限拖延。',
       'Five-round cycle: rest / ramp / ramp / telegraph / burst. Ramp is capped; first round is safe.')
    use(x,1,'Knight of Clubs',1,'Rising Gale','2 black cards','Cycle rounds 2/3.;Attack [e1f1].;Growth capped after six uses.',[('attack','MBD*(0.14+(min(numTimesUsed,6)*0.025))')],'currentRound % 5 == 2 || currentRound % 5 == 3')
    use(x,2,'Sergeant Toad',1,'Gathering Tempest','*None*','Rounds 4/9/14...;NEXT round: Tempest Break.;Block [e1f1].',[B(.08)],'currentRound % 5 == 4')
    use(x,3,'Storm Titan',2,'Tempest Break','*None*','Rounds 5/10/15...;Attack [e1f1].;Become Vulnerable 1.;Following round: no attack.',[A(.68),V],'currentRound % 5 == 0')
    x=reset(8,.9,'每次受击立即抽一张牌\n四连顺重击后自身易伤\n低血后护盾关闭',
       '减少低伤连击，别帮它凑出四连顺；低血时失去护盾，可集中结束战斗。',
       'Every hit draws one card. Four-card Straight causes a heavy attack and Vulnerable; Ward stops below 40% life.')
    x['Visible Cards']='3';x.update({'Modifier 2 Name':'onGetHit','m2description':'Draw 1 card when hit','m2p1':'drawCard','m2p2':'1'})
    use(x,1,'Titan Lord',1,'Royal Cleave','4-card Straight','Attack [e1f1].;Become Vulnerable 1.;Cooldown [cooldown].',[A(.68),V],cd=1)
    use(x,2,'Sergeant Toad',1,'Crown Ward','3 black cards','Above 40% life only.;Block [e1f1].;Cooldown [cooldown].',[B(.18)],'enemyCurrentLife > enemyMaxLife * 0.4',1)
    use(x,3,'Knight of Clubs',1,'Titan Fist','2 red cards','Attack [e1f1].',[A(.20)])
    x=reset(9,.9,'1/5/9 轮：Hex 一件\n3/7/11 轮：冻结一件\n偶数轮只有牌型攻击',
       '控制严格错开；留小牌解冻、准备备用装备，在偶数轮集中使用关键装备。',
       'Hex on rounds 1/5/9; Freeze on 3/7/11. They never coincide; even rounds have only card-based attack.')
    use(x,1,'The Underqueen',1,'Shadow Edict','*None*','Rounds 1/5/9...;Hex 1 to one hero item.;Attack [e2f1].',[('hex','1','1','enemy'),A(.10)],'currentRound % 4 == 1',1)
    use(x,2,'The Underqueen',3,'Frozen Audience','*None*','Rounds 3/7/11...;Freeze [e1f1] one hero item.;Attack [e2f1].',[('freeze','EPC*0.4','1'),A(.10)],'currentRound % 4 == 3',1)
    use(x,3,'Red Dragon',3,'Royal Strike','2 red cards','EVEN rounds only.;Attack [e1f1].',[A(.22)],'currentRound % 2 == 0')
    x=reset(10,.95,'冰 1–3、雷 5–7、火 9–11\n每段之间一轮停攻\n循环重复，三个阶段可控',
       '冰段留解冻牌，雷段抢 Ionize，火段调整装备使用；4/8/12 轮是输出窗口。',
       '12-round cycle: Ice 1-3 / rest 4 / Storm 5-7 / rest 8 / Fire 9-11 / rest 12. Repeat.')
    use(x,1,'The Underqueen',3,'Frost Breath','2 black cards','Cycle rounds 1-3.;Freeze [e1f1] one hero item.;Attack [e2f1].;Cooldown [cooldown].',[('freeze','EPC*0.4','1'),A(.20)],'(currentRound - 1) % 12 < 3',1)
    use(x,2,'Storm Titan',2,'Thundering Wings','3 red cards','Cycle rounds 5-7.;Lightning [e1f1] (max [e1f2]).;Then Ionize 1, shared.;Cooldown [cooldown].',[L(.45),('ionize','1','self')],'(currentRound - 1) % 12 >= 4 && (currentRound - 1) % 12 < 7',1)
    use(x,3,'Hydra',2,'Ember Breath','2 red cards','Cycle rounds 9-11.;Attack [e1f1].;Enflame [e2f1] one hero item.;Cooldown [cooldown].',[A(.30),F(.018)],'(currentRound - 1) % 12 >= 8 && (currentRound - 1) % 12 < 11',1)
    x=reset(11,.9,'半血前：缝合与小额毒伤\n半血后：高伤拳击与重击\n重击下一轮停攻，无复活',
       '半血前准备爆发；跨血线后注意四轮重击周期，在停攻轮反击。',
       'Above 50%: stitched attacks. At 50% or less: rage; Slam every fourth round, followed by no attacks. No revival.')
    use(x,1,'Hydra',1,'Stitched Fist','2 black cards','Above 50% life.;Attack [e1f1].;Poison [e2f1].',[A(.20),('poison','MBD*0.025')],'enemyCurrentLife > enemyMaxLife * 0.5')
    use(x,2,'Red Dragon',3,'Ragged Fury','2 red cards','At 50% life or less.;Only cycle rounds 2/3.;Attack [e1f1].',[A(.36)],'enemyCurrentLife <= enemyMaxLife * 0.5 && (currentRound % 4 == 2 || currentRound % 4 == 3)')
    use(x,3,'Red Dragon',3,'Overloaded Slam','*None*','At 50% life or less, rounds 4/8/12...;Attack [e1f1].;Become Vulnerable 1.;Following round: no attack.',[A(.57),V],'enemyCurrentLife <= enemyMaxLife * 0.5 && currentRound % 4 == 0')
    x=reset(12,.9,'两梅花豪赌后自身易伤\n同一批梅花也用于防御\n红心治疗，仅两次',
       '观察王后自己的梅花和红心；两梅花爆发后利用易伤，治疗有明确上限。',
       'Uses HER OWN Clubs: two for Gambit, one for Guard. Hearts heal twice only; player draws never trigger punishment.')
    use(x,1,'Knight of Clubs',1,'Royal Gambit','2 [suit]','Attack [e1f1].;Become Vulnerable 1.;Cooldown [cooldown].',[A(.47),V],cd=1,params='clubs')
    use(x,2,'Knight of Clubs',2,'Club Guard','1 [suit]','Block [e1f1].',[B(.18)],params='clubs')
    use(x,3,'Tanglewood',2,'Heart Tribute','2 [suit]','Heal [e1f1].;Cooldown [cooldown].;2 uses per combat.',[('heal','EPD*0.12')],cd=2,uses=2,params='hearts')
    x=reset(13,.95,'3/4 轮：锻造护盾与攻击\n第 5 轮预告，第 6 轮砸锤\n1/2 轮停炉，循环重复',
       '第 5/11/17 轮准备防御；重击后有两轮停炉，集中输出，避免护盾累积。',
       'Six-round forge cycle: rest 1-2 / forge 3-4 / telegraph 5 / hammer 6. Hammer exposes the smith.')
    use(x,1,'Sergeant Toad',1,'Forge Iron','2 black cards','Cycle rounds 3/4.;Block [e1f1].;Attack [e2f1].',[B(.14),A(.16)],'currentRound % 6 == 3 || currentRound % 6 == 4')
    use(x,2,'Sergeant Toad',1,'Hammer Raised','*None*','Rounds 5/11/17...;NEXT round: Slag Hammer.;Block [e1f1].',[B(.05)],'currentRound % 6 == 5')
    use(x,3,'Count Spade',2,'Slag Hammer','*None*','Rounds 6/12/18...;Attack [e1f1].;Become Vulnerable 1.;Next TWO rounds: no attacks.',[A(.70),V],'currentRound % 6 == 0')
    return bosses
