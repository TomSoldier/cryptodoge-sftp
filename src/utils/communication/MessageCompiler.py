from src.utils.communication.aesGcmCipher import AesGcmCipher

class MessageCompiler:
    def __init__(self,
                 symKey: bytes,
                 sessionId:bytes,
                 initSeqNum: int = 0):
        '''
        :param symKey:
        :param sessionId: has to be 16 byte long
        :param initSeqNum: initial sequence number
        '''
        if len(symKey) > 16:
            symKey = symKey[-16:]
        self.cipher = AesGcmCipher(symKey)
        self.rcrSeqNum = initSeqNum
        self.sndSeqNum = initSeqNum
        if len(sessionId) != 16:
            raise ValueError("SessionId must be 16 byte long.")
        self.SID = sessionId

    def compileFirstMessage(self):
        thisPart = self.SID

        cmd = (0).to_bytes(3, "big")
        header = b''.join([self.SID, self.sndSeqNum.to_bytes(8, "big"), (len(thisPart)).to_bytes(5, "big")])
        body = b''.join([cmd, thisPart])
        nonce, header, ciphertext, tag = self.cipher.encrypt(header, body)

        self.sndSeqNum += 1
        return (B''.join([nonce, header, ciphertext, tag]))

    def compile(self, message:bytes, cmd:bytes):
        messages = []

        remainingLength = len(message)
        remainingMessage = message
        while(remainingLength > 2**20-1):

            thisPart = remainingMessage[:2**20]
            remainingMessage = remainingMessage[2**20:]

            header = b''.join([self.SID, self.sndSeqNum.to_bytes(8,"big"), (len(thisPart)).to_bytes(5, "big")])
            body = b''.join([cmd, thisPart])
            nonce, header, ciphertext, tag = self.cipher.encrypt(header, body)

            messages.append(B''.join([nonce, header, ciphertext, tag]))
            self.sndSeqNum += 1


        thisPart = remainingMessage

        header = b''.join([self.SID, self.sndSeqNum.to_bytes(8, "big"), (len(thisPart)).to_bytes(5, "big")])
        body = b''.join([cmd, thisPart])
        nonce, header, ciphertext, tag = self.cipher.encrypt(header, body)

        messages.append(B''.join([nonce, header, ciphertext, tag]))
        self.sndSeqNum += 1

        return messages

    def decompile(self, msg:bytes):
        nonce = msg[0:16]
        seqnum = int.from_bytes(msg[32:40],"big")
        length = int.from_bytes(msg[40:45],"big")
        header = msg[16:45]
        body = msg[45:48+length]
        tag = msg[48+length:]

        if not self.rcrSeqNum - 3 < seqnum < self.rcrSeqNum + 3:
            raise ValueError("Received sequence number doesn't match with stored.")
        self.rcrSeqNum += 1

        plainBody = self.cipher.decrypt(nonce, header, body, tag)

        cmd = plainBody[0:3]
        plainText = plainBody[3:]
        return cmd, plainText
