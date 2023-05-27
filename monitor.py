import sys
import socket
# get urls_file name from command line
if len(sys.argv) != 2:
    print('Usage: monitor urls_file')
    sys.exit()
# text file to get list of urls
urls_file = sys.argv[1]

with open(urls_file) as f:
    urls = f.readlines()

# server, port, and path should be parsed from url
host = 'fiu.gov'
default_host = None
port = 80 # use port 80 for http and port 443 for https
path = ''
sock = None
redirects = 0

for url in urls:
    url = url.strip()
    protocol, rest = url.split("://")
    parts = rest.split("/", 1)
    host = parts[0] #if len(parts) > 1 else default_host
    path = '/' + parts[1] if len(parts) > 1 else ''

    # create client socket, connect to server
    try:
        sock = socket.create_connection((host, port), timeout=5)
    except Exception as e:
        print(f'Network Error:\n {e}')
    if sock:
        # send http request
        request = f'GET {path} HTTP/1.0\r\n'
        request += f'Host: {host}\r\n'
        request += '\r\n'
        sock.send(bytes(request, 'utf-8'))

        # receive http response
        response = b''
        while True:
            data = sock.recv(4096)
            response += data
            if not data:
                break
        #print(response.decode('utf-8'))

        status = response.split(b'\r\n')[0].decode('utf-8')
        print(f'URL: {url}')
        print(f'Status: {status}')




        sock.close()
