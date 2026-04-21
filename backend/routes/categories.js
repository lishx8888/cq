module.exports = function(db, saveDatabase) {
  const express = require('express');
  const router = express.Router();

  // 获取所有分类
  router.get('/', (req, res) => {
    try {
      const result = db.exec('SELECT * FROM categories ORDER BY sort_order ASC');
      const categories = result.length > 0 ? result[0].values.map(row => {
        const columns = result[0].columns;
        return row.reduce((obj, val, i) => {
          obj[columns[i]] = val;
          return obj;
        }, {});
      }) : [];
      res.json({ success: true, data: categories });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 获取单个分类
  router.get('/:id', (req, res) => {
    try {
      const result = db.exec('SELECT * FROM categories WHERE id = ?', [parseInt(req.params.id)]);
      if (result.length === 0 || result[0].values.length === 0) {
        return res.status(404).json({ success: false, message: '分类不存在' });
      }
      const columns = result[0].columns;
      const category = result[0].values[0].reduce((obj, val, i) => {
        obj[columns[i]] = val;
        return obj;
      }, {});
      res.json({ success: true, data: category });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 创建分类
  router.post('/', (req, res) => {
    try {
      const { name, slug, sort_order, is_active } = req.body;
      db.run(`
        INSERT INTO categories (name, slug, sort_order, is_active)
        VALUES (?, ?, ?, ?)
      `, [name, slug, sort_order || 0, is_active !== false ? 1 : 0]);
      saveDatabase();
      res.json({ success: true, message: '分类创建成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 更新分类
  router.put('/:id', (req, res) => {
    try {
      const { name, slug, sort_order, is_active } = req.body;
      db.run(`
        UPDATE categories SET name = ?, slug = ?, sort_order = ?, is_active = ?
        WHERE id = ?
      `, [name, slug, sort_order || 0, is_active ? 1 : 0, parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '分类更新成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 删除分类
  router.delete('/:id', (req, res) => {
    try {
      db.run('DELETE FROM categories WHERE id = ?', [parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '分类删除成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  return router;
};