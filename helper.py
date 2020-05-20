import  json
def empty_ledger():

    with open("ledger.json", "w") as file:
        json.dump([],file)