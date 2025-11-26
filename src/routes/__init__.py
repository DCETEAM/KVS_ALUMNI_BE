from src.routes.auth_route import auth_bp
from src.routes.register_route import alumni_routes
from src.routes.markstatus_route import markstatus_routes

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(alumni_routes)
    app.register_blueprint(markstatus_routes)
