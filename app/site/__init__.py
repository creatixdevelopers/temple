from flask import Blueprint, redirect, url_for

from app.helpers import RouteView

site = Blueprint('site', __name__, template_folder='templates')
site.error_handler = lambda e: redirect(url_for('site.index'))

RouteView.register(site, 'index', '/', 'site/index.html', {'title': 'Home'})
RouteView.register(site, 'what_we_do', '/what-we-do/', 'site/what_we_do.html', {'title': 'What We Do'})
RouteView.register(site, 'book_pooja', '/book-pooja/', 'site/book_pooja.html', {'title': 'Book Pooja'})
RouteView.register(site, 'donation', '/donation/', 'site/donation.html', {'title': 'Donation'})
RouteView.register(site, 'volunteer', '/volunteer/', 'site/volunteer.html', {'title': 'Volunteer'})
RouteView.register(site, 'blog', {'/blog/<string:uid>/': {}}, 'site/post.html', {'title': 'Blog'})
RouteView.register(site, 'event', {'/event/<string:uid>/': {}}, 'site/post.html', {'title': 'Event'})
RouteView.register(site, 'terms_and_conditions', '/terms-and-conditions/', 'site/terms_and_conditions.html', {'title': 'Terms and Conditions'})
RouteView.register(site, 'terms_of_use', '/terms-of-use/', 'site/terms_of_use.html', {'title': 'Terms Of Use'})
RouteView.register(site, 'privacy_policy', '/privacy-policy/', 'site/privacy_policy.html', {'title': 'Privacy Policy'})
RouteView.register(site, 'refund_policy', '/refund-policy/', 'site/refund_policy.html', {'title': 'Refund and Cancellation Policy'})
RouteView.register(site, 'disclaimer', '/disclaimer/', 'site/disclaimer.html', {'title': 'Disclaimer'})

