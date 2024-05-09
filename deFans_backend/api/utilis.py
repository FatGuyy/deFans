# Function to create a wallet
def createWallet():
    from bip_utils import Bip39MnemonicGenerator
    from web3 import Web3
    w3 = Web3()
    w3.eth.account.enable_unaudited_hdwallet_features()
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    wallet = w3.eth.account.from_mnemonic(str(mnemonic))
    # print("public key - ", wallet.address)
    # print("mnemonic - ", mnemonic)
    # print("private key - ", wallet.key.hex())
    return wallet, mnemonic
