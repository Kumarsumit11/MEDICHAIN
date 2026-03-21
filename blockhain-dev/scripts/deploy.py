from web3 import Web3
import json

GANACHE_URL = "http://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

assert w3.is_connected(), "Ganache not connected"

account = w3.eth.accounts[0]

with open("abi/contracts_FileHashStorage_sol_FileHashStorage.abi") as f:
    abi = json.load(f)

with open("abi/contracts_FileHashStorage_sol_FileHashStorage.bin") as f:
    bytecode = f.read()

contract = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = contract.constructor().transact({
    "from": account,
    "gas": 3_000_000   # 👈 IMPORTANT
})

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Contract deployed at:")
print(tx_receipt.contractAddress)
