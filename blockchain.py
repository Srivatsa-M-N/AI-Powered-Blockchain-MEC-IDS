import hashlib
import json
from datetime import datetime


class Block:

    def __init__(self, index, timestamp, data,
                 previous_hash):

        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash

        self.hash = self.calculate_hash()

    def calculate_hash(self):

        block_string = json.dumps(
            {
                "index": self.index,
                "timestamp": self.timestamp,
                "data": self.data,
                "previous_hash": self.previous_hash
            },
            sort_keys=True
        )

        return hashlib.sha256(
            block_string.encode()
        ).hexdigest()


class Blockchain:


    def __init__(self):
        try:
            with open("blockchain_log.json", "r") as f:
                data = json.load(f)

            self.chain = []

            for block_data in data:
                block = Block(
                    block_data["index"],
                    block_data["timestamp"],
                    block_data["data"],
                    block_data["previous_hash"]
                )

                block.hash = block_data["hash"]
                self.chain.append(block)

            if len(self.chain) == 0:
                self.chain = [self.create_genesis_block()]

            print(f"Loaded {len(self.chain)} blocks")

        except Exception:
            self.chain = [self.create_genesis_block()]
            self.save_chain()

    def create_genesis_block(self):
        genesis = Block(
            0,
            datetime.utcnow().isoformat(),
            "Genesis Block",
            "0"
        )
        genesis.hash = genesis.calculate_hash()
        return genesis
    def add_block(self, data):

     previous_block = self.chain[-1]

     new_block = Block(
        len(self.chain),
        datetime.utcnow().isoformat(),
        data,
        previous_block.hash
    )

     self.chain.append(new_block)

     self.save_chain()


    def save_chain(self):

       chain_data = []

       for block in self.chain:

        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })

       with open(
        "blockchain_log.json",
        "w"
      ) as f:

        json.dump(
            chain_data,
            f,
            indent=4
        )


    def get_chain(self):

     chain_data = []

     for block in self.chain:

        chain_data.append({
            "index": block.index,
            "timestamp": block.timestamp,
            "data": block.data,
            "previous_hash": block.previous_hash,
            "hash": block.hash
        })

     return chain_data
blockchain = Blockchain()
