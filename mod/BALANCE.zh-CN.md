# Boss Courts 1.4.0：带伤入场的平衡调整

以 26 个原版职业逐一计算血量，覆盖 50%、65%、80%、100% 血量入场，以及慢速、普通、高输出三档构筑。
血量来自 HEROES.csv，世界升级每区 +20；忽略额外血量升级。伤害档位是原版关底 EPD 的 30% / 45% / 60%，是校准假设，**不是实测的职业平均伤害**。相同职业可以因装备、能力和升级落在不同档位。

| 世界 | 慢速 / 普通 / 高输出，每轮 |
|---|---|
| 1 | 23.6 / 35.4 / 47.2 |
| 2 | 36.9 / 55.4 / 73.8 |
| 3 | 52.9 / 79.3 / 105.8 |

## 血量敏感性

| 职业 | 初始最大血量 | W1 / W2 / W3 以 65% 血量进房 |
|---|---:|---|
| Knight | 110 | 72 / 85 / 98 |
| Druid | 90 | 59 / 72 / 85 |
| Wizard | 80 | 52 / 65 / 78 |
| Rogue | 100 | 65 / 78 / 91 |
| Toad | 100 | 65 / 78 / 91 |
| Titan | 250 | 163 / 176 / 189 |
| Vampire | 80 | 52 / 65 / 78 |
| Prince | 130 | 85 / 98 / 111 |
| Monk | 100 | 65 / 78 / 91 |
| Huntress | 100 | 65 / 78 / 91 |
| Warlock | 80 | 52 / 65 / 78 |
| Sorceress | 60 | 39 / 52 / 65 |
| Bard | 110 | 72 / 85 / 98 |
| Banker | 70 | 46 / 59 / 72 |
| Queen | 80 | 52 / 65 / 78 |
| Witch | 100 | 65 / 78 / 91 |
| Ninja | 70 | 46 / 59 / 72 |
| Tortoise | 160 | 104 / 117 / 130 |
| Blacksmith | 100 | 65 / 78 / 91 |
| Assassin | 100 | 65 / 78 / 91 |
| Priest | 100 | 65 / 78 / 91 |
| Alchemist | 140 | 91 / 104 / 117 |
| Paladin | 120 | 78 / 91 / 104 |
| Mummy | 100 | 65 / 78 / 91 |
| Rainbow Knight | 100 | 65 / 78 / 91 |
| Locksmith | 110 | 72 / 85 / 98 |

## 13 位 Boss 与原版参照

| Boss | 总血量旧 → 新 | 最大单次攻击新 | 同世界原版参照：血量 / 单次攻击 |
|---|---:|---:|---|
| Ashwing | 262 → 250 | 18 | Sergeant Toad 287 / 38；Phoenix 314 / 30 |
| Old Thorn | 360 → 336 | 16 | Hexagon 480 / 27 |
| Three Kings | 456 → 408 | 23 | Great Sandwyrm 480 / 73；Hydra 480 / 27 |
| River Serpent | 668 → 633 | 37 | Kraken 562 / 0 |
| Thunder Giant | 668 → 598 | 28 | Count Spade 844 / 44 |
| Black Sail | 668 → 598 | 33 | Kraken 562 / 0 |
| Storm Sovereign | 668 → 633 | 39 | Count Spade 844 / 44 |
| Crowned Titan | 633 → 598 | 39 | Count Spade 844 / 44 |
| Underqueen | 432 → 408 | 18 | Hexagon 480 / 27 |
| Azure Dragon | 668 → 598 | 28 | Kraken 562 / 0 |
| The Reassembled | 432 → 408 | 29 | Hexagon 480 / 27 |
| Queen of Clubs | 235 → 235 | 24 | Sergeant Toad 287 / 38 |
| Obsidian Smith | 456 → 432 | 33 | Great Sandwyrm 480 / 73 |

单次攻击表不含毒后续跳数、灼烧、多个技能叠加或易伤；Kraken 没有普通攻击，靠毒和受击抽牌/恢复施压，不能据其 0 点攻击判断强弱。原版 Count Spade 的恢复和诅咒、Hexagon 的全装备灼烧也必须一起考虑。

## 原生机制参照

