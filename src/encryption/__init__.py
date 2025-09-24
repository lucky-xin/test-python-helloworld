__title__ = 'serialization'
__author__ = 'chaoxin.lu'
__email__ = 'chaoxin.lu@pistonint.com'

__all__ = ['SM2', 'SM3', 'SM4']

import base64
import json

from gmssl import sm2, sm3
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, PKCS7, SM4_DECRYPT


class SM2(object):
    def __init__(self, private_key: str, public_key: str):
        self._public_key = public_key
        self._private_key = private_key

    def encrypt(self, plain_byts: bytes, asn1: bool = True, mode: int = 1) -> bytes:
        """
        使用SM2算法加密给定的字节数据。

        SM2是一种基于椭圆曲线密码学的公钥加密算法，广泛用于中国国内的加密应用。
        该函数通过CryptSM2类实例化一个SM2对象来进行加密操作，支持ASN.1编码和不同的操作模式。

        参数:
        - plain_byts: 待加密的原始字节数据。
        - asn1: 是否使用ASN.1编码，默认为True。ASN.1编码是SM2加密的一种标准格式。
        - mode: 加密模式，默认为1。不同的模式可能适用于不同的安全需求或性能需求。

        返回:
        加密后的字节数据。

        注意:
        - 该函数使用了预置的公钥和私钥，这意味着它要么用于签名验证（使用公钥），要么用于加密（使用私钥）。
        - 实际应用中，公钥和私钥的使用应根据具体的加密通信场景和安全需求进行严格管理。
        """
        # 实例化SM2加密对象，准备进行加密操作
        sm2_crypt = sm2.CryptSM2(
            public_key=self._public_key,
            private_key=self._private_key,
            asn1=asn1,
            mode=mode)

        # 执行加密并返回加密后的数据
        return sm2_crypt.encrypt(plain_byts)

    def encrypt_2_hex(self, plain_byts: bytes, asn1: bool = True, mode: int = 1) -> str:
        """
        加密给定的字节数据，并以十六进制字符串形式返回加密结果。

        该方法首先调用 `encrypt` 方法对输入的明文字节进行加密，然后将加密结果转换为十六进制字符串格式。
        这种格式化后的输出常用于需要文本表示的场景，例如日志记录或用户界面显示。

        参数:
        - plain_byts: 待加密的字节数据。
        - asn1: 是否使用ASN.1编码的布尔值。ASN.1编码可以更有效地表示某些数据结构。
        - mode: 加密模式的整数值，用于指定加密算法的具体模式或配置。

        返回值:
        - 返回加密后的数据的十六进制字符串表示。

        注意:
        - 该方法依赖于内部 `encrypt` 方法进行实际的加密操作。
        - 转换为十六进制字符串是为了便于传输或存储，同时避免了二进制数据在处理过程中的潜在问题。
        """
        # 调用encrypt方法进行加密，然后将结果转为十六进制字符串
        return self.encrypt(plain_byts, asn1, mode).hex()

    def encrypt_2_base64(self, plain_text, asn1: bool = True, mode: int = 1) -> str:
        """
        使用Base64编码加密明文。

        该方法首先使用self.encrypt方法加密明文，然后将加密结果使用Base64编码，
        最后返回Base64编码后的字符串。这种方法常用于需要通过不安全的信道
        传输数据时，增加数据的安全性。

        参数:
        plain_text: 待加密的明文字符串。
        asn1 (bool): 指定是否使用ASN.1编码，默认为True。
        mode (int): 指定加密模式，默认为1。

        返回:
        str: Base64编码后的加密字符串。
        """
        # 调用encrypt方法加密明文，并使用Base64编码
        return base64.b64encode(self.encrypt(plain_text, asn1, mode)).decode('utf8')

    def decrypt(self, cipher_byts: bytes, asn1: bool = True, mode: int = 1) -> bytes:
        """
        使用SM2算法解密给定的密文。

        :param cipher_byts: 待解密的密文，以字节形式表示。
        :param asn1: 是否使用ASN.1编码格式。默认为True。
        :param mode: SM2加密模式。默认为1，表示基本加密模式。
        :return: 解密后的明文，以字节形式返回。

        本函数通过CryptSM2类创建一个SM2加密对象，然后使用该对象的decrypt方法
        来解密传入的密文。函数接收公钥和私钥，以及是否使用ASN.1编码格式和加密模式，
        并返回解密后的明文数据。
        """
        # 如果密文以“04”开头，则去掉前导“04”；否则，密文保持不变。
        cipher_byts = cipher_byts[1:] if cipher_byts[0] == 4 else cipher_byts
        # 创建SM2加密对象，初始化时指定公钥、私钥、ASN.1编码格式以及加密模式
        sm2_crypt = sm2.CryptSM2(
            public_key=self._public_key,
            private_key=self._private_key,
            asn1=asn1,
            mode=mode)

        # 使用SM2加密对象的解密方法解密密文，返回解密后的明文数据
        return sm2_crypt.decrypt(cipher_byts)

    def decrypt_base64(self, cipher_text: str, asn1: bool = True, mode: int = 1) -> bytes:
        """
        使用Base64解密给定的密文。

        :param cipher_text: 需要解密的Base64格式的密文。
        :param asn1: 是否使用ASN.1编码，默认为True。
        :param mode: 解密模式，默认为1。
        :return: 解密后的字节数据。
        """
        # 移除密文前的特定前缀，如果存在的话
        # 调用底层的decrypt方法进行实际解密操作，传入Base64解码后的密文
        return self.decrypt(base64.b64decode(cipher_text), asn1, mode)

    def decrypt_hex(self, cipher_text: str, asn1: bool = True, mode: int = 1) -> bytes:
        """
        解密给定的十六进制密文。

        :param cipher_text: 待解密的十六进制密文。
        :param asn1: 是否使用ASN.1编码，默认为True。
        :param mode: 解密模式，默认为1。
        :return: 解密后的字节数据。
        """
        # 将十六进制密文转换为字节，并调用decrypt方法进行解密。
        return self.decrypt(bytes.fromhex(cipher_text), asn1, mode)

    def decrypt_object(self, cipher_byts: bytes, asn1: bool = True, mode: int = 1) -> dict:
        """
        解密给定的密文字节，返回一个字典对象。

        此方法首先调用自身的`decrypt`方法对密文进行解密，然后将解密后的字节串
        转换为字典。如果原始数据是ASN.1编码且需要特定模式解密，可以通过参数进行指定。

        :param cipher_byts: 密文字节
        :param asn1: 布尔值，指示是否使用ASN.1编码，默认为True
        :param mode: 整数值，指定解密模式，默认为1
        :return: 解密后转换得到的字典对象
        """
        # 调用decrypt方法解密密文，得到字节串
        byts = self.decrypt(cipher_byts, asn1, mode)
        # 将解密后的字节串转换为字典并返回
        return json.loads(byts)


