import struct
from pathlib import Path

def generate_mo(po_path: Path, mo_path: Path):
    lines = po_path.read_text(encoding="utf-8").splitlines()
    entries = {}
    current_msgid = None
    current_msgstr = None
    state = None

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("msgid "):
            if current_msgid is not None and current_msgstr is not None:
                entries[current_msgid] = current_msgstr
            current_msgid = line[6:].strip('"').replace('\\"', '"').replace('\\n', '\n')
            current_msgstr = ""
            state = "msgid"
        elif line.startswith("msgstr "):
            current_msgstr = line[7:].strip('"').replace('\\"', '"').replace('\\n', '\n')
            state = "msgstr"
        elif line.startswith('"') and line.endswith('"'):
            content = line[1:-1].replace('\\"', '"').replace('\\n', '\n')
            if state == "msgid":
                current_msgid += content
            elif state == "msgstr":
                current_msgstr += content

    if current_msgid is not None and current_msgstr is not None:
        entries[current_msgid] = current_msgstr

    # Sort entries by msgid
    sorted_keys = sorted(entries.keys())
    num_strings = len(sorted_keys)

    # Headers: 7 unsigned 32-bit ints (28 bytes)
    # Magic (0x950412de), version (0), count, orig_table_offset, trans_table_offset, hash_size (0), hash_offset (0)
    orig_table_offset = 28
    trans_table_offset = orig_table_offset + num_strings * 8
    strings_offset = trans_table_offset + num_strings * 8

    orig_table = []
    trans_table = []
    orig_data = bytearray()
    trans_data = bytearray()

    # Encode original strings
    curr_orig_pos = strings_offset
    for k in sorted_keys:
        b = k.encode("utf-8") + b"\x00"
        orig_table.append((len(b) - 1, curr_orig_pos))
        orig_data.extend(b)
        curr_orig_pos += len(b)

    curr_trans_pos = curr_orig_pos
    for k in sorted_keys:
        v = entries[k]
        b = v.encode("utf-8") + b"\x00"
        trans_table.append((len(b) - 1, curr_trans_pos))
        trans_data.extend(b)
        curr_trans_pos += len(b)

    header = struct.pack(
        "<Iiiiiii",
        0x950412DE,  # Magic
        0,           # Version
        num_strings,
        orig_table_offset,
        trans_table_offset,
        0,
        0,
    )

    orig_index = bytearray()
    for length, offset in orig_table:
        orig_index.extend(struct.pack("<ii", length, offset))

    trans_index = bytearray()
    for length, offset in trans_table:
        trans_index.extend(struct.pack("<ii", length, offset))

    mo_content = header + orig_index + trans_index + orig_data + trans_data
    mo_path.write_bytes(mo_content)
    print(f"Compiled {po_path} -> {mo_path} ({num_strings} strings)")

def compile_all():
    locales_dir = Path("locale")
    for po_file in locales_dir.rglob("*.po"):
        mo_file = po_file.with_suffix(".mo")
        generate_mo(po_file, mo_file)

if __name__ == "__main__":
    compile_all()
