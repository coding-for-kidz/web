const path = require('path');


var config = {
    mode: "production"
};

var configBootstrap = Object.assign({}, config, {
    entry: {
        'bootstrap': 'bootstrap.js'
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].js'
    }
});

var configServiceWorker = Object.assign({}, config, {
    name: "configServiceWorker",
    entry: "./serviceWorker/sw.js",
    output: {
        path: path.resolve(__dirname, '..', 'website', 'static'),
        filename: "service-worker.js"
    }
});

var configjs = Object.assign({}, config, {
    name: "js",
      entry: ['./js/cacheUpdate.js', './js/customTags.js', './js/flash.js', './js/notifications.js', './js/pwa.js'],
      output: {
        filename: 'main.js',
        path: path.resolve(__dirname, '..', 'website', 'static', 'js'),
      },
});
var configWriter = Object.assign({}, config, {
    name: "configWriter",
      entry: './writer/index.js',
  output: {
    path: path.resolve(__dirname, '..', 'website', 'static', 'writer'),
    filename: 'writer-bundle.js',
  },
})
var configSentry = Object.assign({}, config, {
    name: "configSentry",
  entry: './sentry/index.js',
  output: {
    path: path.resolve(__dirname, '..', 'website', 'static', 'sentry'),
    filename: 'sentry.min.js',
  },
})
var configSettings = Object.assign({}, config, {
    name: "configSettings",
  entry: './settings/index.js',
  output: {
    path: path.resolve(__dirname, '..', 'website', 'static', 'settings'),
    filename: 'settings.min.js',
  },
})

var configPWASettings = Object.assign({}, config, {
    name: "configPWASettings",
    entry: "./pwaSettings/save.js",
    output: {
        path: path.resolve(__dirname, "..", "website", "static", "pwaSettings"),
        filename: "pwaSettings.min.js"
    }
})
// Return Array of Configuration
module.exports = [configServiceWorker, configjs, configWriter, configSentry, configSettings, configPWASettings];