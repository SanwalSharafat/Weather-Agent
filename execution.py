from factual_memory import handle_user_message
from factual_memory import sent_response_back
from project import weather_agent

# Memory
history = []

# -----------------------------------------------------
# CHAT LOOP
# -----------------------------------------------------
def main():
    while True:
        try:
            user = input("ASK ANYTHING FROM YOUR WEATHER ASSISTANCE: ")

            if user.lower() in ["stop", "exit", "quit", "end"]:
                print("ASSISTANT: Goodbye!")
                break

            handle_user_message (user)
            memory = sent_response_back ()

            if memory is None:
                print ("we have nothing in memory.")
            else:
                result = weather_agent(user, history, memory)
                print(f"\nASSISTANT: {result}\n")
            
        except EOFError:
            print("\nASSISTANT: Session ended. Goodbye!")
            break

        except KeyboardInterrupt:
            print("\nStopped by user (Ctrl+C). Goodbye!")
            break

        except Exception as e:
            print(f"\nAn unhandled error occurred: {e}\n")
            break

if __name__ == "__main__":
    main ()