#!/usr/bin/python3

import struct


def encode_bmp(f, width, height, data, bpp=24):
    # 'bpp' stands for "bits per pixel" (usually 24 for RGB, 8+8+8)
    # 'data' should be a bi-dimensional array matching 'width' and 'height'
    
    # Calculate the BMP data size and the required padding (% 4)
    bytes_per_row = width * (bpp // 8)
    if bytes_per_row % 4 == 0:
        padding = bytes(0)
    else:
        padding = bytes(4 - (bytes_per_row % 4))
    
    data_size = height * (width + len(padding))
    
    # BMP Header (14 bytes)
    f.write(b'BM')  # (2) ID
    f.write(struct.pack('<I', 14 + 40 + data_size))  # (4) Size of the file
    f.write(struct.pack('<H', 0))  # (2) Unused
    f.write(struct.pack('<H', 0))  # (2) Unused
    f.write(struct.pack('<I', 14 + 40))  # (4) Offset where the BMP data is located

    # DIB Header (40 bytes)
    f.write(struct.pack('<I', 40))  # (4) Number of bytes on the DIB Header from here
    f.write(struct.pack('<I', width))  # (4) Width in pixels
    f.write(struct.pack('<I', height))  # (4) Height in pixels
    f.write(struct.pack('<H', 2))  # (2) Number of planes
    f.write(struct.pack('<H', bpp))  # (2) Number of bits per pixel
    f.write(struct.pack('<I', 0))  # (4) RGB, no compression
    f.write(struct.pack('<I', 16))  # (4) TODO Size of the raw data
    f.write(struct.pack('<I', 2835))  # (4) Horizontal print resolution per meter
    f.write(struct.pack('<I', 2835))  # (4) Vertical print resolution per meter
    f.write(struct.pack('<I', 0))  # (4) Number of colors in the palette
    f.write(struct.pack('<I', 0))  # (4) Important colors (0 means all)

    # Start of pixel array ('data_size')
    for i in reversed(range(len(data))):
        for j in range(len(data[i])):
            for value in reversed(data[i][j]):  # Should be RGB
                f.write(struct.pack('<B', value))
        f.write(padding)
    
    # BMP written!


g = (  0, 255,   0)  # green
b = (180, 100,  40)  # brown
d = ( 20,  20,  20)  # dark
w = (  0, 128, 255)  # water
s = (255, 255,   0)  # sun
e = (  0,   0,   0)  # empty
img = [
    [e, e, e, e, e, e, e, s, s, e],
    [e, e, e, e, e, e, e, s, s, e],
    [e, e, g, g, g, e, e, e, e, e],
    [e, e, g, g, g, e, e, e, e, e],
    [e, e, g, b, g, e, e, e, e, d],
    [e, e, e, b, e, e, e, e, w, d],
    [e, e, e, b, e, e, e, e, w, d],
    [e, e, e, b, e, e, e, w, d, d],
    [e, d, d, d, d, w, w, w, d, d],
    [d, d, d, d, d, d, d, d, d, d]
]

with open('tst.bmp', 'w+b') as f:
    encode_bmp(f,
               width=len(img[0]),
               height=len(img),
               data=img)
