import random

class ChatGarbler:
    
    def __init__(self, messages):
        self.messages = messages

    def garble(self, avatar, message, type=0):
        newMessage = ''

        if avatar.style:
            avatarType = avatar.style.getType()
            wordList = self.messages[avatarType if avatarType in self.messages else 'default']

        if type == 0:
            numWords = 1
        elif type == 1:
            numWords = random.randint(1, 7)
        elif type == 2:
            numWords = len(message.split(' '))

        for i in xrange(1, numWords + 1):
            wordIndex = random.randint(0, len(wordList) - 1)
            newMessage = newMessage + wordList[wordIndex]

            if i < numWords:
                newMessage = newMessage + ' '

        return newMessage