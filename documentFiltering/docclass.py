'''
Created on 2012-12-4

# encoding=utf-8
@author: jackliu
'''
import re
def getwords(doc):
    spilter = re.compile("\\W*")
    words = [s.lower() for s in spilter.split(doc) if len(s)>2 and len(s) <20]
    return dict([(w,1) for w in words])
class classifier:
    def __init__(self,getfeatures,filename = None):
        
        self.fc = {}
        self.cc = {}
        self.getfeatures = getfeatures
    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat] += 1
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat] += 1
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0
    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0
    def totalcount(self):
        return sum(self.cc.values())
    def categories(self):
        return self.cc.keys()
    def train(self,item,cat):
        features = self.getfeatures(item)
        for f in features:
            self.incf(f,cat)
        self.incc(cat)
    def fprob(self,f,cat):
        if self.catcount(cat) == 0:return 0
        return self.fcount(f, cat) / self.catcount(cat)
    def weightedprod(self,f,cat,prf,weight = 1.0,ap = 0.5):
        basicprob = prf(f,cat)
        totals = sum([self.fcount(f, c) for c in self.categories()])
        bp = (weight * ap + totals * basicprob) / (weight + totals)
        return bp
def sampletrain(cl):
    cl.train("Nobody owns the water.","good")
    cl.train("the quick rabbit jumps fences",'good')
    cl.train("buy pharmaceuticals now",'bad')
    cl.train("make quick money at the online casino",'bad')
    cl.train("the quick brown fox jumps",'good')
def test01():
    cl = classifier(getwords)
    sampletrain(cl)
    print cl.weightedprod("money", "good",cl.fprob)
if __name__ == "__main__":
    test01()
        