from flask import Blueprint, redirect, url_for

from app.helpers import RouteView

site = Blueprint('site', __name__, template_folder='templates')
site.error_handler = lambda e: redirect(url_for('site.index'))

RouteView.register(site, 'index', '/', 'site/index.html', {})
RouteView.register(site, 'book_pooja', '/book-pooja/', 'site/book_pooja.html', {})
RouteView.register(site, 'donation', '/donation/', 'site/donation.html', {})
RouteView.register(site, 'volunteer', '/volunteer/', 'site/volunteer.html', {})
RouteView.register(site, 'blog', {'/blog/<string:uid>/': {}}, 'site/post.html', {})
RouteView.register(site, 'event', {'/event/<string:uid>/': {}}, 'site/post.html', {})

