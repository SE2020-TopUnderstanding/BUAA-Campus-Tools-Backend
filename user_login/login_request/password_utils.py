import base64
from Crypto.Cipher import AES

from API.settings import  KEY
# 目前采用ECB方法
# 调用方法
# password_d = Aescrypt(key,model,iv,encode_)
# en_text = password_d.Aesencrypt('17373349')
# password_d.Aesdecrypt(en_text)
# 编码方式gbk


MODEL = 'ECB'
IV = ''
ENCODE_ = 'gbk'


class Aescrypt():
    """
    加密和解密方法
    支持ECB和CBC两种模式
    """
    def __init__(self, key, model, iv_, encode_):
        self.encode_ = encode_
        self.model = {'ECB': AES.MODE_ECB, 'CBC': AES.MODE_CBC}[model]
        self.key = key
        self.iv_ = self.add_16(iv_)
        if model == 'ECB':
            self.aes = AES.new(self.key, self.model)  # 创建一个aes对象
        elif model == 'CBC':
            self.aes = AES.new(self.key, self.model, self.iv_)  # 创建一个aes对象

        # 这里的密钥长度必须是16、24或32，目前16位的就够用了

    def add_16(self, par):
        """
        par代表加密的文本，文本长度需要补全到16的倍数
        且将文本编码
        """
        par = par.encode(self.encode_)  # 编码
        length = len(par) % 16
        if length == 0:
            i = 0
            while i < 16:
                i = i + 1
                par += b'\x10'
        else:
            length = 16 - length
            length = chr(length).encode(self.encode_)
            while len(par) % 16 != 0:
                par += length
        return par

    def aesencrypt(self, text):
        text = self.add_16(text)
        encrypt_text = self.aes.encrypt(text)
        return base64.encodebytes(encrypt_text).decode().strip()  # 先按照base64编码再解码

    def aesdecrypt(self, text):
        if self.model == AES.MODE_CBC:
            self.aes = AES.new(self.key, self.model, self.iv_)

        text = base64.decodebytes(text.encode(self.encode_))  # 先编码再按照base64解码
        decrypt_text = self.aes.decrypt(text)
        t_all = decrypt_text.decode(self.encode_).strip('\0')
        t_list = list(t_all)
        length = len(t_list)

        surplus = ord(t_list[length - 1])

        return t_all[0:length - surplus]  # 得出解密后的密码再解码


if __name__ == '__main__':
    P = Aescrypt(KEY, MODEL, IV, ENCODE_)
    ST = '17373349'
    ET = P.aesencrypt(ST)
    print('我的密文:', ET)
    print(len(ET))
    print('用我的密文解密的明文:', P.aesdecrypt(ET))

    if P.aesdecrypt(ET) == ST:
        print('相同')
