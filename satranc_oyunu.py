import tkinter as tk
import random

class Chess:
    def __init__(self, root):
        self.root = root
        self.root.title("Basit Satranç")
        self.cell_size = 60
        self.rows, self.cols = 8, 8
        self.canvas = tk.Canvas(root, width=self.cols*self.cell_size, height=self.rows*self.cell_size)
        self.canvas.pack()

        self.colors = ["#F0D9B5", "#B58863"]
        self.pieces_unicode = {
            "wp": "♙", "wr": "♖", "wn": "♘", "wb": "♗", "wq": "♕", "wk": "♔",
            "bp": "♟", "br": "♜", "bn": "♞", "bb": "♝", "bq": "♛", "bk": "♚"
        }
        self.board = [[None]*self.cols for _ in range(self.rows)]
        self.piece_ids = [[None]*self.cols for _ in range(self.rows)]

        self.selected = None
        self.turn = "w"  # Başlangıç beyazın sırası

        self.init_board()
        self.draw_board()
        self.draw_pieces()

        self.canvas.bind("<Button-1>", self.click)

    def init_board(self):
        self.board[0] = ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"]
        self.board[1] = ["bp"]*8
        for r in range(2,6):
            self.board[r] = [None]*8
        self.board[6] = ["wp"]*8
        self.board[7] = ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]

    def draw_board(self):
        self.canvas.delete("square")
        for r in range(self.rows):
            for c in range(self.cols):
                color = self.colors[(r+c)%2]
                x1 = c*self.cell_size
                y1 = r*self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags="square")
        if self.selected:
            r, c = self.selected
            x1 = c*self.cell_size
            y1 = r*self.cell_size
            x2 = x1 + self.cell_size
            y2 = y1 + self.cell_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=3, tags="highlight")

    def draw_pieces(self):
        self.canvas.delete("piece")
        for r in range(self.rows):
            for c in range(self.cols):
                piece = self.board[r][c]
                if piece:
                    x = c*self.cell_size + self.cell_size//2
                    y = r*self.cell_size + self.cell_size//2
                    color = "white" if piece[0] == "w" else "black"
                    self.piece_ids[r][c] = self.canvas.create_text(x, y, text=self.pieces_unicode[piece],
                        font=("Arial", 36), fill=color, tags=("piece", piece))
                else:
                    self.piece_ids[r][c] = None

    def click(self, event):
        if self.turn != "w":
            # Sadece beyazın sırası olduğunda işlem yap
            return

        col = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.selected is None:
            if self.board[row][col] and self.board[row][col][0] == "w":
                self.selected = (row, col)
                self.draw_board()
        else:
            from_r, from_c = self.selected
            if self.is_valid_move(from_r, from_c, row, col):
                self.move_piece(from_r, from_c, row, col)
                self.turn = "b"  # Sıra bilgisayara geçer
                self.selected = None
                self.draw_board()
                self.draw_pieces()
                self.root.after(500, self.computer_move)  # 0.5 saniye sonra bilgisayar oynasın
            else:
                self.selected = None
                self.draw_board()

    def is_valid_move(self, from_r, from_c, to_r, to_c):
        piece = self.board[from_r][from_c]
        if not piece:
            return False
        target = self.board[to_r][to_c]
        if target and target[0] == piece[0]:
            return False

        dr = to_r - from_r
        dc = to_c - from_c
        ptype = piece[1]

        if ptype == "p":
            direction = -1 if piece[0] == "w" else 1
            start_row = 6 if piece[0] == "w" else 1
            if dc == 0 and dr == direction and target is None:
                return True
            if dc == 0 and dr == 2*direction and from_r == start_row and target is None and self.board[from_r+direction][from_c] is None:
                return True
            if abs(dc) == 1 and dr == direction and target is not None and target[0] != piece[0]:
                return True
            return False

        elif ptype == "r":
            if dr == 0 or dc == 0:
                return self.clear_path(from_r, from_c, to_r, to_c)
            return False

        elif ptype == "n":
            if (abs(dr), abs(dc)) in [(2,1),(1,2)]:
                return True
            return False

        elif ptype == "b":
            if abs(dr) == abs(dc):
                return self.clear_path(from_r, from_c, to_r, to_c)
            return False

        elif ptype == "q":
            if dr == 0 or dc == 0 or abs(dr) == abs(dc):
                return self.clear_path(from_r, from_c, to_r, to_c)
            return False

        elif ptype == "k":
            if max(abs(dr), abs(dc)) == 1:
                return True
            return False

        return False

    def clear_path(self, from_r, from_c, to_r, to_c):
        dr = to_r - from_r
        dc = to_c - from_c
        step_r = (dr > 0) - (dr < 0)
        step_c = (dc > 0) - (dc < 0)
        r, c = from_r + step_r, from_c + step_c
        while (r, c) != (to_r, to_c):
            if self.board[r][c] is not None:
                return False
            r += step_r
            c += step_c
        return True

    def move_piece(self, from_r, from_c, to_r, to_c):
        self.board[to_r][to_c] = self.board[from_r][from_c]
        self.board[from_r][from_c] = None

    def computer_move(self):
        # Basit: tüm siyah taşlar için geçerli hamleleri bul ve rastgele birini yap
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                piece = self.board[r][c]
                if piece and piece[0] == "b":
                    for tr in range(self.rows):
                        for tc in range(self.cols):
                            if self.is_valid_move(r, c, tr, tc):
                                moves.append((r, c, tr, tc))

        if moves:
            from_r, from_c, to_r, to_c = random.choice(moves)
            self.move_piece(from_r, from_c, to_r, to_c)

        self.turn = "w"  # Sıra tekrar kullanıcıya geçer
        self.draw_board()
        self.draw_pieces()


if __name__ == "__main__":
    root = tk.Tk()
    game = Chess(root)
    root.mainloop()
