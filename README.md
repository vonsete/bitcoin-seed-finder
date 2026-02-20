# Bitcoin Seed Finder 🔍

A Python tool to recover Bitcoin wallets from incomplete or complete BIP39 seed phrases. It supports both 11-word seeds (generates all valid 12th words) and 12-word seeds (validates and checks specific wallet), with advanced balance and transaction history checking.

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

- ✅ **Dual Mode Support**:
  - **11 words**: Generates all 128 valid 12th words (46x faster than brute force)
  - **12 words**: Validates seed checksum and checks specific wallet
- ✅ **Multiple Address Types**: Generates Legacy (P2PKH), SegWit (P2WPKH-in-P2SH), and Native SegWit (P2WPKH) addresses
- ✅ **Advanced Balance Checking**:
  - Multi-API fallback system (5 providers)
  - Transaction count tracking
  - Identifies wallets with past activity (even if balance is 0)
- ✅ **Resilient API System**: Automatic fallback between blockchain.info, blockstream.info, mempool.space, blockcypher.com, and blockchair.com
- ✅ **Transaction History**: Shows number of transactions for each address
- ✅ **Automatic Result Saving**: Saves all results to a timestamped file
- ✅ **Batch Processing**: Process multiple seeds from a single file (mix 11 and 12-word seeds)
- ✅ **Smart Detection**: Highlights wallets with transaction history even if current balance is zero

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

Create a text file (e.g., `seeds.txt`). You can mix both 11-word and 12-word seeds:

```text
# MODE 1: Incomplete seeds (11 words) - generates all valid 12th words
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon

# MODE 2: Complete seeds (12 words) - validates and checks specific wallet
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about

# You can mix both types in the same file
# Lines starting with # are comments and will be ignored
```

### 2. Run the Script

```bash
# Auto-generate output filename (results_YYYYMMDD_HHMMSS.txt)
python3 bitcoin_seed_finder.py seeds.txt

# Or specify custom output filename
python3 bitcoin_seed_finder.py seeds.txt my_results.txt
```

### 3. Check Results

**For 11-word seeds**, the script will:
- Calculate all 128 valid 12th words
- Check each resulting wallet (384 addresses total)

**For 12-word seeds**, the script will:
- Validate the seed checksum
- If valid, check only that specific wallet (3 addresses)
- If invalid, skip with error message

**For all wallets**, it will:
- Generate Bitcoin addresses (Legacy, SegWit, Native SegWit)
- Check balances and transaction counts
- Identify wallets with past activity
- Save all results to file
- Display summary of wallets with balance or transaction history

## 📊 Example Output

### 11-word seed (generates all possibilities):
```
[Line 1/1] Processing: abandon abandon abandon abandon...
Found 128 valid seed phrase(s)

  [1] 12th word: 'about'
  Full seed: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
    legacy          : 1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA ... Balance: 0 BTC | 📊 TXs: 46 (USED WALLET!) [via blockstream.info]
    segwit          : 37VucYSaXLCAsxYyAPfbSi9eh4iEcbShgf ... Balance: 0 BTC | 📊 TXs: 24 (USED WALLET!) [via blockstream.info]
    native_segwit   : bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu ... Balance: 0 BTC | 📊 TXs: 170 (USED WALLET!) [via blockstream.info]

  📊 WALLET WITH TRANSACTION HISTORY FOUND! 📊
```

### 12-word seed (validates and checks specific wallet):
```
[Line 1/1] Processing: abandon abandon abandon abandon...
✅ Valid 12-word seed phrase detected

  Full seed: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
    legacy          : 1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA ... Balance: 0 BTC | 📊 TXs: 46 (USED WALLET!) [via blockstream.info]
    segwit          : 37VucYSaXLCAsxYyAPfbSi9eh4iEcbShgf ... Balance: 0 BTC | 📊 TXs: 24 (USED WALLET!) [via blockstream.info]
    native_segwit   : bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu ... Balance: 0 BTC | 📊 TXs: 170 (USED WALLET!) [via blockstream.info]
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

- **API Rate Limiting**: 1 second delay between addresses
- **Multi-API Fallback**: Automatic failover across 5 public APIs:
  1. blockchain.info
  2. blockstream.info
  3. mempool.space
  4. blockcypher.com
  5. blockchair.com
- **No Private Keys Stored**: Script never saves private keys to disk
- **Local Processing**: All seed generation and validation happens locally
- **Resilient**: Continues working even when individual APIs are down or rate-limited

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
