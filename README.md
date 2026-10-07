# Boss Courts 1.4.0

## 工坊旧版升级

原版 Mod Manager 可能保留旧版本地副本，即使 Steam 已下载新版；仅取消订阅再订阅或重新勾选也可能仍加载旧数据。首次安装没有旧副本时，无需以下清理步骤。

1. 关闭游戏，打开 Mod Manager，找到 Boss Courts，点击 **Details → Delete Mod** 并确认。这只删除本地模组副本，不删除存档；保持工坊订阅。
2. 关闭并重新打开 Mod Manager，让它从 Steam 已下载的最新版重新导入 Boss Courts。
3. 重新勾选 Boss Courts；同时使用 Travel Run 时，保留 Travel Run 勾选。只启用一份 Boss Courts。
4. 点击 **Run Game** 重新应用并启动游戏，开始新一局。

1.4.0 可用 Ashwing 检查：第一关周期灼烧为 5 点，左右技能图为 Flare / Firestorm；中间火焰图不变。管理器的 Game Version 列是游戏兼容版本，不是模组版本。


为原版平原、沼泽、沙漠、雪山、海洋扩充 13 位区域 Boss。保留原版守关者和最终 Joker，新增 Boss 不进入普通遭遇或墓穴。

## 安装

订阅工坊项目，在游戏附带的 Mod Manager 中启用并应用，重启游戏并开始新局。关闭 Random Bosses 规则以体验区域关底。
使用原版游戏启动方式，无需额外启动器或修改游戏程序。已有手动 BossCourts 时，只启用一份，避免重复安装。
从旧版升级请开始新局：区域抽选配置改变后，同一旧存档的 Boss 和地形可能重新计算。

已有手动安装可关闭游戏后运行 UpdateBossCourts.cmd，脚本备份旧数据并重新应用，需要 Python 3.11；该工具只适用于仅启用 BossCourts 的现有安装。工坊用户使用 Mod Manager 即可。

## 资源和实现

MOD 本体只有 CSV 数据、元数据和说明。画像、技能美术、战斗背景、地图贴图和音乐都引用本地原版资源，不附带图片、脚本、DLL 或 EXE。
内部新增 14 条区域配置记录，名称和原版完全相同，每条仅改变 ID 和关底 Boss。世界数量、地形类型、显示名称、普通怪物池、城镇、音乐和地图生成规则保持原版。
World 2 的沼泽/沙漠、World 3 的雪山/海洋仍各占 50%。沙漠另保留一份原版 Great Sandwyrm 抽选项，因此沙漠内原版 Boss 占 50%，Three Kings 和 Obsidian Smith 各占 25%；其他区域候选等概率。
保留原版名称也保留了原版地图资源路径，修复旧版改名后地图只剩星空的问题。区域记录数量增加不代表新增世界或地形。

## Boss 列表

| 区域 | 新增 Boss |
|---|---|
| World 1 平原 | Ashwing、Queen of Clubs |
| World 2 沼泽 | Old Thorn、Underqueen、The Reassembled |
| World 2 沙漠 | Three Kings、Obsidian Smith |
| World 3 雪山 | Thunder Giant、Storm Sovereign、Crowned Titan |
| World 3 海洋 | River Serpent、Black Sail、Azure Dragon |

## 测试与反馈

1.4.0 已按 26 个职业的血量、带伤入场和三档输出模型重新校准全部 13 位 Boss，详见 BALANCE.zh-CN.md。老荆棘采用偶数轮一次的反攻：自身已损失血量的 10%，受 MBD×11% 上限约束（普通 W2 基础上限 8），可用原版护盾抵挡；不是每次受击即时反弹。

当前版本已验证原版加载器、原生游戏数据加载和地图 Boss 生成；13 场完整战斗及全角色/难度胜率仍需实测。升级平衡版本后请开始新局。
遇到问题请在工坊评论反馈 Boss 名称、角色、难度、装备和截图。

## 美术

复用原版完整画像，包含原版已使用和闲置的资源，不是 13 张全新或全部废弃的画像。素材归 Playsaurus 所有。
工坊封面为九位 Boss 拼图，画廊只显示画像和英文名称，使用此前确认的宣传图片。

## 下载与源码

[Steam 工坊](https://steamcommunity.com/sharedfiles/filedetails/?id=3813933277) · [GitHub 1.4.0 下载](https://github.com/Celestial-Plato/poker-quest-boss-courts/releases/tag/v1.4.0)

`mod/` 为游戏管理器直接加载的模组内容。`tools/` 为数据生成器源码，读取玩家已安装的 Poker Quest v63/build 2021 的 CSV。Python 3.11 或更高版本，在仓库目录的 PowerShell 中运行：

```powershell
$env:POKER_QUEST_DIR = 'E:\SteamLibrary\steamapps\common\Poker Quest'
python tools/build_mod.py
```

生成目录为 `outputs/BossCourts-v1.4.0/content/BossCourts`。完整发布 ZIP 另含手动升级工具与宣传图片；工坊本体只有 CSV、元数据和说明。测试说明见 `docs/TESTING.zh-CN.md`，模型边界与完整对照见 `docs/BALANCE.zh-CN.md`。

画像及美术归 Playsaurus 所有；源码包不包含原版游戏程序、美术或官方反编译 JavaScript。运行数据生成器需要自己的游戏安装。
