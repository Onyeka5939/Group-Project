from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from models import db, Item

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Flask DevOps Project is running!'
    })

@app.route('/api/info')
def info():
    return jsonify({
        'project': 'DevOps Group Project',
        'version': '1.0',
        'team': 'Dream Team'
    })

# CRUD Routes
@app.route('/items')
def list_items():
    #Display all items
    items = Item.query.all()
    return render_template('list.html', items=items)

@app.route('/items/new', methods=['GET', 'POST'])
def new_item():
    #Create a new item
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        
        try:
            item = Item(name=name, description=description, price=float(price), quantity=int(quantity))
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('list_items'))
        except Exception as e:
            return f"Error creating item: {str(e)}", 400
    
    return render_template('form.html', item=None, action='Create')

@app.route('/items/<int:id>')
def detail_item(id):
    #Display item details
    item = Item.query.get_or_404(id)
    return render_template('detail.html', item=item)

@app.route('/items/<int:id>/edit', methods=['GET', 'POST'])
def edit_item(id):
#Edit an item
    item = Item.query.get_or_404(id)
    
    if request.method == 'POST':
        item.name = request.form.get('name')
        item.description = request.form.get('description')
        item.price = float(request.form.get('price'))
        item.quantity = int(request.form.get('quantity'))
        
        try:
            db.session.commit()
            return redirect(url_for('detail_item', id=item.id))
        except Exception as e:
            return f"Error updating item: {str(e)}", 400
    
    return render_template('form.html', item=item, action='Edit')

@app.route('/items/<int:id>/delete', methods=['POST'])
def delete_item(id):
    #Delete an item
    item = Item.query.get_or_404(id)
    
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('list_items'))
    except Exception as e:
        return f"Error deleting item: {str(e)}", 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


