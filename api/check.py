from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        numbers = data.get('numbers', [])
        
        results = []
        # এখানে ১০টি করে নাম্বার চেক করা ভালো (টাইম-আউট এড়াতে)
        for number in numbers:
            try:
                url = f"https://8t09wa0n0a.execute-api.ap-south-1.amazonaws.com/poc/api/v2/parent-user/check-user-exists/{number}"
                response = requests.get(url, timeout=5)
                if response.json() == True:
                    results.append({"number": number, "status": "Exists"})
            except:
                continue
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"results": results}).encode('utf-8'))

