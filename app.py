from flask import Flask, request, render_template_string
import requests
import sqlite3
import time

app = Flask(__name__)

# Create database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (url TEXT, response_time REAL)''')
    conn.commit()
    conn.close()

init_db()

# HTML Template (inside Python)
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>API Performance Monitor</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        input, button { padding: 10px; margin: 5px; }
        table { margin-top: 20px; border-collapse: collapse; }
        th, td { padding: 10px; border: 1px solid black; }
    </style>
</head>
<body>

<h2>🚀 API Performance Monitor</h2>

<form method="POST">
    <input type="text" name="url" placeholder="Enter API URL" required>
    <button type="submit">Check</button>
</form>

<h3>Logs:</h3>
<table>
<tr>
    <th>URL</th>
    <th>Response Time (sec)</th>
</tr>

{% for row in data %}
<tr>
    <td>{{ row[0] }}</td>
    <td>{{ row[1] }}</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            start = time.time()
            r = requests.get(url)
            end = time.time()

            response_time = round(end - start, 3)

            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute("INSERT INTO logs VALUES (?, ?)", (url, response_time))
            conn.commit()
            conn.close()

        except:
            pass

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM logs")
    data = c.fetchall()
    conn.close()

    return render_template_string(HTML, data=data)

if __name__ == '__main__':
    app.run(debug=True)
