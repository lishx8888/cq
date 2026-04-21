module.exports = function(db, saveDatabase) {
  const express = require('express');
  const router = express.Router();

  // 获取所有促销横幅
  router.get('/', (req, res) => {
    try {
      const result = db.exec('SELECT * FROM promotions ORDER BY id ASC');
      const promotions = result.length > 0 ? result[0].values.map(row => {
        const columns = result[0].columns;
        return row.reduce((obj, val, i) => {
          obj[columns[i]] = val;
          return obj;
        }, {});
      }) : [];
      res.json({ success: true, data: promotions });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 获取单个促销横幅
  router.get('/:id', (req, res) => {
    try {
      const result = db.exec('SELECT * FROM promotions WHERE id = ?', [parseInt(req.params.id)]);
      if (result.length === 0 || result[0].values.length === 0) {
        return res.status(404).json({ success: false, message: '促销横幅不存在' });
      }
      const columns = result[0].columns;
      const promotion = result[0].values[0].reduce((obj, val, i) => {
        obj[columns[i]] = val;
        return obj;
      }, {});
      res.json({ success: true, data: promotion });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 创建促销横幅
  router.post('/', (req, res) => {
    try {
      const { title, subtitle, button_text, button_link, background_color, position } = req.body;
      db.run(`
        INSERT INTO promotions (title, subtitle, button_text, button_link, background_color, position)
        VALUES (?, ?, ?, ?, ?, ?)
      `, [title, subtitle || null, button_text || null, button_link || '#', background_color || '#F5F5F5', position || 'home']);
      saveDatabase();
      res.json({ success: true, message: '促销横幅创建成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 更新促销横幅
  router.put('/:id', (req, res) => {
    try {
      const { title, subtitle, button_text, button_link, background_color, position } = req.body;
      db.run(`
        UPDATE promotions SET title = ?, subtitle = ?, button_text = ?, button_link = ?, 
        background_color = ?, position = ?
        WHERE id = ?
      `, [title, subtitle || null, button_text || null, button_link || '#', background_color || '#F5F5F5', position || 'home', parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '促销横幅更新成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  // 删除促销横幅
  router.delete('/:id', (req, res) => {
    try {
      db.run('DELETE FROM promotions WHERE id = ?', [parseInt(req.params.id)]);
      saveDatabase();
      res.json({ success: true, message: '促销横幅删除成功' });
    } catch (error) {
      res.status(500).json({ success: false, message: error.message });
    }
  });

  return router;
};