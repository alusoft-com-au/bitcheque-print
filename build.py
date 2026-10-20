#!/usr/bin/env python3
"""Build bitcheque-print.html: src/print.html with the BIP-39 word list, src/book.js and the wallet's WebAssembly
inlined, so the page is one file that runs from disk with no network.

The wasm is the one recorded in SHA256SUMS (bitcheque_web.wasm): a plain `python3 build.py` reuses the wasm inside the
current bitcheque-print.html and refuses one that does not match the record. A new wasm is taken only on request,
`python3 build.py --wasm PATH`, and only a reproducible build of it (see README: no local paths inside). The build is
deterministic: the same sources and wasm give the same file, so anyone can check SHA256SUMS."""
import base64, hashlib, os, re, sys
D = os.path.dirname(os.path.abspath(__file__))
OUT, SUMS = os.path.join(D, "bitcheque-print.html"), os.path.join(D, "SHA256SUMS")
sha = lambda b: hashlib.sha256(b).hexdigest()
rec = dict(l.split()[::-1] for l in open(SUMS) if l.strip()) if os.path.exists(SUMS) else {}
if "--wasm" in sys.argv:
    wasm = open(sys.argv[sys.argv.index("--wasm") + 1], "rb").read()
    if re.search(rb"/home/|/Users/|[A-Za-z]:\\\\Users\\\\", wasm):
        raise SystemExit("that wasm holds local file paths, so nobody else can rebuild it byte for byte: build it with the README's command")
else:
    old = open(OUT, "rb").read()
    wasm = base64.b64decode(re.search(rb"atob\('([A-Za-z0-9+/=]+)'\)", old).group(1))
    # the published page vouches for its wasm until SHA256SUMS records the wasm itself
    if rec.get("bitcheque_web.wasm", sha(wasm) if rec.get("bitcheque-print.html") == sha(old) else None) != sha(wasm):
        raise SystemExit("the wasm inside bitcheque-print.html does not match SHA256SUMS: restore it from git, or take a new one with --wasm PATH")
src = lambda f: open(os.path.join(D, "src", f)).read()
page = src("print.html")
for k, v in (("/*BIP39*/", src("bip39-en.js")), ("/*BOOK*/", src("book.js")), ("/*WASM*/", base64.b64encode(wasm).decode())):
    assert page.count(k) == 1 and "</script" not in v, k
    page = page.replace(k, v)
open(OUT, "w").write(page)
h = sha(page.encode())
open(SUMS, "w").write(f"{h}  bitcheque-print.html\n{sha(wasm)}  bitcheque_web.wasm\n")
print(f"built bitcheque-print.html, {len(page):,} bytes, sha256 {h}; wasm sha256 {sha(wasm)}")
