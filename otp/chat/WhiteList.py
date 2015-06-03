from bisect import bisect_left

class WhiteList:

    def setWords(self, words):
        self.words = words
        self.numWords = len(self.words)

    def cleanText(self, text):
        return text.strip('.,?!').lower()

    def isWord(self, text):
        return self.cleanText(text) in self.words

    def isPrefix(self, text):
        text = self.cleanText(text)
        i = bisect_left(self.words, text)

        return i != self.numWords and self.words[i].startswith(text)
    
    def getReplacement(self, text, av=None, garbler=None):
        return '\x01WLRed\x01%s\x02' % text if not garbler else garbler.garble(av, text)

    def processText(self, text, av=None, garbler=None):
        if (not self.words) or (text.startswith('~') and not garbler):
            return text

        words = text.split(' ')
        newWords = []

        for word in words:
            if (not word) or self.isWord(word):
                newWords.append(word)
            else:
                newWords.append(self.getReplacement(word, av, garbler))

        lastWord = words[-1]

        if (not lastWord) or self.isPrefix(lastWord):
            newWords[-1] = lastWord
        else:
            newWords[-1] = self.getReplacement(lastWord, av, garbler)

        return ' '.join(newWords)
    
    def processThroughAll(self, text, av=None, garbler=None):
        return self.processText(text, av, garbler)