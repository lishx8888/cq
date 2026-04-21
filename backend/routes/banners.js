module.exports = function(db, saveDatabase) {
  const express = require('express');
  const router = express.Router();

  // 获取所有轮播图
  router.get('/', (req, res) => {
    try {
      const result = db.exec('SELECT * FROM banners ORDER BY sort_order ASC');
      const banners = result.length > 0 ? result[0].values.map(row => {
        const columns = result[0].columns;
        return row.reduce((obj, val, i) => {
          obj[columns[i]] = val;
          return obj;
        }, {});
      }) : [];
      res.json({ success: true, data: banners });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 获取单个轮播图
  router.get('/:id', (req, res) => {
    try {
      const result = db.exec('SELECT * FROM banners WHERE id = ?', [parseInt(req.params.id)]);
      if (result.length === 0 || result[0].values.length === 0) {
        return res.status(404).json({ success: false, message: '轮播图不存在' });
      }
      const columns = result[0].columns;
      const banner = result[0].values[0].reduce((obj, val, i) => {
        obj[columns[i]] = val;
        return obj;
      }, {});
      res.json({ success: true, data: banner });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 创建轮播图
  router.post('/', (req, res) => {
    try {
      const { title, subtitle, button_text, button_link, image, sort_order, is_active } = req.body;
      db.run(`
        INSERT INTO banners (title, subtitle, button_text, button_link, image, sort_order, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `, [title, subtitle, button_text, button_link, image, sort_order || 0, is_active !== false ? 1 : 0]);
      saveDatabase();
      res.json({ success: true, message: '轮播图创建成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 更新轮播图
  router.put('/:id', (req, res) => {
    try {
      const { title, subtitle, button_text, button_link, image, sort_order, is_active } = req.body;
      db.run(`
        UPDATE banners SET title = ?, subtitle = ?, button_text = ?, button_link = ?, 
        image = ?, sort_order = ?, is_active = ?
        WHERE id = ?
      `, [title, subtitle, button_text, button_link, image, sort_order || 0, is_active ? 1 : 0, parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '轮播图更新成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 删除轮播图
  router.delete('/:id', (req, res) => {
    try {
      db.run('DELETE FROM banners WHERE id = ?', [parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '轮播图删除成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  return router;
};