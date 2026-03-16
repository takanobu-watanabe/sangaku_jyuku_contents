#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
魔方陣生成スクリプト
指定されたサイズの魔方陣を生成し、HTML形式で出力します。
"""

import sys
import argparse

def generate_magic_square(n):
    """
    n x n の魔方陣を生成します。
    奇数サイズのみ対応。
    """
    if n % 2 == 0:
        raise ValueError("偶数サイズの魔方陣は未対応です。奇数サイズを指定してください。")

    magic_square = [[0] * n for _ in range(n)]

    # 初期位置
    i = n // 2
    j = n - 1

    num = 1
    while num <= n * n:
        if i == -1 and j == n:  # 境界を超えた場合
            j = n - 2
            i = 0
        else:
            if j == n:
                j = 0
            if i < 0:
                i = n - 1

        if magic_square[i][j] != 0:  # 既に数字がある場合
            j = j - 2
            i = i + 1
            continue
        else:
            magic_square[i][j] = num
            num += 1

        j += 1
        i -= 1

    return magic_square

def generate_html(magic_square, n):
    """
    魔方陣をHTML形式で出力します。
    """
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>魔方陣 {n}x{n}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 20px;
        }}
        .magic-square {{
            display: grid;
            grid-template-columns: repeat({n}, 50px);
            gap: 5px;
            margin: 20px auto;
            width: fit-content;
        }}
        .cell {{
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid #000;
            background-color: #f0f0f0;
        }}
        .sum {{
            margin: 10px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>魔方陣 {n}x{n}</h1>
    <div class="magic-square">
"""

    for row in magic_square:
        for num in row:
            html += f'        <div class="cell">{num}</div>\n'

    html += "    </div>\n"

    # 合計の計算
    total_sum = n * (n * n + 1) // 2
    html += f'    <div class="sum">各行・列・対角線の合計: {total_sum}</div>\n'

    html += """</body>
</html>"""

    return html

def main():
    parser = argparse.ArgumentParser(description='魔方陣を生成し、HTMLファイルとして出力します。')
    parser.add_argument('size', type=int, help='魔方陣のサイズ（奇数）')
    parser.add_argument('--output', '-o', default='magic_square.html', help='出力ファイル名')

    args = parser.parse_args()

    try:
        magic_square = generate_magic_square(args.size)
        html_content = generate_html(magic_square, args.size)

        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"魔方陣 {args.size}x{args.size} を {args.output} に生成しました。")

    except ValueError as e:
        print(f"エラー: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
