import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:
    
    def __init__(self):
        
        '''
        Initialize the blockchain with the genesis block
        '''
        
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
        
    
    def create_block(self, proof, previous_hash):
        
        '''        
        Create a new block and add it to the chain.
        
        Args:
            proof : int
                the proof of work number
                
            previous_hash : str
                the hash of the previous block
        
        Returns:
            dict 
                the new block
        '''
        
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)    
        return block
    
    
    def get_previous_block(self):
        
        '''
        Returns the last block in the chain
        '''
        
        return self.chain[-1]
    
    
    def proof_of_work(self, previous_proof):
        
        """
        Find a number such that the hash of the operation with the previous proof starts with '0000'.
        
        Args:
            previous_proof : int
                the previous block’s proof
        
        Returns:
            int 
                the new valid proof
        """
        
        
        new_proof = 1  #Nounce
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    
    def hash (self, block):
        
        '''
        Generates a SHA-256 
        
        Args:
            block : dict
                the block to be hashed
            
        Returns:
            str
                hash of the block

        '''
        
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    def is_chain_valid(self, chain):
        '''  
        Validates the blockchain by checking hashes and proofs
        
        Args:
            chain :list
                the blockchain
        
        Returns:
                bool 
                    True if valid, False otherwise
        '''
        
        previous_block = chain[0]
        block_index = 1
        
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
            
            return True
        
        
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender, 
                                  'receiver': receiver,
                                  'amount': amount})
            
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
        
        
    def add_node(self, adress):
        parsed_url = urlparse(adress)
        self.nodes.add(parsed_url.netloc)
            
        
    def replace_chain(self): #Protocolo de consenso
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
       

# FLASK SETUP
    
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

node_address = str(uuid4()).replace('-', '')


blockchain = Blockchain()
        
@app.route('/mine_block', methods = ['GET'])
def mine_block():

    '''
    Endpoint to mine a new block
    
    Returns:
        Response: json with mined block data
    '''    

    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address, receiver='Maria', amount=1)
    
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message' : 'Congrats, you mined a block',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transaction' : block['transactions']}
    
    return jsonify(response), 200  


@app.route('/get_chain', methods = ['GET'])
def get_chain():
    
    '''
    Endpoint to return the blockchain
    
    Returns:
        Response: JSON with the chain 
    '''
    
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    
    return jsonify(response), 200


@app.route('/is_valid', methods = ['GET'])
def is_valid():
    
    '''
    Endpoint to see if the blockchain is valid
    
    Returns:
        Response: JSON with the response
    '''
    
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid:
        response = {'message' : 'valid blockchain'}
    else:
        response = {'message' : 'blockchain isnt valid'}
        
    return jsonify(response), 200


@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    
    if not all(key in json for key in transaction_keys):
        return 'Missing keys', 400
    
    index = blockchain.add_transaction(sender=json['sender'], receiver=json['receiver'], amount=json['amount'])
    response = {'message': f'This transaction will be added to the block {index}'}
    return jsonify(response), 201
    

@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    
    if nodes is None:
        return 'Empty node', 400
    
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'Every node is connected',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201
    

@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    
    if is_chain_replaced:
        response = {'message': 'Nodes had a different chain, so they were replaced',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'Theres was no replacement',
                    'actual_chain': blockchain.chain}
    return jsonify(response), 201
        




app.run(host = '0.0.0.0', port = 5003)
    