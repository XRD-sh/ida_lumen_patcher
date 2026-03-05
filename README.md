**Original Forum Post**:
https://forum.xrd.sh/viewtopic.php?p=5#p5

# IDA Lumen Patcher (9.x)

Just some Python scripts to kill the TLS cert pinning in IDA Pro 9.x so you can use custom Lumen servers again.
https://github.com/naim94a/lumen

## The Fix

The network stack is baked into `libida.so` (Linux) and `ida.dll` (Windows) now. These scripts just scan the binaries for the gatekeeper jumps and NOP them out, or force the verification function to just return True.

Once you patch it, IDA will connect to your server and just trust whatever cert it gets.

## How to Use

You need Python 3 installed.

**IMPORTANT: MAKE A BACKUP FIRST!**
Seriously, before you do anything, manually copy your `libida.so` or `ida.dll` somewhere safe. The scripts try to create a `.bak` file for you automatically, but don't blame me if something goes wrong and your IDA gets bricked. BACK. IT. UP.

### Linux

1. Open your terminal in your IDA folder (e.g., `~/ida-pro-9.3`).
2. Drop `linux_x64.py` in there.
3. Run the patcher:
`python3 linux_x64.py`

### Windows

1. Open CMD or PowerShell **AS ADMIN** (since IDA is usually installed in protected folders like `C:\Program Files\`).
2. `cd` into your IDA folder.
3. Drop `windows_x64.py` in there.
4. Run the script:
`python windows_x64.py`

### After Patching

Restart/Open IDA, go to **Options -> Lumina**. Put in your custom host and port.


## Notes

If you update IDA or reinstall, it will overwrite the patched files with the official locked-down versions and you will have to run this again. The byte patterns are fuzzy though, so it should survive most minor 9.x updates.

Enjoy your server.
