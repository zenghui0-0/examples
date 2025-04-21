const express = require('express');
const router = express.Router();
const aiController = require('../controllers/aiController');
const { authenticate } = require('../middleware/auth');

router.post('/complete', authenticate, aiController.getCompletions);
router.post('/expand', authenticate, aiController.expandText);
router.post('/rewrite', authenticate, aiController.rewriteText);

module.exports = router;
