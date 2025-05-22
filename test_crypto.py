import tool.crypto as crypto

encrypted = crypto.encrypt(input("請輸入要加密的文字："))
decrypted = crypto.decrypt(encrypted)
print("{}{}".format( "加密：", encrypted))
print("{}{}".format( "解密：", decrypted))