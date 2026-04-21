from datetime import datetime
import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(__file__), 'skincare.db')

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            icon TEXT DEFAULT '',
            description TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_id INTEGER,
            image_url TEXT DEFAULT '',
            gallery TEXT DEFAULT '[]',
            specs TEXT DEFAULT '',
            ingredients TEXT DEFAULT '',
            benefits TEXT DEFAULT '',
            description TEXT DEFAULT '',
            status TEXT DEFAULT 'enabled',
            is_new INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    ''')
    
    # Add is_new column if not exists (for existing databases)
    try:
        cursor.execute("ALTER TABLE products ADD COLUMN is_new INTEGER DEFAULT 0")
    except:
        pass
    
    # Create admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create banners table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS banners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subtitle TEXT DEFAULT '',
            image TEXT DEFAULT '',
            link TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            status TEXT DEFAULT 'enabled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin if not exists
    cursor.execute("SELECT id FROM admins WHERE username = 'admin'")
    if not cursor.fetchone():
        # Default password: admin123
        cursor.execute(
            "INSERT INTO admins (username, password_hash) VALUES (?, ?)",
            ('admin', 'pbkdf2:sha256:600000$salt$hashedpassword')
        )
    
    # Insert default categories if empty
    cursor.execute("SELECT COUNT(*) FROM categories")
    if cursor.fetchone()[0] == 0:
        default_categories = [
            ('洁面系列', '🧴', '温和清洁'),
            ('精华液', '💧', '高效修护'),
            ('面霜乳液', '🧴', '深层保湿'),
            ('防晒护理', '☀️', '防护隔离'),
            ('面膜专区', '✨', '密集滋养'),
            ('套装礼盒', '🎁', '精致礼遇')
        ]
        cursor.executemany(
            "INSERT INTO categories (name, icon, description) VALUES (?, ?, ?)",
            default_categories
        )
    
    # Insert sample products if empty
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            # 洁面系列 (category_id: 1)
            ('玫瑰精粹洁面乳', 1, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600', '120ml', '玫瑰花水、氨基酸表活、玻尿酸', '温和清洁|补水保湿|舒缓肌肤', '蕴含大马士革玫瑰精粹，温和洁净同时锁住肌肤水分'),
            ('氨基酸温和洁面泡沫', 1, 'https://images.unsplash.com/photo-1570194065650-d99fb4b8ccb0?w=600', '150ml', '氨基酸表面活性剂、椰油酰甘氨酸钠', '温和清洁|不紧绷|适合敏感肌', '弱酸性配方，接近皮肤pH值'),
            ('茶树控油洁面乳', 1, 'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=600', '100ml', '茶树精油、活性炭、薄荷脑', '控油祛痘|深层清洁|清爽止痒', '茶树精华调节油脂分泌，告别油光满面'),
            ('蜂蜜滋养洁面膏', 1, 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=600', '90g', '蜂蜜、蜂胶、蜂王浆提取物', '滋养修护|温和洁净|改善暗沉', '天然蜂蜜成分，洗后肌肤嫩滑不干燥'),
            ('绿茶抗氧洁面乳', 1, 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600', '120ml', '绿茶提取物、EGCG、泛醇', '抗氧化|抗污染|舒缓肌肤', '绿茶多酚抵御自由基，清爽每一天'),
            
            # 精华液 (category_id: 2)
            ('维C焕亮精华液', 2, 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600', '30ml', '10%活性维C、烟酰胺、传明酸', '提亮肤色|淡化色斑|抗氧化', '高浓度维C精华，多维改善暗沉肤色'),
            ('视黄醇抗皱精华', 2, 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=600', '30ml', '0.5%视黄醇、透明质酸、胶原蛋白', '抗皱紧致|促进胶原|平滑肌肤', '添加视黄醇成分，有效对抗细纹'),
            ('玻尿酸补水精华', 2, 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=600', '30ml', '三重玻尿酸、泛醇、神经酰胺', '深层补水|锁水保湿|改善干燥', '小分子玻尿酸直达肌底，持久水润'),
            ('烟酰胺美白精华', 2, 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=600', '30ml', '5%烟酰胺、α-熊果苷、光果甘草', '美白淡斑|均匀肤色|抑制黑色素', '科学配比烟酰胺，有效阻断黑色素转运'),
            ('六胜肽抗衰精华', 2, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=600', '30ml', '六胜肽、三肽-1、弹性蛋白', '紧致提拉|淡化细纹|增加弹性', '类肉毒素肽成分，温和对抗衰老痕迹'),
            
            # 面霜乳液 (category_id: 3)
            ('玻尿酸保湿面霜', 3, 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=600', '50g', '玻尿酸、神经酰胺、积雪草提取物', '深层保湿|修复屏障|锁水滋润', '三重玻尿酸配方，24小时持续保湿'),
            ('修护屏障乳液', 3, 'https://images.unsplash.com/photo-1570194065650-d99fb4b8ccb0?w=600', '100ml', '积雪草、马齿苋、泛醇B5', '修护屏障|舒缓敏感|强韧肌肤', '专为敏感肌设计的屏障修护乳'),
            ('胶原蛋白面霜', 3, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600', '50g', '水解胶原蛋白、弹力蛋白、透明质酸', '补充胶原|提升弹性|紧致轮廓', '小分子胶原蛋白易吸收，肌肤饱满有弹性'),
            ('日夜两用保湿霜', 3, 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600', '50g', '神经酰胺、透明质酸、角鲨烷', '24小时保湿|日间防护|夜间修护', '早晚都能用的全能保湿霜'),
            ('控油哑光乳液', 3, 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=600', '80ml', '茶树精华、金缕梅、水杨酸', '控油哑光|收缩毛孔|平衡水油', '油皮亲妈，告别油光困扰'),
            
            # 防晒护理 (category_id: 4)
            ('多效防晒乳 SPF50+', 4, 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=600', '50ml', '氧化锌、二氧化钛、透明质酸', '高效防晒|隔离UVA/UVB|清爽不油腻', '物理防晒配方，轻薄不闷痘'),
            ('轻透隔离防晒霜', 4, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600', '45ml', 'OMC、二氧化钛、烟酰胺', '隔离防晒|提亮肤色|轻薄透气', '妆前隔离一瓶搞定，轻薄如若无物'),
            ('户外运动防晒喷雾', 4, 'https://images.unsplash.com/photo-1570194065650-d99fb4b8ccb0?w=600', '150ml', '阿伏苯宗、蒂萨罗、美全叶', '长效防晒|防水防汗|方便补涂', '喷雾设计，全身可用，方便快捷'),
            ('敏感肌专用防晒', 4, 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=600', '40ml', '氧化锌、甘草酸铵、马齿苋', '温和防晒|舒缓敏感|不刺激', '无酒精无香精，脆弱肌肤也能用'),
            ('防晒妆前隔离乳', 4, 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=600', '30ml', '化学防晒剂、珍珠粉、云母', '防晒隔离|修饰肤色|隐形毛孔', '一抹提亮，妆前打底一步到位'),
            
            # 面膜专区 (category_id: 5)
            ('金盏花舒缓面膜', 5, 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=600', '25ml x 10片', '金盏花提取物、芦荟胶、维生素B5', '舒缓修护|深层补水|镇定肌肤', '天然金盏花精粹，舒缓换季敏感'),
            ('水漾焕亮睡眠面膜', 5, 'https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=600', '80ml', '烟酰胺、透明质酸、泛醇', '夜间修护|提亮肤色|持久保湿', '夜间专用，醒来肌肤水润透亮'),
            ('黑炭清洁泥面膜', 5, 'https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=600', '100ml', '备长炭、高岭土、茶树油', '深层清洁|吸附黑头|收缩毛孔', '黑色泥浆质地，清洁力超强'),
            ('胶原蛋白眼膜贴', 5, 'https://images.unsplash.com/photo-1608248543803-ba4f8c70ae0b?w=600', '60片', '水解胶原蛋白、咖啡因、蛇毒肽', '淡化眼纹|消除黑眼圈|紧致眼周', '眼周专属，集中修护衰老痕迹'),
            ('玻尿酸补水面膜', 5, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600', '25ml x 5片', '大分子玻尿酸、小分子玻尿酸、尿囊素', '密集补水|深层保湿|改善干燥', '医美级补水，敷出水光肌'),
            ('蜂毒焕颜面膜', 5, 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600', '25ml x 10片', '蜂毒肽、透明质酸、玫瑰花水', '紧致提拉|淡化细纹|焕亮肌肤', '天然蜂毒刺激胶原再生'),
            ('鱼子酱奢享面膜', 5, 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=600', '30ml x 6片', '鲟鱼子酱提取物、金箔、珍珠粉', '奢华抗衰|密集修护|重现年轻', '贵妇级成分，极致护肤体验'),
            
            # 套装礼盒 (category_id: 6)
            ('基础护肤三件套', 6, 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=600', '洁面100ml+精华30ml+面霜50g', '氨基酸洁面、玻尿酸精华、保湿面霜', '清洁|补水|保湿', '入门级护肤套装，满足日常基础护理'),
            ('焕亮美白套装', 6, 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=600', '洁面+精华+面霜+面膜', '维C、烟酰胺、熊果苷、传明酸', '美白|淡斑|提亮肤色', '全方位美白方案，告别暗沉黄气'),
            ('敏感肌修护套装', 6, 'https://images.unsplash.com/photo-1570194065650-d99fb4b8ccb0?w=600', '洁面+喷雾+精华+面霜', '积雪草、马齿苋、泛醇、神经酰胺', '舒缓|修护|强韧屏障', '专为敏感肌设计，温和修护受损肌肤'),
            ('抗老紧致套装', 6, 'https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=600', '精华+眼霜+面霜+睡眠面膜', '视黄醇、六胜肽、胶原蛋白、蜂毒肽', '抗皱|紧致|提升轮廓', '对抗衰老迹象，重现年轻态'),
        ]
        cursor.executemany(
            "INSERT INTO products (name, category_id, image_url, specs, ingredients, benefits, description) VALUES (?, ?, ?, ?, ?, ?, ?)",
            sample_products
        )
    
    # Insert sample banners if empty
    cursor.execute("SELECT COUNT(*) FROM banners")
    if cursor.fetchone()[0] == 0:
        sample_banners = [
            ('纯净护肤，焕活肌肤', '天然成分，科学配方，唤醒肌肤本真之美', 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=1920&q=80', '/products', 1),
            ('温和清洁，净透肌肤', '氨基酸配方，温柔呵护每一寸肌肤', 'https://images.unsplash.com/photo-1570194065650-d99fb4b8ccb0?w=1920&q=80', '/products', 2),
            ('深层修护，焕发新生', '高效活性成分，直达肌底深层修护', 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=1920&q=80', '/products', 3)
        ]
        cursor.executemany(
            "INSERT INTO banners (title, subtitle, image, link, sort_order) VALUES (?, ?, ?, ?, ?)",
            sample_banners
        )
    
    # Create settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create videos table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT DEFAULT '',
            video_url TEXT DEFAULT '',
            cover_url TEXT DEFAULT '',
            sort_order INTEGER DEFAULT 0,
            status TEXT DEFAULT 'enabled',
            product_id INTEGER DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Add product_id column if not exists (for existing databases)
    try:
        cursor.execute("ALTER TABLE videos ADD COLUMN product_id INTEGER DEFAULT NULL")
    except:
        pass
    
    # Insert default settings if empty
    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        default_settings = [
            ('site_name', 'Daidy'),
            ('logo_url', ''),
            ('logo_svg', '<svg viewBox="0 0 32 32" fill="none"><circle cx="16" cy="16" r="14" stroke="#2D5A47" stroke-width="2"/><path d="M16 8 C12 12, 10 16, 16 24 C22 16, 20 12, 16 8" fill="#2D5A47"/></svg>'),
            ('consult_enabled', '1'),
        ]
        cursor.executemany(
            "INSERT INTO settings (key, value) VALUES (?, ?)",
            default_settings
        )
    
    # Add consult_enabled setting if not exists
    cursor.execute("SELECT id FROM settings WHERE key = 'consult_enabled'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO settings (key, value) VALUES ('consult_enabled', '1')")
    
    conn.commit()
    conn.close()

# Initialize database on module load
init_db()
