import webview
from flask import Flask, render_template, request
import requests

class WalletDataRetriever:
    def __init__(self, arbscan_api_key, bscscan_api_key):
        self.arbscan_api_key = arbscan_api_key
        self.bscscan_api_key = bscscan_api_key

    def get_arb_balance(self, wallet_address):
        url = f'https://api.arbiscan.io/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={self.arbscan_api_key}'
        response = requests.get(url)
        data = response.json()
        if data['status'] == '1':
            balance = int(data['result']) / 10**18  # Convert Wei to Ether
            return balance
        else:
            return None

    def get_bsc_balance(self, wallet_address):
        url = f'https://api.bscscan.com/api?module=account&action=balance&address={wallet_address}&tag=latest&apikey={self.bscscan_api_key}'
        response = requests.get(url)
        data = response.json()
        if data['status'] == '1':
            balance = int(data['result']) / 10**18  # Convert Wei to BNB
            return balance
        else:
            return None

    def get_arb_transactions(self, wallet_address, limit=10):
        url = f'https://api.arbiscan.io/api?module=account&action=txlist&address={wallet_address}&sort=desc&apikey={self.arbscan_api_key}'
        response = requests.get(url)
        data = response.json()
        if data['status'] == '1':
            transactions = data['result'][:limit]
            for tx in transactions:
                tx['amount'] = int(tx['value']) / 10**18  # Convert Wei to Ether
            return transactions
        else:
            return []

app = Flask(__name__)
retriever = WalletDataRetriever(
    arbscan_api_key='8537P29179IT9CMID4171AIV1UVV4ASN6P',
    bscscan_api_key='5SMD86272TWU3GRD64A6YIJHJZPYWHG897'
)

@app.route('/')
def index():
    return render_template('input3.html')

@app.route('/get_wallet_data', methods=['POST'])
def get_wallet_data():
    wallet_address = request.form['wallet_address']
    eth_balance = retriever.get_arb_balance(wallet_address)
    bnb_balance = retriever.get_bsc_balance(wallet_address)
    transactions = retriever.get_arb_transactions(wallet_address)

    return render_template(
        'display.html',
        eth_balance=eth_balance,
        bnb_balance=bnb_balance,
        transactions=transactions
    )

if __name__ == '__main__':
    # Create Flask web server in a separate thread
    webview.create_window("O-Block Wallet", "http://127.0.0.1:5000")
    app.run(debug=True)
