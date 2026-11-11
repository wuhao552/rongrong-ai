const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function (req, res, next) {
  if (req.url.startsWith('/api/image')) {
    const targetUrl = 'https://i0.hdslb.com' + req.url.replace('/api/image', '');
    const proxy = createProxyMiddleware({
      target: targetUrl,
      changeOrigin: true,
      pathRewrite: {
        '^/api/image': ''
      }
    });
    proxy(req, res, next);
  } else {
    next();
  }
};