def enc_bytes(data, key=None):
    text = b''
    try:
        rsa_key =
        if key:
            rsa_key = key

        cipher = ciper_lib.new(rsa_key)
        for dat in block_data(data, rsa_key):
            cur_text = cipher.encrypt(dat)
            text += cur_text
    except Exception as err:
        print('RSA加密失败', data, err)
    return text