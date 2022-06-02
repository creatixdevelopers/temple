from flask import Blueprint

from app.utils import RouteView, role_required

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates', static_folder='static')
dashboard.error_handler = lambda e: redirect(url_for('dashboard.error'))

from .auth import *

decorators = [role_required(['admin'])]
RouteView.register(dashboard, 'error', '/error/', 'dashboard/templates/404.html', {'title': 'Page not found'}, decorators)
RouteView.register(dashboard, 'index', '/', 'dashboard/index.html', {'title': 'Dashboard', 'page_title': 'Dashboard'}, decorators)

RouteView.register(dashboard, 'blogs', '/blogs/', 'dashboard/posts/blogs.html', {'title': 'Blogs'}, decorators)
RouteView.register(dashboard, 'events', '/events/', 'dashboard/posts/events.html', {'title': 'Events'}, decorators)
RouteView.register(dashboard, 'post', {'/post/': {'uid': None}, '/post/<string:uid>/': {}}, 'dashboard/posts/post.html', {'title': 'Blogs & Events'},
                   decorators)

RouteView.register(dashboard, 'volunteers', '/volunteers/', 'dashboard/volunteers.html', {'title': 'Volunteers'}, decorators)
RouteView.register(dashboard, 'donations', '/donations/', 'dashboard/donations.html', {'title': 'Donations'}, decorators)

RouteView.register(dashboard, 'pooja', '/pooja/', 'dashboard/master/pooja.html', {'title': 'Pooja'}, decorators)

RouteView.register(dashboard, 'trash', '/trash/', 'dashboard/trash.html', {'title': 'Trash'}, decorators)
