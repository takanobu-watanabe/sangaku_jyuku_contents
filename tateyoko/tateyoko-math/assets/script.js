// たてよこ算パズルのJavaScript
// problems 配列はHTMLに埋め込まれるか、外部から読み込む

let currentIndex = 0;
let selectedCell = null;
let userAnswers = {};

function init() {
    buildNumberPad();
    loadProblem(0);
}

function buildNumberPad() {
    const pad = document.getElementById('number-pad');
    pad.innerHTML = '';
    for (let n = 1; n <= 9; n++) {
        const btn = document.createElement('button');
        btn.textContent = n;
        btn.onclick = () => inputNumber(n);
        pad.appendChild(btn);
    }
    const clearBtn = document.createElement('button');
    clearBtn.textContent = '消す';
    clearBtn.className = 'clear-btn';
    clearBtn.onclick = () => inputNumber(0);
    pad.appendChild(clearBtn);
}

function loadProblem(index) {
    currentIndex = index;
    selectedCell = null;
    const p = problems[index];
    const size = p.size;
    const op = p.type === 'addition' ? '+' : '×';
    const blackCells = (p.black_cells || []).map(bc => bc[0] + ',' + bc[1]);

    if (!userAnswers[index]) {
        userAnswers[index] = {};
    }

    document.getElementById('counter').textContent = (index + 1) + ' / ' + problems.length;
    document.getElementById('prev-btn').disabled = index === 0;
    document.getElementById('next-btn').disabled = index === problems.length - 1;

    const typeLabel = p.type === 'addition' ? 'たし算' : 'かけ算';
    document.getElementById('problem-type').textContent =
        '第' + (index + 1) + '問 (' + size + '×' + size + ' ' + typeLabel + ')';

    const table = document.getElementById('grid-table');
    table.innerHTML = '';

    // ヘッダー行
    const headerRow = document.createElement('tr');
    const opCell = document.createElement('td');
    opCell.className = 'operator';
    opCell.textContent = op;
    headerRow.appendChild(opCell);
    for (let j = 0; j < size; j++) {
        const td = document.createElement('td');
        td.className = 'target-col';
        td.textContent = p.col_targets[j];
        headerRow.appendChild(td);
    }
    table.appendChild(headerRow);

    // データ行
    for (let i = 0; i < size; i++) {
        const tr = document.createElement('tr');
        const rowTarget = document.createElement('td');
        rowTarget.className = 'target-row';
        rowTarget.textContent = p.row_targets[i];
        tr.appendChild(rowTarget);

        for (let j = 0; j < size; j++) {
            const td = document.createElement('td');
            const key = i + ',' + j;
            if (blackCells.includes(key)) {
                td.className = 'black-cell';
            } else {
                td.className = 'cell';
                td.dataset.row = i;
                td.dataset.col = j;
                td.onclick = function() { selectCell(this); };
                if (userAnswers[index][key]) {
                    td.textContent = userAnswers[index][key];
                }
            }
            tr.appendChild(td);
        }
        table.appendChild(tr);
    }

    document.getElementById('feedback').textContent = '';
    document.getElementById('feedback').className = 'feedback';
}

function selectCell(td) {
    if (selectedCell) {
        selectedCell.classList.remove('selected');
    }
    selectedCell = td;
    td.classList.add('selected');
}

function inputNumber(n) {
    if (!selectedCell) return;
    const key = selectedCell.dataset.row + ',' + selectedCell.dataset.col;
    if (n === 0) {
        selectedCell.textContent = '';
        delete userAnswers[currentIndex][key];
    } else {
        selectedCell.textContent = n;
        userAnswers[currentIndex][key] = n;
    }
    selectedCell.classList.remove('correct', 'incorrect');
}

