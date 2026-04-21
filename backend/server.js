const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const initSqlJs = require('sql.js');
const multer = require('multer');

const app = express();
const PORT = 3000;

// 中间件
app.use(cors());
app.use(express.json());

// 文件上传配置
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, 'public/uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    const ext = path.extname(file.originalname);
    cb(null, uniqueSuffix + ext);
  }
});

const upload = multer({ 
  storage,
  limits: { fileSize: 5 * 1024 * 1024 }, // 5MB
  fileFilter: (req, file, cb) => {
    const allowedTypes = /jpeg|jpg|png|gif|webp|svg/;
    const extname = allowedTypes.test(path.extname(file.originalname).toLowerCase());
    const mimetype = allowedTypes.test(file.mimetype);
    if (extname && mimetype) {
      cb(null, true);
    } else {
      cb(new Error('只支持图片文件: jpeg, jpg, png, gif, webp, svg'));
    }
  }
});

// Admin 静态文件（精确匹配）
app.use('/admin', express.static(path.join(__dirname, 'admin')));
app.get('/admin', (req, res) => {
  res.sendFile(path.join(__dirname, 'admin', 'index.html'));
});

// 前台静态文件
app.use(express.static(path.join(__dirname, '../cosmetics-landing')));

// 上传目录（供图片访问）
app.use('/uploads', express.static(path.join(__dirname, 'public/uploads')));

// 图片上传 API
app.post('/api/upload', upload.single('image'), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ success: false, message: '请选择图片文件' });
  }
  const imageUrl = `/uploads/${req.file.filename}`;
  res.json({ success: true, url: imageUrl, filename: req.file.filename });
});

// 上传错误处理
app.use((err, req, res, next) => {
  if (err instanceof multer.MulterError) {
    return res.status(400).json({ success: false, message: err.message });
  }
  if (err) {
    return res.status(400).json({ success: false, message: err.message });
  }
  next();
});

let db;

// 数据库初始化
async function initDatabase() {
  const SQL = await initSqlJs();
  
  const dbPath = path.join(__dirname, 'database.sqlite');
  
  // 尝试加载现有数据库
  if (fs.existsSync(dbPath)) {
    const buffer = fs.readFileSync(dbPath);
    db = new SQL.Database(buffer);
  } else {
    db = new SQL.Database();
  }
  
  // 初始化表
  db.run(`
    CREATE TABLE IF NOT EXISTS categories (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      slug TEXT UNIQUE NOT NULL,
      sort_order INTEGER DEFAULT 0,
      is_active INTEGER DEFAULT 1
    )
  `);
  
  db.run(`
    CREATE TABLE IF NOT EXISTS products (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      category_id INTEGER,
      name TEXT NOT NULL,
      price REAL NOT NULL,
      original_price REAL,
      image TEXT,
      tag TEXT,
      description TEXT,
      stock INTEGER DEFAULT 100,
      is_active INTEGER DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY (category_id) REFERENCES categories(id)
    )
  `);
  
  db.run(`
    CREATE TABLE IF NOT EXISTS banners (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      subtitle TEXT,
      button_text TEXT,
      button_link TEXT,
      image TEXT,
      sort_order INTEGER DEFAULT 0,
      is_active INTEGER DEFAULT 1
    )
  `);
  
  db.run(`
    CREATE TABLE IF NOT EXISTS promotions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      subtitle TEXT,
      button_text TEXT,
      button_link TEXT,
      background_color TEXT,
      position TEXT DEFAULT 'home'
    )
  `);
  
  // 检查是否有数据
  const categoryCount = db.exec('SELECT COUNT(*) as count FROM categories')[0];
  
  if (!categoryCount || categoryCount.values[0][0] === 0) {
    seedData();
  } else {
    // 为已有数据添加 is_active 字段
    try { db.run('ALTER TABLE categories ADD COLUMN is_active INTEGER DEFAULT 1'); } catch(e) {}
    try { db.run('ALTER TABLE products ADD COLUMN stock INTEGER DEFAULT 100'); } catch(e) {}
    try { db.run('ALTER TABLE products ADD COLUMN is_active INTEGER DEFAULT 1'); } catch(e) {}
    try { db.run('ALTER TABLE banners ADD COLUMN is_active INTEGER DEFAULT 1'); } catch(e) {}
  }
  
  saveDatabase();
}

