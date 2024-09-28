class Overs:
    def __init__(self,overs):
        self.Runs = 0
        self.Wickets = 0
        self.Overs = overs
        self.Cur_over = 1

    
    @property
    def Runs(self):
        return self.__runs
    @Runs.setter
    def Runs(self,d):
        self.__runs=d
        return self.__runs

    @property
    def Wickets(self):
        return self.__wickets
    @Wickets.setter
    def Wickets(self,d):
        self.__wickets=d
        return self.__wickets

    @property
    def Overs(self):
        return self.__overs
    @Overs.setter
    def Overs(self,d):
        self.__overs=d
        return self.__overs
        
    @property
    def Cur_over(self):
        return self.__cur_over
    @Cur_over.setter
    def Cur_over(self,d):
        self.__cur_over=d
        return self.__cur_over

    def score_of_one_ball(self, n):
        runs=0
        wickets=0
        if n in (0,1,2,3,4,5,6):
            runs+=n
        elif n.lower()=="w":
            wickets+=1
        elif n.lower()=="wb":
            runs+=1
        elif n.lower()=="nb":
            runs+=1

        self.Runs+=runs
        self.Wickets+=wickets
