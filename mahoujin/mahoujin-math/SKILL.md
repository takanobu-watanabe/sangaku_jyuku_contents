---
name: mahoujin-math
description: 小学生向け魔方陣（magic squares）のインタラクティブHTML教材を生成する。算数塾の教材として使用。魔方陣の作成、操作、学習を支援する。以下の場合に使用する：(1)「魔方陣」「magic squares」「算数教材」に言及があるとき (2) 小学生向けの算数学習教材を作りたいとき (3) 魔方陣を視覚的に学ばせたいとき。対象は小学3〜6年生。
---

# Mahoujin Math

## Overview

このスキルは、小学生向けの魔方陣（magic squares）のインタラクティブHTML教材を生成します。魔方陣の作成、操作、学習を支援し、算数の概念（数のパターン、合計の計算）を視覚的に学べるようにします。

## Quick Start

魔方陣の基本的なHTML教材を作成するには、以下の手順に従います：

1. 魔方陣のサイズを指定（例: 3x3）
2. インタラクティブ機能を追加（数字のドラッグ＆ドロップ、自動チェック）
3. 学習ガイドを付加

## 魔方陣の生成

魔方陣を生成するには、scripts/generate_magic_square.py を使用します。このスクリプトは、指定されたサイズの魔方陣を作成し、HTML形式で出力します。

## インタラクティブ機能

HTML教材には以下の機能を含めます：

- 数字のドラッグ＆ドロップ
- 行・列・対角線の合計自動計算
- 正解チェック機能
- ヒント表示

## 学習ガイド

references/magic_square_guide.md を参照して、魔方陣の学習内容を追加します。算数の概念（パターン認識、数学的思考）を説明します。

## Resources

### scripts/
- generate_magic_square.py: 魔方陣を生成するPythonスクリプト

### references/
- magic_square_guide.md: 魔方陣の学習ガイドと算数概念の説明

### assets/
- template.html: HTML教材のテンプレート
- style.css: スタイルシート
- script.js: インタラクティブ機能のJavaScript

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
