from flask import Blueprint
from routes.selenium_scrap_router import selenium_scrap_router
from routes.playwright_router import playwrite_router
from routes.user_router import user_router
main_router = Blueprint("v1",__name__)
main_router.register_blueprint(selenium_scrap_router)
main_router.register_blueprint(playwrite_router)
main_router.register_blueprint(user_router)