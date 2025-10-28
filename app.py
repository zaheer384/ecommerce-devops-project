from flask import Flask, request, jsonify, render_template_string
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Database configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'productsdb')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS', 'password')

def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def init_db():
    """Initialize database with products table"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    description TEXT,
                    stock INTEGER DEFAULT 0
                )
            ''')
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully!")
        except Exception as e:
            print(f"Database initialization failed: {e}")

# HTML Template for Frontend
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Product Manager</title>
    <style>
        body { font-family: Arial; max-width: 1200px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .form-group { margin: 15px 0; }
        input, textarea { width: 300px; padding: 8px; margin: 5px 0; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .product { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
        .status { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>🛒 Product Management System</h1>
    
    <div id="status"></div>
    
    <h2>Add New Product</h2>
    <div class="form-group">
        <input type="text" id="name" placeholder="Product Name" required>
    </div>
    <div class="form-group">
        <input type="number" id="price" placeholder="Price" step="0.01" required>
    </div>
    <div class="form-group">
        <textarea id="description" placeholder="Description"></textarea>
    </div>
    <div class="form-group">
        <input type="number" id="stock" placeholder="Stock Quantity" required>
    </div>
    <button onclick="addProduct()">Add Product</button>
    
    <h2>Products List</h2>
    <button onclick="loadProducts()">Refresh List</button>
    <div id="products"></div>
    
    <script>
        function showStatus(message, isError = false) {
            const statusDiv = document.getElementById('status');
            statusDiv.className = 'status ' + (isError ? 'error' : 'success');
            statusDiv.textContent = message;
            setTimeout(() => statusDiv.textContent = '', 3000);
        }
        
        async function addProduct() {
            const product = {
                name: document.getElementById('name').value,
                price: parseFloat(document.getElementById('price').value),
                description: document.getElementById('description').value,
                stock: parseInt(document.getElementById('stock').value)
            };
            
            try {
                const response = await fetch('/api/products', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(product)
                });
                
                if (response.ok) {
                    showStatus('Product added successfully!');
                    document.getElementById('name').value = '';
                    document.getElementById('price').value = '';
                    document.getElementById('description').value = '';
                    document.getElementById('stock').value = '';
                    loadProducts();
                } else {
                    showStatus('Failed to add product', true);
                }
            } catch (error) {
                showStatus('Error: ' + error.message, true);
            }
        }
        
        async function loadProducts() {
            try {
                const response = await fetch('/api/products');
                const products = await response.json();
                
                const productsDiv = document.getElementById('products');
                if (products.length === 0) {
                    productsDiv.innerHTML = '<p>No products found. Add some products!</p>';
                } else {
                    productsDiv.innerHTML = products.map(p => `
                        <div class="product">
                            <h3>${p.name} - $${p.price}</h3>
                            <p>${p.description || 'No description'}</p>
                            <p><strong>Stock:</strong> ${p.stock} units</p>
                            <button onclick="deleteProduct(${p.id})">Delete</button>
                        </div>
                    `).join('');
                }
            } catch (error) {
                showStatus('Error loading products: ' + error.message, true);
            }
        }
        
        async function deleteProduct(id) {
            if (confirm('Are you sure you want to delete this product?')) {
                try {
                    const response = await fetch(`/api/products/${id}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        showStatus('Product deleted successfully!');
                        loadProducts();
                    } else {
                        showStatus('Failed to delete product', true);
                    }
                } catch (error) {
                    showStatus('Error: ' + error.message, true);
                }
            }
        }
        
        // Load products when page loads
        loadProducts();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Serve the frontend"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    """Health check endpoint"""
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"status": "healthy", "database": "connected"}), 200
    return jsonify({"status": "unhealthy", "database": "disconnected"}), 503

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM products ORDER BY id DESC')
        products = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        
        if product:
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products', methods=['POST'])
def create_product():
    """Create a new product"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Name and price are required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            'INSERT INTO products (name, price, description, stock) VALUES (%s, %s, %s, %s) RETURNING *',
            (data['name'], data['price'], data.get('description', ''), data.get('stock', 0))
        )
        product = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(product), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    data = request.get_json()
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            'UPDATE products SET name=%s, price=%s, description=%s, stock=%s WHERE id=%s RETURNING *',
            (data.get('name'), data.get('price'), data.get('description'), data.get('stock'), product_id)
        )
        product = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        if product:
            return jsonify(product), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM products WHERE id = %s', (product_id,))
        deleted = cur.rowcount
        conn.commit()
        cur.close()
        conn.close()
        
        if deleted:
            return jsonify({"message": "Product deleted"}), 200
        return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)