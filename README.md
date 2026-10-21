# Bitcheque Print

One HTML file for printing more cheques of a [Bitcheque](https://bitcheque.org) book on your own computer, offline.

A Bitcheque book has 256 cheques on one account number. You print as many as you need when you make the book,
and the rest later from the same 24-word seed. This page does the "later": type the seed, pick the cheques
(say 16 to 31), and it saves part A, part B and a public registration file for them.

## Use it

1. Download [`bitcheque-print.html`](bitcheque-print.html) (Raw → Save as) and check it against `SHA256SUMS`:
   `sha256sum bitcheque-print.html` (Linux), `shasum -a 256 bitcheque-print.html` (macOS),
   `certutil -hashfile bitcheque-print.html SHA256` (Windows).
2. Copy it to a clean computer, switch the internet off, and double-click it. It opens in your browser and
   needs no network: the wallet code, the word list and everything else are inside the file, and its content
   security policy blocks every network request.
3. Type your 24 words, check the lookup code matches your sheets, choose the cheques, and save the three files.
   Print part A and part B separately, then delete them and empty the trash.
4. Take the registration file (no secrets) to any online computer and open
   `https://bitcheque.org/onboard.html#register`. Each 16 cheques take a minute or two of computing.

Reprinting a lost book works the same way, but a reprint has exactly the same cells as the lost copy. If that copy
may be in someone else's hands, reprint only to move away: make a new book with a new seed and sweep the whole
balance to it with the next unused cheque, straight away.

## Build

The page is assembled from `src/` by `build.py`, which inlines the BIP-39 word list, `src/book.js` (the print code,
also used by the website) and the wallet's WebAssembly: the node's own Rust from
[bitcheque-node](https://github.com/alusoft-com-au/bitcheque-node)/`wallet-wasm`, so registrations are built by the
same code the chain checks them with.

`SHA256SUMS` records two hashes: the page, and the wasm inside it (`bitcheque_web.wasm`). A plain `python3 build.py`
reuses the recorded wasm and stops if it does not match; a new wasm is taken only with `--wasm PATH`. The website's
build checks that its own copy of the wasm is byte for byte the one inside this page.

### Rebuilding the wasm

The wasm is reproducible: the same node commit and the same Rust compiler give the same bytes on any machine.
Local paths are mapped to `.`, symbol names are stripped, and the wallet is built as a member of the node's
workspace, so where the repo is checked out never changes the bytes:

```
git clone https://github.com/alusoft-com-au/bitcheque-node && cd bitcheque-node
git checkout <node commit>
RUSTFLAGS="--remap-path-prefix=$PWD=. -C strip=symbols" \
  cargo build --locked --profile wasm -p bitcheque-web --target wasm32-unknown-unknown
sha256sum target/wasm32-unknown-unknown/wasm/bitcheque_web.wasm   # must equal SHA256SUMS
cd .. && git clone https://github.com/alusoft-com-au/bitcheque-print && cd bitcheque-print
python3 build.py --wasm ../bitcheque-node/target/wasm32-unknown-unknown/wasm/bitcheque_web.wasm
```

`build.py --wasm` refuses a wasm that still holds local paths (built without the flags above).

Current release:

| | |
|---|---|
| node commit | 004e2d8 |
| Rust | rustc 1.99.0 (b940084d7 2026-09-28), target wasm32-unknown-unknown |
| wasm sha256 | see `SHA256SUMS` (`bitcheque_web.wasm`) |

This is an experimental research project; the network may change or be reset. MIT licence.
