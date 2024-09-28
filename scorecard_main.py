from cricket_match_class import CricketMatch
from cricket_match_display_class import CricketMatchDisplay
import tkinter as tk

def main():
    t1 = input("Enter Team 1: ")
    t2 = input("Enter Team 2: ")
    ov = int(input("Enter total overs: "))
    print(f"\nTeam {t1} bats\n")
    cm1 = CricketMatch(t1, ov)
    target = cm1.Score
    print(f"\nInnings ended. Target: {target}\n")
    print(f"\nTeam {t2} chases\n")
    cm2 = CricketMatch(t2, ov, target, [])
    root = tk.Tk()
    app = CricketMatchDisplay(root, f"{t1}.db", f"{t2}.db")
    root.mainloop()
main()
