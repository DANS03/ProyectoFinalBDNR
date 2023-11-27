from csv2json import convert, load_csv, save_json

def parseCsvToJson():
    with open('assets/flight_passengers.csv') as r, open('assets/flight_passengers.json', 'w') as w:
        convert(r, w)
