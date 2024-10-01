from flask import Flask, render_template, jsonify
import requests
import json

app = Flask(__name__)

# Define the GraphQL endpoint and API key
API_URL = "https://gateway.thegraph.com/api/16df08424acf103e9641579caf1d68e4/subgraphs/id/GSjXo5Vd1EPaMGRJBYe6HoBKv7WSq3miCrRRZJbTCHkT"

# GraphQL query to fetch the first 20 trades
query = """
{
  collection(id: "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d") {
    trades(first: 20) {
      tokenId
      priceETH
      seller
      buyer
    }
  }
}
"""

# Function to fetch NFT image by token ID
def fetch_nft_image(token_id):
    url = f"https://api.opensea.io/api/v2/chain/ethereum/contract/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/nfts/{token_id}"
    headers = {"accept": "application/json", "x-api-key": "4ce150dabebc4eb4b53b7c86b7f29542"}
    response = requests.get(url, headers=headers)
    nft_data = response.json()
    return nft_data["nft"]["display_image_url"]

# Function to fetch sale and transfer data from OpenSea API
def fetch_sale_data(token_id):
    url = f"https://api.opensea.io/api/v2/events/chain/ethereum/contract/0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d/nfts/{token_id}?event_type=sale&event_type=transfer"
    headers = {"accept": "application/json", "x-api-key": "4ce150dabebc4eb4b53b7c86b7f29542"}
    response = requests.get(url, headers=headers)
    data = response.json()

    sale_prices = []
    for event in data["asset_events"]:
        if event["event_type"] == "sale":
            sale_price_wei = int(event["payment"]["quantity"])
            sale_price_eth = sale_price_wei / 10**18
            sale_prices.append(sale_price_eth)

    return sale_prices

# Function to fetch trade data from The Graph
def fetch_data():
    response = requests.post(API_URL, json={'query': query})
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Query failed with a {response.status_code}: {response.text}")

# Route to fetch NFT data and send it to the front end
@app.route('/nft_data')
def get_nft_data():
    data = fetch_data()
    trades = data['data']['collection']['trades']
    nfts = []
    
    for trade in trades:
        token_id = trade['tokenId']
        price_eth = float(trade['priceETH'])
        
        # Fetch sale data from OpenSea API for this token
        sale_prices = fetch_sale_data(token_id)
        
        # Fetch the image URL
        image_url = fetch_nft_image(token_id)
        
        # Add new NFT to the list
        nfts.append({
            "tokenId": token_id,
            "image": image_url,
            "lastTransaction": {
                "seller": trade['seller'],
                "buyer": trade['buyer'],
                "priceETH": price_eth
            },
            "salePrices": sale_prices
        })
    
    return jsonify(nfts)

# Serve the main page with the HTML template
@app.route('/')
def index():
    return render_template('index2.html')

if __name__ == "__main__":
    app.run(debug=True)
