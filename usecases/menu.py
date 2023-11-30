import sys
from classes.airports import Airport
from repos.flights import FlightsRepo
from assets.menus import menu_options, menu_options_cassandra, menu_options_mongo, menu_options_dgraph

class Menu:
    logo:str
    flights:FlightsRepo
    
    def __init__(self, logo_str,flights):
        self.logo = logo_str
        self.flights = flights
        print(self.logo)
        
        while(True):
            option= input(menu_options)
            
            #if(option == '1'):
            #    self.cassandra_menu()
            if(option == '1'):
                self.mongo_menu()
            elif(option == '2'):
                self.dgraph_menu()
                
            elif(option == 'exit' ):
                return
            else:
                print('Invalid Option')
    
    def cassandra_menu(self):
        while(True):
            option= input(menu_options_cassandra)
            
            if(option == 'back' ):
                return
            else:
                print('Invalid Option')
    
    def mongo_menu(self):
        while(True):
            option= input(menu_options_mongo)
            
            if(option == 'back' ):
                return
            elif(option == '1'):
                self.flights.getNumOfFlightsPerAirportMongo()
            elif(option == '2'):
                print("[PDX, GDL, SJC, LAX, JFK]")
                prefix = input('Please enter a prefix from above :')
                self.flights.getNumOfFlightsPerAirportWithPrefixMongo(prefix)
            elif(option == '3'):
                self.flights.getIdeaOfOpeningARestaurantMongo()
            elif(option=='4'):
                print("[PDX, GDL, SJC, LAX, JFK]")
                prefix = input('Please enter a prefix from above :')
                self.flights.getIdeaOfOpeningARestaurantWithPrefixMongo(prefix)
            else:
                print('Invalid Option')
    
    def dgraph_menu(self):
        while(True):
            option= input(menu_options_dgraph)
            
            if(option == 'back' ):
                return
            if(option == '1'):
                self.flights.getNumOfFlightsPerAirportDgraph()
            elif(option == '2'):
                print("[PDX, GDL, SJC, LAX, JFK]")
                prefix = input('Please enter a prefix from above :')
                self.flights.getNumOfFlightsPerAirportWithPrefixDgraph(prefix)
            elif(option == '3'):
                self.flights.getIdeaOfOpeningLuchRoomDgraph()
            elif(option == '4'):
                print("[PDX, GDL, SJC, LAX, JFK]")
                prefix = input('Please enter a prefix from above :')
                self.flights.getIdeaOfOpeningLuchRoomDgraphWithPrefix(prefix)
            elif(option == 'load'):
                self.flights.loadDataDgraph()
                
            else:
                print('Invalid Option')