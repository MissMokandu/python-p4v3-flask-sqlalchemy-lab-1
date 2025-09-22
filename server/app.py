# server/app.py
#!/usr/bin/env python3

#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False


db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route("/earthquakes/<int:id>", methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)

    if earthquake:
        data ={
            "id":earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        }
        return make_response(jsonify(data),209)
    else:
        return make_response(jsonify({"message":f"Earthquake{id} not found"}), 404)
    
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query all earthquakes with magnitude >= parameter
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    # Serialize each quake into a dictionary
    quakes_list = [
        {
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }
        for quake in quakes
    ]

    # Build response
    response_data = {
        "count": len(quakes_list),
        "quakes": quakes_list
    }

    return make_response(jsonify(response_data), 200)

# Add views here

if __name__ == '__main__':
    app.run(port=5555, debug=True)

