const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const config = require('./config/database');
const { errorHandler } = require('./utils/errorHandlers');

const app = express();

// 数据库连接
mongoose.connect(config.uri, config.options)
  .then(() => console.log('数据库连接成功'))
  .catch(err => console.error('数据库连接失败', err));

// 中间件
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 路由
app.use('/api/auth', require('./routes/authRoutes'));
app.use('/api/docs', require('./routes/docRoutes'));
app.use('/api/ai', require('./routes/aiRoutes'));

// 错误处理
app.use(errorHandler);

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`服务器运行在端口 ${PORT}`));
