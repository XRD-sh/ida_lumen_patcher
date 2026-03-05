import os
import re

pat_func = b"\x40\x56\x57\x48\x81\xec\x88\x04\x00\x00"
sub_func = b"\xb8\x01\x00\x00\x00\xc3\x90\x90\x90\x90"


pat_jump = re.compile(b"...", re.DOTALL) 

def patch():
    f = "ida.dll"
    if not os.path.exists(f):
        print("err: ida.dll not found here bro")
        return

    with open(f, "rb") as file:
        data = bytearray(file.read())

    print("scanning for windows patterns...")
    
    patched = False

    idx = data.find(pat_func)
    if idx != -1:
        data[idx:idx+len(sub_func)] = sub_func
        print("applied global bypass patch")
        patched = True
    else:
        print("couldnt find func pattern")

    for match in pat_jump.finditer(data):
        jnz_idx = match.start() + 10
        if data[jnz_idx] == 0x75:
            data[jnz_idx] = 0xeb
            print("patched gatekeeper jump")
            patched = True

    if not patched:
        print("nothing got patched. maybe wrong version or already done?")
        return

    # backup and save
    bak = f + ".bak"
    if not os.path.exists(bak):
        with open(bak, "wb") as b:
            with open(f, "rb") as orig:
                b.write(orig.read())
        print("backed up original dll")
        
    with open(f, "wb") as file:
        file.write(data)
        
    print("done. lumina should be working now")

if __name__ == "__main__":
    patch()
