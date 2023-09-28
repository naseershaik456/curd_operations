

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'Naseer46@'
jwt = JWTManager(app)

users = {
    'user1': {'password': 'password1'},
    'user2': {'password': 'password2'}

}

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users:
        return jsonify(message='Username already exists'), 400

    users[username] = {'password': password}
    return jsonify(message='Registration successful'), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username]['password'] == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message='Invalid credentials'), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return jsonify(username=current_user), 200

products = []

# Sample product data
sample_product_data = {
    'id': 1,
    'name': 'Bulb',
    'description': 'It is a light.',
    'price': 19.99,
    'category': 'Electronics'
}

# Initialize with a sample product
products.append(sample_product_data)


@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = {
        'id': len(products) + 1,
        'name': data['name'],
        'description': data['description'],
        'price': data['price'],
        'category': data['category']
    }
    products.append(new_product)
    return jsonify(new_product), 201


@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None:
        return jsonify(product)
    else:
        return jsonify(message='Product not found'), 404


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None:
        product['name'] = data['name']
        product['description'] = data['description']
        product['price'] = data['price']
        product['category'] = data['category']
        return jsonify(product)
    else:
        return jsonify(message='Product not found'), 404


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify(message='Product deleted'), 200


if __name__ == '__main__':
    app.run(debug=True)

