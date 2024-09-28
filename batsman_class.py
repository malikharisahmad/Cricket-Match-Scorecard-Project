class Batsman():
    def __init__(self, name = "Player", striker = True):
        self.Name = name
        self.Runs = 0
        self.Balls = 0
        self.Fours = 0
        self.Sixes = 0
        self.Striker = striker
        
    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, s):
        self.__name = s
        return self.__name
        
    @property
    def Runs(self):
        return self.__runs
    @Runs.setter
    def Runs(self, s):
        self.__runs = s
        return self.__runs
        
    @property
    def Balls(self):
        return self.__balls
    @Balls.setter
    def Balls(self, s):
        self.__balls = s
        return self.__balls
        
    @property
    def Fours(self):
        return self.__fours
    @Fours.setter
    def Fours(self, s):
        self.__fours = s
        return self.__fours
        
    @property
    def Sixes(self):
        return self.__sixes
    @Sixes.setter
    def Sixes(self, s):
        self.__sixes = s
        return self.__sixes
        
    @property
    def Sr(self):
        if self.Balls==0:
            s = round(((self.Runs/1)*100), 1)
        else:
            s = round(((self.Runs/self.Balls)*100), 1)
        return s
        
    @property
    def Striker(self):
        return self.__striker
    @Striker.setter
    def Striker(self, s):
        self.__striker = s
        return self.__striker
        
    def bat_one(self, n):
        r = 0
        w = 0
        nb = 0
        wb = 0
        if n==0:
            r+=0
        elif n==1:
            r+=1
        elif n==2:
            r+=2
        elif n==3:
            r+=3
        elif n==4:
            r+=4
            self.Fours+=1
        elif n==5:
            r+=5
        elif n==6:
            r+=6   
            self.Sixes+=1
        elif n in ("wb", "WB", "wB", "Wb"):
            wb+=1
        elif n in ("nb", "NB", "nB", "Nb"):
            nb+=1
        self.Runs+=r+nb+wb
        return (r,w,nb,wb)