class SM4(object):
    def __init__(self, key: bytes, iv: bytes):
        self._key = key
        self._iv = iv

    def encrypt(self, plain_byts: bytes) -> bytes:
        """
        使用SM4算法对明文进行加密。

        :param plain_byts: 明文数据，以字节形式提供。
        :return: 加密后的密文，以字节形式返回。

        本函数通过实例化SM4加密对象，并设置密钥及加密模式，对输入的明文数据进行加密。
        采用的是CBC模式，且使用PKCS7方式进行填充以确保数据块的完整性。
        """
        # 实例化SM4加密对象，准备进行加密操作
        sm4 = CryptSM4(
            mode=SM4_ENCRYPT,
            padding_mode=PKCS7
        )
        # 设置加密密钥
        sm4.set_key(self._key, SM4_ENCRYPT)
        # 执行加密并返回加密后的数据
        return sm4.crypt_cbc(self._iv, plain_byts)

    def encrypt_2_hex(self, plain_byts: bytes) -> str:
        """
        加密给定的字节串并将其转换为十六进制字符串。

        该方法首先使用encrypt方法对输入的字节串进行加密。然后，它将加密后的字节串转换为十六进制字符串。
        这种转换通常用于数据的编码或解码过程，特别是在需要以文本形式处理二进制数据时。

        参数:
        plain_byts (bytes): 需要加密的原始字节串。

        返回:
        str: 加密后的十六进制字符串。
        """
        # 调用encrypt方法进行加密，然后将结果转为十六进制字符串
        return self.encrypt(plain_byts).hex()

    def encrypt_2_base64(self, plain_text) -> str:
        """
        加密并Base64编码明文字符串。

        该方法首先使用encrypt方法对输入的明文进行加密，然后将加密后的密文使用Base64进行编码，
        以便于传输和存储。Base64编码可以确保密文在各种系统和网络环境中不会因为字符集的问题而产生乱码。

        参数:
        plain_text (str): 需要加密的明文字符串。

        返回:
        str: 经过加密和Base64编码后的密文字符串。
        """
        # 调用encrypt方法加密明文，并使用Base64编码
        return base64.b64encode(self.encrypt(plain_text)).decode('utf8')

    def decrypt(self, cipher_byts: bytes) -> bytes:
        """
        使用SM4算法解密数据。

        :param cipher_byts: 已加密的数据，类型为bytes。
        :return: 解密后的数据，类型为bytes。

        本函数通过实例化SM4加密对象，并设置为解密模式，对输入的已加密数据进行解密。
        使用CBC模式进行解密，并且在解密过程中使用了PKCS7填充模式以保证数据的正确性。
        """
        # 实例化SM4加密对象，准备进行加密操作
        sm4 = CryptSM4(
            mode=SM4_DECRYPT,
            padding_mode=PKCS7
        )
        # 设置解密密钥
        sm4.set_key(self._key, SM4_DECRYPT)
        # 执行加密并返回加密后的数据
        return sm4.crypt_cbc(self._iv, cipher_byts)


    def decrypt_base64(self, cipher_text: str) -> bytes:
        """
        解密Base64编码的密文。

        该方法首先检查密文是否包含特定的前缀，如果包含，则移除该前缀。
        之后，使用Python标准库中的base64模块对密文进行Base64解码。
        最后，调用底层的decrypt方法进行实际的解密操作，并返回解密后的字节流。

        参数:
        cipher_text (str): Base64编码的密文字符串。

        返回:
        bytes: 解密后的字节流。
        """
        # 移除密文前的特定前缀，如果存在的话
        # 调用底层的decrypt方法进行实际解密操作，传入Base64解码后的密文
        return self.decrypt(base64.b64decode(cipher_text))

    def decrypt_hex(self, cipher_text: str) -> bytes:
        """
        解密十六进制表示的密文。

        本函数接收一个十六进制字符串形式的密文，将其转换为字节流后，
        调用decrypt方法进行解密，返回解密后的字节数据。

        参数:
        cipher_text (str): 十六进制表示的密文字符串。

        返回:
        bytes: 解密后的字节数据。
        """
        # 将十六进制密文转换为字节，并调用decrypt方法进行解密。
        return self.decrypt(bytes.fromhex(cipher_text))

    def decrypt_object(self, cipher_byts: bytes) -> dict:
        """
        解密给定的密文，并将其转换为字典对象。

        参数:
        cipher_byts (bytes): 需要解密的密文字节串。

        返回:
        dict: 解密后的数据，以字典形式表示。
        """
        # 调用decrypt方法解密密文，得到字节串
        byts = self.decrypt(cipher_byts)
        # 将解密后的字节串转换为字典并返回
        return json.loads(byts)


class SM3(object):

    def hash(self, plaintext: str) -> bytes:
        """
        将明文字符串转换为哈希值。

        使用国密SM3算法对输入的明文进行哈希处理，并返回固定的长度的哈希值。

        参数:
        plaintext (str): 需要进行哈希处理的明文字符串。

        返回:
        bytes: 使用SM3算法生成的哈希值，以字节形式返回。
        """
        # 将明文字符串编码为UTF-8字节序列，并转换为字节列表
        msg_list = [i for i in bytes(plaintext.encode('UTF-8'))]
        # 调用sm3_hash函数，传入处理后的消息列表，返回计算出的哈希值
        return sm3.sm3_hash(msg_list)
