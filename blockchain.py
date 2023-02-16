import functools
import hashlib
import json
import pickle

from hash_utility import hash_string_256, hash_block
from block import Block
from transaction import Transaction

mining_reward = 10
blockchain = []
open_transactions = []
owner = 'Mahdi'
participant = {'Mahdi'}

def load_data():
    global blockchain
    global open_transactions

    try:
        with open('blockchain.txt', mode='r') as f:
            
            # file_content = pickle.loads(f.read())
            # print(file_content)
            # global blockchain 
            # global open_transactions  
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']

            file_content = f.readlines()
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        genesis_block = Block(0, '', [], 100, 0)
    
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('How u doin ? :)')

load_data()

def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            savable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(savable_chain))
            f.write('\n')
            savable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(savable_tx))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving faild!')


def valid_proof(transactions, last_hash, proof):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    tx_received = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_received, 0)
    # amount_received = 0
    # for tx in tx_received:
    #     if len(tx) > 0:
    #         amount_received += tx[0]
    return amount_received - amount_sent


def last_element_of_blockchain():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def get_transaction_value():
    recipient = input('Please enter the name of recipient: ')
    amount = float(input('Please enter the transaction amount: '))
    return recipient, amount


def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


def add_transaction(recipient, sender=owner, amount=1.0):

    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount,
    # }
    transaction = Transaction(sender, recipient, amount)

    if  verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False

def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'someone',
    #     'recipient': owner,
    #     'amount': mining_reward
    # }
    reward_transaction = Transaction('someone', owner, mining_reward)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True

def output_block():
    for block in blockchain:
        print('Block output:')
        print(block)
    else:
        print('-' * 30)
        
def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index -1]):
            return False
        if not valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
            print('Proof of work is invalid!')
            return False
    return True 


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])

waiting_for_input = True

while waiting_for_input:
    print('-' * 40)
    print('[1] Add a transaction.')
    print('[2] mine a new block.')
    print('[3] Show outputing block.')
    print('[4] Show the participants')
    print('[5] Check transaction vadility')
    print('[q] Exit')
    print('-' * 40)
    user_input = input('Please choose of the options:')
    if user_input == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added Transaction')
        else:
            print('Transaction faild')
        print(open_transactions)
    elif user_input == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_input == '3':
        output_block()
    elif user_input == '4':
        print(participant)
    elif user_input == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transaction')
    elif user_input == 'q':
        waiting_for_input = False
    else:
        print('Your input is invalid! please choose again')

    if not verify_chain():
        print('Invalid Blockchain!')
        break
    print('Your tottal balance:')
    print('Balance of {}: {:6.2f}'.format('Max', get_balance('Mahdi')))
else:
    print('User left!')

print('Done!')



