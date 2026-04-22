from flask import Flask, jsonify, request, send_from_directory, make_response
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
import json
import os
import uuid
import mimetypes
import models

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'skincare-secret-key-2026'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)
CORS(app)
jwt = JWTManager(app)

# ============= Product APIs =============

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional category filter."""
    category_id = request.args.get('category_id')
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    if category_id:
        cursor.execute(
            "SELECT * FROM products WHERE category_id = ? AND status = 'enabled' ORDER BY created_at DESC",
            (category_id,)
        )
    else:
        cursor.execute(
            "SELECT * FROM products WHERE status = 'enabled' ORDER BY created_at DESC"
        )
    
    products = []
    for row in cursor.fetchall():
        p = dict(row)
        try:
            p['gallery'] = json.loads(p.get('gallery') or '[]')
        except Exception:
            p['gallery'] = []
        try:
            p['detail_images'] = json.loads(p.get('detail_images') or '[]')
        except Exception:
            p['detail_images'] = []
        products.append(p)
    conn.close()
    
    return jsonify({'data': products})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    
    p = dict(product)
    try:
        p['gallery'] = json.loads(p.get('gallery') or '[]')
    except Exception:
        p['gallery'] = []
    try:
        p['detail_images'] = json.loads(p.get('detail_images') or '[]')
    except Exception:
        p['detail_images'] = []
    
    return jsonify({'data': p})

@app.route('/api/products', methods=['POST'])
@jwt_required()
def create_product():
    """Create a new product."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO products (name, category_id, image_url, gallery, specs, ingredients, benefits, description, status, is_new, detail_images)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('category_id'),
        data.get('image_url', ''),
        data.get('gallery', '[]'),
        data.get('specs', ''),
        data.get('ingredients', ''),
        data.get('benefits', ''),
        data.get('description', ''),
        data.get('status', 'enabled'),
        data.get('is_new', 0),
        data.get('detail_images', '[]')
    ))
    
    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Product created', 'id': product_id}), 201