function checkAnswer() {
    const p = problems[currentIndex];
    const size = p.size;
    const blackCells = (p.black_cells || []).map(bc => bc[0] + ',' + bc[1]);
    const cells = document.querySelectorAll('td.cell');

    let allFilled = true;
    cells.forEach(c => { if (!c.textContent) allFilled = false; });
    if (!allFilled) {
        showFeedback('すべてのマスに数字を入れてください。', 'error');
        return;
    }

    const userGrid = Array.from({length: size}, () => Array(size).fill(0));
    cells.forEach(c => {
        userGrid[parseInt(c.dataset.row)][parseInt(c.dataset.col)] = parseInt(c.textContent);
    });

    let allCorrect = true;

    for (let i = 0; i < size; i++) {
        let val = p.type === 'addition' ? 0 : 1;
        for (let j = 0; j < size; j++) {
            if (blackCells.includes(i + ',' + j)) continue;
            if (p.type === 'addition') val += userGrid[i][j];
            else val *= userGrid[i][j];
        }
        if (val !== p.row_targets[i]) allCorrect = false;
    }

    for (let j = 0; j < size; j++) {
        let val = p.type === 'addition' ? 0 : 1;
        for (let i = 0; i < size; i++) {
            if (blackCells.includes(i + ',' + j)) continue;
            if (p.type === 'addition') val += userGrid[i][j];
            else val *= userGrid[i][j];
        }
        if (val !== p.col_targets[j]) allCorrect = false;
    }

    for (let i = 0; i < size; i++) {
        const vals = [];
        for (let j = 0; j < size; j++) {
            if (!blackCells.includes(i + ',' + j)) vals.push(userGrid[i][j]);
        }
        if (new Set(vals).size !== vals.length) allCorrect = false;
    }

    for (let j = 0; j < size; j++) {
        const vals = [];
        for (let i = 0; i < size; i++) {
            if (!blackCells.includes(i + ',' + j)) vals.push(userGrid[i][j]);
        }
        if (new Set(vals).size !== vals.length) allCorrect = false;
    }

    if (allCorrect) {
        cells.forEach(c => c.classList.add('correct'));
        showFeedback('正解です！おめでとう！', 'success');
    } else {
        cells.forEach(c => {
            const r = parseInt(c.dataset.row);
            const col = parseInt(c.dataset.col);
            if (userGrid[r][col] === p.grid[r][col]) {
                c.classList.add('correct');
            } else {
                c.classList.add('incorrect');
            }
        });
        showFeedback('まだ正しくないところがあります。もう一度考えてみましょう。', 'error');
    }
}

function resetProblem() {
    userAnswers[currentIndex] = {};
    loadProblem(currentIndex);
}

function showHint() {
    const p = problems[currentIndex];
    const emptyCells = [];
    document.querySelectorAll('td.cell').forEach(c => {
        if (!c.textContent) emptyCells.push(c);
    });

    if (emptyCells.length === 0) {
        showFeedback('すべてのマスが埋まっています。', 'hint');
        return;
    }

    const hintCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
    const r = parseInt(hintCell.dataset.row);
    const col = parseInt(hintCell.dataset.col);
    hintCell.textContent = p.grid[r][col];
    userAnswers[currentIndex][r + ',' + col] = p.grid[r][col];
    hintCell.classList.add('correct');
    showFeedback('ヒント：1つのマスを埋めました。', 'hint');
}

function showAnswer() {
    const p = problems[currentIndex];
    document.querySelectorAll('td.cell').forEach(c => {
        const r = parseInt(c.dataset.row);
        const col = parseInt(c.dataset.col);
        c.textContent = p.grid[r][col];
        c.classList.add('correct');
        userAnswers[currentIndex][r + ',' + col] = p.grid[r][col];
    });
    showFeedback('こたえを表示しました。', 'hint');
}

function showFeedback(msg, type) {
    const fb = document.getElementById('feedback');
    fb.textContent = msg;
    fb.className = 'feedback ' + (type || '');
}

function prevProblem() {
    if (currentIndex > 0) loadProblem(currentIndex - 1);
}

function nextProblem() {
    if (currentIndex < problems.length - 1) loadProblem(currentIndex + 1);
}

document.addEventListener('keydown', function(e) {
    if (e.key >= '1' && e.key <= '9') inputNumber(parseInt(e.key));
    else if (e.key === 'Backspace' || e.key === 'Delete') inputNumber(0);
    else if (e.key === 'ArrowLeft') prevProblem();
    else if (e.key === 'ArrowRight') nextProblem();
});

document.addEventListener('DOMContentLoaded', init);
