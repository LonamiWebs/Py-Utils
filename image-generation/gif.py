#!/usr/bin/python3

import re
import struct


# NOTE: For some reason, `encode_gif` fails with some sizes.
# For example, a image of 10x30 will fail. To reproduce
# the bug, extend the example `img` below 3 times.


def convert_little_endian_9bits(nbits):
    """Converts nine-bit long "bytes" to eight-bit bytes on a little-endian like format.
       Source: https://en.wikipedia.org/wiki/GIF#Image_coding"""
    left = ''
    result = []
    for n in nbits:
        b = bin(n)[2:].zfill(9)

        if len(left) == 8:
            # Left makes a full new byte, so write and clear it
            result.append(left)
            left = ''

        # We need to take 8 bits - length of left
        # So we skip 1 (9 - 1) + len(left)
        take = 1 + len(left)
        result.append(b[take:] + left)

        # Now, we've used that left bit, but we're left with more
        left = b[:take]

    # If we're left with anything, pad with 0 (equals to do nothing)
    if left:
        result.append(left.zfill(8))

    # Fix the result
    return [int(s, base=2) for s in result]


def encode_gif(handle, width, height, palette, image_indices_bytes, transparent_index=None):
    if width.bit_length() > 16:
        raise ValueError('The width must be a 16-bit number.')

    if height.bit_length() > 16:
        raise ValueError('The height must be a 16-bit number.')

    if len(palette) != 256:
        raise ValueError('The palette must contain 256 colors as a ternary tuple (R, G, B) each.')

    if len(image_indices_bytes) != width * height:
        raise ValueError('The amount of indices does not match the file dimensions.')
    
    # (6) Header
    handle.write(b'GIF89a')

    # Logical Screen Descriptor
    handle.write(struct.pack('<H', width))  # (2) Width in pixels
    handle.write(struct.pack('<H', height))  # (2) Height in pixels
    handle.write(struct.pack('<B', 0xF7))  # (1) Stuff
    handle.write(struct.pack('<B', 0))  # (1) Background color index
    handle.write(struct.pack('<B', 0))  # (1) Pixel aspect ratio

    # Global Color Table
    for r, g, b in palette:
        handle.write(struct.pack('<B', r))  # R
        handle.write(struct.pack('<B', g))  # G
        handle.write(struct.pack('<B', b))  # B

    handle.write(struct.pack('>H', 0x21F9))  # (2) Graphic Control Extension
    handle.write(struct.pack('<B', 4))  # (1) 4 bytes of GCE data follow
    
    # (1) Transparent bit
    if transparent_index is None:
        handle.write(struct.pack('<B', 0))
    else:
        handle.write(struct.pack('<B', 1))
    handle.write(struct.pack('<H', 0))  # (2) Animation delay (not used)
    
    # (1) The index of the transparent color
    if transparent_index is None:
        handle.write(struct.pack('<B', 0))
    else:
        handle.write(struct.pack('<B', transparent_index))
    handle.write(struct.pack('<B', 0))  # (1) End of block

    handle.write(struct.pack('<B', 0x2C))  # Image Descriptor
    handle.write(struct.pack('<H', 0))  # (2) Start corner X
    handle.write(struct.pack('<H', 0))  # (2) Start corner Y
    handle.write(struct.pack('<H', width))  # (2) End corner X
    handle.write(struct.pack('<H', height))  # (2) End corner Y
    handle.write(struct.pack('<B', 0))  # (1) No local color table

    # Start of image
    handle.write(struct.pack('<B', 8))

    # Convert the nine bits of the image_indices_bytes to eight bits
    nine_bits = [0x100]  # Start of uncompressed data
    for index in image_indices_bytes:
        nine_bits.append(index)
    nine_bits.append(0x101)  # End of uncompressed data
    eight_bits = convert_little_endian_9bits(nine_bits)

    # In chunks of 255 bytes
    chunk_count = (len(eight_bits) + 254) // 255
    for i in range(chunk_count):
        chunk = eight_bits[i * 255:(i + 1) * 255]
        
        # (1) n bytes of uncompressed data follows
        handle.write(struct.pack('<B', len(chunk)))
        # Write the actual data
        handle.write(bytes(chunk))
    handle.write(struct.pack('<B', 0))  # (1) End

    handle.write(struct.pack('<B', 0x3B))  # (1) GIF file terminator


from random import randint
pal = [(j, j, j) for j in range(256)]
img = [
    [  0,   0,   0,   0,   0,   0,   0, 200, 200,   0],
    [  0,   0,   0,   0,   0,   0, 200, 200, 200, 200],
    [  0,   0, 255, 255, 255,   0,   0,   0,   0,   0],
    [  0,   0, 255, 255, 255,   0,   0,   0,   0,   0],
    [  0,   0, 255, 120, 255,   0,   0,   0,   0,  50],
    [  0,   0,   0, 120,   0,   0,   0,   0,   0,  50],
    [  0,   0,   0, 120,   0,   0,   0,   0,   0,  50],
    [  0,   0,   0, 120,   0,   0,   0,   0,  50,  50],
    [  0,   0,  50,  50,  50,   0,   0,   0,  50,  50],
    [ 50,  50,  50,  50,  50,  50,  50,  50,  50,  50]
    
]
flat_img = [item for sublist in img for item in sublist]
with open('test.gif', 'w+b') as f:
    encode_gif(f,
               width=len(img[0]),
               height=len(img),
               palette=pal,
               image_indices_bytes=flat_img)

