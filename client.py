# AI DECLARATION: ChatGPT o1 and o3-mini-high has been used for coding help

import xmlrpc.client # RPC client
import random
import test
import sys

# List of server URLs
SERVER_URLS = [
    "http://localhost:9000/RPC2",
    "http://localhost:9001/RPC2"
]

def get_proxy():
    server_url = random.choice(SERVER_URLS)
    return xmlrpc.client.ServerProxy(server_url, allow_none=True)

def main():
    while True:
        print("\n=== Client menu ===")
        print("1) Add content")
        print("2) Get content by topic")
        print("3) Add wiki article to a topic")
        print("4) Exit")
        print("5) Test")
        choice = input("Enter your choice: ").strip()

        proxy = get_proxy()  # Get a random server proxy each time
        
        if choice == '1':
            topic = input("Enter topic: ")
            note_name = input("Enter note name/title: ")
            note_text = input("Enter note text: ")
            timestamp = None
            try:
                result = proxy.add_content(topic, note_name, note_text, timestamp)
                print(result)
            except Exception as e:
                print(e)

        elif choice == '2':
            topic = input("Enter topic: ")
            try:
                notes = proxy.get_content(topic)
                if notes:
                    print(f"\n=== Topic: {topic} ===")
                    for idx, n in enumerate(notes, 1):
                        print(f"  {idx}. Name: {n['name']}")
                        print(f"     Text:{n['text']}")
                        print(f"     Timestamp:{n['timestamp']}")
                else:
                    print(f"No content found for '{topic}'.")
            except Exception as e:
                print(f"{e}")

        elif choice == '3':
            topic = input("Enter the topic where data should be appended: ")
            search_query = input("Enter the Wikipedia search query: ")
            try:
                result = proxy.add_wiki(topic, search_query)
                print(f"{result}")
            except Exception as e:
                print(f"{e}")

        elif choice == '4':
            print("Exiting...")
            sys.exit(0)

        elif choice == '5':
            test.main()

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
