### What are cryptographic hash functions?&nbsp;<div></div>
Mathematical algorithms that convert input data of any size into a fixed-length string (hash).

### What are the key properties of cryptographic hash functions?
-&nbsp;<b>one-way</b>: easy to compute forward, but extremely difficult to reverse (you have to guess)<br>-&nbsp;<b>deterministic</b>: same input = same hash<br>-&nbsp;<b>avalanche effect</b>: tiny changes produce completely different outputs<br>-&nbsp;<b>collision resistant</b>:&nbsp;extremely hard to find two inputs with same hash<br>-&nbsp;<b>fixed output size</b>: regardless of input size

### How are hash functions used in blockchain?
<li>Create unique identifiers for blocks</li>
<li>Link blocks together in chronological order</li>
<li>Verify data integrity without revealing actual data</li>
<li>Enable efficient merkle tree structures for transaction verification</li>

### What is SHA-256?
A widely adopted cryptographic hash function&nbsp;that converts any input into a fixed 256-bit output, typically displayed as a 64-character hexadecimal string.

### What is a rainbow table?
A precomputed lookup table containing millions of hash-to-plaintext mappings, used to quickly reverse cryptographic hashes and crack passwords. An easy defense is to use a salt (add unique random data before hashing).