@app.route('/api/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update an existing product."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    # Check if product exists
    cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Product not found'}), 404
    
    cursor.execute('''
        UPDATE products SET
            name = COALESCE(?, name),
            category_id = COALESCE(?, category_id),
            image_url = COALESCE(?, image_url),
            gallery = COALESCE(?, gallery),
            specs = COALESCE(?, specs),
            ingredients = COALESCE(?, ingredients),
            benefits = COALESCE(?, benefits),
            description = COALESCE(?, description),
            status = COALESCE(?, status),
            is_new = COALESCE(?, is_new),
            detail_images = COALESCE(?, detail_images),
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    ''', (
        data.get('name'),
        data.get('category_id'),
        data.get('image_url'),
        data.get('gallery'),
        data.get('specs'),
        data.get('ingredients'),
        data.get('benefits'),
        data.get('description'),
        data.get('status'),
        data.get('is_new'),
        data.get('detail_images'),
        product_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Product updated'})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete a product and its uploaded files."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    # Get product data first (to know which files to delete)
    cursor.execute("SELECT image_url, gallery, detail_images FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return jsonify({'message': 'Product not found'}), 404
    
    # Collect all image paths to delete
    files_to_delete = []
    if row['image_url']:
        files_to_delete.append(row['image_url'])
    if row['gallery']:
        try:
            gallery = json.loads(row['gallery'])
            files_to_delete.extend(gallery)
        except Exception:
            pass
    if row['detail_images']:
        try:
            detail_images = json.loads(row['detail_images'])
            files_to_delete.extend(detail_images)
        except Exception:
            pass
    
    # Delete product from database
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    
    # Delete associated files from disk
    for file_path in files_to_delete:
        # Remove leading /uploads/ if present
        if file_path.startswith('/uploads/'):
            file_path = file_path[10:]
        full_path = os.path.join(UPLOAD_FOLDER, file_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except Exception as e:
                print(f'Failed to delete file {full_path}: {e}')
    
    return jsonify({'message': 'Product deleted'})

@app.route('/api/products/new', methods=['GET'])
def get_new_products():
    """Get products marked as new (for homepage)."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM products WHERE is_new = 1 AND status = 'enabled' ORDER BY updated_at DESC"
    )
    products = []
    for row in cursor.fetchall():
        p = dict(row)
        try:
            p['gallery'] = json.loads(p.get('gallery') or '[]')
        except Exception:
            p['gallery'] = []
        products.append(p)
    conn.close()
    
    return jsonify({'data': products})

@app.route('/api/products/new', methods=['PUT'])
@jwt_required()
def set_new_products():
    """Set which products are marked as new for homepage."""
    data = request.get_json()
    product_ids = data.get('product_ids', [])
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    # First, set all products to not new
    cursor.execute("UPDATE products SET is_new = 0")
    
    # Then set selected products as new (max 4)
    for product_id in product_ids[:4]:
        cursor.execute(
            "UPDATE products SET is_new = 1 WHERE id = ?",
            (product_id,)
        )
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'New products updated'})

# ============= Category APIs =============

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all categories."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT c.*, COUNT(p.id) as product_count FROM categories c LEFT JOIN products p ON c.id = p.category_id GROUP BY c.id ORDER BY c.sort_order, c.id")
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'data': categories})

@app.route('/api/categories', methods=['POST'])
@jwt_required()
def create_category():
    """Create a new category."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO categories (name, icon, description, sort_order)
        VALUES (?, ?, ?, ?)
    ''', (
        data.get('name'),
        data.get('icon', ''),
        data.get('description', ''),
        data.get('sort_order', 0)
    ))
    
    category_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Category created', 'id': category_id}), 201

@app.route('/api/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    """Update an existing category."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM categories WHERE id = ?", (category_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Category not found'}), 404
    
    cursor.execute('''
        UPDATE categories SET
            name = COALESCE(?, name),
            icon = COALESCE(?, icon),
            description = COALESCE(?, description),
            sort_order = COALESCE(?, sort_order)
        WHERE id = ?
    ''', (
        data.get('name'),
        data.get('icon'),
        data.get('description'),
        data.get('sort_order'),
        category_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Category updated'})

@app.route('/api/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    """Delete a category."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM categories WHERE id = ?", (category_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Category not found'}), 404
    
    cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Category deleted'})

# ============= Admin APIs =============

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Admin login endpoint."""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'message': 'Username and password required'}), 400
        
        # Check credentials - for demo, accept 'admin' / 'admin123'
        if username == 'admin' and password == 'admin123':
            access_token = create_access_token(identity=username)
            return jsonify({'token': access_token})
        
        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        # Log the error for debugging
        print(f"Login error: {str(e)}")
        # Even if there's an error, allow demo login for admin/admin123
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        if username == 'admin' and password == 'admin123':
            access_token = create_access_token(identity=username)
            return jsonify({'token': access_token})
        return jsonify({'message': 'Login failed. Please try again.'}), 500

@app.route('/api/admin/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """Get admin dashboard statistics."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM products")
    product_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM categories")
    category_count = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'data': {
            'products': product_count,
            'categories': category_count
        }
    })

# ============= Banner APIs =============

@app.route('/api/banners', methods=['GET'])
def get_banners():
    """Get all banners."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM banners WHERE status = 'enabled' ORDER BY sort_order, id")
    banners = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'data': banners})

@app.route('/api/banners', methods=['POST'])
@jwt_required()
def create_banner():
    """Create a new banner."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO banners (title, subtitle, image, link, sort_order, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title'),
        data.get('subtitle', ''),
        data.get('image', ''),
        data.get('link', ''),
        data.get('sort_order', 0),
        data.get('status', 'enabled')
    ))
    
    banner_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Banner created', 'id': banner_id}), 201

@app.route('/api/banners/<int:banner_id>', methods=['PUT'])
@jwt_required()
def update_banner(banner_id):
    """Update an existing banner."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM banners WHERE id = ?", (banner_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Banner not found'}), 404
    
    cursor.execute('''
        UPDATE banners SET
            title = COALESCE(?, title),
            subtitle = COALESCE(?, subtitle),
            image = COALESCE(?, image),
            link = COALESCE(?, link),
            sort_order = COALESCE(?, sort_order),
            status = COALESCE(?, status)
        WHERE id = ?
    ''', (
        data.get('title'),
        data.get('subtitle'),
        data.get('image'),
        data.get('link'),
        data.get('sort_order'),
        data.get('status'),
        banner_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Banner updated'})

@app.route('/api/banners/<int:banner_id>', methods=['DELETE'])
@jwt_required()
def delete_banner(banner_id):
    """Delete a banner."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM banners WHERE id = ?", (banner_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Banner not found'}), 404
    
    cursor.execute("DELETE FROM banners WHERE id = ?", (banner_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Banner deleted'})

# ============= Settings APIs =============

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get all settings."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT key, value FROM settings")
    settings = {}
    for row in cursor.fetchall():
        settings[row['key']] = row['value']
    conn.close()
    
    return jsonify({'data': settings})

@app.route('/api/settings/<setting_key>', methods=['PUT'])
@jwt_required()
def update_setting(setting_key):
    """Update a single setting."""
    data = request.get_json()
    value = data.get('value', '')
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO settings (key, value) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
    ''', (setting_key, value))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Setting updated'})

@app.route('/api/settings/logo', methods=['POST'])
@jwt_required()
def upload_logo():
    """Upload logo image."""
    if 'logo' not in request.files:
        return jsonify({'message': 'No file provided'}), 400
    
    file = request.files['logo']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(f'logo_{uuid.uuid4().hex[:8]}_{file.filename}')
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Save to settings
        logo_url = f'/uploads/{filename}'
        conn = models.get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO settings (key, value) VALUES ('logo_url', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
        ''', (logo_url,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Logo uploaded', 'url': logo_url})
    
    return jsonify({'message': 'Invalid file type'}), 400

# ============= Health Check =============

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

# ============= Video APIs =============

@app.route('/api/videos', methods=['GET'])
def get_videos():
    """Get all videos."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM videos WHERE status = 'enabled' ORDER BY sort_order, id")
    videos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'data': videos})

@app.route('/api/videos/all', methods=['GET'])
@jwt_required()
def get_all_videos():
    """Get all videos (including disabled) for admin."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM videos ORDER BY sort_order, id")
    videos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'data': videos})

@app.route('/api/videos', methods=['POST'])
@jwt_required()
def create_video():
    """Create a new video."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO videos (title, description, video_url, cover_url, sort_order, status, product_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get('title'),
        data.get('description', ''),
        data.get('video_url', ''),
        data.get('cover_url', ''),
        data.get('sort_order', 0),
        data.get('status', 'enabled'),
        data.get('product_id')
    ))
    
    video_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Video created', 'id': video_id}), 201

@app.route('/api/videos/<int:video_id>', methods=['PUT'])
@jwt_required()
def update_video(video_id):
    """Update an existing video."""
    data = request.get_json()
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM videos WHERE id = ?", (video_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Video not found'}), 404
    
    cursor.execute('''
        UPDATE videos SET
            title = COALESCE(?, title),
            description = COALESCE(?, description),
            video_url = COALESCE(?, video_url),
            cover_url = COALESCE(?, cover_url),
            sort_order = COALESCE(?, sort_order),
            status = COALESCE(?, status),
            product_id = ?
        WHERE id = ?
    ''', (
        data.get('title'),
        data.get('description'),
        data.get('video_url'),
        data.get('cover_url'),
        data.get('sort_order'),
        data.get('status'),
        data.get('product_id'),
        video_id
    ))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Video updated'})

@app.route('/api/videos/<int:video_id>', methods=['DELETE'])
@jwt_required()
def delete_video(video_id):
    """Delete a video."""
    conn = models.get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM videos WHERE id = ?", (video_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Video not found'}), 404
    
    cursor.execute("DELETE FROM videos WHERE id = ?", (video_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Video deleted'})

@app.route('/api/videos/reorder', methods=['PUT'])
@jwt_required()
def reorder_videos():
    """Reorder videos."""
    data = request.get_json()
    video_ids = data.get('video_ids', [])
    
    conn = models.get_db()
    cursor = conn.cursor()
    
    for index, video_id in enumerate(video_ids):
        cursor.execute("UPDATE videos SET sort_order = ? WHERE id = ?", (index, video_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Videos reordered'})

# ============= Image Upload API =============

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'ogg', 'mov'}

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower() if len(filename.rsplit('.', 1)) > 1 else ''
    return ext in ALLOWED_EXTENSIONS

def allowed_video_file(filename):
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower() if len(filename.rsplit('.', 1)) > 1 else ''
    return ext in ALLOWED_VIDEO_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
@jwt_required()
def upload_image():
    """Upload an image file to image hosting service and return the URL."""
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'message': 'File type not allowed'}), 400
    
    try:
        import urllib.request
        import json
        
        # 图床地址
        host = 'https://pic.lishx.dpdns.org'
        upload_url = f'{host}/upload'
        
        # 读取文件内容
        file_content = file.stream.read()
        
        # 构建multipart/form-data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        parts = []
        parts.append(f'--{boundary}'.encode('utf-8'))
        parts.append(f'Content-Disposition: form-data; name="file"; filename="{file.filename}"'.encode('utf-8'))
        parts.append(f'Content-Type: {file.mimetype}'.encode('utf-8'))
        parts.append(b'')
        parts.append(file_content)
        parts.append(f'--{boundary}--'.encode('utf-8'))
        
        data = b'\r\n'.join(parts)
        
        # 构建请求
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(data)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        req = urllib.request.Request(upload_url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.getcode() == 200:
                response_body = response.read()
                
                # 检查是否是gzip压缩的响应
                content_encoding = response.headers.get('Content-Encoding', '')
                if 'gzip' in content_encoding:
                    import gzip
                    response_body = gzip.decompress(response_body)
                
                result = json.loads(response_body.decode('utf-8'))
                # 图床返回格式: [{"src": "/file/xxx"}]
                if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
                    image_path = result[0]['src']
                    image_url = f'{host}{image_path}'
                    return jsonify({'url': image_url})
                # 或者返回错误
                elif isinstance(result, dict) and 'error' in result:
                    return jsonify({'message': f'图床上传失败: {result["error"]}'}), 502
            
            return jsonify({'message': f'图床上传失败: HTTP {response.getcode()}'}), 502
            
    except Exception as e:
        print(f"Image upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        # 上传到图床失败，返回错误（禁用本地存储）
        return jsonify({'message': f'图床上传失败: {str(e)}'}), 502

@app.route('/api/upload/video', methods=['POST'])
@jwt_required()
def upload_video():
    """Upload a video file to image hosting service and return the URL."""
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    if not allowed_video_file(file.filename):
        return jsonify({'message': 'Video file type not allowed. Allowed: mp4, webm, ogg, mov'}), 400
    
    try:
        import urllib.request
        import json
        
        # 图床地址
        host = 'https://pic.lishx.dpdns.org'
        upload_url = f'{host}/upload'
        
        # 读取文件内容
        file_content = file.stream.read()
        
        # 构建multipart/form-data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        parts = []
        parts.append(f'--{boundary}'.encode('utf-8'))
        parts.append(f'Content-Disposition: form-data; name="file"; filename="{file.filename}"'.encode('utf-8'))
        parts.append(f'Content-Type: {file.mimetype}'.encode('utf-8'))
        parts.append(b'')
        parts.append(file_content)
        parts.append(f'--{boundary}--'.encode('utf-8'))
        
        data = b'\r\n'.join(parts)
        
        # 构建请求
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(data)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        req = urllib.request.Request(upload_url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=60) as response:
            if response.getcode() == 200:
                response_body = response.read()
                
                # 检查是否是gzip压缩的响应
                content_encoding = response.headers.get('Content-Encoding', '')
                if 'gzip' in content_encoding:
                    import gzip
                    response_body = gzip.decompress(response_body)
                
                result = json.loads(response_body.decode('utf-8'))
                # 图床返回格式: [{"src": "/file/xxx"}]
                if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
                    video_path = result[0]['src']
                    video_url = f'{host}{video_path}'
                    return jsonify({'url': video_url})
                # 或者返回错误
                elif isinstance(result, dict) and 'error' in result:
                    return jsonify({'message': f'图床上传失败: {result["error"]}'}), 502
            
            return jsonify({'message': f'图床上传失败: HTTP {response.getcode()}'}), 502
            
    except Exception as e:
        print(f"Video upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        # 上传到图床失败，返回错误（禁用本地存储）
        return jsonify({'message': f'图床上传失败: {str(e)}'}), 502

@app.route('/api/upload/cover', methods=['POST'])
@jwt_required()
def upload_cover():
    """Upload a video cover image to image hosting service and return the URL."""
    if 'file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'message': 'Image file type not allowed'}), 400
    
    try:
        import urllib.request
        import json
        
        # 图床地址
        host = 'https://pic.lishx.dpdns.org'
        upload_url = f'{host}/upload'
        
        # 读取文件内容
        file_content = file.stream.read()
        
        # 构建multipart/form-data
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        parts = []
        parts.append(f'--{boundary}'.encode('utf-8'))
        parts.append(f'Content-Disposition: form-data; name="file"; filename="{file.filename}"'.encode('utf-8'))
        parts.append(f'Content-Type: {file.mimetype}'.encode('utf-8'))
        parts.append(b'')
        parts.append(file_content)
        parts.append(f'--{boundary}--'.encode('utf-8'))
        
        data = b'\r\n'.join(parts)
        
        # 构建请求
        headers = {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(len(data)),
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
        req = urllib.request.Request(upload_url, data=data, headers=headers, method='POST')
        
        with urllib.request.urlopen(req, timeout=30) as response:
            if response.getcode() == 200:
                response_body = response.read()
                
                # 检查是否是gzip压缩的响应
                content_encoding = response.headers.get('Content-Encoding', '')
                if 'gzip' in content_encoding:
                    import gzip
                    response_body = gzip.decompress(response_body)
                
                result = json.loads(response_body.decode('utf-8'))
                # 图床返回格式: [{"src": "/file/xxx"}]
                if isinstance(result, list) and len(result) > 0 and 'src' in result[0]:
                    image_path = result[0]['src']
                    image_url = f'{host}{image_path}'
                    return jsonify({'url': image_url})
                # 或者返回错误
                elif isinstance(result, dict) and 'error' in result:
                    return jsonify({'message': f'图床上传失败: {result["error"]}'}), 502
            
            return jsonify({'message': f'图床上传失败: HTTP {response.getcode()}'}), 502
            
    except Exception as e:
        print(f"Cover upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        # 上传到图床失败，返回错误（禁用本地存储）
        return jsonify({'message': f'图床上传失败: {str(e)}'}), 502

# ============= Custom URL API =============
@app.route('/api/upload/url', methods=['POST'])
@jwt_required()
def upload_by_url():
    """Accept custom URL for images/videos (e.g., from image hosting services)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No data provided'}), 400
        
        url = data.get('url')
        if not url:
            return jsonify({'message': 'URL is required'}), 400
        
        # Validate URL format
        if not (url.startswith('http://') or url.startswith('https://')):
            return jsonify({'message': 'Invalid URL format'}), 400
        
        # Return the provided URL directly
        return jsonify({
            'url': url
        })
    except Exception as e:
        print(f"URL upload error: {str(e)}")
        return jsonify({'message': 'Invalid request'}), 400

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files."""
    # Determine MIME type based on file extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    mime_types = {
        'mp4': 'video/mp4',
        'webm': 'video/webm',
        'ogg': 'video/ogg',
        'mov': 'video/quicktime',
        'avi': 'video/x-msvideo',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'svg': 'image/svg+xml'
    }
    
    response = make_response(send_from_directory(UPLOAD_FOLDER, filename))
    response.headers['Content-Type'] = mime_types.get(ext, 'application/octet-stream')
    return response

# ============= Media Library API =============
@app.route('/api/media/list', methods=['GET'])
@jwt_required()
def get_media_list():
    """Get list of all uploaded images and videos."""
    images = []
    videos = []
    
    try:
        for f in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, f)
            if os.path.isfile(filepath):
                url = f'/uploads/{f}'
                if f.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
                    videos.append({'filename': f, 'url': url, 'size': os.path.getsize(filepath)})
                else:
                    images.append({'filename': f, 'url': url, 'size': os.path.getsize(filepath)})
        
        # Sort by filename descending (newest first)
        videos.sort(key=lambda x: x['filename'], reverse=True)
        images.sort(key=lambda x: x['filename'], reverse=True)
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500
    
    return jsonify({
        'code': 200,
        'data': {
            'images': images,
            'videos': videos
        }
    })

@app.route('/api/media/delete', methods=['POST'])
@jwt_required()
def delete_media():
    """Delete an uploaded file."""
    data = request.get_json()
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'code': 400, 'message': 'Filename required'})
    
    # Security: prevent path traversal
    if '..' in filename or '/' in filename or '\\' in filename:
        return jsonify({'code': 400, 'message': 'Invalid filename'})
    
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            return jsonify({'code': 200, 'message': 'Deleted successfully'})
        except Exception as e:
            return jsonify({'code': 500, 'message': str(e)}), 500
    else:
        return jsonify({'code': 404, 'message': 'File not found'})

@app.route('/api/media/batch-delete', methods=['POST'])
@jwt_required()
def batch_delete_media():
    """Batch delete uploaded files."""
    data = request.get_json()
    filenames = data.get('filenames', [])
    
    if not filenames or not isinstance(filenames, list):
        return jsonify({'code': 400, 'message': 'Filenames required as a list'})
    
    # Security: prevent path traversal
    for filename in filenames:
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({'code': 400, 'message': 'Invalid filename'})
    
    deleted_count = 0
    for filename in filenames:
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete {filename}: {str(e)}")
    
    return jsonify({'code': 200, 'message': f'Successfully deleted {deleted_count} files', 'deleted_count': deleted_count})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
