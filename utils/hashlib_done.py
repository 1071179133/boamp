"""密码加密"""
import hashlib

def encryption(strs):
    md5 = hashlib.md5() #哈希加密
    md5.update(strs.encode("utf-8"))  #utf8转换
    strs = md5.hexdigest()  #转成十六进制
    return strs
