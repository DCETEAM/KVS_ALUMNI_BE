from flask import request


def dynamic_mask_routes(app):
    @app.before_request
    def mask_routes():
        if not request.path.startswith("/api/v1"):
            real_path = f"/api/v1{request.path}"
            request.environ["PATH_INFO"] = real_path
