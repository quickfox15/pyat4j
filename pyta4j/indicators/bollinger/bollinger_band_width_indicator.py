from pyta4j.indicators import CachedIndicator

class BollingerBandWidthIndicator(CachedIndicator):
    
    def __init__(self, bbl,bbm,bbu):
        super().__init__()
        self.bbl = bbl
        self.bbm = bbm
        self.bbu = bbu
        
    def calculate(self, index):
        return (self.bbu.get_value(index) - self.bbl.get_value(index)) / self.bbm.get_value(index) * 100