| 新 Boss | 原版对应实现 | 调整的原因 |
|---|---|---|
| Ashwing | Phoenix：受击烧全装备；Red Dragon：无牌全装备火 | 改成每三轮单件 5 火，不让多段攻击叠加整套灼烧 |
| Old Thorn | Tanglewood：Charm / 治疗 / 可重复小攻击；原生 CounterAttack 状态：50% | 普通怪物表未直接采用反击；故用原生 attack 实现有系数和上限的定时反攻，保留治疗但限次数 |
| Three Kings | Hydra：K 毒、Q 全体火、J 雷，各头可同时行动 | 恢复三头可用，增加攻击补足关底压力；降低单头雷和毒，火限制单件并加冷却 |
| River Serpent | Leviathan：对子成长，四同点 2.5×MBD 大攻击；Kraken：受击抽牌/回血/毒 | 舍弃高倍不可控爆发，采用有预告的 0.42×MBD 吞噬、恢复窗口和较小护盾 |
| Thunder Giant | Storm Titan：A Ionize 2、三红雷 0.45×MBD；Yellow Dragon：先 Ionize 再雷 | 不改先充雷顺序；改为 1 次共享机会、雷 0.32×MBD 并冷却，避免两技能叠加逼迫带伤职业 |
| Black Sail | Lady Blackheart：对子多件 Hex、两对 Stun | Hex 限单件和冷却，移除整手 Stun；33 点炮击后 Weak 与小攻击分摊压力 |
| Storm Sovereign | Storm Titan：牌型雷击 | 原版不存在该固定五轮蓄力循环；循环为新设计，爆发调到 0.45×MBD，成长上限调到 0.23×MBD |
| Crowned Titan | Titan Lord：受击抽牌、四顺攻击 1×MBD | 保留受击抽牌；四顺降到 0.45×MBD、冷却并给自己易伤，低血关闭护盾 |
| Underqueen | The Underqueen / Hexagon：装备控制 | Hex 与 Freeze 错开，单件/冷却限制，减冻结强度而小幅提高普通牌型攻击 |
| Azure Dragon | White Dragon：Freeze；Yellow Dragon：Ionize/雷；Red Dragon：火 | 三阶段仍为新增机制；3 点单件冻结、最大 28 雷、单件 7 火，并保留休息轮 |
| The Reassembled | Franken's Monster：复活一次、无牌 Stun 冷却、单牌小攻击 | 原版已有实际定义；新设计移除复活/Stun，以半血前后攻势和可预见重击替代，减少重击增加小毒压力 |
| Queen of Clubs | Knight of Clubs / Sergeant Toad：花色攻防 | 减牌量降低两梅花概率，并降低爆发；攻击与护盾仍竞争同一花色、回血只有两次 |
| Obsidian Smith | Maddened Dwarf：奇偶牌攻防/永久强化 | 固定锻造循环为新设计；大锤减到 0.45×MBD，提高平时小攻击、减少护盾，避免过久消耗 |

Tanglewood、Titan Lord、Lady Blackheart 含原生定义但不代表当前普通流程启用；Franken's Monster 的常规 Spawn Weight 为 0。完整原生数值与启用/刷新标记均保留在 balance-model.json 中。对照这些定义说明实现与量级，不能声称它们经过与当前关底一样的玩家实测。

## 老荆棘：10% 系数的含义

原生即时 CounterAttack 硬编码为 50%，CSV 无法直接改系数。新版替换为原生 attack 技能：偶数轮敌方行动时反攻一次，伤害 = round(min(MBD×0.11，自身已损失血量×0.10))。普通第二世界上限 8 点；跟随原版 MBD 难度倍率缩放。奇数轮不反攻，多段、毒、火伤不会逐次反击。原版玩家 CounterAttack 不改。

自身损失 40 点血时反攻 4 点，损失 80 点时约 8 点，此后封顶。8 点可以被 Block 完全抵挡，Tough 可降到 4 点；玩家有 Vulnerable 时会升到 12 点，所以这是基础上限，**不是任何状态下都最多掉 8 血**。

336 血的老荆棘，在忽略回血/护盾并以慢速 36.9、普通 55.35、高输出 73.8 伤害推进时，模型分别暴露于约 31 / 24 / 16 点反攻；对第二世界 65% 血量入场的 Sorceress（52 血），约占 60% / 46% / 31%，且尚未扣除玩家防御。对照旧版：360 基础血量×50%伤害落在反击轮×50%返还，粗略反伤预算 90 点，已经超过该职业进房血量。

## 具体改动

- Ashwing：两条各 125 血，三轮烧一件装备 5 点；基础攻击 16、低血扑击 18。火仍是一次性惩罚，可等衰减；使用 flare / firestorm 原版技能图。
- Three Kings：不再按血量禁用另外两个头，K/Q/J 共用手牌且各冷却一轮；13 点攻击+4 毒、15 点攻击+4 火、最大 23 雷。偶尔可多头一起行动，不能仅看单头伤害。
- River Serpent / Storm Sovereign / Crowned Titan：重击从 52 / 59 / 59 降为 37 / 39 / 39；保留预告、停攻或易伤窗口。泰坦仍受击抽牌，多段构筑需控制喂牌。
- Thunder Giant：雷击最大 40 → 28、护盾 28 → 18，血量 668 → 598；保留 Ionize 1 共享机会和冷却。
- Black Sail：炮击 48 → 33、普通攻击 16 → 14；Hex 仍只影响一件装备并有冷却，炮击后自身 Weak。
- Underqueen / Azure Dragon：冻结强度 5 → 3；控制仍错开、保留冷却。Azure 雷击上限 39 → 28，火改为 7 点一次灼烧。
- The Reassembled：毒 2 → 3、前半攻击 15 → 16；狂怒攻击 26 → 20、重击 42 → 29；保持无复活及停攻窗口。
- Queen of Clubs：5 → 4 张牌，爆发 28 → 24，护盾 14 → 9，回血 9 → 8；同一梅花预算防止攻防免费叠加。
- Obsidian Smith：砸锤 51 → 33、锻造护盾 17 → 12、普通攻击 12 → 16；降低致命爆发，补充平时压力。

## 验证边界

数值使用匹配版本的原版公式计算器；技能门槛使用原版 HScript 解释器。344 项反攻测试核对了施法者缺血、整数取整、封顶、Block、Tough 和 Vulnerable；加载器使用隔离存档目录。
balance-model.json 保存全部 1,352 个职业/入场案例及三档伤害敏感性；其中 exposure index 是粗略压力指标，独立牌型概率会忽略技能抢牌、真实 AI 和状态联动，**不能解读为真实战斗掉血或胜率**。
新版在隔离目录完成原生启动：实际加载全部 13 位 Boss，原生地图抽选得到 Ashwing / Underqueen / Storm Sovereign / The Wild Joker，地图 241 个节点。测试副本仅重定向存储/启动并记录原生函数，未更改用户实际程序与存档。
尚未进行 13 场完整实机战斗或全职业统计。原生加载与地图抽选成功不能证明战斗平衡已通过。
