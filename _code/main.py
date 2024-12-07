import os
import math
import cProfile


_os = 'Mac' if os.name == 'posix' else 'Windows'
_url = '/Users/sobj2/iCloudDrive/Documents/Programming/python/wordl/{}' if _os == 'Windows' /{}'
allowed_words_url = _url.format('_assets/allowed_text.txt')





with open(allowed_words_url,'r', encoding='utf-8') as file:
    global allowed_words
    allowed_words =[item.replace('\n','')for item in file.readlines()]
    num_words = len(allowed_words)






class prediction:
    def __init__(self) -> None:
        self.remaining_words = allowed_words

    def get_pattern(self,sample,compare):
        answer = {k:0 for k in range(len(sample))}
        compare = [(i,e) for i,e in enumerate(compare)]
        
        #check greens
        for i,e in enumerate(sample):
            if (i,e) in compare:
                answer[i] = 2
                compare.remove((i,e))
        compare = [item[1] for item in compare]
        for i,e in enumerate(sample):
            if e in compare and answer[i] == 0:
                answer[i] = 1
                compare.remove(e)

        return "".join(str(answer[item]) for item in answer)

    def predict(self,sample,pattern,remaining_words):
        self.pos_pairs = [(self.get_pattern(sample,word),word)for word in remaining_words]
        self.query = {key: [x for k, x in self.pos_pairs if k == key] for key in set(k for k, _ in self.pos_pairs)}
        self.remaining_words = self.query[pattern]
        self.entros = [self.rEntropy(word) for word in self.remaining_words]
        return len(self.entros),sorted(self.entros,key=lambda item: item[1],reverse=True )[:10],self.remaining_words
            

            
            
    def rEntropy(self,word):
        log2 = lambda x: math.log(x)/math.log(2)
        I = lambda p: round(log2(1/p),2)
        pats = [(self.get_pattern(word,compare_to),compare_to) for compare_to in self.remaining_words]
        query = {key: [x for k, x in pats if k == key] for key in set(k for k, _ in pats)}
        probabilities = dict(sorted({key:round(len(query[key])/num_words,4) for key in query}.items(),key=lambda item:item[0]))


        entropies = [probabilities[pattern]*I(probabilities[pattern]) for pattern in query]
        return (word,round(sum(entropies),2))

    def get_best(self):
        print(sorted([self.rEntropy(word)for word in allowed_words],key=lambda x:x[1],reverse=True)[:20])


            


 
if __name__ == '__main__':
    cProfile.run('prediction().get_best()')