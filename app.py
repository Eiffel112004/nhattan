from flask import Flask, render_template, session, redirect, url_for, request
from products import products

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart_items = []
    total = 0
    if 'cart' in session:
        for pid in session['cart']:
            product = next((p for p in products if p['id'] == pid), None)
            if product:
                cart_items.append(product)
                total += product['price']
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
