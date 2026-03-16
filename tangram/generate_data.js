const fs = require('fs');
const path = require('path');

const codeDir = path.join(__dirname, 'TangramGenerator/Code');
const files = ['helpers.js','intadjoinsqrt2.js','point.js','lineSegement.js',
               'directions.js','tan.js','evaluation.js','tangram.js'];

for (const f of files) {
  eval(fs.readFileSync(path.join(codeDir, f), 'utf-8'));
}

const genCode = fs.readFileSync(path.join(codeDir, 'generator.js'), 'utf-8');
eval(genCode.replace(/importScripts\(.*?\);/, ''));

const results = [];
for (let i = 0; i < 200 && results.length < 20; i++) {
  try {
    const t = generateTangram();
    if (!t) continue;
    const outline = computeOutline(t.tans, true);
    if (!outline || outline.length === 0) continue;

    const silParts = outline.map(part =>
      part.map(p => [Math.round(p.toFloatX()*100)/100, Math.round(p.toFloatY()*100)/100])
    );
    const piecesData = t.tans.map(tan => {
      const pts = tan.getPoints();
      return pts.map(p => [Math.round(p.toFloatX()*100)/100, Math.round(p.toFloatY()*100)/100]);
    });
    const score = evaluateTangram(t);

    results.push({ silhouette: silParts, pieces: piecesData, score: Math.round(score*100)/100 });
    process.stdout.write(`${results.length} `);
  } catch(e) {}
}

results.sort((a, b) => b.score - a.score);
fs.writeFileSync(path.join(__dirname, 'generated_tangrams.json'), JSON.stringify(results, null, 2));
console.log(`\n${results.length}個生成 → generated_tangrams.json`);
