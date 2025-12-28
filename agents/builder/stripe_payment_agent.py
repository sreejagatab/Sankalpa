
import sys
import os
# Add the project root to the path to allow direct imports
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from agents.base import BaseAgent

class StripePaymentAgent(BaseAgent):
    def run(self, input_data):
        files = {
            "backend/services/stripe.py": """
import stripe

stripe.api_key = 'sk_test_...'

def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Pro Subscription'},
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='subscription',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )
    return session.url
"""
        }
        return {
            "message": "Stripe payment system scaffolded.",
            "files": files
        }