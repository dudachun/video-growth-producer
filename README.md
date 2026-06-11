<p align="center">
  <img src="assets/readme/hero.svg" alt="Video Growth Producer" width="100%" />
</p>

<p align="center">
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/badge/License-MIT-16a34a?style=for-the-badge"></a>
  <img alt="Codex Skill" src="https://img.shields.io/badge/Codex-Skill-111827?style=for-the-badge">
  <img alt="Remotion" src="https://img.shields.io/badge/Video-Remotion-2563eb?style=for-the-badge">
  <img alt="imagegen" src="https://img.shields.io/badge/Visual-imagegen-f59e0b?style=for-the-badge">
  <img alt="HyperFrames" src="https://img.shields.io/badge/Motion-HyperFrames-06b6d4?style=for-the-badge">
  <img alt="Chinese README" src="https://img.shields.io/badge/Docs-%E4%B8%AD%E6%96%87-ef4444?style=for-the-badge">
</p>

<p align="center">
  <strong>把选题、文案、封面、字幕、AI 旁白、Remotion 成片和数据复盘，变成一套可训练的短视频生产流程。</strong>
</p>

# Video Growth Producer

`video-growth-producer` 是一个可训练的 Codex Skill，用来帮助创作者批量生产短视频内容。

它可以把一个选题、一段文案，或者一个账号方向，推进成一套完整的短视频生产流程：

- 选题与爆款开头
- 口播文案
- 分镜与画面策划
- 封面方案
- 字幕与重点词高亮
- Remotion 竖屏视频工程
- 可选的 imagegen 画面素材
- 可选的 HyperFrames 动态页面增强
- 本地声音克隆流程建议
- 发布后数据复盘与内容记忆

适用平台包括：抖音、TikTok、视频号、Reels、YouTube Shorts、小红书竖屏视频等。

## 30 秒理解

| 你给它 | 它帮你输出 |
| --- | --- |
| 一个账号方向 | 可持续训练的创作者资料与内容记忆 |
| 一个选题 | 爆款开头、口播文案、分镜和封面方案 |
| 一段文案 | 字幕时间轴、画面策划、Remotion 视频生成流程 |
| 发布后的数据截图 | 原因分析、下期优化建议、长期经验记录 |

## 这个 Skill 适合谁

这个 Skill 不是只服务某一个固定赛道。

你可以把它训练成自己的短视频制作助手，例如：

- AI 工具账号
- 知识付费账号
- 企业服务账号
- 本地生活账号
- 健身账号
- 职场技能账号
- 教育培训账号
- 产品推广账号
- 个人 IP 账号

核心思路是：公共 Skill 只提供工作流、脚本、模板和方法；每个用户在自己的本地工作区里训练自己的账号方向。

## 核心能力

### 1. 训练你的内容方向

你可以随时告诉 Codex：

```text
以后我的账号方向是给中小企业老板讲 AI 落地，最终目的是让他们找我咨询或合作。
```

也可以继续修正：

```text
以后开头不要先讲概念，要先给真实场景、冲突或结果证明。
```

或者：

```text
我这个账号不是做 AI 工具，而是做健身小白减脂，目标是转化私教课。
```

Skill 会把这些长期偏好写入本地资料，例如：

```text
profiles/default/
  creator-profile.yaml
  content-memory.md
  winning-patterns.md
  forbidden-patterns.md
  visual-style.md
  episode-ledger.jsonl
  performance-ledger.jsonl
```

### 2. 生成短视频文案

你可以直接说：

```text
使用 video-growth-producer，帮我生成一期视频。
```

如果你没有给具体文案，Codex 会先读取你的账号方向和内容记忆，再生成一篇适合当前账号的短视频文案。

如果你已经写好了文案，可以直接给 Codex：

```text
使用 video-growth-producer，把下面这段文案做成短视频：

<粘贴你的文案>
```

### 3. 生成视频方案与 Remotion 工程

默认视频引擎是 Remotion。

Skill 会优先生成竖屏短视频方案，包括：

- 画面结构
- 镜头节奏
- 字幕位置
- 重点词高亮
- 封面构图
- 素材需求
- Remotion 渲染建议

默认生成发布版视频时，也要同时生成一张独立封面图。推荐封面比例是 `3:4`，背景可以用 imagegen 生成，但中文标题必须用本地脚本或设计工具叠加，避免 AI 生成错字和乱码。

如果你启用了 imagegen，可以让 Codex 为每个重点画面生成视觉素材。

如果你启用了 HyperFrames，可以把部分画面升级成更强的动态页面或演示动画。

## 安装方式

把仓库克隆到 Codex 的 Skills 目录。

macOS / Linux：

```bash
git clone https://github.com/dudachun/video-growth-producer.git ~/.codex/skills/video-growth-producer
```

Windows PowerShell：

```powershell
git clone https://github.com/dudachun/video-growth-producer.git $env:USERPROFILE\.codex\skills\video-growth-producer
```

