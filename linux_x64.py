import os
import re

#Tested on Linux 9.1 and 9.3

# original bytes patterns with wildcards for offsets/jumps
# patch 1: SSL_get_verify_result check
# looking for: call [rax+F8h]; test eax, eax; jnz ...
pat1 = re.compile(b"\xff\x90\xf8\x00\x00\x00\x85\xc0\x0f\x85....", re.DOTALL)
sub1 = b"\xff\x90\xf8\x00\x00\x00\x85\xc0\x90\x90\x90\x90\x90\x90"

# patch 2: internal.hex-rays.com check
# looking for: repe cmpsb; setnbe al; sbb al, 0; test al, al; jz ...
pat2 = re.compile(b"\xf3\xa6\x0f\x97\xc0\x1c\x00\x84\xc0\x74.", re.DOTALL)
sub2 = b"\xf3\xa6\x0f\x97\xc0\x1c\x00\x84\xc0\x90\x90"

def patch():
    f = "libida.so"
    if not os.path.exists(f):
        print("err: libida.so not found here")
        return

    with open(f, "rb") as file:
        data = file.read()

    print("scanning for patterns...")
    
    # check if already patched
    if sub1 in data and sub2 in data:
        print("already patched. u good")
        return

    new_data = data
    
    m1 = pat1.search(data)
    if m1:
        print(f"found patch 1 at {hex(m1.start())}")
        new_data = pat1.sub(sub1, new_data)
    else:
        print("couldnt find patch 1 pattern")

    m2 = pat2.search(data)
    if m2:
        print(f"found patch 2 at {hex(m2.start())}")
        new_data = pat2.sub(sub2, new_data)
    else:
        print("couldnt find patch 2 pattern")

    if new_data != data:
        with open(f, "wb") as file:
            file.write(new_data)
        print("done. patched successfully")
    else:
        print("nothing changed. make sure you're using 9.x on Linux?")

if __name__ == "__main__":
    patch()
