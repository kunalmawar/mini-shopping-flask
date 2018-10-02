from mini_shopping import app, db
from flask import jsonify, session, request, Blueprint
from mini_shopping.models import ShoppingList, ListItem, Item

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/fetch_shopping_lists/')
def fetch_shopping_lists():
    user_id = session.get('user_id')
    query_string = request.args.get('query_s').strip()
    try:
        sl = ShoppingList.query.filter_by(user_id=user_id)
        if query_string:
            sl = sl.filter(ShoppingList.title.ilike('%' + query_string + '%'))
        sl = sl.order_by(ShoppingList.title)
        data = [{'id': li.id, 'title': li.title, 'store': li.store,
                 'updated_on': li.updated_on if li.updated_on else li.created_on} for li in sl]
    except Exception as e:
        return jsonify({'status': 'failed', 'msg': str(e)})
    return jsonify({'status': 'success', 'data': data})


@app.route('/fetch_items/')
def fetch_items():
    try:
        items = [{'sku': item.sku, 'name': item.name} for item in Item.query.all()]
    except Exception as e:
        return jsonify({'status': 'failed', 'msg': str(e)})
    return jsonify({'status': 'success', 'data': items})


@bp.route('/create_shopping_list/', methods=['POST'])
def create_shopping_list():
    if request.method == 'POST':
        try:
            user_id = session.get('user_id')
            title = request.form['title']
            store = request.form['store']
            if not title or not store:
                return jsonify({'status': 'failed', 'msg': 'Missing Field'})
            if request.form['id']:
                sl = ShoppingList.query.filter_by(id=request.form['id']).first()
                if sl:
                    sl.title = title
                    sl.store = store
                    db.session.commit()
            else:
                new_sl = ShoppingList(title=title, store=store, user_id=user_id)
                db.session.add(new_sl)
                db.session.commit()
        except Exception as e:
            return jsonify({'status': 'failed', 'msg': str(e)})
        return jsonify({'status': 'success', 'msg': 'Shopping List Created'})


@bp.route('/add_item_to_list/', methods=['POST'])
def add_item_to_list():
    if request.method == 'POST':
        try:
            list_id = request.form['list_id']
            quantity = request.form['quantity']
            product_id = request.form['product_id']
            if not list_id:
                return jsonify({'status': 'failed', 'msg': 'List Id Missing'})
            if not quantity:
                return jsonify({'status': 'failed', 'msg': 'Quantity Missing'})
            if not product_id:
                return jsonify({'status': 'failed', 'msg': 'Product Id Missing'})
            li = ListItem.query.filter_by(shopping_list_id=list_id, item_id=product_id).first()
            if li:
                new_quantity = li.quantity + int(quantity)
                if new_quantity == 0:
                    db.session.delete(li)
                else:
                    li.quantity = new_quantity
                db.session.commit()
            else:
                li = ListItem(shopping_list_id=list_id, item_id=product_id, quantity=quantity)
                new_quantity = quantity
                db.session.add(li)
                db.session.commit()
        except Exception as e:
            return jsonify({'status': 'failed', 'msg': str(e)})
        return jsonify({'status': 'success', 'new_quantity': new_quantity})


@bp.route('/delete_shopping_list/', methods=['POST'])
def delete_shopping_list():
    if request.method == 'POST':
        list_id = request.form['id']
        # Deleting items first and then Shopping list
        ListItem.query.filter_by(shopping_list_id=list_id).delete()
        ShoppingList.query.filter_by(id=list_id).delete()
        db.session.commit()
    return jsonify({'status': 'success', 'msg': 'Shopping List Deleted'})