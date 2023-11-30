import json
from pymongo import database
from services.dgraph import Dgraph


class FlightsRepo:
    dbMongo: database
    dbDgraph: Dgraph

    def __init__(self, dbMongo, dbDgraph):
        self.dbMongo = dbMongo
        self.dbDgraph = dbDgraph

    

    def getNumOfFlightsPerAirportMongo(self):
        query = [{"$group": {"_id": "$from", "totalFlights": {"$sum": 1}}}]
        result = self.dbMongo.passengers_data.aggregate(query)

        for entry in result:
            print(f"Airport: {entry['_id']}, Total flights: {entry['totalFlights']}")

    def getNumOfFlightsPerAirportWithPrefixMongo(self, prefix: str):
        query = [
            {"$match": {"from": prefix}},
            {"$group": {"_id": "$from", "totalFlights": {"$sum": 1}}},
        ]
        result = self.dbMongo.passengers_data.aggregate(query)

        for entry in result:
            print(f"Airport: {entry['_id']}, Total flights: {entry['totalFlights']}")

    def getIdeaOfOpeningARestaurantMongo(self):
        collection = self.dbMongo.passengers_data
        after_eating_hours = [8, 16, 20]

        queryConnection = [
            {"$match": {"connection": True}},
            {"$group": {"_id": "$from", "totalFlightsWithConnection": {"$sum": 1}}},
        ]

        queryHours = [
            {"$match": {"departure": {"$in": after_eating_hours}}},
            {"$group": {"_id": "$from", "totalFlights": {"$sum": 1}}},
        ]

        resultConnection = collection.aggregate(queryConnection)
        resultHours = collection.aggregate(queryHours)

        flights_with_connection = {
            entry["_id"]: entry["totalFlightsWithConnection"]
            for entry in resultConnection
        }
        flights_with_departure = {
            entry["_id"]: entry["totalFlights"] for entry in resultHours
        }

        for airport, total_flights in flights_with_connection.items():
            total_flights_departure = flights_with_departure.get(airport, 0)
            if total_flights + total_flights_departure > 10:
                print(
                    f"Airport: {airport}, Total flights with connection = true: {total_flights}, Total flights with departure at 8, 16, and 20: {total_flights_departure} ---->New restaurant needed!!!"
                )
            else:
                print(
                    f"Airport: {airport}, Total flights with connection = true: {total_flights}, Total flights with departure at 8, 16, and 20: {total_flights_departure}"
                )

    def getIdeaOfOpeningARestaurantWithPrefixMongo(self, prefix):
        collection = self.dbMongo.passengers_data
        after_eating_hours = [8, 16, 20]

        queryConnection = [
            {"$match": {"connection": True, "from": prefix}},
            {"$group": {"_id": "$from", "totalFlightsWithConnection": {"$sum": 1}}},
        ]

        queryHours = [
            {"$match": {"departure": {"$in": after_eating_hours}, "from": prefix}},
            {"$group": {"_id": "$from", "totalFlights": {"$sum": 1}}},
        ]

        resultConnection = collection.aggregate(queryConnection)
        resultHours = collection.aggregate(queryHours)

        total_flights = sum(
            entry["totalFlightsWithConnection"] for entry in resultConnection
        )
        total_flights_departure = sum(entry["totalFlights"] for entry in resultHours)

        if total_flights + total_flights_departure > 10:
            print(
                f"Airport: {prefix}, Total flights with connection = true: {total_flights}, Total flights with departure at 8, 16, and 20: {total_flights_departure} ---->New restaurant needed!!!"
            )
        else:
            print(
                f"Airport: {prefix}, Total flights with connection = true: {total_flights}, Total flights with departure at 8, 16, and 20: {total_flights_departure} ---->NO restaurant needed!!!"
            )

    def loadDataDgraph(self):
        self.dbDgraph.loadData()

    def getNumOfFlightsPerAirportDgraph(self):
        query = """
        query flightPerAirport($name: string) {
            flightsCount(func: eq(from, $name)) {
                count: count(uid)
                }
        }
        """
        airports = ["PDX", "GDL", "SJC", "LAX", "JFK"]
        for prefix in airports:
            variables = {'$name': prefix}
            res = self.dbDgraph.client.txn(read_only=True).query(
                query, variables=variables
            )
            count = json.loads(res.json)

            print(f"Airport: {prefix} :\n{json.dumps(count, indent=2)}")
    
    def getNumOfFlightsPerAirportWithPrefixDgraph(self, prefix):
        query = """
        query flightPerAirport($name: string) {
            flightsCount(func: eq(from, $name)) {
                count: count(uid)
                }
        }
        """
        
        variables = {'$name': prefix}
        res = self.dbDgraph.client.txn(read_only=True).query(
            query, variables=variables
        )
        count = json.loads(res.json)

        print(f"Airport: {prefix} :\n{json.dumps(count, indent=2)}")
    
    def getIdeaOfOpeningLuchRoomDgraph(self):
        query = """
        query flightPerAirport($name: string) {
            flightsCount(func: eq(from, $name)) {
                airline
                from
                connection
                
                }
        }
        """
        airports = ["PDX", "GDL", "SJC", "LAX", "JFK"]
        for prefix in airports:
            variables = {'$name': prefix}
            res = self.dbDgraph.client.txn(read_only=True).query(
                query, variables=variables
            )
            
            data= json.loads(res.json)
            
            aa_count=0
            da_count=0
            a_count=0
            am_count=0
            v_count=0
            limit_amount =5
            for key, value in data.items() :    
                print('--')
                for item in value:
                    currAirline = ''
                    for innerkey, innervalue in item.items() :
                        if(innerkey=='airline'):
                            currAirline = innervalue
                        else:
                            if(innervalue):
                                if(currAirline == "American Airlines"):
                                    aa_count=aa_count+1
                                elif (currAirline == "Delta Airlines"):
                                    da_count=da_count+1
                                elif (currAirline == "Alaska"):
                                    a_count=a_count+1
                                elif (currAirline == "Aeromexico"):
                                    am_count=am_count+1
                                elif (currAirline == "Volaris"):
                                    v_count=v_count+1
            if(aa_count > limit_amount):
                print("American Airlines need a Lunch Room for : ",prefix)
            if(da_count > limit_amount):
                print("Delta Airlines need a Lunch Room for : ",prefix)
            if(a_count > limit_amount):
                print("Alaska need a Lunch Room for : ",prefix)
            if(am_count > limit_amount):
                print("Aeromexico need a Lunch Room for : ",prefix) 
            if(v_count > limit_amount):
                print("Volaris need a Lunch Room for : ",prefix)                
            #print(f"Airport: {prefix} :\n{json.dumps(count, indent=2)}")
    
    def getIdeaOfOpeningLuchRoomDgraphWithPrefix(self,prefix):
        query = """
        query flightPerAirport($name: string) {
            flightsCount(func: eq(from, $name)) {
                airline
                from
                connection
                
                }
        }
        """
       
        variables = {'$name': prefix}
        res = self.dbDgraph.client.txn(read_only=True).query(
            query, variables=variables
        )
            
        data= json.loads(res.json)
            
        aa_count=0
        da_count=0
        a_count=0
        am_count=0
        v_count=0
        limit_amount = 5
        for key, value in data.items() :    
            print('--')
            for item in value:
                currAirline = ''
                for innerkey, innervalue in item.items() :
                    if(innerkey=='airline'):
                        currAirline = innervalue
                    else:
                        if(innervalue):
                            if(currAirline == "American Airlines"):
                                aa_count=aa_count+1
                            elif (currAirline == "Delta Airlines"):
                                da_count=da_count+1
                            elif (currAirline == "Alaska"):
                                a_count=a_count+1
                            elif (currAirline == "Aeromexico"):
                                am_count=am_count+1
                            elif (currAirline == "Volaris"):
                                v_count=v_count+1
            if(aa_count > limit_amount):
                print("American Airlines need a Lunch Room for : ",prefix)
            if(da_count > limit_amount):
                print("Delta Airlines need a Lunch Room for : ",prefix)
            if(a_count > limit_amount):
                print("Alaska need a Lunch Room for : ",prefix)
            if(am_count > limit_amount):
                print("Aeromexico need a Lunch Room for : ",prefix) 
            if(v_count > limit_amount):
                print("Volaris need a Lunch Room for : ",prefix)                   
        
