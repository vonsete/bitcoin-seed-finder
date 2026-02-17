# Bitcoin Seed Finder

Script para encontrar la palabra #12 de una frase semilla BIP39 y verificar saldos en wallets Bitcoin.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

1. Crea un archivo de texto (por ejemplo `seeds.txt`) donde cada línea tenga 11 palabras:

```
abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon
word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11
# Líneas que empiezan con # son ignoradas
```

2. Ejecuta el script:

```bash
# Genera automáticamente el archivo de salida (results_YYYYMMDD_HHMMSS.txt)
python3 bitcoin_seed_finder.py seeds.txt

# O especifica tu propio archivo de salida
python3 bitcoin_seed_finder.py seeds.txt mis_resultados.txt
```

## Qué hace el script

1. **Calcula las palabras #12 válidas**: Encuentra todas las palabras posibles que crean un checksum válido
2. **Genera direcciones Bitcoin**: Para cada seed válida genera:
   - Legacy (P2PKH) - Direcciones que empiezan con "1"
   - SegWit (P2WPKH-in-P2SH) - Direcciones que empiezan con "3"
   - Native SegWit (P2WPKH) - Direcciones que empiezan con "bc1"
3. **Verifica saldos**: Usa APIs públicas (blockchain.info y Blockchair) para verificar si tienen fondos
4. **Guarda resultados**: Todos los resultados se guardan automáticamente en un archivo
5. **Resumen final**: Si encuentra wallets con saldo, muestra un resumen al final

## Mejoras implementadas

- ✅ **Delays aumentados**: 1.5-2 segundos entre requests para evitar rate limiting
- ✅ **Guardado automático**: Todos los resultados se guardan en archivo con timestamp
- ✅ **Resumen de wallets con saldo**: Al final muestra todas las wallets que tienen fondos
- ✅ **Soporte para comentarios**: Líneas que empiezan con # son ignoradas

## Salida de ejemplo

```
[Line 1/1] Processing: abandon abandon abandon abandon abandon...
--------------------------------------------------------------------------------
Found 8 valid seed phrase(s)

  [1] 12th word: 'about'
  Full seed: abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about
    legacy          : 1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA Balance: 0 BTC
    segwit          : 37VucYSaXLCAsxYyAPfbSi9eh4iEcbShgf Balance: 0 BTC
    native_segwit   : bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu Balance: 0 BTC
```

## ⚠️ Advertencias

- **USO ÉTICO SOLAMENTE**: Este script debe usarse solo para recuperar tus propias wallets perdidas
- Nunca intentes acceder a fondos que no te pertenecen
- Las APIs públicas tienen límites de tasa - el script incluye delays para respetarlos
- Guarda tu seed phrase de forma segura y nunca la compartas

## Notas técnicas

- Usa el estándar BIP39 para validación de semillas
- Genera direcciones según BIP44 (legacy), BIP49 (segwit), BIP84 (native segwit)
- Derivation paths: m/44'/0'/0'/0/0, m/49'/0'/0'/0/0, m/84'/0'/0'/0/0
- Rate limiting: 1.5 segundos entre requests, 2 segundos para reintentos
- Los resultados se guardan en tiempo real (flush después de cada escritura)
