from uuid import uuid4

from blockchain import Blockchain
from verification import Verification

class Node:
    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'Mahdi'
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        recipient = input('Please enter the name of recipient: ')
        amount = float(input('Please enter the transaction amount: '))
        return recipient, amount
    
    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input

    def print_blockchain_elements(self):
        for block in self.blockchain.get_chain():
            print('Block output:')
            print(block)
        else:
            print('-' * 30)
        
    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print('-' * 40)
            print('[1] Add a transaction.')
            print('[2] mine a new block.')
            print('[3] Show outputing block.')
            print('[4] Check transaction vadility')
            print('[q] Exit')
            print('-' * 40)
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print('Added Transaction')
                else:
                    print('Transaction faild')
                print(self.blockchain.get_open_transactions())
            elif user_choice == '2':
                self.blockchain.mine_block()
            elif user_choice == '3':
                self.print_blockchain_elements()
            elif user_choice == '4':
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transaction')
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Your input is invalid! please choose again')
            
            if not Verification.verify_chain(self.blockchain.get_chain()):
                print('Invalid Blockchain!')
                break
            print('Your tottal balance:')
            print('Balance of {}: {:6.2f}'.format(self.id, self.blockchain.get_balance()))
        else:
            print('User left!')

        print('Done!')

node = Node()
node.listen_for_input()