class Bowler():
    def __init__(self, name, runs = 0, dots = 0.0, overs = 0, wickets = 0):
        self.Name = name
        self.Overs = overs + 1
        self.Dots = dots
        self.Runs = runs
        self.Wickets = wickets
        
    @property
    def Name(self):
        return self.__name
    @Name.setter
    def Name(self, s):
        self.__name = s
        return self.__name
    
    @property
    def Overs(self):
        return self.__overs
    @Overs.setter
    def Overs(self, s):
        self.__overs = s
        return self.__overs
    
    @property
    def Dots(self):
        return self.__dots
    @Dots.setter
    def Dots(self, s):
        self.__dots = s
        return self.__dots
    
    @property
    def Runs(self):
        return self.__runs
    @Runs.setter
    def Runs(self, s):
        self.__runs = s
        return self.__runs
    
    @property
    def Wickets(self):
        return self.__wickets
    @Wickets.setter
    def Wickets(self, s):
        self.__wickets = s
        return self.__wickets
    
    @property
    def Er(self):
        return round((self.Runs/self.Overs), 1)
    
    def bowl_one(self, n):
        r = 0
        w = 0
        nb = 0
        wb = 0
        if n==0:
            r+=0
            self.Dots+=1
        elif n==1:
            r+=1
        elif n==2:
            r+=2
        elif n==3:
            r+=3
        elif n==4:
            r+=4
        elif n==5:
            r+=5
        elif n==6:
            r+=6
        elif n in ("w", "W"):
            w+=1
            self.Wickets+=w
        elif n in ("wb", "WB", "wB", "Wb"):
            wb+=1
        elif n in ("nb", "NB", "nB", "Nb"):
            nb+=1
        self.Runs+=(r+nb+wb)
        
        return (r,w,nb,wb)