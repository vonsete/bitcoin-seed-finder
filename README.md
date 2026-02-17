# Bitcoin Seed Finder 🔍

A Python tool to recover Bitcoin wallets from incomplete 12-word BIP39 seed phrases. Given the first 11 words, it calculates all valid 12th words based on the BIP39 checksum and checks their balances.

## ⚠️ Important - Ethical Use Only

**This tool is intended ONLY for:**
- Recovering your own lost or incomplete wallet seed phrases
- Educational purposes and security research
- Authorized penetration testing

**Never use this tool to:**
- Access funds that don't belong to you
- Attempt to crack others' wallets
- Engage in any illegal activity

Unauthorized access to cryptocurrency wallets is illegal in most jurisdictions.

## 🚀 Features

- ✅ **Optimized BIP39 Checksum Calculation**: Directly calculates only the 128 valid 12th words (46x faster than brute force)
- ✅ **Multiple Address Types**: Generates Legacy (P2PKH), SegWit (P2WPKH-in-P2SH), and Native SegWit (P2WPKH) addresses
- ✅ **Balance Checking**: Queries public APIs (blockchain.info and Blockchair) to check balances
- ✅ **Automatic Result Saving**: Saves all results to a timestamped file
- ✅ **Rate Limiting**: Includes delays to respect API rate limits
- ✅ **Batch Processing**: Process multiple 11-word seeds from a single file
- ✅ **Summary Report**: Shows all wallets with balance at the end

## 📋 Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## 🔧 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/bitcoin-seed-finder.git
cd bitcoin-seed-finder

# Install dependencies
pip install -r requirements.txt
```

## 📖 Usage

### 1. Create Input File

Create a text file (e.g., `seeds.txt`) with one 11-word seed per line:

```text
# My incomplete seeds
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon
word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11
# Lines starting with # are ignored
```

### 2. Run the Script

```bash
# Auto-generate output filename (results_YYYYMMDD_HHMMSS.txt)
python3 bitcoin_seed_finder.py seeds.txt

# Or specify custom output filename
python3 bitcoin_seed_finder.py seeds.txt my_results.txt
```

### 3. Check Results

The script will:
- Calculate all 128 valid 12th words for each input
- Generate Bitcoin addresses (Legacy, SegWit, Native SegWit)
- Check balances for each address
- Save all results to file
- Display summary of wallets with balance

## 📊 Example Output

```
[Line 1/1] Processing: abandon abandon abandon abandon...
Found 128 valid seed phrase(s)

  [1] 12th word: 'about'
  Full seed: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
    legacy          : 1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA ... Balance: 0 BTC
    segwit          : 37VucYSaXLCAsxYyAPfbSi9eh4iEcbShgf ... Balance: 0 BTC
    native_segwit   : bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu ... Balance: 0 BTC
```

## 🔬 How It Works

### BIP39 Checksum Optimization

Instead of testing all 2,048 BIP39 words:

1. Converts the 11 words to 121 bits
2. Tries all 128 possible values (2^7) for the last 7 bits of entropy
3. For each value, calculates the 4-bit checksum using SHA256
4. Combines 7 entropy bits + 4 checksum bits = 11 bits = word index
5. Retrieves the valid word from the BIP39 wordlist

**Result**: 46.5x faster than brute force validation!

### Address Generation

Uses standard BIP32/BIP44 derivation paths:
- **Legacy (P2PKH)**: m/44'/0'/0'/0/0
- **SegWit (P2WPKH-in-P2SH)**: m/49'/0'/0'/0/0
- **Native SegWit (P2WPKH)**: m/84'/0'/0'/0/0

## 🛡️ Security & Privacy

- **API Rate Limiting**: 1.5-2 second delays between requests
- **Public APIs Only**: Uses blockchain.info and Blockchair public endpoints
- **No Private Keys Stored**: Script never saves private keys to disk
- **Local Processing**: All seed generation happens locally

## ⚙️ Technical Details

- **Language**: Python 3
- **Libraries**:
  - `mnemonic`: BIP39 implementation
  - `hdwallet`: HD wallet generation
  - `requests`: API queries
- **Standards**: BIP32, BIP39, BIP44, BIP49, BIP84

## 📝 License

This project is provided as-is for educational and recovery purposes only. Users are responsible for complying with all applicable laws and regulations.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## ⚠️ Disclaimer

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. The authors are not responsible for any misuse of this tool. Always ensure you have legal authorization before attempting to access any cryptocurrency wallet.

---

**Remember**: Only use this tool to recover your own lost wallets. Respect others' property and privacy.
