# 微信沉淀 · WeChat Deposit

> 把微信聊天里的文字、截图、转发文件、公众号文章整理成结构化知识卡片，脱敏后存入 ima 知识库

![License](https://img.shields.io/badge/license-MIT-5a6b4f)
![Type](https://img.shields.io/badge/type-Agent%20Skill-4a6b7c)
![Platform](https://img.shields.io/badge/platform-WorkBuddy%20%7C%20Claude%20Code-b8935a)

## 它解决什么问题

微信是大多数人真正在产生信息的地方，但它是**只进不出**的：好内容沉在聊天记录里，三个月后彻底找不回来。

这个 skill 把「发给我一段聊天」变成「知识库里多了一张卡片」，并且保证你在 3 秒内能确认「存好了、存的是什么」。

## 两种模式

| 模式 | 触发语 | 行为 |
|---|---|---|
| 单条 | 「沉淀一下」「存着」「整理入库」 | 处理当前这一条内容，出一张卡片 |
| 批量 | 「批量沉淀」「今日清算」 | 处理今天所有待沉淀内容，卡片编号成组 |

## 卡片模板

```markdown
# <主题标题，15 字以内>

## 核心要点
（2-4 句，说清这件事到底是什么）

## 金句原文
（保留原话，标出处，不改写）

## 我可以怎么用
（一条具体的行动或场景，不写「值得学习」这种废话）
```

## 脱敏规则

- 人名 → 角色（「同事 A」「客户 B」）
- 手机号、身份证、地址、公司名 → 一律抹掉
- 涉及金额保留量级（「几千」），不留精确数字
- 截图里的头像、昵称、群名一律不转录

## 工作流程

1. 判断内容类型（观点 / 方法 / 数据 / 故事）→ 决定卡片重心
2. 抽取可脱离上下文独立成立的知识点（**不能独立的不要**）
3. 脱敏
4. 写入 ima 知识库「微信沉淀库」
5. 回一句确认：卡片标题 + 存到哪个库 + 一句话摘要

## 配套技能

- [`wechat-weekly-digest`](https://github.com/px-pangu/wechat-weekly-digest) — 每周把这些卡片盘成一份周刊
- [`ima-knowledge-loop`](https://github.com/px-pangu/ima-knowledge-loop) — 把正式产出反向回传到 ima

## 目录结构

```
wechat-deposit/
├─ SKILL.md          角色 · 模式判断 · 标准流程 · 卡片模板 · 硬性规则
├─ assets/           模板与示例
├─ references/       ima 知识库写入说明
└─ scripts/          辅助脚本
```

## 许可

MIT © 2026 px-pangu


## 安装

把本仓库整个目录放进 Agent 的 skills 目录即可，目录名保持仓库名：

```bash
# WorkBuddy
git clone https://github.com/px-pangu/wechat-deposit.git ~/.workbuddy/skills/wechat-deposit

# Claude Code
git clone https://github.com/px-pangu/wechat-deposit.git ~/.claude/skills/wechat-deposit
```

装好后在对话里说一句相关的话就会自动触发，也可以用 `@wechat-deposit` 显式点名。

