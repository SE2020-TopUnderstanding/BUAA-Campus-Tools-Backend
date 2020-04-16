#小写字母a=z z=a b=y y=b以此类推
#大写字母E=0 F=1 J=2 H=3 I=4 J=5 K=6 L=7 M=8 N=9
#数字0=N 1=M 2=L 3=K 4=J 5=I 6=H 7=J 8=F 9=E
#其他ASCALL+3
def encrypt_string(message):
    encode_result = ""
    for char in message:
        char_int = ord(char)#返回ascall值
        if  (char_int >= 97) & (char_int <= 122):#小写字母
            encode_result += chr(122-(char_int-97))
        elif (char_int >= 69) & (char_int <= 78):#E-N
            encode_result += chr(char_int-21)
        elif (char_int >= 48) & (char_int <= 57):#0-9
            encode_result += chr(78-char_int+48)
        else:
            encode_result += char
    return encode_result

def decrypt_string(message):
    decode_result = ""
    for char in message:
        char_int = ord(char)#返回ascall值
        if  (char_int >= 97) & (char_int <= 122):#小写字母
            decode_result += chr(122-(char_int-97))
        elif (char_int >= 69) & (char_int <= 78):#E-N
            decode_result += chr(57-char_int+69)
        elif (char_int >= 48) & (char_int <= 57):#0-9
            decode_result += chr(69+char_int-48)
        else:
            decode_result += char
    return decode_result

