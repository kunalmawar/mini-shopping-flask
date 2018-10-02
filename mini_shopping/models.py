from mini_shopping import db
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return self.username


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return self.sku


class ShoppingList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    store = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('shopping_lists', lazy=True))
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_on = db.Column(db.DateTime, onupdate=datetime.datetime.now)

    def __repr__(self):
        return self.title


class ListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shopping_list_id = db.Column(db.Integer, db.ForeignKey('shopping_list.id'), nullable=False)
    shopping_list = db.relationship('ShoppingList', backref=db.backref('item_list', lazy=True))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item')
    quantity = db.Column(db.Integer, default=1)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '%s - %s' % (self.shopping_list.title, self.item.sku)