from Crypto.Cipher import AES
import base64
class aescrypt():
    def __init__(self,key,model,iv,encode_):
        self.encode_ = encode_
        self.model =  {'ECB':AES.MODE_ECB,'CBC':AES.MODE_CBC}[model]
        self.key = self.add_16(key)
        self.iv = self.add_16(iv)
        if model == 'ECB':
            self.aes = AES.new(self.key,self.model) #创建一个aes对象
        elif model == 'CBC':
            self.aes = AES.new(self.key,self.model,self.iv) #创建一个aes对象

        #这里的密钥长度必须是16、24或32，目前16位的就够用了

    def add_16(self,par):
        '''
        par代表加密的文本，文本长度需要补全到16的倍数
        且将文本编码
        '''
        par = par.encode(self.encode_)#编码
        while len(par) % 16 != 0:
            par += b'\x00'
        return par

    def aesencrypt(self,text):
        text = self.add_16(text)
        self.encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(self.encrypt_text).decode().strip()#先按照base64编码再解码

    def aesdecrypt(self,text):
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key, self.model, self.iv)
        
        text = base64.decodebytes(text.encode(self.encode_))#先编码再按照base64解码
        self.decrypt_text = self.aes.decrypt(text)
        return self.decrypt_text.decode(self.encode_).strip('\0')#得出解密后的密码再解码

if __name__ == '__main__':
    pr = aescrypt('12345','CBC','2','gbk')
    en_text = pr.aesencrypt('好好学习')
    print('密文:',en_text)
    print('明文:',pr.aesdecrypt(en_text))