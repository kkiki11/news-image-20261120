"""Entry program for make.fun news-image-20261120.

Copies the bundled newspaper front page (repo/entry.png) to
/output/entry.png, verifying it byte for byte first: PNG magic bytes,
the 1 MiB size cap, and the expected SHA-256 digest. No network, no
randomness: two runs write identical bytes.
"""
import hashlib
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"
DEST = Path("/output/entry.png")
EXPECTED_SHA256 = "95168ca3f170f1199e8d178e5b4e47d6cf63c72e785063d525aa0fd4c3bde5e4"
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def main():
    data = SOURCE.read_bytes()
    if not data.startswith(PNG_MAGIC):
        return fail("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        return fail(f"entry.png is {len(data)} bytes, over the 1 MiB cap")
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        return fail(f"sha256 mismatch: expected {EXPECTED_SHA256}, got {digest}")
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_bytes(data)
    written = DEST.read_bytes()
    if hashlib.sha256(written).hexdigest() != digest:
        return fail("written file does not match the verified digest")
    print(f"wrote {DEST} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