安装后，新开一个 Codex 会话，然后这样调用：

```text
使用 video-growth-producer，帮我初始化短视频账号资料。
```

## 快速开始

进入 Skill 目录后，先初始化本地账号资料：

```bash
python scripts/init_creator_profile.py --profile default
```

检查工作区是否准备好：

```bash
python scripts/check_workspace.py --profile default
```

然后告诉 Codex：

```text
使用 video-growth-producer，帮我生成一期适合我账号方向的短视频。
```

## 推荐工作流

### 第一步：初始化账号方向

告诉 Codex：

```text
使用 video-growth-producer，帮我初始化账号方向。
我的目标用户是：准备学习 AI 工具的新手。
我的最终目标是：让他们关注我，并购买我的课程或咨询服务。
我的内容风格是：直接、实用、有冲突感，不要太官方。
```

### 第二步：训练偏好

每次你觉得文案或视频哪里不好，直接告诉 Codex：

```text
以后不要用这种开头，太平了。我要前 2 秒就给冲突和结果。
```

或者：

```text
以后每期不要只讲一个工具，普通小工具可以一次讲 3 个，大项目再单独讲 1 个。
```

这些反馈应该被写入本地记忆，后续生成时继续使用。

### 第三步：生成文案

```text
使用 video-growth-producer，给我一篇 45 秒左右的短视频文案。
```

### 第四步：生成视频

```text
使用 video-growth-producer，用这篇文案生成一个 9:16 竖屏视频。
```

### 第五步：复盘数据

发布后，把平台数据截图或指标发给 Codex：

```text
这是这期视频的数据，帮我分析为什么播放量低，并记录以后不要再犯的问题。
```

Skill 会把有效经验写入：

```text
profiles/default/performance-ledger.jsonl
profiles/default/winning-patterns.md
profiles/default/forbidden-patterns.md
```

## 爆款开头规则

短视频最重要的是前 2 秒和前 5 秒。

开头不要只放：

- 空背景
- 氛围动画
- Logo 动画
- 抽象标题
- 没有信息量的过场

更推荐直接展示：

- 错误做法 vs 正确做法
- 使用前 vs 使用后
- 真实结果
- 工具界面
- 成品预览
- 数据变化
- 强冲突观点
- 观众正在遇到的问题

工具类视频默认：

```text
先展示结果，再讲工具名。
```

知识类视频默认：

```text
先指出错误认知，再给正确方法。
```

## 声音工作流

这个 Skill 推荐使用本地 CosyVoice 做声音克隆，但不会随仓库附带任何私人声音文件。

公共仓库不包含：

- 私人音频样本
- 声纹文件
- 克隆模型
- 已生成旁白
- 私人账号数据
- 发布数据截图
- 生成后的视频成片

用户可以在自己的本地工作区里选择：

- 使用 CosyVoice
- 使用其他 TTS 服务
- 导入真人录音
- 先生成无声预览
- 自己接入其他语音方案

生成发布版视频前，必须单独质检开头第一句：抽取最终旁白前 5 秒，用 Whisper 或其他 ASR 转写，确认第一个词、否定词和核心动词没有读错。如果开头读错，要先重生成语音或改写第一句，再继续渲染。

声音相关说明见：

```text
references/voice-cosyvoice.md
```

## Remotion 视频模板

默认模板位于：

```text
assets/remotion-template/
```

你可以直接复制这个模板作为新项目起点，也可以把 Skill 的流程接入你已有的 Remotion 项目。

相关说明见：

```text
references/video-generation-remotion.md
```

## 常用脚本

```text
scripts/init_creator_profile.py
scripts/check_workspace.py
scripts/create_caption_timeline.py
scripts/create_cover.py
scripts/validate_video.py
scripts/update_content_memory.py
scripts/update_performance_ledger.py
```

脚本的作用：

- `init_creator_profile.py`：初始化本地创作者资料
- `check_workspace.py`：检查当前工作区是否准备好
- `create_caption_timeline.py`：根据文案和时长生成字幕时间轴
- `create_cover.py`：把标题叠加到封面背景图上，生成发布用封面
- `validate_video.py`：用 `ffprobe` 检查成片规格
- `update_content_memory.py`：记录内容方向变化
- `update_performance_ledger.py`：记录发布数据和复盘结果

## 目录结构

```text
video-growth-producer/
  SKILL.md
  README.md
  LICENSE
  agents/
  references/
  scripts/
  assets/
```

## 发布前隐私检查

如果你 fork 了这个仓库，或者准备把自己的版本推到 GitHub，请确认不要提交下面这些本地文件：

```text
profiles/
voice_samples/
voice_models/
.generated/
input/
output/
*.wav
*.mp3
*.mp4
*.mov
*.m4a
账号截图
发布数据截图
私人声纹文件
```

仓库里的 `.gitignore` 已经默认排除了常见的私人文件和生成文件。

## 开源协议

MIT License
