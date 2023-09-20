import zlib


def calc_crc32(path):
    with open(path, 'rb') as file:
        crc32_hash = 0

        while True:
            data = file.read(65536)
            if not data:
                break
            crc32_hash = zlib.crc32(data, crc32_hash)
    crc32_hex = '%08X' % (crc32_hash & 0xFFFFFFFF)

    return crc32_hex