import base64

from src.encryption import SM2, SM3, SM4


def test_sm2_encrypt_and_variants():
    sm2 = SM2(private_key="priv", public_key="pub")
    data = b"hello"

    enc = sm2.encrypt(data)
    assert isinstance(enc, bytes)
    assert enc.startswith(b"E")

    enc_hex = sm2.encrypt_2_hex(data)
    assert bytes.fromhex(enc_hex) == enc

    enc_b64 = sm2.encrypt_2_base64(data)
    assert base64.b64decode(enc_b64) == enc


def test_sm2_decrypt_paths():
    sm2 = SM2(private_key="priv", public_key="pub")
    # 加密返回以 b"E" 前缀，decrypt 内部会去掉 0x04 前缀，这里覆盖两条路径
    cipher = b"E" + b"world"
    plain = sm2.decrypt(cipher)
    assert plain == b"world"

    # 覆盖 decrypt_base64 与 decrypt_hex
    cipher_b64 = base64.b64encode(cipher).decode("utf8")
    assert sm2.decrypt_base64(cipher_b64) == b"world"

    cipher_hex = cipher.hex()
    assert sm2.decrypt_hex(cipher_hex) == b"world"

    # decrypt_object：json 场景
    json_bytes = b'{"k": "v"}'
    cipher_json = b"E" + json_bytes
    obj = sm2.decrypt_object(cipher_json)
    assert obj == {"k": "v"}


def test_sm4_encrypt_and_decrypt_variants():
    key = b"k" * 16
    iv = b"i" * 16
    sm4 = SM4(key=key, iv=iv)

    data = b"abcdefg"
    enc = sm4.encrypt(data)
    assert isinstance(enc, bytes)
    assert enc == data[::-1]

    enc_hex = sm4.encrypt_2_hex(data)
    assert bytes.fromhex(enc_hex) == enc

    enc_b64 = sm4.encrypt_2_base64(data)
    assert base64.b64decode(enc_b64) == enc

    dec = sm4.decrypt(enc)
    assert dec == data

    # decrypt_base64 / decrypt_hex / decrypt_object
    cipher_b64 = base64.b64encode(enc).decode("utf8")
    assert sm4.decrypt_base64(cipher_b64) == data

    cipher_hex = enc.hex()
    assert sm4.decrypt_hex(cipher_hex) == data


def test_sm3_hash():
    sm3 = SM3()
    out = sm3.hash("abc")
    assert isinstance(out, str)
    assert out == "stubbed-sm3-hash"

