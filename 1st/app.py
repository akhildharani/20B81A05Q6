from flask import Flask, request, jsonify
import requests
import asyncio

app = Flask(__name__)

async def fetch_numbers(url):
    try:
        response = await asyncio.wait_for(requests.get(url), timeout=0.5)
        data = response.json()
        if "numbers" in data and isinstance(data["numbers"], list):
            return data["numbers"]
    except (requests.Timeout, requests.RequestException, asyncio.TimeoutError):
        pass
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [fetch_numbers(url) for url in urls]
    results = loop.run_until_complete(asyncio.gather(*tasks))
    loop.close()

    merged_numbers = sorted(list(set([num for sublist in results for num in sublist])))
    return jsonify({"numbers": merged_numbers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
