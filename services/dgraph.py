import pydgraph
import json
from scripts.csvjson import parseCsvToJson

class Dgraph:
    client = None
    def __init__(
        self,
        connection_string: str,
        api_key:str
    ):
        
        DGRAPH_ENDPOINT = connection_string
        
        client_stub = pydgraph.DgraphClientStub.from_cloud(connection_string, api_key)
        client = pydgraph.DgraphClient(client_stub)
        self.client=client
        print("You successfully connected to Dgraph!")
    
    def formatData(self):
        parseCsvToJson()
        
    def set_schema(self):
        schema = """
        type flight {
            airline
            from
            to
            day
            month
            year
            age
            gender
            reason
            stay
            transit
            connection
            wait
            departure
        }

        type airport {
            from
            flight
        }

        type airline {
            airline
            connected
        }
        
        airline : string @index(exact) .
        from: string @index(exact) .
        flight: [uid] @reverse .
        connected: [uid] @reverse .
        to: string . 
        day: int .
        month: int .
        year: int .
        age: int .
        gender: string .
        reason: string .
        stay: string .
        transit: string .
        connection: bool .
        wait: int .
        departure: int .


        """
        return self.client.alter(pydgraph.Operation(schema=schema))
    
    def loadData(self):
        with open('assets/flight_passengers.json') as json_file:
            data = json.load(json_file)

        txn = self.client.txn()
        try:
            response = txn.mutate(set_obj = data)
            commit_response = txn.commit()
            print(f"Commit Response: {commit_response}")
        finally:
            txn.discard() 
            
