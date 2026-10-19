#!/usr/bin/env python3
"""Build bitcheque-print.html: src/print.html with the BIP-39 word list, src/book.js and the wallet's WebAssembly
inlined, so the page is one file that runs from disk with no network. The wasm comes from a node checkout beside
this repo (../bitcheque-node or ../block, wallet-wasm built with `cargo build --release --target wasm32-unknown-unknown`).
The build is deterministic: the same sources and wasm give the same file, so anyone can check SHA256SUMS."""
import base64, hashlib, os
D = os.path.dirname(os.path.abspath(__file__))
WASM = next((p for p in (os.path.join(D, "..", r, "wallet-wasm/target/wasm32-unknown-unknown/release/bitcheque_web.wasm") for r in ("bitcheque-node", "block")) if os.path.exists(p)), None)
if not WASM: raise SystemExit("wallet wasm not found: build bitcheque-node/wallet-wasm first")
src = lambda f: open(os.path.join(D, "src", f)).read()
page = src("print.html")
for k, v in (("/*BIP39*/", src("bip39-en.js")), ("/*BOOK*/", src("book.js")), ("/*WASM*/", base64.b64encode(open(WASM, "rb").read()).decode())):
    assert page.count(k) == 1 and "</script" not in v, k
    page = page.replace(k, v)
out = os.path.join(D, "bitcheque-print.html")
open(out, "w").write(page)
h = hashlib.sha256(page.encode()).hexdigest()
open(os.path.join(D, "SHA256SUMS"), "w").write(f"{h}  bitcheque-print.html\n")
print(f"built bitcheque-print.html, {len(page):,} bytes, sha256 {h}")
