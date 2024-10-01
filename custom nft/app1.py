from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

headers = {
    "accept": "application/json",
    "x-api-key": "4ce150dabebc4eb4b53b7c86b7f29542"
}
def fetch_sales_data(contract_address, token_id):
    url = f"https://api.opensea.io/api/v2/events/chain/ethereum/contract/{contract_address}/nfts/{token_id}?event_type=sale&event_type=transfer"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {}, 0, 0, []
    data = response.json()
    sale_prices = []
    last_transaction = {}
    for event in data.get("asset_events", []):
        if event["event_type"] == "sale":
            sale_price_wei = int(event["payment"]["quantity"])
            sale_price_eth = sale_price_wei / 10**18
            last_transaction = {
                "seller": event["seller"],
                "buyer": event["buyer"],
                "priceETH": sale_price_eth
            }
            sale_prices.append(sale_price_eth)
    return last_transaction, max(sale_prices, default=0), min(sale_prices, default=0), sale_prices
# [Fetch functions remain unchanged]
def fetch_nft_image(contract_address, token_id):
    url = f"https://api.opensea.io/api/v2/chain/ethereum/contract/{contract_address}/nfts/{token_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        nft_data = response.json()
        return nft_data["nft"].get("display_image_url", "")
    return ""

@app.route('/')
def input_screen():
    return render_template('input1.html')

@app.route('/nft-details', methods=['POST'])
def nft_details():
    contract_address = request.form['contract_id']
    token_id = request.form['token_id']
    last_transaction, highest_price, lowest_price, sale_prices = fetch_sales_data(contract_address, token_id)
    image_url = fetch_nft_image(contract_address, token_id)
    nft = {
        "tokenId": token_id,
        "image": image_url,
        "lastTransaction": last_transaction,
        "highestPrice": highest_price,
        "lowestPrice": lowest_price,
        "salePrices": sale_prices
    }

    # Option 1: Process sale prices here
    sale_prices_list = ', '.join([str(round(price, 4)) for price in nft['salePrices']])

    return render_template('nft_details.html', nft=nft, sale_prices_list=sale_prices_list)

if __name__ == "__main__":
    app.run(debug=True)
