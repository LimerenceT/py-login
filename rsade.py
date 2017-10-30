import rsa

# rsa加密
def rsaEncrypt(str):
    # 生成公钥、私钥
    (pubkey, privkey) = rsa.newkeys(512)
    with open('public.pem', 'w+') as f:
        f.write(pubkey.save_pkcs1().decode())
    with open('privkey.pem','w+') as f:
        f.write(privkey.save_pkcs1().decode())
    # 明文编码格式
    content = str.encode('utf-8')
    # 公钥加密
    crypto = rsa.encrypt(content, pubkey)
    return (crypto, privkey)

# rsa解密
def rsaDecrypt(str, pk):
    # 私钥解密
    content = rsa.decrypt(str, pk)
    con = content.decode('utf-8')
    return con
