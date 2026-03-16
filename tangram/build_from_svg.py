#!/usr/bin/env python3
"""KiloGram SVGから10問のパズルデータを生成（SVG座標をそのまま使用）"""
import xml.etree.ElementTree as ET
import os, json, math, random
from shapely.geometry import Polygon
from shapely.ops import unary_union

SVG_DIR = "/Users/watanabetakanobu/sangaku_contents/tangram/kilogram/dataset/tangrams-svg"

def parse_svg(filepath):
    tree = ET.parse(filepath)
    pieces = []
    for elem in tree.iter():
        if 'polygon' in elem.tag.lower():
            pts_str = elem.get('points', '')
            pts = []
            for pair in pts_str.split():
                x, y = pair.split(',')
                pts.append([float(x), float(y)])
            if pts:
                pieces.append(pts)
    return pieces

def normalize(pieces, target_size=8):
    """全ピースを target_size × target_size の範囲に正規化"""
    all_pts = [p for piece in pieces for p in piece]
    minx = min(p[0] for p in all_pts)
    miny = min(p[1] for p in all_pts)
    maxx = max(p[0] for p in all_pts)
    maxy = max(p[1] for p in all_pts)
    w, h = maxx - minx, maxy - miny
    scale = target_size / max(w, h)
    # 中央寄せ
    offx = (target_size - w * scale) / 2
    offy = (target_size - h * scale) / 2
    result = []
    for piece in pieces:
        result.append([[round((p[0]-minx)*scale+offx, 2), round((p[1]-miny)*scale+offy, 2)] for p in piece])
    return result

def classify_piece(pts):
    """頂点数と面積からピースタイプを推定"""
    poly = Polygon(pts)
    area = poly.area
    n = len(pts)
    return n, round(area, 2)

# 全SVGスキャン
svgs = sorted([f for f in os.listdir(SVG_DIR) if f.endswith('.svg')])
candidates = []

for fname in svgs:
    try:
        pieces = parse_svg(os.path.join(SVG_DIR, fname))
        if len(pieces) != 7: continue
        polys = [Polygon(pts) for pts in pieces]
        if not all(p.is_valid and p.area > 0 for p in polys): continue
        union = unary_union(polys)
        if union.geom_type != 'Polygon': continue
        
        sil = list(union.exterior.coords)[:-1]
        n_verts = len(sil)
        minx,miny,maxx,maxy = union.bounds
        w, h = maxx-minx, maxy-miny
        aspect = round(min(w,h)/max(w,h), 2) if max(w,h)>0 else 1
        compact = round(union.area/(w*h), 2) if w*h>0 else 1
        
        # 重なりチェック
        max_ov = 0
        for i in range(7):
            for j in range(i+1,7):
                ov = polys[i].intersection(polys[j]).area
                if ov > max_ov: max_ov = ov
        if max_ov > union.area * 0.001: continue
        
        candidates.append({
            'file': fname, 'pieces': pieces, 'n_verts': n_verts,
            'aspect': aspect, 'compact': compact,
        })
    except:
        continue

print(f"有効候補: {len(candidates)}個")

# 多様な10問を選ぶ
random.seed(123)
random.shuffle(candidates)
selected = []
sigs = set()

# まず異なるコンパクトさ・アスペクト比の組み合わせを優先
for c in candidates:
    sig = (c['n_verts']//4, int(c['aspect']*5), int(c['compact']*5))
    if sig in sigs: continue
    sigs.add(sig)
    selected.append(c)
    if len(selected) >= 10: break

print(f"選択: {len(selected)}問")

# PUZZLES配列を生成
titles = ["かいじゅう","ねこ","とり","ふね","いえ",
          "さかな","ロケット","ひこうき","にんげん","ふしぎなかたち"]
diffs = [1,1,2,2,3,3,4,4,5,5]
hints_map = {0:[0,1,2],1:[0,1,2],2:[0,1],3:[0,1],4:[0],5:[0],6:[],7:[],8:[],9:[]}
hint_texts = ["大きい三角形から置こう","しっぽに注目","つばさの形をよく見よう",
              "船底から作ろう","屋根を先に置こう","ヒレの形がポイント",
              "先端から組み立てよう","翼を広げて考えよう","頭から作ってみよう",
              "全力チャレンジ！"]

js = "const PUZZLES = [\n"
for i, c in enumerate(selected):
    pieces = normalize(c['pieces'])
    polys = [Polygon(pts) for pts in pieces]
    union = unary_union(polys)
    if union.geom_type == 'MultiPolygon':
        union = max(union.geoms, key=lambda g: g.area)
    if union.geom_type != 'Polygon':
        print(f"  Q{i+1}: skip (not Polygon)")
        continue
    sil = [[round(x,2), round(y,2)] for x,y in union.exterior.coords[:-1]]
    
    pid = f"Q{i+1}"
    d = diffs[i]
    title = titles[i]
    hints = json.dumps(hints_map.get(i,[]))
    hint = hint_texts[i]
    
    # ピースデータ: 直接頂点座標で定義
    pieces_js = json.dumps(pieces)
    sil_js = json.dumps([sil])
    
    js += f'  {{ id:"{pid}", difficulty:{d}, title:"{title}",\n'
    js += f'    file:"{c["file"]}",\n'
    js += f'    silhouette:{sil_js},\n'
    js += f'    pieces:{pieces_js},\n'
    js += f'    hints:{hints},\n'
    js += f'    hint:"{hint}" }},\n'
    
    print(f"  Q{i+1} ({c['file']}): {c['n_verts']}verts asp={c['aspect']} comp={c['compact']} area={union.area:.1f}")

js += "];"

with open("/Users/watanabetakanobu/sangaku_contents/tangram/svg_puzzles.js", "w") as f:
    f.write(js)

print(f"\n出力: svg_puzzles.js")
