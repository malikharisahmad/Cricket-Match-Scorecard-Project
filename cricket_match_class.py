from overs_class import Overs
from batsman_class import Batsman
from bowler_class import Bowler
import sqlite3 as dbms

class CricketMatch:
    def __init__(self, team, total_overs, target = None, score = []):
        self.Team = team
        self.Target = target
        self.Total_overs = total_overs
        self.Ov = self.create_overs()
        self.Bm1 = self.create_batsman()
        self.Bm2 = self.create_batsman(False)
        self.Bl = self.create_bowler()
        self.__score = score
        self.all_overs()
        
    @property
    def Score(self):
        return sum(self.__score)
    @Score.setter
    def Score(self, s):
        self.__score.append(s)
        return self.__score
    
    @property
    def Team(self):
        return self.__team
    @Team.setter
    def Team(self, s):
        self.__team = s
        return self.__team
        
    @property
    def Target(self):
        return self.__target
    @Target.setter
    def Target(self, s):
        self.__target = s
        return self.__target
        
    @property
    def Total_overs(self):
        return self.__total_overs
    @Total_overs.setter
    def Total_overs(self, s):
        self.__total_overs = s
        return self.__total_overs
        
    @property
    def Bm1(self):
        return self.__bm1
    @Bm1.setter
    def Bm1(self, s):
        self.__bm1 = s
        return self.__bm1
        
    @property
    def Bm2(self):
        return self.__bm2
    @Bm2.setter
    def Bm2(self, s):
        self.__bm2 = s
        return self.__bm2
        
    @property
    def Bl(self):
        return self.__bl
    @Bl.setter
    def Bl(self, s):
        self.__bl = s
        return self.__bl
        
    @property
    def Ov(self):
        return self.__ov
    @Ov.setter
    def Ov(self, s):
        self.__ov = s
        return self.__ov
    
    def create_batsman(self, st=True):
        bm_name = input("Enter batsman name: ")
        bm = Batsman(bm_name, st)
        return bm
        
    def create_bowler(self):
        bl_name = input("\nEnter bowler name: ")
        check_query = "SELECT Player, Runs, Dots, Overs, Wickets from Bowler WHERE Player = ?"
        self.create_tables(f'{self.Team}.db')
        con = dbms.connect(f'{self.Team}.db')
        cur = con.cursor()
        cur.execute(check_query, (bl_name,))
        check = cur.fetchone()
        if check:
            bl = Bowler(*check)
        else:
            bl = Bowler(bl_name)
        return bl
    
    def create_overs(self):
        ov = Overs(self.Total_overs)
        return ov
        
    def swap_striker(self, b1,b2):
        b1.Striker, b2.Striker = b2.Striker, b1.Striker
        return
        
    def one_ball(self, n):
        if n in ('0','1','2','3','4','5','6'):
            self.Score = int(n)
            self.Bl.bowl_one(int(n))
            if self.Bm1.Striker:
                self.Bm1.bat_one(int(n))
                self.Bm1.Balls+=1
            elif self.Bm2.Striker:
                self.Bm2.bat_one(int(n))
                self.Bm2.Balls+=1
            self.Ov.score_of_one_ball(int(n))
            if int(n)%2!=0:
                self.swap_striker(self.Bm1, self.Bm2)
            
        elif n in ("wb", "nb", "WB", "NB", "Nb", "nB", "Wb", "wB"):
            self.Bl.bowl_one(n)
            self.Score = 1
            if self.Bm1.Striker:
                self.Bm1.bat_one(n)
                self.Bm1.Balls+=1
            elif self.Bm2.Striker:
                self.Bm2.bat_one(n)
                self.Bm2.Balls+=1
            self.Ov.score_of_one_ball(n)
            e = int(input("Enter score on extra ball: "))
            self.Bl.bowl_one(e)
            self.Score = e
            if self.Bm1.Striker:
                self.Bm1.bat_one(e)
            elif self.Bm2.Striker:
                self.Bm2.bat_one(e)
            if int(e)%2!=0:
                self.swap_striker(self.Bm1, self.Bm2)
            self.Ov.score_of_one_ball(int(e))
        else:
            if n in ("w", "W"):
                self.Bl.bowl_one(n)
                if self.Bm1.Striker:
                    self.Bm1.Balls+=1
                    self.add_batsman_to_db(self.Bm1)
                    self.Bm1 = self.create_batsman()
                elif self.Bm2.Striker:
                    self.Bm2.Balls+=1
                    self.add_batsman_to_db(self.Bm2)
                    self.Bm2 = self.create_batsman()
                self.Ov.score_of_one_ball(n)
                
    def one_over(self):
        if self.Target:
            for i in range (6):
                if self.Score>self.Target:
                    self.add_bowler_to_db(self.Bl)
                    self.add_over_to_db(self.Ov)
                    return
                b = input(f"Enter score on ball {i+1}\n(ENTER 'w' for WICKET, 'nb' for NO BALL, 'wb' for WIDE BALL):\n")
                self.one_ball(b)
                
        else:
            for i in range (6):
                b = input(f"Enter score on ball {i+1}\n(ENTER 'w' for WICKET, 'nb' for NO BALL, 'wb' for WIDE BALL):\n")
                self.one_ball(b)
        self.add_bowler_to_db(self.Bl)
        self.add_over_to_db(self.Ov)
        
    def all_overs(self):
        for i in range (self.Total_overs):
            self.Ov.Cur_over = i+1
            print(f"\nOver {i+1}\n")
            self.one_over()
            if i < self.Total_overs-1:
                self.Bl = self.create_bowler()
                self.Ov = self.create_overs()
        self.add_batsman_to_db(self.Bm1)
        self.add_batsman_to_db(self.Bm2)
                    
    def  add_bowler_to_db(self, b):
        player_ = f"{b.Name}"
        overs_ = f"{b.Overs}"
        dots_ = f"{b.Dots}"
        runs_ = f"{b.Runs}"
        wickets_ = f"{b.Wickets}"
        er_ = f"{b.Er}"
        check_query = "SELECT Player, Runs, Dots, Overs, Wickets, Economy_Rate from Bowler WHERE Player = ?"
        query = "INSERT INTO Bowler(Player, Runs, Dots, Overs, Wickets, Economy_Rate) VALUES (?, ?, ?, ?, ?, ?)"
        update_query = "UPDATE Bowler SET Runs = ?, Dots = ?, Overs = ?, Wickets = ?, Economy_Rate = ? WHERE Player = ?"
        self.create_tables(f'{self.Team}.db')
        con = dbms.connect(f'{self.Team}.db')
        cur = con.cursor()
        cur.execute(check_query, (player_,))
        check = cur.fetchone()
        if check:
            cur.execute(update_query, (runs_, dots_, overs_, wickets_, er_, player_))
        else:
            cur.execute(query, (player_, runs_, dots_, overs_, wickets_, er_))
        con.commit()
        cur.close()
        con.close()
        
    def  add_batsman_to_db(self, b):
        player_ = f"{b.Name}"
        balls_ = f"{b.Balls}"        
        runs_ = f"{b.Runs}"
        fours_ = f"{b.Fours}"
        sixes_ = f"{b.Sixes}"
        sr_ = f"{b.Sr}"
        query = "INSERT INTO Batsmen(player_name, runs, balls, fours, sixes, strike_rate) VALUES (?, ?, ?, ?, ?, ?)"
        self.create_tables(f'{self.Team}.db')
        con = dbms.connect(f'{self.Team}.db')
        cur = con.cursor()
        cur.execute(query, (player_, runs_, balls_, fours_, sixes_, sr_))
        con.commit()
        cur.close()
        con.close()
        
    def add_over_to_db(self, o):
        over_ = f"Over {o.Cur_over}"       
        runs_ = f"{o.Runs}"
        wickets_ = f"{o.Wickets}"
        query = "INSERT INTO Overs(over, runs, wickets) VALUES (?, ?, ?)"
        self.create_tables(f'{self.Team}.db')
        con = dbms.connect(f'{self.Team}.db')
        cur = con.cursor()
        cur.execute(query, (over_, runs_, wickets_))
        con.commit()
        cur.close()
        con.close()
        
    def score(self, s=0):
        scores = []
        scores.append(s)
        # query = "SELECT runs from Overs"
        # con = dbms.connect(f'{self.Team}.db')
        # cur = con.cursor()
        # cur.execute(query)
        # r = cur.fetchall()
        # if r:
            # for i in r:
                # scores+= int(i[0])
        # con.commit()
        # cur.close()
        # con.close()
        return sum(scores)
        
    def create_tables(self, db_name):
        try:
            con = dbms.connect(db_name)
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Bowler (Player TEXT, Runs REAL, Dots INT, Overs INT, Wickets INT, Economy_Rate REAL)")
            cur.execute("CREATE TABLE IF NOT EXISTS Batsmen (player_name TEXT,runs INT, balls INT,fours INT,sixes INT,strike_rate REAL)")
            cur.execute("CREATE TABLE IF NOT EXISTS Overs (over INT,runs INT,wickets INT)")
            con.commit()
            cur.close()
            con.close()
        except:
            print(end="")
            