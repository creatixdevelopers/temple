from flask import Blueprint

from app.utils import RouteView, role_required

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard', template_folder='templates', static_folder='static')
dashboard.error_handler = lambda e: redirect(url_for('dashboard.error'))

from .auth import *

decorators = [role_required(['admin', 'user'])]
RouteView.register(dashboard, 'error', '/error/', 'dashboard/templates/404.html', {'title': 'Page not found'}, decorators)
RouteView.register(dashboard, 'index', '/', 'dashboard/index.html', {'title': 'Dashboard'}, decorators)

RouteView.register(dashboard, 'devotees', '/devotees/', 'dashboard/devotees.html', {'title': 'Devotees'}, decorators)
RouteView.register(dashboard, 'devotee', '/devotee/<string:uid>', 'dashboard/devotee.html', {'title': 'Devotee'}, decorators)
RouteView.register(dashboard, 'bookings', '/bookings/', 'dashboard/bookings.html', {'title': 'Bookings'}, decorators)
RouteView.register(dashboard, 'donations', '/donations/', 'dashboard/donations.html', {'title': 'Donations'}, decorators)

RouteView.register(dashboard, 'volunteers', '/volunteers/', 'dashboard/volunteers.html', {'title': 'Volunteers'}, decorators)

RouteView.register(dashboard, 'blogs', '/blogs/', 'dashboard/posts/blogs.html', {'title': 'Blogs'}, decorators)
RouteView.register(dashboard, 'events', '/events/', 'dashboard/posts/events.html', {'title': 'Events'}, decorators)
RouteView.register(dashboard, 'post', {'/post/': {'uid': None}, '/post/<string:uid>/': {}}, 'dashboard/posts/post.html', {'title': 'Blogs & Events'},
                   decorators)
RouteView.register(dashboard, 'gallery', '/gallery/', 'dashboard/gallery.html', {'title': 'Gallery'}, decorators)

RouteView.register(dashboard, 'pooja', '/pooja/', 'dashboard/master/pooja.html', {'title': 'Pooja'}, decorators)
RouteView.register(dashboard, 'pooja_page', '/pooja-page/', 'dashboard/master/pooja_page.html', {'title': 'Pooja Page'}, decorators)
RouteView.register(dashboard, 'settings', '/settings/', 'dashboard/master/settings.html', {'title': 'Settings'}, decorators)

RouteView.register(dashboard, 'trash', '/trash/', 'dashboard/trash.html', {'title': 'Trash'}, decorators)
