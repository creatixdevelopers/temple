from flask import Blueprint, redirect, url_for

from app.utils import RouteView

site = Blueprint('site', __name__, template_folder='templates')
site.error_handler = lambda e: redirect(url_for('site.index'))

RouteView.register(site, 'index', '/', 'site/index.html', {'title': 'Home'})
RouteView.register(site, 'what_we_do', '/what-we-do/', 'site/what_we_do.html', {'title': 'What We Do'})
RouteView.register(site, 'book_pooja', '/book-pooja/', 'site/book_pooja.html', {'title': 'Book Pooja'})
RouteView.register(site, 'donation', '/donation/', 'site/donation.html', {'title': 'Donation'})
RouteView.register(site, 'volunteer', '/volunteer/', 'site/volunteer.html', {'title': 'Volunteer'})
RouteView.register(site, 'blog', {'/blog/<string:uid>/': {}}, 'site/post.html', {'title': 'Blog'})
RouteView.register(site, 'event', {'/event/<string:uid>/': {}}, 'site/post.html', {'title': 'Event'})
RouteView.register(site, 'pooja_page', '/pooja-page/', 'site/pooja_page.html', {'title': 'Pooja Page'})

RouteView.register(site, 'terms_and_conditions', '/terms-and-conditions/', 'site/legal/terms_and_conditions.html', {'title': 'Terms and Conditions'})
RouteView.register(site, 'terms_of_use', '/terms-of-use/', 'site/legal/terms_of_use.html', {'title': 'Terms Of Use'})
RouteView.register(site, 'privacy_policy', '/privacy-policy/', 'site/legal/privacy_policy.html', {'title': 'Privacy Policy'})
RouteView.register(site, 'refund_policy', '/refund-policy/', 'site/legal/refund_policy.html', {'title': 'Refund and Cancellation Policy'})
RouteView.register(site, 'disclaimer', '/disclaimer/', 'site/legal/disclaimer.html', {'title': 'Disclaimer'})
RouteView.register(site, 'intellectual_property', '/intellectual-property/', 'site/legal/intellectual_property.html',
                   {'title': 'Intellectual Property'})

RouteView.register(site, 'donation_receipt', '/donation-receipt/<string:uid>', 'site/receipts/donation_receipt.html', {'title': 'Donation Receipt'})
RouteView.register(site, 'pooja_receipt', '/pooja-receipt/<string:uid>', 'site/receipts/pooja_receipt.html', {'title': 'Pooja Receipt'})
