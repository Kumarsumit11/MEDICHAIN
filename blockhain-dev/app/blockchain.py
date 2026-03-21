from web3 import Web3
import json
import hashlib
import os

GANACHE_URL = "http://127.0.0.1:7545"
ABI_PATH = os.path.join("abi", "contracts_FileHashStorage_sol_FileHashStorage.abi")

w3 = None
contract = None
account = None


def init_blockchain():
    global w3, contract, account

    if w3:
        return  # already initialized

    print("🔄 Initializing blockchain...")

    w3 = Web3(Web3.HTTPProvider(GANACHE_URL))

    if not w3.is_connected():
        raise Exception("❌ Ganache not running")

    with open(ABI_PATH) as f:
        abi = json.load(f)

    CONTRACT_ADDRESS = Web3.to_checksum_address("0xd8050c51A8f3be07557961be5ce710B7D3A7FB19")

    contract = w3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=abi
    )

    account = w3.eth.accounts[0]

    print("✅ Blockchain initialized")


def generate_file_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()


def store_hash_on_chain(file_hash: str):
    init_blockchain()
    tx = contract.functions.storeHash(file_hash).transact({
        "from": account
    })
    w3.eth.wait_for_transaction_receipt(tx)


def verify_hash_on_chain(file_hash: str) -> bool:
    init_blockchain()
    return contract.functions.verifyHash(file_hash).call()
