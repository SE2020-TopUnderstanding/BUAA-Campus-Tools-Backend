from Crypto.Cipher import AES
import base64
'''
目前采用ECB方法
调用方法
pr = aescrypt(key,model,iv,encode_)
en_text = pr.aesencrypt('17373349')
pr.aesdecrypt(en_text)
编码方式gbk
'''
key =  b'hangxu@buaase_20'#公钥 注意公钥只能为16的长度


model = 'ECB'
iv = ''
encode_ = 'gbk'
class aescrypt():
    '''
    加密和解密方法
    支持ECB和CBC两种模式
    '''
    def __init__(self,key,model,iv,encode_):
        self.encode_ = encode_
        self.model =  {'ECB':AES.MODE_ECB,'CBC':AES.MODE_CBC}[model]
        self.key = key
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
        a = len(par) % 16 
        if a == 0:
            a = 16 - a
            for i in range(16):
               par += b'\x10'
        else:
            a = 16 - a
            a = chr(a).encode(self.encode_)
            while len(par) % 16 != 0:
                par += a
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
        t = self.decrypt_text.decode(self.encode_).strip('\0')
        t_list = list(t)
        length = len(t_list)
        
        surplus = 0#多余的字符串
        for i in t_list:
            if i == t_list[length-1]:
                surplus = surplus + 1

        t = t[0:length-surplus] + "\0"
        return t#得出解密后的密码再解码