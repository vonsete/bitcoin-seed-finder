#!/usr/bin/env python3
"""
Bitcoin Wallet Finder from 11-word seeds
Finds valid 12th words, generates wallets, and checks balances
"""

import sys
import time
import requests
import hashlib
from datetime import datetime
from mnemonic import Mnemonic
from hdwallet import HDWallet
from hdwallet.symbols import BTC

# Output file handle (global)
output_file = None

def log_print(message, console=True, file_only=False):
    """Print to console and/or file"""
    if console and not file_only:
        print(message)
    if output_file:
        output_file.write(message + "\n")
        output_file.flush()

def get_valid_12th_words(eleven_words):
    """
    Given 11 words, calculate all valid 12th words based on BIP39 checksum
    This is much faster than testing all 2048 words
    """
    mnemo = Mnemonic("english")
    wordlist = mnemo.wordlist

    # Convert words to indices
    words = eleven_words.split()
    if len(words) != 11:
        return []

    try:
        indices = [wordlist.index(w) for w in words]
    except ValueError:
        return []

    # Convert indices to bits (11 bits per word)
    bits = ""
    for idx in indices:
        bits += bin(idx)[2:].zfill(11)

    # We have 121 bits from 11 words
    # For a 12-word seed: 128 bits entropy + 4 bits checksum = 132 bits total
    # Word 12 needs: 7 bits entropy + 4 bits checksum = 11 bits

    valid_seeds = []

    # Try all 128 possible values for the last 7 bits of entropy
    for i in range(128):
        # Add the 7 bits of entropy
        entropy_bits = bits + bin(i)[2:].zfill(7)

        # Convert bits to bytes for hashing
        entropy_bytes = int(entropy_bits, 2).to_bytes(16, byteorder='big')

        # Calculate checksum: first 4 bits of SHA256
        hash_bytes = hashlib.sha256(entropy_bytes).digest()
        checksum_bits = bin(hash_bytes[0])[2:].zfill(8)[:4]

        # The 12th word is the last 7 entropy bits + 4 checksum bits
        last_word_bits = bin(i)[2:].zfill(7) + checksum_bits
        last_word_index = int(last_word_bits, 2)
        last_word = wordlist[last_word_index]

        # Create full seed phrase
        seed_phrase = f"{eleven_words} {last_word}"
        valid_seeds.append(seed_phrase)

    return valid_seeds

def generate_addresses(seed_phrase):
    """
    Generate Bitcoin addresses from a seed phrase
    Returns dict with different address types
    """
    addresses = {}

    try:
        # Legacy address (P2PKH) - m/44'/0'/0'/0/0
        hdwallet = HDWallet(symbol=BTC)
        hdwallet.from_mnemonic(seed_phrase)
        hdwallet.from_path("m/44'/0'/0'/0/0")
        addresses['legacy'] = hdwallet.p2pkh_address()

        # SegWit address (P2WPKH-in-P2SH) - m/49'/0'/0'/0/0
        hdwallet.clean_derivation()
        hdwallet.from_mnemonic(seed_phrase)
        hdwallet.from_path("m/49'/0'/0'/0/0")
        addresses['segwit'] = hdwallet.p2wpkh_in_p2sh_address()

        # Native SegWit address (P2WPKH) - m/84'/0'/0'/0/0
        hdwallet.clean_derivation()
        hdwallet.from_mnemonic(seed_phrase)
        hdwallet.from_path("m/84'/0'/0'/0/0")
        addresses['native_segwit'] = hdwallet.p2wpkh_address()

    except Exception as e:
        log_print(f"Error generating addresses: {e}")

    return addresses

def check_balance(address):
    """
    Check Bitcoin balance for an address using blockchain.info API
    Returns balance in BTC
    """
    try:
        url = f"https://blockchain.info/q/addressbalance/{address}"
        response = requests.get(url, timeout=1000)
        if response.status_code == 200:
            satoshis = int(response.text)
            btc = satoshis / 100000000
            return btc
        else:
            return None
    except Exception as e:
        return None

def check_balance_blockchair(address):
    """
    Alternative: Check balance using Blockchair API
    """
    try:
        url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            balance = data['data'][address]['address']['balance']
            btc = balance / 100000000
            return btc
        else:
            return None
    except Exception as e:
        return None

