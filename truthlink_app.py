# truthlink_app.py – TruthLink: AI-Validated Factchain (Flask, Vercel)

from flask import Flask, jsonify, request, render_template_string
import hashlib
import json
import time
import os
from uuid import uuid4

CHAIN_FILE = 'truthlink_chain.json'
app = Flask(__name__)

class Block:
    def __init__(self, index, timestamp, claim_id, statement, sources, validation_level, ai_opinion, validator_signature, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.claim_id = claim_id
        self.statement = statement
        self.sources = sources
        self.validation_level = validation_level
        self.ai_opinion = ai_opinion
        self.validator_signature = validator_signature
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

class TruthLinkChain:
    difficulty = 3

    def __init__(self):
        self.queue = []
        self.chain = self.load_chain()

    def create_genesis_block(self):
        return [Block(0, time.time(), "GENESIS", "This is the root of TruthLink.", [], "absolute", "true", "root-signature", "0")]

    def last_block(self):
        return self.chain[-1]

    def submit_claim(self, statement, sources, validation_level, ai_opinion, validator_signature):
        claim_id = str(uuid4())
        self.queue.append({
            'claim_id': claim_id,
            'statement': statement,
            'sources': sources,
            'validation_level': validation_level,
            'ai_opinion': ai_opinion,
            'validator_signature': validator_signature
        })
        return claim_id

    def proof_of_work(self, block):
        block.nonce = 0
        hashed = block.compute_hash()
        while not hashed.startswith('0' * TruthLinkChain.difficulty):
            block.nonce += 1
            hashed = block.compute_hash()
        return hashed

    def add_block(self, block, proof):
        if self.last_block().hash != block.previous_hash:
            return False
        if not proof.startswith('0' * TruthLinkChain.difficulty):
            return False
        if proof != block.compute_hash():
            return False
        self.chain.append(block)
        self.save_chain()
        return True

    def mine_claim(self):
        if not self.queue:
            return False
        data = self.queue.pop(0)
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            claim_id=data['claim_id'],
            statement=data['statement'],
            sources=data['sources'],
            validation_level=data['validation_level'],
            ai_opinion=data['ai_opinion'],
            validator_signature=data['validator_signature'],
            previous_hash=self.last_block().hash
        )
        proof = self.proof_of_work(block)
        if self.add_block(block, proof):
            return block.index
        return False

    def save_chain(self):
        with open(CHAIN_FILE, 'w') as f:
            json.dump([b.__dict__ for b in self.chain], f, indent=4)

    def load_chain(self):
        if not os.path.exists(CHAIN_FILE):
            return self.create_genesis_block()
        with open(CHAIN_FILE, 'r') as f:
            return [Block(**b) for b in json.load(f)]

chain = TruthLinkChain()

@app.route('/')
def explorer():
    html = """
    <html><head><title>TruthLink Explorer</title><style>
    body { font-family: sans-serif; background: #f4f7fa; padding: 20px; }
    .block { background: white; padding: 15px; border-radius: 8px; margin: 10px 0; box-shadow: 0 0 5px rgba(0,0,0,0.1); }
    </style></head><body>
    <h1>📚 TruthLink – Blockchain of Verifiable Claims</h1>
    {% for block in chain %}
    <div class="block">
        <h3>Block #{{ block.index }}</h3>
        <p><b>Statement:</b> {{ block.statement }}</p>
        <p><b>Sources:</b> {{ block.sources }}</p>
        <p><b>Validation:</b> {{ block.validation_level }}</p>
        <p><b>AI Opinion:</b> {{ block.ai_opinion }}</p>
        <p><b>Validator Signature:</b> {{ block.validator_signature }}</p>
        <p><b>Hash:</b> {{ block.hash }}</p>
        <p><b>Previous Hash:</b> {{ block.previous_hash }}</p>
    </div>
    {% endfor %}
    </body></html>
    """
    return render_template_string(html, chain=chain.chain)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    required = ('statement', 'sources', 'validation_level', 'ai_opinion', 'validator_signature')
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400
    claim_id = chain.submit_claim(
        data['statement'], data['sources'], data['validation_level'],
        data['ai_opinion'], data['validator_signature']
    )
    return jsonify({'message': 'Claim submitted', 'claim_id': claim_id})

@app.route('/mine')
def mine():
    index = chain.mine_claim()
    return jsonify({'message': f'Block #{index} mined' if index is not False else 'No claims to mine'})

@app.route('/chain')
def full_chain():
    return jsonify([b.__dict__ for b in chain.chain])

app = app  # Vercel compatibility
