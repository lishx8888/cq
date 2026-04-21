module.exports = function(db, saveDatabase) {
  const express = require('express');
  const router = express.Router();

  // 获取所有产品
  router.get('/', (req, res) => {
    try {
      const result = db.exec(`
        SELECT p.*, c.name as category_name 
        FROM products p 
        LEFT JOIN categories c ON p.category_id = c.id 
        ORDER BY p.created_at DESC
      `);
      const products = result.length > 0 ? result[0].values.map(row => {
        const columns = result[0].columns;
        return row.reduce((obj, val, i) => {
          obj[columns[i]] = val;
          return obj;
        }, {});
      }) : [];
      res.json({ success: true, data: products });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 获取单个产品
  router.get('/:id', (req, res) => {
    try {
      const result = db.exec('SELECT * FROM products WHERE id = ?', [parseInt(req.params.id)]);
      if (result.length === 0 || result[0].values.length === 0) {
        return res.status(404).json({ success: false, message: '产品不存在' });
      }
      const columns = result[0].columns;
      const product = result[0].values[0].reduce((obj, val, i) => {
        obj[columns[i]] = val;
        return obj;
      }, {});
      res.json({ success: true, data: product });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 创建产品
  router.post('/', (req, res) => {
    try {
      const { category_id, name, price, original_price, image, tag, description, stock, is_active } = req.body;
      db.run(`
        INSERT INTO products (category_id, name, price, original_price, image, tag, description, stock, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `, [category_id, name, price, original_price || null, image, tag || null, description || null, stock || 100, is_active !== false ? 1 : 0]);
      saveDatabase();
      res.json({ success: true, message: '产品创建成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 更新产品
  router.put('/:id', (req, res) => {
    try {
      const { category_id, name, price, original_price, image, tag, description, stock, is_active } = req.body;
      db.run(`
        UPDATE products SET category_id = ?, name = ?, price = ?, original_price = ?, 
        image = ?, tag = ?, description = ?, stock = ?, is_active = ?
        WHERE id = ?
      `, [category_id, name, price, original_price || null, image, tag || null, description || null, stock || 100, is_active ? 1 : 0, parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '产品更新成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 删除产品
  router.delete('/:id', (req, res) => {
    try {
      db.run('DELETE FROM products WHERE id = ?', [parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '产品删除成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  return router;
};