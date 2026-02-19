# Databricks CLI
# Copyright 2017 Databricks, Inc.

from __future__ import absolute_import

import json

try:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer

from databricks_cli.virtual_engineers.planner import (
    AI_ENGINEER_ROLES,
    TECHNICAL_SKILLS,
    build_engineer_blueprint,
)

ENGINEERS = []

INDEX_HTML = """<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Virtual Engineer Factory</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; background: #f8fafc; color: #0f172a; }
    .card { background: white; border-radius: 10px; padding: 1rem 1.5rem; box-shadow: 0 5px 20px rgba(0,0,0,.08); max-width: 900px; }
    label { display: block; margin-top: .8rem; font-weight: bold; }
    input, textarea, select { width: 100%; margin-top: .2rem; padding: .5rem; }
    .skills { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .25rem; }
    button { margin-top: 1rem; background: #2563eb; color: white; border: none; padding: .6rem 1rem; border-radius: 6px; cursor: pointer; }
    pre { white-space: pre-wrap; background: #020617; color: #e2e8f0; padding: 1rem; border-radius: 10px; }
  </style>
</head>
<body>
  <h1>AI Virtual Engineer Platform</h1>
  <p>Create and deploy AI-powered engineering employees using multi-agent orchestration.</p>
  <div class=\"card\">
    <label>Full Name</label><input id=\"fullName\" />
    <label>Company Name</label><input id=\"companyName\" />
    <label>Engineer Role</label><select id=\"role\"></select>
    <label>Technical Skills</label><div class=\"skills\" id=\"skills\"></div>
    <label>Responsibilities / Workflows (one per line)</label><textarea id=\"responsibilities\" rows=\"5\"></textarea>
    <button onclick=\"deployEngineer()\">Generate & Deploy AI Engineer</button>
  </div>
  <h2>Deployment Output</h2>
  <pre id=\"output\">No deployment yet.</pre>
<script>
async function loadOptions() {
  const response = await fetch('/api/options');
  const data = await response.json();
  const roleEl = document.getElementById('role');
  data.roles.forEach(role => {
    const option = document.createElement('option');
    option.value = role;
    option.innerText = role;
    roleEl.appendChild(option);
  });
  const skillsEl = document.getElementById('skills');
  data.skills.forEach(skill => {
    const label = document.createElement('label');
    label.innerHTML = `<input type=\"checkbox\" value=\"${skill}\" /> ${skill}`;
    skillsEl.appendChild(label);
  });
}

async function deployEngineer() {
  const skills = Array.from(document.querySelectorAll('#skills input:checked')).map(x => x.value);
  const responsibilities = document.getElementById('responsibilities').value
    .split('\n').map(line => line.trim()).filter(Boolean);

  const payload = {
    full_name: document.getElementById('fullName').value,
    company_name: document.getElementById('companyName').value,
    role: document.getElementById('role').value,
    skills: skills,
    responsibilities: responsibilities
  };

  const response = await fetch('/api/engineers', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
  });
  const deployed = await response.json();
  document.getElementById('output').textContent = JSON.stringify(deployed, null, 2);
}

loadOptions();
</script>
</body>
</html>"""


class VirtualEngineerHandler(BaseHTTPRequestHandler):

    def _write_json(self, body, status_code=200):
        encoded = json.dumps(body).encode('utf-8')
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def _write_html(self, body):
        encoded = body.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == '/':
            self._write_html(INDEX_HTML)
            return
        if self.path == '/api/options':
            self._write_json({'roles': AI_ENGINEER_ROLES, 'skills': TECHNICAL_SKILLS})
            return
        if self.path == '/api/engineers':
            self._write_json({'engineers': ENGINEERS})
            return
        self._write_json({'error': 'Not found'}, 404)

    def do_POST(self):
        if self.path != '/api/engineers':
            self._write_json({'error': 'Not found'}, 404)
            return

        content_length = int(self.headers.get('Content-Length') or 0)
        raw_payload = self.rfile.read(content_length)

        try:
            payload = json.loads(raw_payload.decode('utf-8') or '{}')
        except ValueError:
            self._write_json({'error': 'Invalid JSON payload'}, 400)
            return

        deployed_engineer = build_engineer_blueprint(payload)
        ENGINEERS.append(deployed_engineer)
        self._write_json(deployed_engineer, 201)


def run_server(host, port):
    server = HTTPServer((host, port), VirtualEngineerHandler)
    return server
