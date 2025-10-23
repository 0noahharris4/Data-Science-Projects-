import random
#defining class for AirlineBot
class AirlineBot:
    #defining variables to store exit and negative reponses entered by end user 
    negative_responses = ("no", "no thanks", "bye", "goodbye", "nope", "nah", "not a chance", "sorry")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
#Using dictionary data structure to list city names, departure times, and arrival times
    loc_depart_land = {
        "Dallas 305": ["4:00PM", "10:00PM"],
        "Chicago 306": ["3:00AM", "12:00PM"],
        "Columbus 307": ["2:00PM", "8:00PM"]
    }
#defining greet method to initiate the dialog, collect general information, and welcome the end user. 
    def greet(self):
        print("Hi! Good afternoon. Thank you for choosing Astro Airlines.")
        print("Before I can assist you, I’ll need some info.")
        self.name = input("What is your name? ")
        print(f"Hi {self.name}! I'm happy to help you with your flight information today.")
#Using while conditional statement to continue conversation with end user and provide them with options for the chat 
        while True:
            user_input = input("\nType a city and flight number (e.g., 'Dallas 305'), 'list flights', 'help', or 'exit': ")

            #Confirming end user wants to exit the chat
            if user_input.lower() in self.exit_commands:
                confirm = input("Are you sure you'd like to end the chat? (yes/no) ")
                if confirm in ("yes", "y"):
                    print("Thank you for choosing Astro Airlines. Have a safe flight!")
                    break
                else:
                    print("No problem! Let's continue.")
                    continue

            #Assisting user with options available in the chat if request is for "help"
            if user_input.lower() == "help":
                print("\nYou can:")
                print("- Ask about a flight (e.g., 'Dallas 305')")
                print("- Type 'list flights' to see all available flights")
                print("- Type 'exit' to leave the chat")
                continue

            # List available flights for end user if request if for "list flights"
            if user_input.lower() == "list flights":
                print("\nHere are the available flights:")
                for flight in self.loc_depart_land:
                    #printing out list of flights for user to inquire about
                    print(f"- {flight}")
                continue

            # Try to extract and respond to flight info
            self.provide_flight_info(user_input)

    def provide_flight_info(self, request):
        # Normalize input: remove extra spaces and capitalize
        request = ' '.join(request.strip().split()).title()

        if request in self.loc_depart_land:
            depart, land = self.loc_depart_land[request]
            #Generating list of potential responses to end users flight inquiry
            responses = [
                f"Flight {request} departs at {depart} and lands at {land}.",
                f"You're booked on {request}. Departure: {depart}, Arrival: {land}.",
                f"{request} takes off at {depart} and touches down at {land}.",
                f"Confirmed: {request} leaves at {depart} and arrives at {land}."
            ]
            #using random.choice to generate random reponse to end users flight inquiry request
            print(random.choice(responses))
        else:
            print("Sorry, I couldn't find that flight. Please try again with a valid city and flight number.")

# Create and run the bot
if __name__ == "__main__":
    my_bot = AirlineBot()
    my_bot.greet()