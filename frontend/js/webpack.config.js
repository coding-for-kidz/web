const path = require('path');

module.exports = {
  entry: ['./notifications.js', './cacheUpdate.js', './pwa.js'],
  output: {
    filename: './main.js',
    path: path.resolve(__dirname, '..', '..', 'website', 'static', 'js'),
  },
  mode: 'production'
};
