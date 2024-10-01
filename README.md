"# the-graph-protocol"
  NFT and Wallet Data Web Application

to run the program open all the program file!

This project is a Flask-based web application that fetches NFT trade data from The Graph and OpenSea APIs and retrieves wallet balances and transactions from Arbitrum and Binance Smart Chain using the Arbiscan and BscScan APIs.

 #Features
- Display latest NFT trade information for a specific collection.
- Fetch sale and transfer data for individual NFTs.
- Retrieve balances and transaction data for Ethereum (on Arbitrum) and Binance Smart Chain wallets.
- Displays wallet information on a simple front-end.

#Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)
- [Contact](#contact)

 #Installation

1. Clone the repository
   ```bash
   git clone https://github.com/sakthitdev/the-graph-protocol.git
   cd project-name
#Create and activate a virtual environment

bash

python3 -m venv venv
source venv/bin/activate

#Install dependencies

bash

pip install -r requirements.txt

#Create an index.html file Add a simple HTML template to display NFT data. Example:

html

<!DOCTYPE html>
<html>
<head>
    <title>NFT and Wallet Data</title>
</head>
<body>
    <h1>NFT Trades</h1>
    <div id="nft-data"></div>
    <script>
        fetch('/nft_data')
            .then(response => response.json())
            .then(data => {
                document.getElementById('nft-data').innerHTML = JSON.stringify(data, null, 2);
            });
    </script>
</body>
</html>

#Obtain API keys

For OpenSea: Sign up for an API key here.
For Arbiscan and BscScan: Obtain keys from Arbiscan and BscScan.

#Run the application

pip install Flask
pip install requests
pip install pywebview

python

API_URL = "https://gateway.thegraph.com/api/your-api-key/subgraphs/id/your-subgraph-id"

#OpenSea API Key
Replace your OpenSea API key in the fetch_nft_image and fetch_sale_data functions:

python

headers = {"accept": "application/json", "x-api-key": "your-opensea-api-key"}

#Arbiscan and BscScan API Keys
Ensure you set the correct Arbiscan and BscScan API keys in the WalletDataRetriever class:

python

arbscan_api_key='your-arbiscan-api-key',
bscscan_api_key='your-bscscan-api-key'

#Usage
NFT Data

The /nft_data endpoint fetches the latest 20 trades for the specified NFT collection and displays them, including details like token ID, price in ETH, seller, buyer, and sale prices.
It also fetches the image and sale history of each NFT from OpenSea.
Wallet Data

Enter a wallet address to retrieve its ETH and BNB balances, as well as recent transactions from Arbitrum and Binance Smart Chain.

#Example Use Case:
Access the app at http://127.0.0.1:5000.
Enter a wallet address in the input form to see balances and recent transactions.
Navigate to /nft_data to see the latest NFT trades.
Project Structure
graphql

.
├── app.py                      # Main Flask application
├── wallet_data_retriever.py     # Logic for retrieving wallet data
├── templates/
│   ├── index.html               # Main HTML page for displaying wallet input form
│   └── display.html             # Page for showing wallet balance and transactions
└── README.md                    # Project documentation (this file)
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contact
For any questions or suggestions, feel free to contact:

Your Name - sakthit2005@gmail.com
GitHub: https://github.com/sakthitdev



