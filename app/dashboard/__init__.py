from flask import Blueprint

from app.helpers import RouteView, role_required

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates', static_folder='static')
dashboard.error_handler = lambda e: redirect(url_for('dashboard.error'))

from .auth import *

decorators = [role_required(['admin'])]
RouteView.register(dashboard, 'error', '/error/', 'dashboard/templates/404.html', {'title': 'Page not found'}, decorators)
RouteView.register(dashboard, 'index', '/', 'dashboard/index.html', {'title': 'Dashboard', 'page_title': 'Dashboard'}, decorators)
RouteView.register(dashboard, 'users', '/users/', 'dashboard/users.html', {'title': 'Users', 'page_title': 'Users'}, decorators)
RouteView.register(dashboard, 'trash', '/trash/', 'dashboard/trash.html', {'title': 'Trash', 'page_title': 'Trash'}, decorators)