import json


class Item:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def get_cost(self):
        return self.cost

    def get_name(self):
        return self.name


class Participant:
    def __init__(self, name):
        self.name = name
        self.item_shares = {}

    def set_item_share(self, item, share):
        self.item_shares[item] = share

    def get_item_share(self, item):
        return self.item_shares.get(item, 0.0)

    def get_name(self):
        return self.name


def calculate_bill_share(participants, items):
    person_shares = {}

    for participant in participants:
        participant_name = participant.get_name()
        total_share = 0.0

        for item in items:
            share = participant.get_item_share(item.get_name()) * item.get_cost()
            total_share += share

        person_shares[participant_name] = total_share

    return person_shares


def main():
    print("Welcome to the Bill Splitter!")

    with open("data.json", "r") as file:
        data = json.load(file)

    participants_data = data["participants"]
    items_data = data["items"]

    participants = [Participant(participant_data["name"]) for participant_data in participants_data]
    items = [Item(item_data["name"], item_data["cost"]) for item_data in items_data]

    for item in items_data:
        item_name = item["name"]
        print("=" * 50)
        print(item_name.upper())
        for participant in participants:
            share = float(input(f"{participant.get_name()}'s share: "))
            participant.set_item_share(item_name, share)

    person_shares = calculate_bill_share(participants, items)

    print("=" * 50)
    print("=" * 50)
    print("\nBILL SUMMARY:")
    for person, share in person_shares.items():
        formatted_share = "{:.2f}".format(share)
        print(f"{person} should pay: ${formatted_share}")


if __name__ == "__main__":
    main()
