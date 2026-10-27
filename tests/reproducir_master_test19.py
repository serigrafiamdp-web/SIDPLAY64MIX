#!/usr/bin/env python3
"""Reproducir exactamente el MASTER TEST19 a partir del TEST13 original.

Uso:
    python tests/reproducir_master_test19.py TEST13_13_SIDS_RETURN_FIX.d64 TEST19_MASTER.d64

No necesita herramientas externas; comprueba hashes, tamanos y solo dos bytes modificados.
"""
import argparse
import hashlib
from pathlib import Path

TEST13_SHA256 = "ecb884ca6fb125c34b644b540c677d61fb70d621bb7c0c52e4749376dadac58e"
TEST19_SHA256 = "b247f58ce9d3df87025d0f09ca145998bffe31e8f9e520c5c29dcfc238d66cc5"
PATCHES = ((0x2928F, 0x0A, 0x09), (0x29292, 0x01, 0x05))
IMAGE_BYTES = 174848

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("test13", type=Path, help="D64 base TEST13 (VICE PASS)")
    parser.add_argument("output", type=Path, help="D64 MASTER TEST19 a generar")
    args = parser.parse_args()
    src = args.test13.read_bytes()
    assert len(src) == IMAGE_BYTES, f"Tamaño incorrecto: {len(src)}"
    assert sha256(src) == TEST13_SHA256, "TEST13 no coincide con la base validada. No parchear."
    dst = bytearray(src)
    for index, old, new in PATCHES:
        assert dst[index] == old, f"Byte esperado {old:#x} en offset {index:#x}; hallado {dst[index]:#x}"
        dst[index] = new
    assert sum(a != b for a, b in zip(src, dst)) == 2
    assert sha256(dst) == TEST19_SHA256, "La imagen obtenida no coincide con el MASTER aprobado."
    args.output.write_bytes(dst)
    print(f"PASS -- master byte-identico: {args.output}")
    print(f"bytes={len(dst)}, SHA256={sha256(dst)}")
    print("Prefetch: desde 00:05 (TOD segundos). Timer final de Glenn sin modificar.")

if __name__ == "__main__":
    main()
