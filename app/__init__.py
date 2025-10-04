from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes.git_analysis import git_analysis_bp
    app.register_blueprint(git_analysis_bp)

    return app