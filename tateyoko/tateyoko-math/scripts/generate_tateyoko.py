#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
たてよこ算 問題生成・検証スクリプト
指定サイズ・演算子の問題を生成し、HTML形式で出力する。
"""

import argparse
import itertools
import json
import random
import sys
from typing import List, Tuple, Optional, Dict


def generate_addition_2x2(count: int) -> List[Dict]:
    """2×2足し算の問題を生成する。"""
    problems = []
    seen = set()

    # 1〜9から重複なしで4つ選び、2×2グリッドに配置
    all_combos = list(itertools.combinations(range(1, 10), 4))
    random.shuffle(all_combos)

    for combo in all_combos:
        if len(problems) >= count:
            break
        nums = list(combo)
        # 全順列を試して、行・列の制約を満たすものを探す
        for perm in itertools.permutations(nums):
            grid = [[perm[0], perm[1]], [perm[2], perm[3]]]
            # 同じ行に同じ数字がないか確認
            if grid[0][0] == grid[0][1] or grid[1][0] == grid[1][1]:
                continue
            # 同じ列に同じ数字がないか確認
            if grid[0][0] == grid[1][0] or grid[0][1] == grid[1][1]:
                continue

            row_sums = [sum(row) for row in grid]
            col_sums = [grid[0][j] + grid[1][j] for j in range(2)]

            # 正規化してユニーク判定
            key = (tuple(row_sums), tuple(col_sums))
            if key not in seen:
                seen.add(key)
                problems.append({
                    "type": "addition",
                    "size": 2,
                    "grid": grid,
                    "row_targets": row_sums,
                    "col_targets": col_sums,
                    "black_cells": []
                })
                break

    return problems[:count]


def generate_multiplication_2x2(count: int) -> List[Dict]:
    """2×2掛け算の問題を生成する。"""
    problems = []
    seen = set()

    all_combos = list(itertools.combinations(range(1, 10), 4))
    random.shuffle(all_combos)

    for combo in all_combos:
        if len(problems) >= count:
            break
        nums = list(combo)
        for perm in itertools.permutations(nums):
            grid = [[perm[0], perm[1]], [perm[2], perm[3]]]
            if grid[0][0] == grid[0][1] or grid[1][0] == grid[1][1]:
                continue
            if grid[0][0] == grid[1][0] or grid[0][1] == grid[1][1]:
                continue

            row_products = [grid[i][0] * grid[i][1] for i in range(2)]
            col_products = [grid[0][j] * grid[1][j] for j in range(2)]

            key = (tuple(row_products), tuple(col_products))
            if key not in seen:
                seen.add(key)
                problems.append({
                    "type": "multiplication",
                    "size": 2,
                    "grid": grid,
                    "row_targets": row_products,
                    "col_targets": col_products,
                    "black_cells": []
                })
                break

    return problems[:count]


def generate_addition_3x3(count: int, with_black_cells: bool = False) -> List[Dict]:
    """3×3足し算の問題を生成する。"""
    problems = []
    seen = set()
    attempts = 0
    max_attempts = count * 500

    while len(problems) < count and attempts < max_attempts:
        attempts += 1
        # 1〜9から9つ選ぶ（または重複なしで配置）
        nums = random.sample(range(1, 10), 9)
        grid = [nums[i*3:(i+1)*3] for i in range(3)]

        # 行内・列内の重複チェック
        valid = True
        for i in range(3):
            if len(set(grid[i])) != 3:
                valid = False
                break
        if not valid:
            continue
        for j in range(3):
            col = [grid[i][j] for i in range(3)]
            if len(set(col)) != 3:
                valid = False
                break
        if not valid:
            continue

        black_cells = []
        if with_black_cells:
            # ランダムに1〜2個の黒マスを配置
            num_black = random.choice([1, 2])
            black_cells = random.sample([(i, j) for i in range(3) for j in range(3)], num_black)

        row_sums = []
        for i in range(3):
            s = sum(grid[i][j] for j in range(3) if (i, j) not in black_cells)
            row_sums.append(s)

        col_sums = []
        for j in range(3):
            s = sum(grid[i][j] for i in range(3) if (i, j) not in black_cells)
            col_sums.append(s)

        key = (tuple(row_sums), tuple(col_sums), tuple(sorted(black_cells)))
        if key not in seen:
            seen.add(key)
            problems.append({
                "type": "addition",
                "size": 3,
                "grid": grid,
                "row_targets": row_sums,
                "col_targets": col_sums,
                "black_cells": black_cells
            })

    return problems[:count]


def generate_multiplication_3x3(count: int, with_black_cells: bool = False) -> List[Dict]:
    """3×3掛け算の問題を生成する。"""
    problems = []
    seen = set()
    attempts = 0
    max_attempts = count * 500

    while len(problems) < count and attempts < max_attempts:
        attempts += 1
        nums = random.sample(range(1, 10), 9)
        grid = [nums[i*3:(i+1)*3] for i in range(3)]

        valid = True
        for i in range(3):
            if len(set(grid[i])) != 3:
                valid = False
                break
        if not valid:
            continue
        for j in range(3):
            col = [grid[i][j] for i in range(3)]
            if len(set(col)) != 3:
                valid = False
                break
        if not valid:
            continue

        black_cells = []
        if with_black_cells:
            num_black = random.choice([1, 2])
            black_cells = random.sample([(i, j) for i in range(3) for j in range(3)], num_black)

        row_products = []
        for i in range(3):
            p = 1
            for j in range(3):
                if (i, j) not in black_cells:
                    p *= grid[i][j]
            row_products.append(p)

        col_products = []
        for j in range(3):
            p = 1
            for i in range(3):
                if (i, j) not in black_cells:
                    p *= grid[i][j]
            col_products.append(p)

        key = (tuple(row_products), tuple(col_products), tuple(sorted(black_cells)))
        if key not in seen:
            seen.add(key)
            problems.append({
                "type": "multiplication",
                "size": 3,
                "grid": grid,
                "row_targets": row_products,
                "col_targets": col_products,
                "black_cells": black_cells
            })

    return problems[:count]


def verify_problem(problem: Dict) -> Tuple[bool, str]:
    """問題の解が正しいか検証する。"""
    grid = problem["grid"]
    size = problem["size"]
    ptype = problem["type"]
    row_targets = problem["row_targets"]
    col_targets = problem["col_targets"]
    black_cells = [tuple(bc) for bc in problem.get("black_cells", [])]

    # 行チェック
    for i in range(size):
        if ptype == "addition":
            actual = sum(grid[i][j] for j in range(size) if (i, j) not in black_cells)
        else:
            actual = 1
            for j in range(size):
                if (i, j) not in black_cells:
                    actual *= grid[i][j]
        if actual != row_targets[i]:
            return False, f"行{i+1}: 期待値{row_targets[i]}, 実際値{actual}"

    # 列チェック
    for j in range(size):
        if ptype == "addition":
            actual = sum(grid[i][j] for i in range(size) if (i, j) not in black_cells)
        else:
            actual = 1
            for i in range(size):
                if (i, j) not in black_cells:
                    actual *= grid[i][j]
        if actual != col_targets[j]:
            return False, f"列{j+1}: 期待値{col_targets[j]}, 実際値{actual}"

    # 行内重複チェック
    for i in range(size):
        vals = [grid[i][j] for j in range(size) if (i, j) not in black_cells]
        if len(vals) != len(set(vals)):
            return False, f"行{i+1}に重複あり: {vals}"

    # 列内重複チェック
    for j in range(size):
        vals = [grid[i][j] for i in range(size) if (i, j) not in black_cells]
        if len(vals) != len(set(vals)):
            return False, f"列{j+1}に重複あり: {vals}"

    return True, "OK"


def verify_all(problems: List[Dict]) -> bool:
    """全問題を検証する。"""
    all_ok = True
    for i, p in enumerate(problems):
        ok, msg = verify_problem(p)
        op = "＋" if p["type"] == "addition" else "×"
        if ok:
            print(f"  問{i+1} ({p['size']}×{p['size']} {op}): ✓ OK")
        else:
            print(f"  問{i+1} ({p['size']}×{p['size']} {op}): ✗ NG - {msg}")
            all_ok = False
    return all_ok


def generate_html(problems: List[Dict], title: str = "たてよこ算") -> str:
    """問題をインタラクティブHTML形式で出力する。"""
    problems_json = json.dumps(problems, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Helvetica Neue', Arial, 'Hiragino Sans', sans-serif;
            background: #f0f4f8;
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }}
        h1 {{
            text-align: center;
            color: #2c3e50;
            margin-bottom: 8px;
            font-size: 28px;
        }}
        .subtitle {{
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 20px;
            font-size: 14px;
        }}
        .instructions {{
            max-width: 600px;
            margin: 0 auto 20px;
            background: #e8f4fd;
            padding: 12px 16px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            font-size: 14px;
            line-height: 1.6;
        }}
        .nav {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .nav button {{
            background: #3498db;
            color: white;
            border: none;
            padding: 8px 20px;
            margin: 0 5px;
            border-radius: 6px;
            font-size: 15px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .nav button:hover {{ background: #2980b9; }}
        .nav button:disabled {{ background: #bdc3c7; cursor: default; }}
        .nav .problem-counter {{
            display: inline-block;
            margin: 0 15px;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
            vertical-align: middle;
        }}
        .game-area {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }}
        .grid-container {{
            display: inline-block;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        table {{
            border-collapse: collapse;
        }}
        td {{
            width: 64px;
            height: 64px;
            text-align: center;
            vertical-align: middle;
            font-size: 22px;
            font-weight: bold;
            border: 2px solid #ddd;
        }}
        td.operator {{
            background: #3498db;
            color: white;
            font-size: 26px;
            border-color: #3498db;
        }}
        td.target-col {{
            background: #eaf2f8;
            color: #2c3e50;
            border-color: #bdd5ea;
        }}
        td.target-row {{
            background: #eaf2f8;
            color: #2c3e50;
            border-color: #bdd5ea;
        }}
        td.cell {{
            background: white;
            cursor: pointer;
            transition: all 0.15s;
            position: relative;
        }}
        td.cell:hover {{
            background: #ebf5fb;
            border-color: #3498db;
        }}
        td.cell.selected {{
            background: #d4effd;
            border-color: #3498db;
            box-shadow: inset 0 0 0 2px #3498db;
        }}
        td.cell.correct {{
            background: #d5f5e3;
            color: #27ae60;
        }}
        td.cell.incorrect {{
            background: #fadbd8;
            color: #e74c3c;
        }}
        td.black-cell {{
            background: #2c3e50;
            border-color: #2c3e50;
            cursor: default;
        }}
        .number-pad {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            justify-content: center;
            max-width: 350px;
        }}
        .number-pad button {{
            width: 50px;
            height: 50px;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid #ddd;
            border-radius: 10px;
            background: white;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .number-pad button:hover {{
            background: #3498db;
            color: white;
            border-color: #3498db;
        }}
        .number-pad button.clear-btn {{
            width: 70px;
            background: #e74c3c;
            color: white;
            border-color: #e74c3c;
        }}
        .number-pad button.clear-btn:hover {{
            background: #c0392b;
        }}
        .controls {{
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .controls button {{
            padding: 10px 24px;
            font-size: 15px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            color: white;
            transition: background 0.2s;
        }}
        .btn-check {{ background: #27ae60; }}
        .btn-check:hover {{ background: #219a52; }}
        .btn-reset {{ background: #e74c3c; }}
        .btn-reset:hover {{ background: #c0392b; }}
        .btn-hint {{ background: #f39c12; }}
        .btn-hint:hover {{ background: #e67e22; }}
        .btn-answer {{ background: #8e44ad; }}
        .btn-answer:hover {{ background: #7d3c98; }}
        .feedback {{
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            min-height: 30px;
            margin-top: 10px;
        }}
        .feedback.success {{ color: #27ae60; }}
        .feedback.error {{ color: #e74c3c; }}
        .feedback.hint {{ color: #f39c12; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="subtitle" id="problem-type"></div>
    <div class="instructions">
        <strong>＜ルール＞</strong><br>
        タテに足す（かける）と上の数字に、ヨコに足す（かける）と左の数字になるように、数字を入れましょう。<br>
        ただし、同じ行・同じ列に同じ数字を使ってはいけません。
    </div>

    <div class="nav">
        <button id="prev-btn" onclick="prevProblem()">◀ 前へ</button>
        <span class="problem-counter" id="counter">1 / 1</span>
        <button id="next-btn" onclick="nextProblem()">次へ ▶</button>
    </div>

    <div class="game-area">
        <div class="grid-container">
            <table id="grid-table"></table>
        </div>
        <div class="number-pad" id="number-pad"></div>
        <div class="controls">
            <button class="btn-check" onclick="checkAnswer()">チェック</button>
            <button class="btn-reset" onclick="resetProblem()">リセット</button>
            <button class="btn-hint" onclick="showHint()">ヒント</button>
            <button class="btn-answer" onclick="showAnswer()">こたえ</button>
        </div>
        <div class="feedback" id="feedback"></div>
    </div>

    <script>
    const problems = {problems_json};
    let currentIndex = 0;
    let selectedCell = null;
    let userAnswers = {{}};

    function init() {{
        buildNumberPad();
        loadProblem(0);
    }}

    function buildNumberPad() {{
        const pad = document.getElementById('number-pad');
        pad.innerHTML = '';
        for (let n = 1; n <= 9; n++) {{
            const btn = document.createElement('button');
            btn.textContent = n;
            btn.onclick = () => inputNumber(n);
            pad.appendChild(btn);
        }}
        const clearBtn = document.createElement('button');
        clearBtn.textContent = '消す';
        clearBtn.className = 'clear-btn';
        clearBtn.onclick = () => inputNumber(0);
        pad.appendChild(clearBtn);
    }}

    function loadProblem(index) {{
        currentIndex = index;
        selectedCell = null;
        const p = problems[index];
        const size = p.size;
        const op = p.type === 'addition' ? '+' : '×';
        const blackCells = (p.black_cells || []).map(bc => bc[0] + ',' + bc[1]);

        // 保存済み回答を復元、なければ空
        if (!userAnswers[index]) {{
            userAnswers[index] = {{}};
        }}

        document.getElementById('counter').textContent = (index + 1) + ' / ' + problems.length;
        document.getElementById('prev-btn').disabled = index === 0;
        document.getElementById('next-btn').disabled = index === problems.length - 1;

        const typeLabel = p.type === 'addition' ? 'たし算' : 'かけ算';
        document.getElementById('problem-type').textContent =
            '第' + (index + 1) + '問 (' + size + '×' + size + ' ' + typeLabel + ')';

        const table = document.getElementById('grid-table');
        table.innerHTML = '';

        // ヘッダー行（演算子 + 列目標値）
        const headerRow = document.createElement('tr');
        const opCell = document.createElement('td');
        opCell.className = 'operator';
        opCell.textContent = op;
        headerRow.appendChild(opCell);
        for (let j = 0; j < size; j++) {{
            const td = document.createElement('td');
            td.className = 'target-col';
            td.textContent = p.col_targets[j];
            headerRow.appendChild(td);
        }}
        table.appendChild(headerRow);

        // データ行
        for (let i = 0; i < size; i++) {{
            const tr = document.createElement('tr');
            // 行目標値
            const rowTarget = document.createElement('td');
            rowTarget.className = 'target-row';
            rowTarget.textContent = p.row_targets[i];
            tr.appendChild(rowTarget);

            for (let j = 0; j < size; j++) {{
                const td = document.createElement('td');
                const key = i + ',' + j;
                if (blackCells.includes(key)) {{
                    td.className = 'black-cell';
                }} else {{
                    td.className = 'cell';
                    td.dataset.row = i;
                    td.dataset.col = j;
                    td.onclick = function() {{ selectCell(this); }};
                    // 保存済み回答があれば表示
                    if (userAnswers[index][key]) {{
                        td.textContent = userAnswers[index][key];
                    }}
                }}
                tr.appendChild(td);
            }}
            table.appendChild(tr);
        }}

        document.getElementById('feedback').textContent = '';
        document.getElementById('feedback').className = 'feedback';
    }}

    function selectCell(td) {{
        if (selectedCell) {{
            selectedCell.classList.remove('selected');
        }}
        selectedCell = td;
        td.classList.add('selected');
    }}

    function inputNumber(n) {{
        if (!selectedCell) return;
        const row = selectedCell.dataset.row;
        const col = selectedCell.dataset.col;
        const key = row + ',' + col;

        if (n === 0) {{
            selectedCell.textContent = '';
            delete userAnswers[currentIndex][key];
        }} else {{
            selectedCell.textContent = n;
            userAnswers[currentIndex][key] = n;
        }}
        selectedCell.classList.remove('correct', 'incorrect');
    }}

    function checkAnswer() {{
        const p = problems[currentIndex];
        const size = p.size;
        const blackCells = (p.black_cells || []).map(bc => bc[0] + ',' + bc[1]);
        const cells = document.querySelectorAll('td.cell');

        // 全セル埋まっているか確認
        let allFilled = true;
        cells.forEach(c => {{
            if (!c.textContent) allFilled = false;
        }});
        if (!allFilled) {{
            showFeedback('すべてのマスに数字を入れてください。', 'error');
            return;
        }}

        // ユーザーのグリッドを取得
        const userGrid = Array.from({{length: size}}, () => Array(size).fill(0));
        cells.forEach(c => {{
            const r = parseInt(c.dataset.row);
            const col = parseInt(c.dataset.col);
            userGrid[r][col] = parseInt(c.textContent);
        }});

        let allCorrect = true;

        // 行チェック
        for (let i = 0; i < size; i++) {{
            let val = p.type === 'addition' ? 0 : 1;
            for (let j = 0; j < size; j++) {{
                if (blackCells.includes(i + ',' + j)) continue;
                if (p.type === 'addition') val += userGrid[i][j];
                else val *= userGrid[i][j];
            }}
            if (val !== p.row_targets[i]) allCorrect = false;
        }}

        // 列チェック
        for (let j = 0; j < size; j++) {{
            let val = p.type === 'addition' ? 0 : 1;
            for (let i = 0; i < size; i++) {{
                if (blackCells.includes(i + ',' + j)) continue;
                if (p.type === 'addition') val += userGrid[i][j];
                else val *= userGrid[i][j];
            }}
            if (val !== p.col_targets[j]) allCorrect = false;
        }}

        // 行内重複チェック
        for (let i = 0; i < size; i++) {{
            const vals = [];
            for (let j = 0; j < size; j++) {{
                if (!blackCells.includes(i + ',' + j)) vals.push(userGrid[i][j]);
            }}
            if (new Set(vals).size !== vals.length) allCorrect = false;
        }}

        // 列内重複チェック
        for (let j = 0; j < size; j++) {{
            const vals = [];
            for (let i = 0; i < size; i++) {{
                if (!blackCells.includes(i + ',' + j)) vals.push(userGrid[i][j]);
            }}
            if (new Set(vals).size !== vals.length) allCorrect = false;
        }}

        if (allCorrect) {{
            cells.forEach(c => c.classList.add('correct'));
            showFeedback('正解です！おめでとう！', 'success');
        }} else {{
            // 間違っているセルを表示
            cells.forEach(c => {{
                const r = parseInt(c.dataset.row);
                const col = parseInt(c.dataset.col);
                if (userGrid[r][col] === p.grid[r][col]) {{
                    c.classList.add('correct');
                }} else {{
                    c.classList.add('incorrect');
                }}
            }});
            showFeedback('まだ正しくないところがあります。もう一度考えてみましょう。', 'error');
        }}
    }}

    function resetProblem() {{
        userAnswers[currentIndex] = {{}};
        loadProblem(currentIndex);
    }}

    function showHint() {{
        const p = problems[currentIndex];
        const size = p.size;
        const blackCells = (p.black_cells || []).map(bc => bc[0] + ',' + bc[1]);

        // 空いているセルからランダムに1つヒントを出す
        const emptyCells = [];
        const cells = document.querySelectorAll('td.cell');
        cells.forEach(c => {{
            if (!c.textContent) emptyCells.push(c);
        }});

        if (emptyCells.length === 0) {{
            showFeedback('すべてのマスが埋まっています。', 'hint');
            return;
        }}

        const hintCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
        const r = parseInt(hintCell.dataset.row);
        const col = parseInt(hintCell.dataset.col);
        hintCell.textContent = p.grid[r][col];
        userAnswers[currentIndex][r + ',' + col] = p.grid[r][col];
        hintCell.classList.add('correct');
        showFeedback('ヒント：1つのマスを埋めました。', 'hint');
    }}

    function showAnswer() {{
        const p = problems[currentIndex];
        const cells = document.querySelectorAll('td.cell');
        cells.forEach(c => {{
            const r = parseInt(c.dataset.row);
            const col = parseInt(c.dataset.col);
            c.textContent = p.grid[r][col];
            c.classList.add('correct');
            userAnswers[currentIndex][r + ',' + col] = p.grid[r][col];
        }});
        showFeedback('こたえを表示しました。', 'hint');
    }}

    function showFeedback(msg, type) {{
        const fb = document.getElementById('feedback');
        fb.textContent = msg;
        fb.className = 'feedback ' + (type || '');
    }}

    function prevProblem() {{
        if (currentIndex > 0) loadProblem(currentIndex - 1);
    }}

    function nextProblem() {{
        if (currentIndex < problems.length - 1) loadProblem(currentIndex + 1);
    }}

    // キーボード入力対応
    document.addEventListener('keydown', function(e) {{
        if (e.key >= '1' && e.key <= '9') {{
            inputNumber(parseInt(e.key));
        }} else if (e.key === 'Backspace' || e.key === 'Delete') {{
            inputNumber(0);
        }} else if (e.key === 'ArrowLeft') {{
            prevProblem();
        }} else if (e.key === 'ArrowRight') {{
            nextProblem();
        }}
    }});

    init();
    </script>
</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(description='たてよこ算 問題生成・検証')
    parser.add_argument('--size', type=int, default=2, choices=[2, 3], help='グリッドサイズ (2 or 3)')
    parser.add_argument('--add', type=int, default=0, help='足し算の問題数')
    parser.add_argument('--mul', type=int, default=0, help='掛け算の問題数')
    parser.add_argument('--black', action='store_true', help='3×3で黒マスを含める')
    parser.add_argument('--output', '-o', type=str, default=None, help='出力HTMLファイル名')
    parser.add_argument('--verify', action='store_true', help='生成した問題を検証する')
    parser.add_argument('--seed', type=int, default=None, help='乱数シード')

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.add == 0 and args.mul == 0:
        print("エラー: --add または --mul で問題数を指定してください。")
        sys.exit(1)

    problems = []

    if args.size == 2:
        if args.add > 0:
            print(f"2×2 足し算 {args.add}問を生成中...")
            problems.extend(generate_addition_2x2(args.add))
        if args.mul > 0:
            print(f"2×2 掛け算 {args.mul}問を生成中...")
            problems.extend(generate_multiplication_2x2(args.mul))
    elif args.size == 3:
        if args.add > 0:
            print(f"3×3 足し算 {args.add}問を生成中...")
            problems.extend(generate_addition_3x3(args.add, with_black_cells=args.black))
        if args.mul > 0:
            print(f"3×3 掛け算 {args.mul}問を生成中...")
            problems.extend(generate_multiplication_3x3(args.mul, with_black_cells=args.black))

    print(f"\n合計 {len(problems)}問 生成完了")

    # 検証
    print("\n--- 検証結果 ---")
    all_ok = verify_all(problems)
    if all_ok:
        print("\n✓ 全問題の検証に成功しました。")
    else:
        print("\n✗ 一部の問題に問題があります。")
        sys.exit(1)

    # HTML出力
    if args.output:
        title = f"たてよこ算 ({args.size}×{args.size})"
        html = generate_html(problems, title)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"\nHTMLファイルを出力しました: {args.output}")


if __name__ == "__main__":
    main()
