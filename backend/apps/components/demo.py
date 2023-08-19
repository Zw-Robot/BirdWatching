from apps.components.WXBizDataCrypt import WXBizDataCrypt

def getInfo(appId,sessionKey,encryptedData,iv):
    appId = 'wx34396991c4ea8e2c'
    # sessionKey = 'nudI38rMtSWr3lzun0qDWw=='
    # encryptedData = "2za/NdA3UVneDgJvK008RO285BOkVezKIYPGbjm1nKeqBygdBIJJjQ2OWmRVeZYYxEMkhZtTP8w19y71dElmJgqPp5dWgWVvfwAxzUo/cmd31p+KFrHB8xx8nOfV0XuytjgrRJuBaHrW2H5QkrN2cGVvSuqmJle3Z+duytIOsSKomBqPECnYnTsaaFNM/ETVe9aoH2yxWY5dAIecjP1GmeLVxZ6qsZ2EO9HCOomZZgmNWP4+RFQtQwgnOWp0QCThnu+JKEbhcrdckWRsd3+6aIiWDwx7Ik5RcPMC23Om+Hx5YHjsZvMLGgC12+SOcoD91G8KwP+chMt+6oeM5XDiPjjHkmsBd82+VPDxcVWs3oyBlLCGacA5ysZW0OKQkM2dQRCdHCbXc8dutrB2NYQMT+dN34Rc6czxYHPvxHvRiXHEIGN9dx6OHu9Z8qR/G3uf"
    # iv = "vXcwi251xUxRLV8s6Jtwtg=="

    pc = WXBizDataCrypt(appId, sessionKey)
    info = pc.decrypt(encryptedData, iv)
    print(info)
    return info
