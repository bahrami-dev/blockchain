import functools
import hashlib
from collections import OrderedDict

from hash_utility import hash_string_256, hash_block


mining_reward = 10
genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions': [],
        'proof': 100
    }
blockchain = [genesis_block]
open_transactions = []
owner = 'Mahdi'
participant = {'Mahdi'}


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
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
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    tx_received = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
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
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


def add_transaction(recipient, sender=owner, amount=1.0):

    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount,
    # }
    transaction = OrderedDict([('sender', sender), ('recipient', recipient), ('amount', amount)])

    if  verify_transaction(transaction):
        open_transactions.append(transaction)
        participant.add(sender)
        participant.add(recipient)
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
    reward_transaction = OrderedDict([('sender', 'someone'), ('recipient', owner), ('amount',mining_reward)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof,
    }
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
        if block['previous_hash'] != hash_block(blockchain[index -1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
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
    print('[h] Changing first block element!')
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
    elif user_input == '3':
        output_block()
    elif user_input == '4':
        print(participant)
    elif user_input == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transaction')
    elif user_input == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = genesis_block = {
                                'previous_hash': '',
                                'index': 0,
                                'transactions': [{
                                    'sender': 'mhd',
                                    'recipient': 'hmd',
                                    'amount': 100,
                                }],
                            }
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



