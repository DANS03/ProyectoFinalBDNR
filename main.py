from services.mongodb import mongoDB
from services.dgraph import Dgraph
from repos.flights import FlightsRepo
from assets.logo import logo
from usecases.menu import Menu

#Get Secrets
connection_string_mongo =  "mongodb+srv://david:rI6H12rYN3wRmitd@airportoptimization.img63rf.mongodb.net/?retryWrites=true&w=majority" 
connection_string_dgraph = "blue-surf-1230056.grpc.us-east-1.aws.cloud.dgraph.io:443"
api_key_dgrph = "NjBkNjZmODVmZDBjYjI4M2IwNjEwMTUyYjY3NTk5NWE="
# Init Services
mongo = mongoDB(connection_string_mongo)
dgraph = Dgraph(connection_string_dgraph,api_key_dgrph )

# Init Repos
flights = FlightsRepo(dbMongo=mongo.db,dbDgraph=dgraph)

# Init Usescases
menu = Menu(logo,flights)



# Init Controllers / Resolvers /

# Init Routers