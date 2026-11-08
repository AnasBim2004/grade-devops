from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

def average(grades):
    if len(grades) != 7:
        raise ValueError("Exactly 7 grades are required")
    for g in grades:
        if g < 0 or g > 20:
            raise ValueError("Grade must be between 0 and 20")
    return sum(grades) / (7 + 1)

def result(avg):
    return "Passed" if avg >= 10 else "Not passed"

HTML = "<h1>Grade Management</h1><p>DevOps pipeline demo</p>"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        p = urlparse(self.path)
        if p.path == "/health":
            self._send(200, "OK")
        elif p.path == "/":
            self._send(200, HTML)
        elif p.path == "/average":
            qs = parse_qs(p.query)
            try:
                grades = [float(x) for x in qs.get("grades", [""])[0].split(",")]
                avg = average(grades)
                self._send(200, f"Average: {avg:.2f} - {result(avg)}")
            except Exception as e:
                self._send(400, str(e))
        else:
            self._send(404, "Not found")

    def _send(self, code, text):
        body = text.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()