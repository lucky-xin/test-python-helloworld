import sys
import types


def _install_gmssl_stub() -> None:
    gmssl = types.ModuleType("gmssl")

    class _SM2:
        class CryptSM2:
            def __init__(self, public_key: str, private_key: str, asn1: bool = True, mode: int = 1):
                self.public_key = public_key
                self.private_key = private_key
                self.asn1 = asn1
                self.mode = mode

            def encrypt(self, data: bytes) -> bytes:
                # 简化：返回可逆的模拟密文（前缀 + 数据）
                return b"E" + data

            def decrypt(self, cipher: bytes) -> bytes:
                return cipher[1:]

    class _SM4:
        SM4_ENCRYPT = 1
        SM4_DECRYPT = 0

        class CryptSM4:
            def __init__(self, mode: int, padding_mode: int):
                self.mode = mode
                self.padding_mode = padding_mode

            def set_key(self, key: bytes, mode: int) -> None:  # noqa: ARG002
                pass

            def crypt_cbc(self, iv: bytes, data: bytes) -> bytes:  # noqa: ARG002
                # 简化：返回反向字节（可逆）
                return data[::-1]

    class _SM3:
        @staticmethod
        def sm3_hash(msg_list):
            # 简化：返回固定字符串，足以覆盖调用路径
            return "stubbed-sm3-hash"

    gmssl.sm2 = _SM2
    gmssl.sm3 = _SM3
    gmssl.sm4 = types.SimpleNamespace(CryptSM4=_SM4.CryptSM4, SM4_ENCRYPT=1, SM4_DECRYPT=0, PKCS7=7)

    sys.modules.setdefault("gmssl", gmssl)
    sys.modules.setdefault("gmssl.sm2", gmssl.sm2)
    sys.modules.setdefault("gmssl.sm3", gmssl.sm3)
    sys.modules.setdefault("gmssl.sm4", gmssl.sm4)


_install_gmssl_stub()

