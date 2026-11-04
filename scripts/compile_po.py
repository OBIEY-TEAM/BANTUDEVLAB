"""
Pure Python PO to MO compiler with proper empty msgid header (charset UTF-8) support
"""
import struct
import array
from pathlib import Path

def compile_po_to_mo(po_file_path, mo_file_path):
    po_path = Path(po_file_path)
    mo_path = Path(mo_file_path)

    with open(po_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    catalog = {}
    msgid = None
    msgstr = ''
    in_msgid = False
    in_msgstr = False

    for line in lines:
        line_s = line.strip()
        if not line_s or line_s.startswith('#'):
            if msgid is not None and in_msgstr:
                catalog[msgid] = msgstr
            in_msgid = False
            in_msgstr = False
            continue

        if line_s.startswith('msgid '):
            if msgid is not None and in_msgstr:
                catalog[msgid] = msgstr
            msgid = eval(line_s[6:])
            msgstr = ''
            in_msgid = True
            in_msgstr = False
        elif line_s.startswith('msgstr '):
            msgstr = eval(line_s[7:])
            in_msgid = False
            in_msgstr = True
        elif line_s.startswith('"'):
            val = eval(line_s)
            if in_msgid:
                msgid += val
            elif in_msgstr:
                msgstr += val

    if msgid is not None and in_msgstr:
        catalog[msgid] = msgstr

    # Ensure header msgid "" has Content-Type: text/plain; charset=UTF-8
    header_content = catalog.get('', '')
    if 'charset=' not in header_content.lower():
        catalog[''] = "Content-Type: text/plain; charset=UTF-8\n"

    # In GNU gettext, msgid "" must be the FIRST entry in the table
    other_keys = sorted([k for k in catalog.keys() if k != ''])
    keys = [''] + other_keys if '' in catalog else other_keys

    offsets = []
    ids = b''
    strs = b''

    for key in keys:
        trans = catalog[key]
        key_bytes = key.encode('utf-8') + b'\x00'
        trans_bytes = trans.encode('utf-8') + b'\x00'
        offsets.append((len(ids), len(key_bytes) - 1, len(strs), len(trans_bytes) - 1))
        ids += key_bytes
        strs += trans_bytes

    keystart = 7 * 4 + 16 * len(keys)
    valuestart = keystart + len(ids)

    koffsets = []
    voffsets = []
    for o1, l1, o2, l2 in offsets:
        koffsets += [l1, keystart + o1]
        voffsets += [l2, valuestart + o2]

    header = struct.pack(
        "Iiiiiii",
        0x950412de,  # magic
        0,           # format version
        len(keys),   # number of strings
        7 * 4,       # offset of table with original strings
        7 * 4 + len(keys) * 8,  # offset of table with translation strings
        0,           # size of hashing table
        0            # offset of hashing table
    )

    output = header + array.array("i", koffsets).tobytes() + array.array("i", voffsets).tobytes() + ids + strs

    mo_path.parent.mkdir(parents=True, exist_ok=True)
    with open(mo_path, 'wb') as f:
        f.write(output)

    print(f"Compiled {po_path} ({len(keys)} strings, header present: {'' in catalog}) -> {mo_path}")

if __name__ == '__main__':
    locales_dir = Path("locale")
    for lang in ["en", "sw", "pt", "fr"]:
        po = locales_dir / lang / "LC_MESSAGES" / "django.po"
        mo = locales_dir / lang / "LC_MESSAGES" / "django.mo"
        if po.exists():
            compile_po_to_mo(po, mo)
