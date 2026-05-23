# cvbuilder-cli

专业的 PDF 简历生成工具 - 将 Markdown 简历快速转换为精美 PDF 文件，支持多种样式、自定义页眉页脚、LLM 智能格式化。

## 功能特性

- 📝 **Markdown 转 PDF** - 一键生成专业简历
- 🎨 **4 种内置样式** - default / modern / classic / elegant，满足不同场景需求
- 🌐 **中英文支持** - 自动检测语言或手动指定
- 🤖 **LLM 智能格式化** - 原始文本自动转为标准简历格式
- 📋 **自定义页眉页脚** - 支持文字和图片
- ⚡ **CLI 命令行工具** - 简洁高效的工作流
- 🎯 **左对齐/右对齐布局** - 教育背景和经历的时间段自动右对齐

## 安装和环境配置

### 1. 安装 cvbuilder-cli

```bash
pip install cvbuilder-cli
```

### 2. 安装 Playwright 浏览器

cvbuilder 使用 Playwright 进行 PDF 渲染，需要安装 Chromium 浏览器：

```bash
playwright install chromium
```

### 3. （可选）配置 LLM

如果需要使用 LLM 自动格式化功能，需要配置 llmdog。详细教程请查看下方的 [LLM 配置完整教程](#llm-配置完整教程)。

## 使用示例和代码片段

### 基础使用流程（完整步骤）

#### 1. 创建工作目录

```bash
mkdir my-resume && cd my-resume
```

#### 2. 初始化模板文件

```bash
# 获取所有模板（中英文 + 4 种样式）
cvbuilder init

# 仅获取中文模板
cvbuilder init --lang zh

# 仅获取英文模板
cvbuilder init --lang en
```

#### 3. 编辑简历内容

用文本编辑器打开 `resume_zh.md` 或 `resume_en.md`，填入你的信息。

#### 4. 生成 PDF

```bash
cvbuilder build --md resume_zh.md --output 张三简历.pdf
```

---

### CLI 命令详解

cvbuilder 提供 5 个核心命令：

| 命令 | 功能 | 常用参数 |
|------|------|----------|
| `init` | 初始化模板文件 | `--lang`, `--force` |
| `build` | 从 Markdown 生成 PDF | `--md`, `--css`, `--output`, `--header`, `--footer` |
| `format` | LLM 智能格式化 + 生成 PDF | `--input`, `--output`, `--md-only`, `--lang` |
| `styles` | 查看可用样式列表 | 无 |
| `llm-config` | 生成 LLM 配置示例 | 无 |

#### 命令 1：init - 初始化模板

**功能**：复制模板文件到当前目录

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--lang` | string | all | 语言：zh（中文）、en（英文）、all（全部） |
| `--force`, `-f` | flag | false | 强制覆盖已存在的文件 |

**使用示例**：

```bash
# 获取所有模板
cvbuilder init

# 仅获取中文模板
cvbuilder init --lang zh

# 强制覆盖已有文件
cvbuilder init --force

# 简写形式
cvbuilder init -f
```

#### 命令 2：build - 生成 PDF

**功能**：将 Markdown 简历转换为 PDF

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--md` | Path | resume.md | Markdown 文件路径 |
| `--css` | string | default | 样式名称或 CSS 文件路径 |
| `--output` | Path | 同名.pdf | 输出 PDF 路径 |
| `--lang` | string | auto | 语言：zh、en、auto |
| `--header` | string | - | 页眉文字 |
| `--header-image` | string | - | 页眉图片路径 |
| `--footer` | string | - | 页脚文字 |
| `--footer-image` | string | - | 页脚图片路径 |
| `--no-html` | flag | false | 不生成中间 HTML 文件 |

**使用示例**：

```bash
# 基础用法
cvbuilder build --md resume_zh.md

# 指定输出文件
cvbuilder build --md resume_zh.md --output 张三简历.pdf

# 使用不同样式
cvbuilder build --md resume_zh.md --css elegant

# 添加页眉页脚
cvbuilder build --md resume_zh.md \
  --header "张三 | 138-0000-0000" \
  --footer "机密文档"

# 添加图片页眉
cvbuilder build --md resume_zh.md --header-image logo.png

# 使用自定义 CSS
cvbuilder build --md resume_zh.md --css my-style.css

# 不生成 HTML 文件
cvbuilder build --md resume_zh.md --no-html
```

#### 命令 3：format - LLM 智能格式化

**功能**：使用 LLM 将原始文本格式化为标准 Markdown 简历

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--input`, `-i` | Path | **必填** | 输入文件路径（txt 或 json） |
| `--output`, `-o` | Path | 同名.pdf | 输出 PDF 路径 |
| `--css` | string | default | 样式名称或 CSS 文件路径 |
| `--lang` | string | auto | 目标语言：zh、en、auto |
| `--header` | string | - | 页眉文字 |
| `--header-image` | string | - | 页眉图片路径 |
| `--footer` | string | - | 页脚文字 |
| `--footer-image` | string | - | 页脚图片路径 |
| `--md-only` | flag | false | 只输出 Markdown，不生成 PDF |
| `--verbose`, `-v` | flag | false | 显示 LLM 配置信息 |

**使用示例**：

```bash
# 基础用法：从文本生成 PDF
cvbuilder format --input raw_resume.txt

# 指定输出文件
cvbuilder format --input raw_resume.txt --output resume.pdf

# 只生成 Markdown（不生成 PDF）
cvbuilder format --input raw_resume.txt --md-only

# 指定语言和样式
cvbuilder format --input raw_resume.txt --lang zh --css elegant

# 添加页眉页脚
cvbuilder format --input raw_resume.txt \
  --header "张三 | 138-0000-0000" \
  --md-only

# 显示 LLM 配置信息
cvbuilder format --input raw_resume.txt --verbose

# 简写形式
cvbuilder format -i raw_resume.txt -o resume.pdf -v
```

#### 命令 4：styles - 查看样式列表

**功能**：列出所有可用的内置样式

**使用示例**：

```bash
cvbuilder styles
```

输出：
```
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
│ 样式名称 │ 说明                         │
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ default  │ 默认样式 - 中英文通用        │
│ modern   │ 现代风格 - 大留白、简约      │
│ classic  │ 经典风格 - 传统正式          │
│ elegant  │ 优雅风格 - 渐变强调色        │
└──────────┴──────────────────────────────┘
```

#### 命令 5：llm-config - 生成 LLM 配置

**功能**：生成 llmdog 配置文件示例

**使用示例**：

```bash
cvbuilder llm-config
```

---

### 样式选择指南

cvbuilder 提供 4 种精心设计的样式，满足不同场景需求：

| 样式名称 | 视觉特点 | 适用场景 | 行业推荐 |
|---------|---------|---------|----------|
| **default** | 居中标题、蓝色强调线 | 技术岗位、互联网 | 程序员、工程师 |
| **modern** | 左对齐、大留白、大写标题 | 设计、创意、海外 | 设计师、产品经理 |
| **classic** | 衬线字体、传统正式 | 金融、政府、学术 | 银行、公务员、教授 |
| **elegant** | 渐变色彩、卡片区块 | 高端岗位、管理岗 | 高管、咨询顾问 |

**快速选择建议**：

1. **不确定选哪个？** → 使用 `default`
2. **申请外企/海外岗位？** → 使用 `modern`
3. **申请传统行业？** → 使用 `classic`
4. **想要脱颖而出？** → 使用 `elegant`

**样式对比示例**：

```bash
# 生成同一简历的 4 种样式版本
cvbuilder build --md resume_zh.md --css default --output 简历_默认.pdf
cvbuilder build --md resume_zh.md --css modern --output 简历_现代.pdf
cvbuilder build --md resume_zh.md --css classic --output 简历_经典.pdf
cvbuilder build --md resume_zh.md --css elegant --output 简历_优雅.pdf
```

---

### LLM 格式化功能详解

#### 使用场景

当你有以下格式的原始简历时，可以使用 LLM 自动格式化：
- 纯文本简历
- JSON 格式简历
- 非标准 Markdown
- 需要翻译的简历

#### 完整工作流程

**方式 1：直接生成 PDF（推荐）**

```bash
# 一步完成：格式化 + 生成 PDF
cvbuilder format --input raw_resume.txt --output resume.pdf
```

**方式 2：先预览 Markdown，再决定样式**

```bash
# 第一步：只生成 Markdown
cvbuilder format --input raw_resume.txt --md-only

# 第二步：查看生成的 Markdown
cat raw_resume.md

# 第三步：选择样式生成 PDF
cvbuilder build --md raw_resume.md --css elegant --output resume.pdf
```

#### 语言处理

| 场景 | 参数 | 说明 |
|------|------|------|
| 自动检测 | `--lang auto` | 根据输入内容自动判断 |
| 强制中文 | `--lang zh` | 输出中文简历 |
| 强制英文 | `--lang en` | 输出英文简历 |
| 翻译简历 | `--lang en` | 输入中文，输出英文 |

**示例**：

```bash
# 中文输入 → 中文输出
cvbuilder format --input 中文简历.txt --lang zh

# 中文输入 → 英文输出（翻译）
cvbuilder format --input 中文简历.txt --lang en --output English_Resume.pdf
```

---

### md-only 模式详细说明

#### 什么是 md-only 模式？

`--md-only` 参数让 `format` 命令只输出 Markdown 文件，跳过 PDF 生成步骤。

#### 使用场景

1. **预览 LLM 输出** - 检查格式化结果是否符合预期
2. **手动调整** - 生成 Markdown 后手动编辑细节
3. **多样式对比** - 用同一 Markdown 生成多个 PDF 版本
4. **节省时间** - 不需要 PDF 时跳过渲染步骤

#### 使用示例

```bash
# 基础用法
cvbuilder format --input raw_resume.txt --md-only

# 指定输出文件名
cvbuilder format --input raw_resume.txt --md-only --output my_resume.md

# 指定语言
cvbuilder format --input raw_resume.txt --md-only --lang zh
```

#### 后续操作

生成 Markdown 后，可以：

```bash
# 1. 查看生成的内容
cat my_resume.md

# 2. 手动编辑（可选）
vim my_resume.md

# 3. 使用不同样式生成多个 PDF
cvbuilder build --md my_resume.md --css default --output 简历_默认.pdf
cvbuilder build --md my_resume.md --css elegant --output 简历_优雅.pdf
cvbuilder build --md my_resume.md --css modern --output 简历_现代.pdf

# 4. 添加页眉页脚
cvbuilder build --md my_resume.md \
  --header "张三 | 138-0000-0000" \
  --footer "更新日期：2024-01-01"
```

---

### 常见使用场景和最佳实践

#### 场景 1：快速创建中文简历

```bash
# 1. 创建项目
mkdir my-resume && cd my-resume

# 2. 初始化模板
cvbuilder init --lang zh

# 3. 编辑简历
vim resume_zh.md

# 4. 生成 PDF
cvbuilder build --md resume_zh.md --output 张三简历.pdf
```

#### 场景 2：从原始文本快速生成

```bash
# 一步完成
cvbuilder format --input raw_resume.txt --output resume.pdf

# 或分步进行
cvbuilder format --input raw_resume.txt --md-only
vim raw_resume.md  # 手动调整
cvbuilder build --md raw_resume.md --css elegant
```

#### 场景 3：多语言简历

```bash
# 生成中文版
cvbuilder format --input raw_resume.txt --lang zh --md-only --output 中文简历.md
cvbuilder build --md 中文简历.md --output 张三_中文.pdf

# 生成英文版（翻译）
cvbuilder format --input raw_resume.txt --lang en --md-only --output English_Resume.md
cvbuilder build --md English_Resume.md --output John_English.pdf
```

#### 场景 4：多样式对比选择

```bash
# 1. 生成 Markdown
cvbuilder format --input raw_resume.txt --md-only

# 2. 生成 4 种样式版本
cvbuilder build --md raw_resume.md --css default --output v1_default.pdf
cvbuilder build --md raw_resume.md --css modern --output v2_modern.pdf
cvbuilder build --md raw_resume.md --css classic --output v3_classic.pdf
cvbuilder build --md raw_resume.md --css elegant --output v4_elegant.pdf

# 3. 对比后选择最满意的版本
```

#### 场景 5：添加公司信息

```bash
# 添加公司 Logo 和保密信息
cvbuilder build --md resume_zh.md \
  --header-image company_logo.png \
  --header "内部使用 - 请勿外传" \
  --footer "Confidential" \
  --output 简历_公司版.pdf
```

---

### 参数组合示例

#### 组合 1：完整配置

```bash
cvbuilder build --md resume_zh.md \
  --css elegant \
  --output 张三简历.pdf \
  --lang zh \
  --header "张三 | 138-0000-0000 | zhangsan@email.com" \
  --header-image logo.png \
  --footer "更新日期：2024-01-01"
```

#### 组合 2：LLM 格式化 + 优雅样式

```bash
cvbuilder format --input raw.txt \
  --lang zh \
  --css elegant \
  --header "内部简历" \
  --output 格式化简历.pdf
```

#### 组合 3：批量生成多语言版本

```bash
# 中文版
cvbuilder format -i raw.txt --lang zh --md-only -o zh.md
cvbuilder build --md zh.md --css default -o 张三_中文.pdf

# 英文版
cvbuilder format -i raw.txt --lang en --md-only -o en.md
cvbuilder build --md en.md --css modern -o John_English.pdf
```

#### 组合 4：自定义样式 + 页眉页脚

```bash
cvbuilder build --md resume.md \
  --css my_custom.css \
  --header-image company_logo.png \
  --header "机密文档" \
  --footer "Page 1" \
  --output custom_resume.pdf \
  --no-html
```

## 样式详细介绍

cvbuilder 提供 4 种精心设计的样式，每种都有独特的视觉风格：

### 1. default - 默认样式

**特色**：
- 居中标题，专业简洁
- 蓝色左侧强调线（section headers）
- 无衬线字体，通用性强

**适用场景**：
- ✅ 技术岗位简历
- ✅ 互联网行业
- ✅ 通用型简历

**使用方式**：
```bash
cvbuilder build --md resume.md --css default
```

### 2. modern - 现代风格

**特色**：
- 左对齐大标题，简约设计
- 蓝色大写字母章节标题
- 充足留白，现代感十足

**适用场景**：
- ✅ 设计师简历
- ✅ 创意行业
- ✅ 海外求职

**使用方式**：
```bash
cvbuilder build --md resume.md --css modern
```

### 3. classic - 经典风格

**特色**：
- 衬线字体（Georgia/宋体）
- 传统横线分隔
- 保守配色，正式感强

**适用场景**：
- ✅ 金融/银行行业
- ✅ 政府机关
- ✅ 学术岗位
- ✅ 传统企业

**使用方式**：
```bash
cvbuilder build --md resume.md --css classic
```

### 4. elegant - 优雅风格（NEW！）

**特色**：
- 渐变紫色强调色（#6366f1 → #818cf8）
- 渐变标题背景效果
- 卡片式区块设计
- 圆角边框，柔和视觉层次

**适用场景**：
- ✅ 高端岗位
- ✅ 管理岗位
- ✅ 希望脱颖而出的场景
- ✅ 外企/跨国公司

**使用方式**：
```bash
cvbuilder build --md resume.md --css elegant
```

## 样式配置方法

### 方法 1：使用内置样式

```bash
# 查看所有可用样式
cvbuilder styles

# 使用指定样式
cvbuilder build --md resume.md --css <样式名>
```

### 方法 2：自定义 CSS

1. 初始化获取所有样式文件：
```bash
cvbuilder init
```

2. 复制并修改任意样式文件：
```bash
cp default.css my-custom.css
# 编辑 my-custom.css，修改颜色、字体等
```

3. 使用自定义样式：
```bash
cvbuilder build --md resume.md --css my-custom.css
```

### 常用 CSS 修改示例

**修改强调色**：
```css
:root {
    --accent: #ff6b6b;  /* 改为红色 */
}
```

**修改字体**：
```css
html, body {
    font-family: "你的字体", sans-serif;
}
```

**调整页边距**：
```css
@page {
    margin: 15mm 20mm;  /* 上下 15mm，左右 20mm */
}
```

## 文本对齐格式说明

### 教育背景/工作经历布局

使用 `edu-row` 类实现左右对齐布局：

```markdown
### <div class="edu-row"><strong>左侧内容</strong> <span>右侧内容</span></div>
```

**实际效果**：
```
北京大学 - 计算机硕士              2020.09 - 2023.06
高级后端工程师 - 字节跳动           2023.07 - 至今
```

**注意事项**：
- 左侧内容使用 `<strong>` 标签，左对齐
- 右侧内容使用 `<span>` 标签，右对齐且不换行
- 中间自动填充空白
- 适用于教育背景和工作经历的时间段显示

## API 接口说明

### Python API

```python
from cvbuilder import convert

# 基本用法
convert(
    md_path="resume.md",
    css_path="resume.css",
    output="resume.pdf",
    lang="zh"  # zh / en / auto
)

# 完整参数
convert(
    md_path="resume.md",
    css_path="elegant.css",
    output="resume.pdf",
    lang="zh",
    header_text="页眉文字",
    header_image="logo.png",
    footer_text="页脚文字",
    footer_image="footer.png"
)
```

### LLM 格式化 API

```python
from cvbuilder.formatter import format_resume

# 格式化原始文本
md_content = format_resume(
    input_text="你的原始简历文本...",
    lang="zh"  # zh / en / auto
)

# 保存为 Markdown 文件
with open("resume.md", "w") as f:
    f.write(md_content)
```

## 依赖项清单

### 核心依赖

- **typer** (>=0.9, <1.0) - CLI 框架
- **markdown** (>=3.5, <4.0) - Markdown 解析
- **playwright** (>=1.40, <2.0) - 浏览器自动化（PDF 渲染）
- **pypdf** (>=3.0, <5.0) - PDF 处理
- **llmdog** - LLM 调用封装
- **larkfunc** - LLM 响应清理
- **rich** (>=13.0, <14.0) - 终端美化输出

### 系统依赖

- Python >= 3.10
- Playwright Chromium 浏览器（通过 `playwright install chromium` 安装）

## LLM 配置完整教程

本教程将指导你完成 llmdog 的配置，让你能够使用 LLM 智能格式化功能。

### 什么是 llmdog？

llmdog 是一个 LLM 调用封装库，cvbuilder 使用它来调用大语言模型（如 DeepSeek、OpenAI 等），将你的原始简历文本自动格式化为标准的 Markdown 简历格式。

### 配置前准备

在开始配置之前，你需要：

1. **获取 API Key** - 从 LLM 服务提供商获取 API 密钥
   - DeepSeek: https://platform.deepseek.com/
   - OpenAI: https://platform.openai.com/
   - 其他支持 OpenAI 兼容 API 的服务

2. **确认 API 地址** - 不同服务商的 API 地址不同
   - DeepSeek: `https://api.deepseek.com/v1/chat/completions`
   - OpenAI: `https://api.openai.com/v1/chat/completions`

### 第一步：生成配置文件示例

在项目根目录执行以下命令：

```bash
cvbuilder llm-config
```

执行后会生成 `.llmdog.yaml.example` 文件，内容如下：

```yaml
# llmdog 配置文件
# 将此文件复制为 .llmdog.yaml 并填入真实配置
api_key: sk-xxxxxxxxxxxxxxxxxxxxxxxx
api_url: https://api.deepseek.com/v1/chat/completions
model: deepseek-chat
timeout: 60
verify_ssl: true
```

### 第二步：创建配置文件

复制示例文件为实际配置文件：

```bash
cp .llmdog.yaml.example .llmdog.yaml
```

### 第三步：编辑配置文件

用任意文本编辑器打开 `.llmdog.yaml`，修改为你的真实配置：

```yaml
# .llmdog.yaml - LLM 配置文件

# 【必填】API Key - 从服务商处获取
api_key: sk-your-real-api-key-here

# 【必填】API 地址 - 根据你使用的服务修改
api_url: https://api.deepseek.com/v1/chat/completions

# 【必填】模型名称 - 根据你使用的服务修改
model: deepseek-chat

# 【可选】超时时间（秒）- 默认 60 秒
timeout: 60

# 【可选】是否验证 SSL 证书 - 默认 true
verify_ssl: true
```

### 配置文件参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `api_key` | string | ✅ | 无 | 你的 API 密钥，从 LLM 服务商获取 |
| `api_url` | string | ✅ | 无 | API 请求地址，不同服务商地址不同 |
| `model` | string | ✅ | 无 | 使用的模型名称 |
| `timeout` | int | ❌ | 60 | 请求超时时间（秒） |
| `verify_ssl` | bool | ❌ | true | 是否验证 SSL 证书 |

### 常见服务商配置示例

#### DeepSeek（推荐）

```yaml
api_key: sk-xxxxxxxxxxxxxxxxxxxxxxxx
api_url: https://api.deepseek.com/v1/chat/completions
model: deepseek-chat
timeout: 60
verify_ssl: true
```

#### OpenAI

```yaml
api_key: sk-xxxxxxxxxxxxxxxxxxxxxxxx
api_url: https://api.openai.com/v1/chat/completions
model: gpt-4o
timeout: 60
verify_ssl: true
```

#### 其他兼容 OpenAI API 的服务

```yaml
api_key: your-api-key
api_url: https://your-api-domain.com/v1/chat/completions
model: your-model-name
timeout: 60
verify_ssl: true
```

### 配置优先级顺序

cvbuilder 按照以下顺序查找配置文件（优先级从高到低）：

1. **项目根目录** - `./llmdog.yaml`（当前工作目录）
2. **家目录** - `~/.llmdog.yaml`（用户主目录）
3. **环境变量** - 通过 `.env` 文件设置
4. **默认配置** - 使用内置默认值

**示例**：

```bash
# 优先级 1：项目级配置（推荐）
./your-project/.llmdog.yaml

# 优先级 2：全局配置（所有项目共享）
~/.llmdog.yaml  # Linux/macOS: /home/user/.llmdog.yaml
                # Windows: C:\Users\user\.llmdog.yaml

# 优先级 3：环境变量配置
echo "LLMDOG_API_KEY=sk-xxx" >> .env
```

**建议**：
- ✅ 每个项目使用独立的 `.llmdog.yaml`（优先级 1）
- ✅ 多台电脑共享配置可使用家目录配置（优先级 2）
- ❌ 避免在代码中硬编码 API Key

### 安全注意事项 ⚠️

**重要：保护你的 API Key！**

1. **加入 .gitignore**

   绝对不要将 `.llmdog.yaml` 提交到 Git 仓库！

   ```bash
   # 在项目根目录创建或编辑 .gitignore 文件
   echo ".llmdog.yaml" >> .gitignore
   ```

2. **检查是否已忽略**

   ```bash
   # 检查文件是否被 Git 跟踪
   git status

   # 如果显示 .llmdog.yaml，立即移除
   git rm --cached .llmdog.yaml
   ```

3. **权限设置**（Linux/macOS）

   ```bash
   # 设置文件仅所有者可读写
   chmod 600 .llmdog.yaml
   ```

4. **不要分享给他人**

   - API Key 等同于密码
   - 泄露可能导致费用损失
   - 定期更换 API Key

5. **使用环境变量（可选）**

   对于团队协作，可以使用环境变量：

   ```bash
   # 在 .env 文件中设置（也需加入 .gitignore）
   echo "LLMDOG_API_KEY=sk-xxx" >> .env
   echo ".env" >> .gitignore
   ```

### 验证配置

配置完成后，测试是否成功：

```bash
# 方法 1：使用 format 命令测试
cvbuilder format --input test_resume.txt --output test.pdf

# 方法 2：查看配置是否被正确读取（推荐）
cvbuilder format --input test_resume.txt --md-only --verbose
```

**使用 `--verbose` 参数查看配置**：

```bash
cvbuilder format --input raw_resume.txt --verbose
```

输出示例：
```
📋 LLM 配置信息:
  API 端点: https://api.deepseek.com/v1/chat/completions
  模型名称: deepseek-chat
  超时时间: 60秒
  最大重试: 3次
  后端类型: 默认
  目标语言: 中文
```

如果配置正确，应该能看到完整的配置信息并成功生成 PDF。

### 常见问题解答（FAQ）

#### Q1: 提示 "LLM 返回空响应" 怎么办？

**A**: 可能原因：
1. API Key 错误 - 检查是否正确复制
2. API 地址错误 - 确认 URL 格式
3. 网络问题 - 检查网络连接
4. 余额不足 - 确认账户有足够余额

**解决步骤**：
```bash
# 1. 检查配置文件
cat .llmdog.yaml

# 2. 测试 API 连接（使用 curl）
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-your-key" \
  -d '{"model": "deepseek-chat", "messages": [{"role": "user", "content": "Hello"}]}'
```

#### Q2: 可以使用免费的 LLM 吗？

**A**: 可以！以下是一些免费选项：
- DeepSeek: 注册即送免费额度
- OpenAI: 新用户有免费额度
- 本地部署: Ollama、LM Studio 等

#### Q3: 如何切换不同的 LLM 服务商？

**A**: 修改 `.llmdog.yaml` 中的 `api_url` 和 `model`：

```yaml
# 从 DeepSeek 切换到 OpenAI
api_url: https://api.openai.com/v1/chat/completions
model: gpt-4o
```

#### Q4: 多个项目需要不同配置怎么办？

**A**: 每个项目创建独立的 `.llmdog.yaml`：

```bash
# 项目 A
project-a/.llmdog.yaml  # 使用 DeepSeek

# 项目 B
project-b/.llmdog.yaml  # 使用 OpenAI
```

#### Q5: 配置后仍然无法使用？

**A**: 按以下步骤排查：

1. **检查文件位置**
   ```bash
   # 确认配置文件在当前目录
   ls -la .llmdog.yaml
   ```

2. **检查 YAML 格式**
   - 使用空格，不要使用 Tab
   - 键值对用冒号分隔
   - 字符串不需要引号（除非包含特殊字符）

3. **查看错误日志**
   ```bash
   # 使用 verbose 模式运行
   cvbuilder format --input test.txt --output test.pdf -v
   ```

4. **联系支持**
   - 提交 Issue 到 GitHub
   - 附上错误信息（隐藏 API Key）

### 快速配置清单

- [ ] 获取 API Key
- [ ] 运行 `cvbuilder llm-config`
- [ ] 复制 `.llmdog.yaml.example` 为 `.llmdog.yaml`
- [ ] 编辑 `.llmdog.yaml`，填入真实配置
- [ ] 将 `.llmdog.yaml` 加入 `.gitignore`
- [ ] 测试配置是否成功

完成以上步骤后，你就可以使用 `cvbuilder format` 命令享受 LLM 智能格式化功能了！

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 开发环境设置

```bash
# 克隆仓库
git clone <repository-url>
cd cvbuilder

# 安装开发依赖
pip install -e .

# 安装 Playwright
playwright install chromium
```

### 提交 Pull Request

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范

- 遵循 PEP 8 编码规范
- 使用 type hints
- 添加必要的注释

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件
