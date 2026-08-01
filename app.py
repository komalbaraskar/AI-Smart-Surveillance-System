from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_data():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Total alerts
    cursor.execute("SELECT COUNT(*) FROM logs")
    total_alerts = cursor.fetchone()[0]

    # Latest people count
    cursor.execute("SELECT count FROM people_count ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    people_count = row[0] if row else 0

    # Recent logs
    cursor.execute("SELECT message, time FROM logs ORDER BY id DESC LIMIT 10")
    logs = cursor.fetchall()

    conn.close()
    return total_alerts, people_count, logs

@app.route("/")
def dashboard():
    total_alerts, people_count, logs = get_data()
    return render_template(
        "dashboard.html",
        total_alerts=total_alerts,
        people_count=people_count,
        logs=logs
    )

if __name__ == "__main__":
    app.run(debug=True)