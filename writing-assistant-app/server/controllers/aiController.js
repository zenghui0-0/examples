const axios = require('axios');
const AILog = require('../models/AILog');
const { OPENAI_API_KEY } = process.env;

exports.getCompletions = async (req, res) => {
  try {
    const { text, max_length, creativity } = req.body;
    
    // 记录AI使用情况
    await AILog.create({
      userId: req.user.id,
      action: 'completion',
      length: text.length
    });

    // 调用本地或远程AI服务
    const response = await axios.post('http://ai-service:8000/api/ai/complete', {
      text,
      max_length,
      creativity
    });

    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};
