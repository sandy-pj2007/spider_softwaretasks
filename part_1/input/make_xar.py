import struct

with open("minimal.xar", "wb") as f:
    # Header (24 bytes total)

    f.write(b"XAR!")                    # magic
    f.write(struct.pack("<H", 1))       # version
    f.write(struct.pack("<H", 0))       # flags
    f.write(struct.pack("<I", 1234))    # archive_id
    f.write(struct.pack("<I", 16))      # metadata_size
    f.write(struct.pack("<I", 0))       # chunk_count
    f.write(struct.pack("<I", 40))      # chunk_area_offset

    # Metadata (16 bytes total)
    f.write(struct.pack("<I", 0))       # creator_offset
    f.write(struct.pack("<I", 0))       # comment_offset
    f.write(struct.pack("<I", 100))       # creator_length
    f.write(struct.pack("<I", 0))       # comment_length

print("Created minimal.xar")