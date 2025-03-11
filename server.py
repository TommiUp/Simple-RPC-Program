# AI DECLARATION: ChatGPT o1 and o3-mini-high has been used for coding help
import sys
from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler # RPC server
from socketserver import ThreadingMixIn # Threaded server
import xml.etree.ElementTree as ET # ElementTree
import time # Timestamps
import requests # Wikipedia

XML_FILE = 'data.xml'

# Function to read/write the XML file, loads XML from disk and returns ElementTree object
def load_xml_database(): 
    try:
        tree = ET.parse(XML_FILE)
        return tree
    except (ET.ParseError, FileNotFoundError):
        # If the file doesn't exist or is invalid, start a new one
        root = ET.Element("data")
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)
        return tree

# Function to save ElementTree to the XML file
def save_xml_database(tree):
    tree.write(XML_FILE, encoding='utf-8', xml_declaration=True)

# Function to add content, adds content to given topic
def add_content(topic, note_name, note_text, timestamp=None):
    if not timestamp:
        # Generate a timestamp if none provided
        timestamp = time.strftime('%m/%d/%Y - %H:%M:%S')
        
    tree = load_xml_database()
    root = tree.getroot()

    # Find or create the topic
    topic_element = None
    for t in root.findall('topic'):
        if t.get('name') == topic:
            topic_element = t
            break

    if topic_element is None:
        topic_element = ET.SubElement(root, 'topic', {'name': topic})

    # Create the note
    note_element = ET.SubElement(topic_element, 'note', {'name': note_name})

    text_element = ET.SubElement(note_element, 'text')
    text_element.text = note_text

    ts_element = ET.SubElement(note_element, 'timestamp')
    ts_element.text = timestamp

    # Save changes
    save_xml_database(tree)
    return f"Content added under topic '{topic}' with timestamp {timestamp}."

# Function to return all content for a given topic
def get_content(topic):
    tree = load_xml_database()
    root = tree.getroot()

    # Find the topic
    for t in root.findall('topic'):
        if t.get('name') == topic:
            # Get content / notes
            notes_data = []
            for note in t.findall('note'):
                text = note.find('text').text if note.find('text') is not None else ''
                timestamp = note.find('timestamp').text if note.find('timestamp') is not None else ''
                notes_data.append({
                    'name': note.get('name'),
                    'text': text,
                    'timestamp': timestamp
                })
            return notes_data

    return []  # If not found

# Function to search data from wiki and add it under the topic
def add_wiki(topic, search_query):
    # First, perform a call to Wikipedia
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        'action': 'opensearch',
        'search': search_query,
        'limit': 1,
        'namespace': 0,
        'format': 'json'
    }
    response = requests.get(url, params=params, timeout=5)
    response.raise_for_status()

    data = response.json()  # [search_term, titles, descriptions, links]
    if len(data) >= 4 and data[3]:
        # data[3] is a list of links
        wikipedia_link = data[3][0] if data[3] else "No link found"
    else:
        wikipedia_link = "No link found"

    # Next, add result to the XML as a note
    note_name = f"Wiki article about {search_query}"
    note_text = f"Wikipedia link for '{search_query}': {wikipedia_link}"
    result_message = add_content(topic, note_name, note_text)

    return f"Wikipedia article appended. {result_message}"

# Threaded server
class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def main():
    # Create a threaded server
    port = 9000  # default port
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    server = ThreadedXMLRPCServer(
        ("localhost", port),
        requestHandler=RequestHandler,
        allow_none=True
    )
    

    # Register our RPC methods
    server.register_introspection_functions()
    server.register_function(add_content, "add_content")
    server.register_function(get_content, "get_content")
    server.register_function(add_wiki, "add_wiki")

    print(f"Server listening on port {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server shutting down.")

if __name__ == "__main__":
    main()
