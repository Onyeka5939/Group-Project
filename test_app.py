import pytest
from app import app, db
from models import Item

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def test_home_page(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_info_endpoint(client):
    """Test info endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    data = response.get_json()
    assert 'project' in data
    assert 'version' in data

# CRUD Tests
def test_list_items_empty(client):
    """Test listing items when empty"""
    response = client.get('/items')
    assert response.status_code == 200

def test_create_item(client):
    """Test creating a new item"""
    response = client.post('/items/new', data={
        'name': 'Test Item',
        'description': 'A test item',
        'price': '19.99',
        'quantity': '5'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Check that the item was created
    item = Item.query.filter_by(name='Test Item').first()
    assert item is not None
    assert item.price == 19.99
    assert item.quantity == 5

def test_list_items_with_data(client):
    """Test listing items with data"""
    # Create an item
    item = Item(name='Item 1', description='Description 1', price=10.0, quantity=5)
    db.session.add(item)
    db.session.commit()
    
    response = client.get('/items')
    assert response.status_code == 200
    assert b'Item 1' in response.data

def test_detail_item(client):
    """Test viewing item details"""
    # Create an item
    item = Item(name='Test Item', description='Test Description', price=25.50, quantity=10)
    db.session.add(item)
    db.session.commit()
    
    response = client.get(f'/items/{item.id}')
    assert response.status_code == 200
    assert b'Test Item' in response.data
    assert b'Test Description' in response.data

def test_edit_item(client):
    """Test editing an item"""
    # Create an item
    item = Item(name='Original Name', description='Original Description', price=15.0, quantity=3)
    db.session.add(item)
    db.session.commit()
    
    response = client.post(f'/items/{item.id}/edit', data={
        'name': 'Updated Name',
        'description': 'Updated Description',
        'price': '20.00',
        'quantity': '8'
    }, follow_redirects=True)
    assert response.status_code == 200
    
    # Verify the item was updated
    updated_item = Item.query.get(item.id)
    assert updated_item.name == 'Updated Name'
    assert updated_item.price == 20.00
    assert updated_item.quantity == 8

def test_delete_item(client):
    """Test deleting an item"""
    # Create an item
    item = Item(name='Item to Delete', description='Will be deleted', price=5.0, quantity=1)
    db.session.add(item)
    db.session.commit()
    item_id = item.id
    
    response = client.post(f'/items/{item_id}/delete', follow_redirects=True)
    assert response.status_code == 200
    
    # Verify the item was deleted
    deleted_item = Item.query.get(item_id)
    assert deleted_item is None

def test_item_not_found(client):
    """Test accessing non-existent item"""
    response = client.get('/items/999')
    assert response.status_code == 404
