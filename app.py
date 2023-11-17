from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import the CORS extension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)

# Create the database tables within the application context
with app.app_context():
    db.create_all()

# Dummy data for initial testing
events = [
    {"title": "Event 1", "date": "2023-11-16"},
    {"title": "Event 2", "date": "2023-11-17"},
]

# Seed the initial data into the database
with app.app_context():
    for event in events:
        new_event = Event(title=event["title"], date=event["date"])
        db.session.add(new_event)

    db.session.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/events", methods=["GET", "POST"])
def api_events():
    if request.method == "GET":
        with app.app_context():
            events = Event.query.all()
            return jsonify([{"id": event.id, "title": event.title, "date": event.date} for event in events])
    elif request.method == "POST":
        data = request.get_json()
        new_event = Event(title=data["title"], date=data["date"])
        with app.app_context():
            db.session.add(new_event)
            db.session.commit()
        return jsonify({"id": new_event.id, "title": new_event.title, "date": new_event.date})

if __name__ == "__main__":
    app.run(debug=True)
