const express = require('express');
const router = express.Router();
const controller = require('../controllers/index');

// Define routes
router.get('/', controller.home);
router.get('/resources', controller.resources);
router.get('/contact', controller.contact);

// Export the router
module.exports = router;