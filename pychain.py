# PyChain Ledger
# Imports
import pwd
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

# Create a Record Data Class
# Create a Record Data Class that consists of the `sender`, `receiver`, and
# `amount` attributes

@dataclass
class Record:
    sender: str
    receiver: str
    amount: float

# Modify the Existing Block Data Class to Store Record Data
# Set the data type of the `record` attribute to `Record`.

@dataclass
class Block:
    record: Record

    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()

# Create pychain data class

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

# Adds the cache decorator for Streamlit
@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

# Add markdown on streamlit app
st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

# Add Relevant User Inputs to the Streamlit Interface

# Create these input areas to capture the sender, receiver, and
# amount for each transaction that you’ll store in the `Block` record.

# Add an input area where you can get a value for `sender` from the user.
sender = st.text_input("Sender")

# Add an input area where you can get a value for `receiver` from the user.
receiver = st.text_input("Receiver")

# Add an input area where you can get a value for `amount` from the user.
amount = st.text_input("Enter amount")

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Update `new_block` so that `Block` consists of an attribute named `record`
    new_block = Block(
        record=Record,
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()


# Streamlit Code for ledger dataframe

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

# Set pychain difficulty
difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

# Create sidebar block inspector for the pychain
st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

# Create button to validate pychain
if st.button("Validate Chain"):
    st.write(pychain.is_valid())
