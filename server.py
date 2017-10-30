from uuid import uuid4

from flask import Flask, jsonify, request

from blockchain import Blockchain

app = Flask(__name__)

node_id = str(uuid4())

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    blockchain.new_transaction(sender="0", recipient=node_id, amount=1)

    block = blockchain.new_block(proof)

    response = {
        'message': 'New block mined!',
        'index': block['index'],
        'transactions': block['transaction'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing parameters', 400

    index = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['amount']
    )
    response = {
        'message': f'Transaction accepted, will be added in block: {index}'
    }
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
