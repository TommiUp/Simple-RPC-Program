# AI DECLARATION: ChatGPT o1 and o3-mini-high has been used for coding help

import random
import xmlrpc.client
import xml.etree.ElementTree as ET
import threading

print_lock = threading.Lock()


# List of server URLs
SERVER_URLS = [
    "http://localhost:9000/RPC2",
    "http://localhost:9001/RPC2"
]

def fetch_and_print(topic):
    local_proxy = xmlrpc.client.ServerProxy(random.choice(SERVER_URLS), allow_none=True)
    try:
        notes = local_proxy.get_content(topic)
        output_lines = [f"\n=== Topic: {topic} ==="]
        if notes:
            for idx, note in enumerate(notes, 1):
                output_lines.append(f"{idx}. Name: {note['name']}")
                output_lines.append(f"   Text: {note['text']}")
                output_lines.append(f"   Timestamp: {note['timestamp']}")
        else:
            output_lines.append("No content found.")
        # Lock printing is used to avoid interleaved outputs
        with print_lock:
            for line in output_lines:
                print(line)
    except Exception as e:
        with print_lock:
            print(f"Error fetching content for topic '{topic}': {e}")

def main():
    try:
        tree = ET.parse("data.xml")
        root = tree.getroot()
    except Exception as e:
        print("Could not load 'data.xml'. Please ensure the file exists and is a valid XML database.")
        return

    threads = []
    print(f"\n=== All Content From Topics ===")
    for topic_element in root.findall('topic'):
        topic_name = topic_element.get('name')
        t = threading.Thread(target=fetch_and_print, args=(topic_name,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