// 保存数据库到文件
function saveDatabase() {
  const data = db.export();
  const buffer = Buffer.from(data);
  fs.writeFileSync(path.join(__dirname, 'database.sqlite'), buffer);
}

// 插入示例数据
function seedData() {
  // 插入分类
  const categories = [
    ['畅销单品', 'bestseller', 1],
    ['精华液', 'serum', 2],
    ['保湿修护', 'moisturizer', 3],
    ['新品', 'new', 4],
    ['冻干粉', 'freeze-dried', 5],
    ['爽肤水', 'toner', 6],
    ['护肤胶囊', 'capsule', 7]
  ];
  categories.forEach(cat => {
    db.run('INSERT INTO categories (name, slug, sort_order) VALUES (?, ?, ?)', cat);
  });

  // 插入产品
  const products = [
    [1, '生物活性神经酰胺保湿霜', 168, 198, 'https://placehold.co/400x400/FFF5E6/333?text=Ceramides', '畅销'],
    [1, '透明质酸保湿精华', 128, null, 'https://placehold.co/400x400/E6F0FF/333?text=Hyaluronic', null],
    [1, '视黄醇抗衰老精华', 198, 238, 'https://placehold.co/400x400/FFE6E6/333?text=Retinol', '热卖'],
    [1, '维生素C亮白精华液', 178, null, 'https://placehold.co/400x400/FFFDE6/333?text=Vitamin+C', null],
    [2, '维C亮白精华液', 178, null, 'https://placehold.co/400x400/FFF5E6/333?text=VC+Serum', null],
    [2, '烟酰胺控油精华', 158, 188, 'https://placehold.co/400x400/E6FFE6/333?text=Niacinamide', '新品'],
    [2, '玻尿酸保湿精华', 138, null, 'https://placehold.co/400x400/E6F0FF/333?text=Hyaluronic', null],
    [2, 'EGF修复精华液', 218, null, 'https://placehold.co/400x400/FFE6F0/333?text=EGF', null],
    [3, '屏障修护保湿霜', 188, 228, 'https://placehold.co/400x400/FFF5E6/333?text=Barrier', '热卖'],
    [3, '深层补水乳霜', 158, null, 'https://placehold.co/400x400/E6F5FF/333?text=Hydrating', null],
    [3, '积雪草舒缓霜', 168, null, 'https://placehold.co/400x400/E6FFE6/333?text=Cica', null],
    [3, '胶原蛋白面霜', 238, 288, 'https://placehold.co/400x400/FFF0E6/333?text=Collagen', '新品'],
    [4, '外泌体焕活精华液', 298, null, 'https://placehold.co/400x400/F0E6FF/333?text=Exosome', '新品'],
    [4, '益生菌平衡精华', 188, null, 'https://placehold.co/400x400/E6FFF0/333?text=Probiotic', '新品'],
    [4, '蓝铜胜肽修护霜', 258, null, 'https://placehold.co/400x400/E6F0FF/333?text=Copper+Peptide', '新品'],
    [4, '烟酰胺亮肤精华', 168, null, 'https://placehold.co/400x400/FFE6E6/333?text=Niacinamide+Plus', '新品'],
    [5, '寡肽修护冻干粉', 198, null, 'https://placehold.co/400x400/FFF5E6/333?text=Oligopeptide', null],
    [5, '胶原蛋白冻干粉', 228, 268, 'https://placehold.co/400x400/E6F0FF/333?text=Collagen+FD', null],
    [5, '虾青素抗氧化冻干粉', 258, null, 'https://placehold.co/400x400/FFF0E6/333?text=Astaxanthin', null],
    [5, '传明酸美白冻干粉', 188, null, 'https://placehold.co/400x400/F0E6E6/333?text=Tranexamic', null],
    [6, '金盏花舒缓爽肤水', 128, null, 'https://placehold.co/400x400/FFFDE6/333?text=Calendula', null],
    [6, '玫瑰纯露爽肤水', 118, 138, 'https://placehold.co/400x400/FFE6E6/333?text=Rose+Water', null],
    [6, '茶树控油爽肤水', 108, null, 'https://placehold.co/400x400/E6FFE6/333?text=Tea+Tree', null],
    [6, '烟酰胺亮肤爽肤水', 138, null, 'https://placehold.co/400x400/FFE6F0/333?text=Niacinamide+Toner', null],
    [7, '维E修护胶囊', 168, null, 'https://placehold.co/400x400/FFF5E6/333?text=Vitamin+E', null],
    [7, '视黄醇抗衰胶囊', 228, 268, 'https://placehold.co/400x400/E6F0FF/333?text=Retinol+Capsule', null],
    [7, '维C亮白胶囊', 198, null, 'https://placehold.co/400x400/FFFDE6/333?text=VC+Capsule', null],
    [7, '日夜修护胶囊套装', 368, 428, 'https://placehold.co/400x400/F0E6FF/333?text=Day+Night+Set', '热卖']
  ];
  products.forEach(prod => {
    db.run('INSERT INTO products (category_id, name, price, original_price, image, tag) VALUES (?, ?, ?, ?, ?, ?)', prod);
  });

  // 插入轮播图
  const banners = [
    ['生物活性神经酰胺保湿霜', '深层修护肌肤屏障，改善干燥敏感', '立即选购', '/product.html?id=1', 'https://placehold.co/800x600/FFF5E6/333?text=Banner+1', 1],
    ['透明质酸保湿精华', '三重分子量渗透，12小时持续保湿', '了解详情', '/product.html?id=2', 'https://placehold.co/800x600/E6F0FF/333?text=Banner+2', 2],
    ['视黄醇抗衰老精华', '淡化细纹皱纹，重现肌肤年轻态', '限时特惠', '/product.html?id=3', 'https://placehold.co/800x600/FFE6E6/333?text=Banner+3', 3],
    ['维生素C亮白精华液', '高浓度维C，提亮肤色抗氧化', '立即选购', '/product.html?id=4', 'https://placehold.co/800x600/FFFDE6/333?text=Banner+4', 4],
    ['外泌体焕活精华液', '前沿生物科技，唤醒肌肤活力', '新品首发', '/product.html?id=13', 'https://placehold.co/800x600/F0E6FF/333?text=Banner+5', 5]
  ];
  banners.forEach(banner => {
    db.run('INSERT INTO banners (title, subtitle, button_text, button_link, image, sort_order) VALUES (?, ?, ?, ?, ?, ?)', banner);
  });

  // 插入促销横幅
  db.run('INSERT INTO promotions (title, subtitle, button_text, button_link, background_color, position) VALUES (?, ?, ?, ?, ?, ?)', 
    ['新用户首单立减50元', '使用优惠码 WELCOME50', '领取优惠', '#', '#F5F5F5', 'home']);

  console.log('示例数据已插入');
  saveDatabase();
}

// API 路由
const productsRouter = require('./routes/products')(db, saveDatabase);
const categoriesRouter = require('./routes/categories')(db, saveDatabase);
const bannersRouter = require('./routes/banners')(db, saveDatabase);
const promotionsRouter = require('./routes/promotions')(db, saveDatabase);

app.use('/api/products', productsRouter);
app.use('/api/categories', categoriesRouter);
app.use('/api/banners', bannersRouter);
app.use('/api/promotions', promotionsRouter);

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 启动
initDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`\n🚀 Daidy API 服务已启动`);
    console.log(`📍 http://localhost:${PORT}`);
    console.log(`📦 数据库: database.sqlite\n`);
  });
}).catch(err => {
  console.error('数据库初始化失败:', err);
  process.exit(1);
});