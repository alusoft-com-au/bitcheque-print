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

Reprinting a lost book works the same way: print only numbers above your last cheque used, and destroy the old
copy if it turns up.

## Build

The page is assembled from `src/` by `build.py`, which inlines the BIP-39 word list, `src/book.js` (the print code,
also used by the website) and the wallet's WebAssembly: the node's own Rust from
[bitcheque-node](https://github.com/alusoft-com-au/bitcheque-node)/`wallet-wasm`, so registrations are built by the
same code the chain checks them with.

```
git clone https://github.com/alusoft-com-au/bitcheque-node
(cd bitcheque-node/wallet-wasm && cargo build --release --target wasm32-unknown-unknown)
git clone https://github.com/alusoft-com-au/bitcheque-print
cd bitcheque-print && python3 build.py
```

The build is deterministic: the same sources and the same wallet wasm give the same file and the same `SHA256SUMS`.

This is an experimental research project; the network may change or be reset. MIT licence.
