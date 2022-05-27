from flask import Blueprint, redirect, url_for

from app.helpers import RouteView

site = Blueprint('site', __name__, template_folder='templates')
site.error_handler = lambda e: redirect(url_for('site.index'))

RouteView.register(site, 'index', '/', 'site/index.html', {})
RouteView.register(site, 'book_pooja', '/book-pooja/', 'site/book_pooja.html', {})
RouteView.register(site, 'donation', '/donation/', 'site/donation.html', {})
RouteView.register(site, 'blog', '/blog/', 'site/blog.html', {})
