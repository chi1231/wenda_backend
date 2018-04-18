#!/usr/bin/env python
# encoding: utf-8


def __swap(n):
    base = {0: 1893274973, 1: 778459911, 2: 1626806752, 3: 1267116246,
            16: 109020924, 17: 1742652622, 18: 312356055, 19: 2094271335}

    mask = 19

    idx = n & mask
    xor = base[idx] ^ n
    return ((xor | mask) ^ mask) | idx


def _reverse(strs):
    reverse = list(strs)
    reverse.reverse()
    return ''.join(reverse)


def create_code(i):
    loop = '0123456789abcdefghijklmnopqrstuvwxyz'
    n = __swap(i)
    a = []
    while n != 0:
        a.append(loop[n % 36])
        n = n / 36

    a.reverse()
    out = ''.join(a)
    return out


def create_12_code_base_10(restaurant_id, red_packet_id):
    random_code = __swap(red_packet_id)
    # 生成随机数
    len_random_code = len(str(random_code))
    restaurant_id %= 10 ** (12 - len_random_code)
    # 根据随机数保留饭店ID
    return _reverse((str(restaurant_id)).zfill(12
                                               - len_random_code)) + str(random_code)  # 在饭店ID和随机数之间补齐12位
