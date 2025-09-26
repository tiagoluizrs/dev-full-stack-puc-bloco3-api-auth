from flask import request, jsonify
from controllers.user import register_user, login_user, validate_user_token, reset_user_token

def register_auth_routes(app):
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        response, status = register_user(data)
        return jsonify(response), status

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        response, status = login_user(data)
        return jsonify(response), status

    @app.route('/auth/validate-token', methods=['POST'])
    def validate():
        data = request.get_json()
        response, status = validate_user_token(data)
        return jsonify(response), status

    @app.route('/auth/reset-token', methods=['POST'])
    def reset():
        data = request.get_json()
        response, status = reset_user_token(data)
        return jsonify(response), status