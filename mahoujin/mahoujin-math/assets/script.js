// 魔方陣パズルのJavaScript

class MagicSquarePuzzle {
    constructor() {
        this.size = 3;
        this.targetSum = 15;
        this.numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9];
        this.draggedElement = null;

        this.init();
        this.setupEventListeners();
    }

    init() {
        this.createGrid();
        this.createNumberPool();
        this.updateTargetSum();
    }

    createGrid() {
        const grid = document.getElementById('magic-square');
        grid.innerHTML = '';

        for (let i = 0; i < this.size * this.size; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.index = i;
            cell.addEventListener('dragover', this.handleDragOver.bind(this));
            cell.addEventListener('drop', this.handleDrop.bind(this));
            grid.appendChild(cell);
        }
    }

    createNumberPool() {
        const pool = document.getElementById('number-pool');
        pool.innerHTML = '';

        // シャッフルした数字をプールに追加
        const shuffledNumbers = [...this.numbers].sort(() => Math.random() - 0.5);

        shuffledNumbers.forEach(num => {
            const numberItem = document.createElement('div');
            numberItem.className = 'number-item';
            numberItem.textContent = num;
            numberItem.draggable = true;
            numberItem.addEventListener('dragstart', this.handleDragStart.bind(this));
            pool.appendChild(numberItem);
        });
    }

    setupEventListeners() {
        document.getElementById('check-btn').addEventListener('click', () => this.checkSolution());
        document.getElementById('reset-btn').addEventListener('click', () => this.reset());
        document.getElementById('hint-btn').addEventListener('click', () => this.showHint());
    }

    handleDragStart(e) {
        this.draggedElement = e.target;
        e.dataTransfer.effectAllowed = 'move';
        e.target.style.opacity = '0.5';
    }

    handleDragOver(e) {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        e.target.classList.add('dragged-over');
    }

    handleDrop(e) {
        e.preventDefault();
        e.target.classList.remove('dragged-over');

        if (this.draggedElement && e.target.classList.contains('cell')) {
            // セルに数字をドロップ
            if (e.target.textContent) {
                // セルに既に数字がある場合は交換
                const temp = e.target.textContent;
                e.target.textContent = this.draggedElement.textContent;
                this.draggedElement.textContent = temp;
            } else {
                // 空のセルに数字を配置
                e.target.textContent = this.draggedElement.textContent;
                this.draggedElement.remove();
            }
        }

        this.draggedElement.style.opacity = '1';
        this.draggedElement = null;
    }

    checkSolution() {
        const cells = document.querySelectorAll('.cell');
        const grid = [];

        // グリッドの値を取得
        for (let i = 0; i < this.size; i++) {
            const row = [];
            for (let j = 0; j < this.size; j++) {
                const value = parseInt(cells[i * this.size + j].textContent);
                if (isNaN(value)) {
                    this.showFeedback('全てのマスに数字を配置してください。', 'error');
                    return;
                }
                row.push(value);
            }
            grid.push(row);
        }

        // 行の合計をチェック
        for (let i = 0; i < this.size; i++) {
            const rowSum = grid[i].reduce((a, b) => a + b, 0);
            if (rowSum !== this.targetSum) {
                this.showFeedback(`行 ${i + 1} の合計が ${this.targetSum} ではありません。`, 'error');
                return;
            }
        }

        // 列の合計をチェック
        for (let j = 0; j < this.size; j++) {
            const colSum = grid.reduce((sum, row) => sum + row[j], 0);
            if (colSum !== this.targetSum) {
                this.showFeedback(`列 ${j + 1} の合計が ${this.targetSum} ではありません。`, 'error');
                return;
            }
        }

        // 対角線の合計をチェック
        let diagonal1 = 0, diagonal2 = 0;
        for (let i = 0; i < this.size; i++) {
            diagonal1 += grid[i][i];
            diagonal2 += grid[i][this.size - 1 - i];
        }

        if (diagonal1 !== this.targetSum || diagonal2 !== this.targetSum) {
            this.showFeedback('対角線の合計が正しくありません。', 'error');
            return;
        }

        this.showFeedback('おめでとうございます！魔方陣を完成させました！', 'success');
    }

    reset() {
        const cells = document.querySelectorAll('.cell');
        cells.forEach(cell => cell.textContent = '');
        this.createNumberPool();
        this.showFeedback('');
    }

    showHint() {
        const hints = [
            '各行の合計が15になるように数字を配置しましょう。',
            '各列の合計も15です。',
            '左上から右下への対角線と、右上から左下への対角線の合計も15です。',
            '真ん中のマスには5を置くと良いでしょう。',
            '対称性を考えて配置してみましょう。'
        ];

        const randomHint = hints[Math.floor(Math.random() * hints.length)];
        this.showFeedback(randomHint, 'hint');
    }

    showFeedback(message, type = '') {
        const feedback = document.getElementById('feedback');
        feedback.textContent = message;
        feedback.className = `feedback ${type}`;
    }

    updateTargetSum() {
        document.getElementById('target-sum').textContent = this.targetSum;
    }
}

// ページ読み込み時にパズルを初期化
document.addEventListener('DOMContentLoaded', () => {
    new MagicSquarePuzzle();
});