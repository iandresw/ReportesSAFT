def ms_encrypt(word: str, key: str) -> str:
    result_bytes = bytearray()
    w = len(word)
    k = len(key)
    p = 0
    for j in range(w):
        cd = word[j]
        if p == k:
            p = 0
        kd = key[p]
        p += 1
        nuchr = ord(cd) + ord(kd)
        if nuchr > 255:
            nuchr -= 255
        result_bytes.append(nuchr)
    
    # Interpretar como Windows-1252 (como lo haría VB6)
    return result_bytes.decode('windows-1252')

