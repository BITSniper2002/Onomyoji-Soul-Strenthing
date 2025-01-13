# from flask import Flask, render_template, jsonify
# import random
# from decimal import Decimal, ROUND_HALF_UP
# from Onmyoji_Soul import Soul,boost
#
# app = Flask(__name__)
#
#
# soul_warehouse = []
#
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/initialize/<int:num_souls>')
# def initialize_souls(num_souls):
#     global soul_warehouse
#     soul_warehouse = [Soul() for _ in range(num_souls)]
#     return jsonify({"message": f"{num_souls} souls initialized."})
#
#
# @app.route('/warehouse')
# def warehouse():
#     return jsonify({"souls": [{"name": s.name, "slot": s.slot, "prime": s.prime, "prime_value": s.prime_value} for s in
#                               soul_warehouse]})
#
#
# @app.route('/help')
# def help_info():
#     return jsonify({"message": "This is Soul Master. Click 'Initialize' to generate souls, 'Warehouse' to view them, and 'Hide Warehouse' to hide."})
#
#
# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, render_template, jsonify, request, session
from Onmyoji_Soul import Soul,boost

app = Flask(__name__)


soul_warehouse = []

def get_souls():
    return session.get("souls", [])

def save_souls(souls):
    session["souls"] = souls


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/initialize/<int:num_souls>')
def initialize_souls(num_souls):
    global soul_warehouse
    tmp = [Soul() for _ in range(num_souls)]
    soul_warehouse.extend(tmp)
    return jsonify({"message": f"{num_souls} souls initialized."})


@app.route('/warehouse')
def warehouse():
    return jsonify({"souls": [{
        "name": s.name,
        "slot": s.slot,
        "level" : s.level,
        "prime": s.prime,
        "prime_value": s.prime_value,
        "non_prime": s.non_prime,
        "non_prime_value": s.non_prime_value
    } for s in soul_warehouse]})

# @app.route('/boost/<int:soul_index>', methods=['POST'])
# def boost_soul(soul_index):
#     soul_index = int(request.form.get('index'))
#     exp = int(request.form.get('exp', 1000))
#     boost(soul_warehouse[soul_index], exp)
#     return jsonify({"status": "boosted"})
#
# @app.route('/delete', methods=['POST'])
# def delete_soul():
#     soul_index = int(request.form.get('index'))
#     if 0 <= soul_index < len(soul_warehouse):
#         del soul_warehouse[soul_index]
#     return jsonify({"status": "deleted"})

@app.route('/boost/<int:soul_index>', methods=['POST'])
def boost_soul(soul_index):
    print(soul_index)
    # souls = get_souls()  # Load existing souls
    data = request.get_json()  # Get JSON data from request
    # print(souls,'\n',data)
    exp = int(data.get('exp', 1000))  # Read `exp` safely

    if 0 <= soul_index < len(soul_warehouse):
        soul = soul_warehouse[soul_index]
        # print(soul)
        boost(soul, exp)  # Boost the soul
        # save_souls(soul)  # Save updated souls
        # print(soul)
        return jsonify({"message": f"Soul boosted by {exp} XP!"})

    return jsonify({"error": "Invalid soul index"}), 400


@app.route('/delete/<int:soul_index>', methods=['POST'])
def delete_soul(soul_index):
    # souls = get_souls()
    if 0 <= soul_index < len(soul_warehouse):
        del soul_warehouse[soul_index]
        return jsonify({"message": f"Soul deleted"})
    return jsonify({"error": "Invalid soul index"}), 400

if __name__ == '__main__':
    app.run(debug=True)
