from eth_account import Account

account = Account.create()
print("private key - ", account.key)
print("publix key - ", account.address)

Account.enable_unaudited_hdwallet_features()
acc, mnemonic = Account.create_with_mnemonic()
print("mnemonic - ",mnemonic)
print("private key - ", acc.key)
print("publix key - ", acc.address)
