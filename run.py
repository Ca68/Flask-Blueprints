from app import create_app, db
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post
from app.blueprints.shop.models import Cart, Order, Product, StripeProduct

app = create_app()

@app.shell_context_processor
def make_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
        'Cart' : Cart,
        'Order' : Order,
        'Product' : Product,
        'StripeProduct': StripeProduct
    }
