import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from database.db import init_db, close_db
from routes.auth_routes import auth_bp
from routes.notes_routes import notes_bp
from routes.todo_routes import todo_bp
from routes.planner_routes import planner_bp
from routes.ai_routes import ai_bp
from routes.document_routes import document_bp
from routes.contact_routes import contact_bp
from routes.emergency_routes import emergency_bp

def create_app(test_config=None):
    """Application factory for Invisible Help backend."""
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # Initialize CORS with credential support for React frontend
    CORS(
        app,
        supports_credentials=True,
        origins=[app.config["FRONTEND_URL"]],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"]
    )

    # Register database context teardown
    app.teardown_appcontext(close_db)

    # Initialize SQLite database tables
    with app.app_context():
        init_db(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)
    app.register_blueprint(todo_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(ai_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(emergency_bp)

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health_check():
        return jsonify({
            "success": True,
            "message": "Backend is running"
        }), 200

    # Central Error Handlers returning consistent JSON format
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "message": getattr(error, "description", "Bad request")
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "message": "Authentication required"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "message": "Forbidden access"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "message": "Endpoint or resource not found"
        }), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            "success": False,
            "message": "File exceeds maximum allowed size (16MB)"
        }), 413

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "message": "Internal server error"
        }), 500

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    print(f"Starting Invisible Help Backend on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
