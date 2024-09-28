import tkinter as tk
from tkinter import ttk
import sqlite3 as dbms

class CricketMatchDisplay:
    def __init__(self, root, db1, db2):
        self.root = root
        self.root.title("Cricket Match Scorecard")  

        self.notebook = ttk.Notebook(root)

        self.databases = [db1, db2]
        tables = self.get_tables_from_databases(self.databases)

        for table in tables:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=f"Team {table.title()}")
            self.display_data(frame, table)

        self.notebook.pack(expand=1, fill="both")

    def get_tables_from_databases(self, databases):
        all_tables = set()
        for db_name in databases:
            con = dbms.connect(db_name)
            cur = con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cur.fetchall()
            all_tables.update(table[0] for table in tables)
            con.close()
        return list(all_tables)

    def display_data(self, frame, table):
        tree = ttk.Treeview(frame, show="headings")

        columns = self.get_columns_from_table(self.databases[0], table)
        tree["columns"] = columns

        for col in tree["columns"]:
            tree.heading(col, text=col.title())

        for col in tree["columns"]:
            tree.column(col, width=80, anchor="center")

        empty_cells = (len(columns) - 1) // 2

        team_runs = {db_name: 0 for db_name in self.databases}
        for db_index, db_name in enumerate(self.databases):
            con = dbms.connect(db_name)
            cur = con.cursor()

            cur.execute(f"SELECT * FROM {table}")
            data = cur.fetchall()

            team_row = [""] * empty_cells + [f"Team {db_name.rsplit('.', 1)[0]}"] + ([""] * (len(columns) - 1 - empty_cells))
            tree.insert("", "end", values=team_row)

            for row in data:
                tree.insert("", "end", values=list(row))
                team_runs[db_name] += int(row[1])  # Using 2nd column for overs

            con.close()

            totals_row = [""] * empty_cells + [f"Totals: {team_runs[db_name]}"] + ([""] * (len(columns) - 1 - empty_cells))
            tree.insert("", "end", values=totals_row)

            if db_index == 0 and len(self.databases) > 1:
                tree.insert("", "end", values=[""] * len(columns))

        winner = self.databases[0] if team_runs[self.databases[0]] > team_runs[self.databases[1]] else self.databases[1]
        winner_name = f"Team {winner.rsplit('.', 1)[0]} Wins!"
        tree.insert("", "end", values=([""] * empty_cells) + [winner_name] + ([""] * (len(columns) - 1 - empty_cells)))

        tree.pack(expand=1, fill="both")

    def get_columns_from_table(self, db_name, table):
        con = dbms.connect(db_name)
        cur = con.cursor()
        cur.execute(f"PRAGMA table_info({table})")
        columns = cur.fetchall()
        con.close()
        return [col[1] for col in columns]

