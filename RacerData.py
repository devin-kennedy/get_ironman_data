class RacerData:
    def __init__(self, name: str = None, pos: int = None, swim: str = None, t1: str = None, bike: str = None,
                 t2: str = None, run: str = None, final: str = None):
        self.name = name
        self.pos = pos
        self.swim = swim
        self.t1 = t1
        self.bike = bike
        self.t2 = t2
        self.run = run
        self.final = final
        self.gender = None
        self.division = None

    def __str__(self):
        outData = [self.name, str(self.pos), self.swim, self.t1, self.bike, self.t2, self.run, self.final, self.division]
        outData = ",".join(outData)
        return outData

    def listOf(self):
        return [self.name, str(self.pos), self.swim, self.t1, self.bike, self.t2, self.run, self.final, self.gender, self.division]

    def import_data(self, col):
        self.name = col[1].text
        self.pos = col[6].text
        self.swim = col[7].text
        self.bike = col[8].text
        self.run = col[9].text
        self.final = col[10].text