def process_file(filename):
    """
    Process input file with 11 words per line
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        log_print(f"Error: File '{filename}' not found")
        return

    total_lines = len(lines)
    log_print(f"Processing {total_lines} line(s) from {filename}\n")
    log_print("=" * 80)

    wallets_with_balance = []

    for idx, line in enumerate(lines, 1):
        eleven_words = line.strip()

        if not eleven_words or eleven_words.startswith('#'):
            continue

        word_count = len(eleven_words.split())
        if word_count != 11:
            log_print(f"\nLine {idx}: Invalid word count ({word_count}), skipping...")
            continue

        log_print(f"\n[Line {idx}/{total_lines}] Processing: {eleven_words[:50]}...")
        log_print("-" * 80)

        # Find valid 12th words
        valid_seeds = get_valid_12th_words(eleven_words)
        log_print(f"Found {len(valid_seeds)} valid seed phrase(s)")

        for seed_idx, seed in enumerate(valid_seeds, 1):
            last_word = seed.split()[-1]
            log_print(f"\n  [{seed_idx}] 12th word: '{last_word}'")
            log_print(f"  Full seed: {seed}")

            # Generate addresses
            addresses = generate_addresses(seed)

            if not addresses:
                log_print("  Failed to generate addresses")
                continue

            # Check balances
            found_balance = False
            wallet_info = {
                'seed': seed,
                'addresses': {},
                'total_balance': 0
            }

            for addr_type, address in addresses.items():
                msg = f"    {addr_type:15} : {address} ... "
                print(msg, end="", flush=True)
                if output_file:
                    output_file.write(msg)
                    output_file.flush()

                # Try blockchain.info first
                balance = check_balance(address)

                # If failed, try blockchair
                if balance is None:
                    time.sleep(2.0)  # Increased delay
                    balance = check_balance_blockchair(address)

                if balance is not None:
                    wallet_info['addresses'][addr_type] = {
                        'address': address,
                        'balance': balance
                    }
                    if balance > 0:
                        result_msg = f"💰 BALANCE: {balance:.8f} BTC"
                        log_print(result_msg, console=True, file_only=False)
                        found_balance = True
                        wallet_info['total_balance'] += balance
                    else:
                        log_print(f"Balance: 0 BTC")
                else:
                    log_print("Balance: Unable to check")

                time.sleep(1.5)  # Increased delay between requests

            if found_balance:
                log_print("\n  ⚠️  WALLET WITH BALANCE FOUND! ⚠️")
                wallets_with_balance.append(wallet_info)

        log_print("=" * 80)

    # Summary at the end
    if wallets_with_balance:
        log_print("\n" + "=" * 80)
        log_print("SUMMARY - WALLETS WITH BALANCE FOUND:")
        log_print("=" * 80)
        for idx, wallet in enumerate(wallets_with_balance, 1):
            log_print(f"\n[{idx}] Seed: {wallet['seed']}")
            log_print(f"    Total Balance: {wallet['total_balance']:.8f} BTC")
            for addr_type, info in wallet['addresses'].items():
                if info['balance'] > 0:
                    log_print(f"    {addr_type:15} : {info['address']} = {info['balance']:.8f} BTC")
        log_print("=" * 80)

def main():
    global output_file

    if len(sys.argv) < 2:
        print("Usage: python3 bitcoin_seed_finder.py <input_file> [output_file]")
        print("\nInput file format: Each line should contain 11 space-separated BIP39 words")
        print("Output file: Optional. If not specified, creates results_YYYYMMDD_HHMMSS.txt")
        sys.exit(1)

    filename = sys.argv[1]

    # Generate output filename
    if len(sys.argv) >= 3:
        output_filename = sys.argv[2]
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"results_{timestamp}.txt"

    # Open output file
    try:
        output_file = open(output_filename, 'w', encoding='utf-8')
        print(f"📄 Results will be saved to: {output_filename}\n")
    except Exception as e:
        print(f"Error creating output file: {e}")
        sys.exit(1)

    log_print("=" * 80)
    log_print("  Bitcoin Wallet Finder from 11-word Seeds")
    log_print("=" * 80)
    log_print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_print("\n⚠️  ETHICAL USE ONLY - For recovering your own lost wallets")
    log_print("⚠️  Unauthorized access to others' funds is illegal\n")

    try:
        process_file(filename)
    finally:
        log_print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log_print("\nProcessing complete!")

        if output_file:
            output_file.close()
            print(f"\n✅ Results saved to: {output_filename}")

if __name__ == "__main__":
    main()
