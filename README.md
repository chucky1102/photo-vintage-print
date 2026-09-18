# photo-vintage-print · 旧刊新印

把用户提供的实拍照片转译成 20 世纪中期复古印刷插画或杂志封面：保留人物关系与原片配色，使用轮廓、限色油墨、半调网点和克制的旧纸质感。

Turn a supplied photograph into a mid-century editorial print or magazine cover with source-derived colors, bold contours, limited inks, halftone screening, and restrained aged-paper texture.

## 适用范围 / Scope

- 适合：照片转复古插画、旧杂志封面、限色印刷艺术。
- 不适合：只调色、完全不重绘的纪实修图，或没有原片的通用文章封面。
- 默认执行仓库中用户验证过的完整原始 Prompt，不自动压缩、重排或写死标题与配色。
- Uses the supplied photograph as the sole visual source. It does not silently scan neighboring folders or publish outputs.

## 安装 / Install

```bash
git clone https://github.com/chucky1102/photo-vintage-print.git ~/.codex/skills/photo-vintage-print
```

安装后重新打开 Codex，使 Skill 清单刷新。也可以下载 GitHub Release 中的 ZIP，直接解压到 `~/.codex/skills/`；压缩包本身已经包含 `photo-vintage-print/` 顶层目录，不要再套一层同名文件夹。

Restart Codex after installation so the skill list refreshes.

## 使用 / Usage

在 Codex 中提供一张本地照片或附件，然后调用：

```text
使用 $photo-vintage-print 把这张照片转成旧刊新印风格的复古杂志封面。
```

可以明确要求“纯插画不加字”“只保留一个标题”“少做旧”或指定标题。未指定时，Skill 采用默认封面模式，让完整原始 Prompt 根据照片生成标题、配色与版式。

v1.1.0 新增可选版式参考模式。只有明确要求换版式、制作小红书封面、Twitter/X 横图或指定图片窗口、多面板、中文竖排等结构时才启用；默认原始 Prompt 和原片转换路线不变。

## 工作方式 / How it works

1. 实际查看用户提供的最高分辨率原片。
2. 使用 `scripts/prepare_prompt.py` 保存与 `references/original-prompt.md` 逐字节一致的执行 Prompt。
3. 通过当前环境提供的原生 imagegen 生成一张作品。
4. 按内容与设计两条路径验收；关键错误最多定向修正一次。
5. 在独立目录保存原生结果、Prompt 和验收记录，不覆盖原片。

## 隐私与限制 / Privacy and limitations

- 生成时，用户选择的照片会由当前环境的原生图像生成工具处理；本仓库本身不包含上传脚本、API 密钥或第三方服务连接。
- 生成授权不包含公开发布。照片、结果和工作记录不会自动上传到 GitHub、图库或社交平台。
- 生成式插画不能保证身份、手指、道具和文字逐像素一致；Skill 会检查并如实报告差异。
- 原生生成尺寸取决于实际图像工具；插值放大不等于恢复原片细节。

## 验证 / Validate

```bash
./scripts/validate_package.py
```

该命令只读 Skill 文件并在系统临时目录测试 Prompt 复制，不生成图片、不联网。它会验证所需文件、版本格式、Skill 名称与默认调用引用、原始 Prompt 哈希锁以及复制结果。Codex 的完整 Skill 元数据验证应另用当前 Codex 环境提供的 `quick_validate.py`。

## 目录 / Structure

```text
photo-vintage-print/
├── .github/workflows/validate.yml
├── SKILL.md
├── agents/openai.yaml
├── references/
│   ├── original-prompt.md
│   ├── original-prompt.sha256
│   ├── layout-routing.md
│   ├── print-controls.md
│   └── quality-check.md
├── scripts/
│   ├── prepare_prompt.py
│   └── validate_package.py
├── VERSION
├── LICENSE
├── LICENSE.baoyu-cover-image
└── THIRD_PARTY_NOTICES.md
```

## License

The project is released under the [MIT License](LICENSE). Adapted upstream material and attribution are documented in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and [LICENSE.baoyu-cover-image](LICENSE.baoyu-cover-image).
