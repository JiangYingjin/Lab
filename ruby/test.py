from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import base64
import struct

# SSH RSA 公钥字符串
ssh_rsa_key = """
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDO1c77X9oBDZ7XROYon/lwqXrB3YOHJIHoROGl4iQGmsbBNNTtIRqoTAuwjUIJezL6AQ6J4YOzkcRLSMdMYFLI7MLCoFjqOSyvADQMOkJ+O+FeiMKNujhdrazfgDyhHDe/SGfnw2E78V4xDx7Ps0yQZql9NTOHKuepMuI/pFSvFt2+/h487H8DarL8sP8d1wYX+rlQxDbRurZKXSrMbj9rpeHS3RDxmUzkl2PMuo2kYwdSR76HZJDqGLhhQo4kJ5cA8uq4gnBAWy2Mk+/hYPD/lkIg91XWRxLvbSgWGzSHHaa4irVimVmfCgOxL43kYVCevoEBX0aI7TvLj0iwSMN8Mm0h9c8znNlq3/lljfH8AKZu1VCEwU7rB/SgOUohPCI3c92zGXvo/OZzHs0v/J2gXmxh8zzuF3Kj5EqokjoITgwm0aACp2yV4HO1mCj5uR7An6LHCKSWEl571nIpy1rPociy7qccyf5wmTGqRRS+TBEWdA95rW4vDETfGfASGfc= JiangYingjin
"""


def parse_ssh_public_key(key_data):
    # 提取 Base64 内容
    parts = key_data.strip().split()
    if len(parts) < 2:
        raise ValueError("Invalid SSH public key format")

    # 解码 Base64 数据
    decoded = base64.b64decode(parts[1])
    print(f"公钥解码前长度为 {len(parts[1])} 字节，内容为 {parts[1]}")
    print(f"公钥解码后长度为 {len(decoded)} 字节，内容为 {decoded}")

    # 解析 SSH 格式
    try:
        # 跳过key类型字符串
        pos = 0
        print(f"pos -> {pos}")
        print("读取 length（4 bytes）中 ...")
        # `struct.unpack` 用于解包二进制数据
        length = struct.unpack(">I", decoded[pos : pos + 4])[0]
        print(f"length: {length} (bytes)")
        pos += 4
        print(f"pos -> {pos}")
        pos += length
        print(f"pos -> {pos}")

        # 读取指数 e
        print(f"读取 e_length（4 bytes）中 ...")
        e_length = struct.unpack(">I", decoded[pos : pos + 4])[0]
        print(f"e_length: {e_length} (bytes)")
        pos += 4
        print(f"pos -> {pos}")
        print(f"读取 e 中 ({e_length} bytes) ...")
        e = int.from_bytes(decoded[pos : pos + e_length], "big")
        print(f"e: {e}")
        pos += e_length
        print(f"pos -> {pos}")

        # 读取模数 n
        print(f"读取 n_length（4 bytes）中 ...")
        n_length = struct.unpack(">I", decoded[pos : pos + 4])[0]
        print(f"n_length: {n_length} (bytes)")
        pos += 4
        print(f"pos -> {pos}")
        print(f"读取 n 中 ({n_length} bytes) ...")
        n = int.from_bytes(decoded[pos : pos + n_length], "big")
        print(f"n: {n}，其位数为 {n.bit_length()} 位，十进制长度为 {len(str(n))}")
        pos += n_length
        print(f"pos -> {pos}")

        # 构造 RSA 公钥
        return rsa.RSAPublicNumbers(e=e, n=n).public_key()
    except Exception as ex:
        raise ValueError(f"Failed to parse SSH public key: {str(ex)}")


# 解析公钥
try:
    public_key = parse_ssh_public_key(ssh_rsa_key)

    # 获取并打印公钥详情
    numbers = public_key.public_numbers()
    print(f"模数 (n): {numbers.n}")
    print(f"模数位数: {numbers.n.bit_length()} 位")
    print(f"公钥指数 (e): {numbers.e}")
except ValueError as e:
    print(f"解析错误: {str(e)}")


def parse_rsa_private_key(file_path):
    # 从 PEM 文件加载 RSA 私钥
    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # 如果私钥有密码保护，请在这里填写密码
        )

    # 确保加载的私钥是 RSA 类型
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise ValueError("提供的私钥不是有效的 RSA 私钥")

    # 提取私钥的数字组成部分
    private_numbers = private_key.private_numbers()

    # 打印私钥详细信息
    print("解析 RSA 私钥中的详细信息：")
    print(f"模数 (n): {private_numbers.public_numbers.n}")
    print(f"模数位数: {private_numbers.public_numbers.n.bit_length()} 位")
    print(f"公钥指数 (e): {private_numbers.public_numbers.e}")
    print(f"私钥指数 (d): {private_numbers.d}")
    print(f"素数 p: {private_numbers.p}")
    print(f"素数 q: {private_numbers.q}")
    # 打印素数的二进制长度
    print(f"p 的二进制长度为 {private_numbers.p.bit_length()} 位")
    print(f"q 的二进制长度为 {private_numbers.q.bit_length()} 位")
    print(f"dp = d % (p-1): {private_numbers.dmp1}")
    print(f"dq = d % (q-1): {private_numbers.dmq1}")
    print(f"q_inv = q^(-1) % p: {private_numbers.iqmp}")


# 示例：从本地文件解析私钥
file_path = "/root/.ssh/id_rsa"  # 替换为你的私钥文件路径
parse_rsa_private_key(file_path)
