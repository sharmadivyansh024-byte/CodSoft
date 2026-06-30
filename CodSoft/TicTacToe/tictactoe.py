import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Tic Tac Toe AI")
root.geometry("320x380")
root.resizable(False, False)

board = [""] * 9
buttons = []
game_over = False

win_patterns = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]

status = tk.Label(root, text="Your Turn (X)", font=("Arial", 14))
status.pack(pady=10)

frame = tk.Frame(root)
frame.pack()

def check_winner(player):
    for a, b, c in win_patterns:
        if board[a] == board[b] == board[c] == player:
            return True
    return False

def board_full():
    return "" not in board

def ai_move():
    if game_over:
        return

    # Try to win
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            if check_winner("O"):
                buttons[i]["text"] = "O"
                finish("AI Wins!")
                return
            board[i] = ""

    # Block player
    for i in range(9):
        if board[i] == "":
            board[i] = "X"
            if check_winner("X"):
                board[i] = "O"
                buttons[i]["text"] = "O"
                if check_winner("O"):
                    finish("AI Wins!")
                else:
                    status.config(text="Your Turn (X)")
                return
            board[i] = ""

    # Random move
    empty = [i for i in range(9) if board[i] == ""]
    if empty:
        move = random.choice(empty)
        board[move] = "O"
        buttons[move]["text"] = "O"

    if check_winner("O"):
        finish("AI Wins!")
    elif board_full():
        finish("It's a Draw!")
    else:
        status.config(text="Your Turn (X)")

def click(index):
    global game_over

    if game_over or board[index] != "":
        return

    board[index] = "X"
    buttons[index]["text"] = "X"

    if check_winner("X"):
        finish("You Win!")
        return

    if board_full():
        finish("It's a Draw!")
        return

    status.config(text="AI Thinking...")
    root.after(500, ai_move)

def finish(message):
    global game_over
    game_over = True
    status.config(text=message)
    messagebox.showinfo("Game Over", message)

def restart():
    global board, game_over
    board = [""] * 9
    game_over = False

    for btn in buttons:
        btn.config(text="")

    status.config(text="Your Turn (X)")

for i in range(9):
    btn = tk.Button(
        frame,
        text="",
        width=6,
        height=3,
        font=("Arial", 20),
        command=lambda i=i: click(i)
    )
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

restart_btn = tk.Button(root, text="Restart", command=restart)
restart_btn.pack(pady=15)

root.mainloop()