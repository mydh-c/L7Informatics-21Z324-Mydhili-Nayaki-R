from flask import Flask, request, jsonify
from models import db, Flavor, Allergen

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ice_cream.db'
db.init_app(app)

@app.route('/')
def home():
    return "Welcome to the Ice Cream Parlor API! Use /flavors to get all flavors."

@app.route('/flavors', methods=['GET'])
def get_flavors():
    flavors = Flavor.query.all()
    return jsonify([{'id': f.id, 'name': f.name,'seasonal':f.seasonal} for f in flavors])

@app.route('/add_flavor', methods=['POST'])
def add_flavor():
    data = request.json
    new_flavor = Flavor(name=data['name'], seasonal=data.get('seasonal', False))
    db.session.add(new_flavor)
    db.session.commit()
    return jsonify({'message': 'Flavor added!'}), 201

@app.route('/add_allergen', methods=['POST'])
def add_allergen():
    data = request.json
    if not Allergen.query.filter_by(name=data['name']).first():
        new_allergen = Allergen(name=data['name'], flavor_id=data['flavor_id'])
        db.session.add(new_allergen)
        db.session.commit()
        return jsonify({'message': 'Allergen added!'}), 201
    return jsonify({'message': 'Allergen already exists!'}), 400

@app.route('/allergens', methods=['GET'])
def get_allergens():
    # Fetch all allergens or filter by flavor_id if provided
    flavor_id = request.args.get('flavor_id')
    
    if flavor_id:
        allergens = Allergen.query.filter_by(flavor_id=flavor_id).all()
    else:
        allergens = Allergen.query.all()
    
    return jsonify([{'id': a.id, 'name': a.name, 'flavor_id': a.flavor_id} for a in allergens])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
