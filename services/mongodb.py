from pymongo import MongoClient

class mongoDB:
    db = None
    def __init__(
        self,
        connection_string: str
    ):
        
        MONGO_URI = connection_string
        client = MongoClient(MONGO_URI)
        db = client["Flights"]
        try:
            client.admin.command("ping")
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        self.db=db
