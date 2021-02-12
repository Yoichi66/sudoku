from __future__ import annotations
from pprint import pformat
from typing import List, Set, Tuple
import tkinter as tk
import numpy as np

ROWS = COLS = 9
NUMBERS = [x for x in range(1, 9 + 1)]

def main():
    def get_input():
        grid_num = [[], [], [], [], [], [], [], [], []]
        num = 0
        for i in range(81):
            #c_num = num // 9
            r_num = num % 9
            grid_num[r_num].append(int(entries[i].get()))
            num += 1

        grid = Grid(list(grid_num))
        print('---Question---')
        print(Grid(grid_num))

        results = solve_all(grid)
        for r in results:
            print('---Answer---')
            print(r)

    def make_format():
        num = 0
        entries = []
        for i in range(81):
            c_num = num // 9
            r_num = num % 9
            if (c_num == 0 or c_num == 1 or c_num == 2) and (0 <= r_num <= 2 or 6 <= r_num <= 8):
                clr = 'yellow'
            elif (c_num == 3 or c_num == 4 or c_num == 5) and (3 <= r_num <= 5):
                clr = 'yellow'
            elif (c_num == 6 or c_num == 7 or c_num == 8) and (0 <= r_num <= 2 or 6 <= r_num <= 8):
                clr = 'yellow'
            else:
                clr = 'white'

            entry_num = tk.Entry(width=8, bg=clr)
            entry_num.grid(column=c_num, row=r_num)
            entry_num.insert(tk.END, 0)  # 最初から文字を入れておく
            entries.append(entry_num)
            num += 1
        return entries

    # メインウィンドウ作成
    app = tk.Tk()
    app.title("sudoku")
    app.geometry("470x200")
    make_format()
    entries = make_format()
    button = tk.Button(master=app, text="Enter",  # 初期値
        width=6,  # 幅,
        bg="lightblue",  # 色
        command=get_input  # クリックに実行する関数
    )

    button.grid(column=4, row=9, sticky='e')
    # メインループ
    app.mainloop()


class Grid:
    """数独のクイズを表すグリッド"""

    _values: List[List[int]]

    def __init__(self, values: List[List[int]]):
        assert isinstance(values, list)
        assert len(values) == ROWS
        for row in values:
            assert isinstance(row, list)
            assert len(row) == COLS

        self._values = values

    def __hash__(self):
        """hashable 化するための __hash__ 定義

        - set() で利用するため
        """
        return hash(''.join(str(x) for row in self._values for x in row))

    def __str__(self):
        """`print()` で出力されたときの表現を定義する"""
        return '{}(\n{}\n)'.format(type(self).__name__, pformat(self._values))

    def solved(self) -> bool:
        """空セルがなくなったかどうかを判定する"""
        all_values = [x for row in self._values for x in row]
        return 0 not in all_values

    def possible_numbers(self) -> List[Tuple[int, int, List[int]]]:
        """すべての空セルと入りうる数字の組み合わせを全件洗い出す"""
        return [
            (row, col, self._possible_numbers_for_cell(row, col))
            for row, values in enumerate(self._values)
            for col, x in enumerate(values)
            if x == 0
        ]

    def clone_filled(self, row, col, number) -> Grid:
        """特定のセルに指定された値が入った新しい grid を返す"""
        values = [[x for x in row] for row in self._values]
        values[row][col] = number
        return type(self)(values)

    def _possible_numbers_for_cell(self, row, col) -> List[int]:
        row_numbers = [x for x in self._values[row]]
        col_numbers = [row[col] for row in self._values]
        block_numbers = self._block_numbers(row, col)

        return [
            x
            for x in NUMBERS
            if (x not in row_numbers)
            and (x not in col_numbers)
            and (x not in block_numbers)
        ]

    def _block_numbers(self, row, col) -> List[int]:
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        return [
            x
            for row in self._values[row_start : row_start + 3]
            for x in row[col_start : col_start + 3]
        ]

def solve_all(grid: Grid) -> Set[Grid]:
    """指定された数独に対する解を全件返す"""
    solutions = set()

    def _solve(grid: Grid):
        # S4. 空のセルがなくなったら正解として追加
        if grid.solved():
            solutions.add(grid)
            return

        # S1. すべてのセルに対して入りうる数字をリストアップする
        possible_numbers = grid.possible_numbers()

        # S2 + S3. 入りうち数字が最も少ないセルに仮に数字を入れて再帰
        row, col, numbers = min(possible_numbers, key=lambda x: len(x[-1]))

        # S5. 入りうる数字がひとつも無い空のセルがある場合はそのルートは間違いなので終了
        if not numbers:
            return

        for number in numbers:
            next_grid = grid.clone_filled(row, col, number)
            _solve(next_grid)

    _solve(grid)

    return solutions

# tk.Frameを継承したApplicationクラスを作成
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # ウィンドウの設定
        self.master.title("sudoku")

        # 実行内容
        self.pack()
        self.create_widget1()

    # create_widget1メソッドを定義
    def create_widget1(self):

        # label1ウィジェット
        self.label1 = tk.Label(self, text="数独の問題を入力してください", padx=50)
        self.label1.pack(padx=5, pady=5)

        items = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

        # button1が押された時に実行されるfetchメソッドを定義
        def fetch(entries):  # entriesリストの要素は(項目名, entryウィジェット)のタプルとなっている
            for entry in entries:  # ループ開始
                item = entry[0]  # 項目名を取得
                text = entry[1].get()  # entryウィジェットの入力値を取得
                print('{}: "{}"'.format(item, text))  # 値をフォーマットして出力

        # 各項目のlabelとentry
        def makeform(self, items):  # 処理を呼び出せるようmakeform関数としてまとめる
            entries = []  # entriesリストを定義
            num = 0
            for i in range(9):
                c_num = num // 9
                r_num = num % 9
                cf_num = r_num // 3
                rf_num = r_num % 3
                row = tk.Frame(self)
                #label = tk.Label(row, text=item)
                entry = tk.Entry(row)
                row.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5) # tk.TOP side=tk.LEFT,
                #label.grid(column=0, row=0)
                entry.grid(column=cf_num, row=rf_num)
                #entries.append((item, entry))  # 項目名と生成したentryウィジェットのタプルを1つの要素としてentriesリストに追加
                num += 1

            return entries  # entriesリストを返り値として返す

        ents = makeform(self, items)  # ents変数を定義してmakeform関数を代入

        self.button1 = tk.Button(self, text="確認", command=(lambda e=ents: fetch(e)))  # ボタンが押されるとmakeform関数を実行してその返り値を使ってfetch関数を実行
        self.button2 = tk.Button(self, text="終了", command=root.quit)
        self.button1.pack(side=tk.LEFT, padx=5, pady=5)
        self.button2.pack(side=tk.LEFT, padx=5, pady=5)

if __name__ == '__main__':
    #make_format()
    #root = tk.Tk()
    #app = Application(master=root)
    #app.mainloop()
    main()