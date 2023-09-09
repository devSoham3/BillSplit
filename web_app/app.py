import os
import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
from main import Participant, Item, calculate_bill_share

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate_json', methods=['POST'])
def generate_json():
    participants_input = request.form.get('participants')
    item_names = request.form.getlist('item_name[]')  # Get a list of item names
    item_costs = request.form.getlist('item_cost[]')  # Get a list of item costs

    # Parse user input into lists
    participants_list = [{"name": name.strip()} for name in participants_input.split(',')]

    # Create a list of items with both name and cost
    items_list = []
    for name, cost in zip(item_names, item_costs):
        items_list.append({"name": name.strip(), "cost": float(cost)})

    # Create a JSON dictionary
    json_data = {
        "participants": participants_list,
        "items": items_list
    }

    # Write JSON data to a file
    with open('data.json', 'w') as json_file:
        json_file.write(json.dumps(json_data, indent=4))

    return redirect(url_for('home'))


@app.route('/get_json_data', methods=['GET'])
def get_json_data():
    try:
        with open('data.json', 'r') as json_file:
            json_data = json.load(json_file)
        return jsonify(json_data)
    except FileNotFoundError:
        return jsonify({"participants": [], "items": []})


@app.route('/enter_shares', methods=['GET', 'POST'])
def enter_shares():
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            participants_data = data["participants"]
            items_data = data["items"]

        participants = [Participant(participant_data["name"]) for participant_data in participants_data]
        items = [Item(item_data["name"], item_data["cost"]) for item_data in items_data]

        if request.method == 'POST':
            for participant in participants:
                for item in items:
                    share_key = f'{participant.name}_{item.name}'
                    share = float(request.form.get(share_key, 0.0))
                    participant.set_item_share(item.name, share)

            person_shares = calculate_bill_share(participants, items)
            return render_template('bill_summary.html', person_shares=person_shares)

        return render_template('enter_shares.html', participants=participants, items=items)
    except FileNotFoundError:
        return jsonify({"participants": [], "items": []})


@app.route('/calculate_bill', methods=['POST'])
def calculate_bill():
    try:
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
            participants_data = data["participants"]
            items_data = data["items"]

        participants = [Participant(participant_data["name"]) for participant_data in participants_data]
        items = [Item(item_data["name"], item_data["cost"]) for item_data in items_data]

        if request.method == 'POST':
            for participant in participants:
                for item in items:
                    share_key = f'{participant.name}_{item.name}'
                    share = float(request.form.get(share_key, 0.0))
                    participant.set_item_share(item.name, share)

            person_shares = calculate_bill_share(participants, items)
            return render_template('bill_summary.html', person_shares=person_shares)

        return render_template('enter_shares.html', participants=participants, items=items)
    except FileNotFoundError:
        return jsonify({"participants": [], "items": []})


if __name__ == '__main__':
    app.run(debug=True)
