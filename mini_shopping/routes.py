from mini_shopping import app
from flask import render_template, request
from mini_shopping.auth import login_required
from mini_shopping.models import ListItem, Item


@login_required
@app.route('/')
def index():
    return render_template('index.html')


@login_required
@app.route('/products/')
def products():
    list_id = request.args.get('id')
    list_items = ListItem.query.filter_by(shopping_list_id=list_id).all()
    helper_dict = dict()
    for li in list_items:
        helper_dict[li.item_id] = li.quantity
    items = [{'id': item.id, 'sku': item.sku, 'name': item.name,
              'quantity': helper_dict[item.id] if item.id in helper_dict else 0} for item in Item.query.all()]
    return render_template('products.html', list_id=list_id, items=items)


@login_required
@app.route('/shopping_lists/')
def shopping_lists():
    return render_template('shopping_lists.html')