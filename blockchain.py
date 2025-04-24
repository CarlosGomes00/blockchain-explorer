import datetime
import hashlib
import json
from flask import Flask, jsonify

# BLOCKCHAIN

class Blockchain:
    
    def __init__(self):
        
        '''
        Initialize the blockchain with the genesis block
        '''
        
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    
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
                 'previous_hash': previous_hash}
        
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
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode().hexdigest())
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
            
            return True
       

# FLASK SETUP
    
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


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
    
    block = blockchain.create_block(proof, previous_hash)
    
    response = {'message' : 'congrats, you mined a block',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash']}
    
    return jsonify(response), 200  

@app.route('/get_chain', methods = ['GET'])

def get_chain():
    
    '''
    Endpoint to return the blockchain
    
    Returns:
        Response: JSON with the chain 
    '''
    
    response = {'chain' : blockchain.chain,
                'lenght' : len(blockchain.chain)}
    
    return jsonify(response), 200

app.run(host = '0.0.0.0', port = 5000)
    
    
    
    
    
    
    
    