import random

class ChatGarbler:
    
    def __init__(self, messages):
        self.messages = messages

    def garble(self, avatar, message):
        newMessage = ''

        if avatar.style:
            avatarType = avatar.style.getType()
            wordList = self.messages[avatarType if avatarType in self.messages else 'default']

        numWords = len(message.split(' '))

        for i in xrange(1, numWords + 1):
            wordIndex = random.randint(0, len(wordList) - 1)
            newMessage = newMessage + wordList[wordIndex]

            if i < numWords:
                newMessage = newMessage + ' '

        return '\x01WLDisplay\x01%s\x02' % newMessage