import localforage from "localforage";

// Using config()
localforage.config({
  driver: [
    localforage.INDEXEDDB,
    localforage.LOCALSTORAGE,
    localforage.WEBSQL,
  ],
  name: 'cfk'
});

function notifyUpdate() {
    navigator.serviceWorker.ready.then(function(registration) {
        registration.showNotification('The Coding for Kidz App has been updated', {
                                        lang: "en-US",
                                        title: "Updates",
                                        requireInteraction: true,
                                        body: "This app has been updated to the latest version with the latest changes",
                                        icon: "/static/favicon_ico/favicon-512x512.png",
                                        actions: [{
                                            action: "viewreleasenotes",
                                            title: "View Release Notes"
                                        },
                                        {
                                            action: "close",
                                            title: "Close",
                                        }]
                                    });
      });
}

function updateStaticCache() {
    if (caches.has("static")) {
        caches.delete("static")
    }
    caches.open('static').then((cache) => cache.addAll([
        '/',
        '/about',
        '/offline',
        '/favicon.ico',
        '/service-worker.js',
        'manifest.webmanifest',
        '/static/favicon_ico/favicon-192x192.png',

        // /bootstrap
        '/static/bootstrap/css/bootstrap.css',
        '/static/bootstrap/css/bootstrap.rtl.css',
        '/static/bootstrap/css/bootstrap-grid.css',
        '/static/bootstrap/css/bootstrap-grid.rtl.css',
        '/static/bootstrap/css/bootstrap-reboot.css',
        '/static/bootstrap/css/bootstrap-reboot.rtl.css',
        '/static/bootstrap/css/bootstrap-utilities.css',
        '/static/bootstrap/css/bootstrap-utilities.rtl.css',
        '/static/bootstrap/js/bootstrap.bundle.js',
        '/static/bootstrap/js/bootstrap.esm.js',
        '/static/bootstrap/js/bootstrap.js',
        '/static/bootstrap/css/bootstrap.css.map',
        '/static/bootstrap/js/bootstrap.bundle.js.map',

        // /css
        '/static/css/bundle.min.css',
        '/static/css/writer.css',
        '/static/css/code_editor.css',
        '/os-css.css',

        '/static/favicon_ico/favicon-32x32.png',
        '/static/favicon_ico/favicon.ico',
        '/static/img/home-light.png',
        '/static/img/home-dark.png',
        '/static/img/about-light.png',
        '/static/img/about-dark.png',
        '/static/img/signin-light.png',
        '/static/img/signin-dark.png',
        '/static/img/signup-light.png',
        '/static/img/signup-dark.png',

        // /js
        '/static/js/jquery.js',
        '/static/js/main.js',
        '/static/js/run-code/skulpt-compiler.js',
        '/static/js/run-code/html-viewer.js',

        '/static/sentry/sentry.min.js',

        '/static/skulpt/skulpt.min.js',

        '/static/writer/writer-bundle.js'
    ]));
}

function updateServiceWorker() {
    if ("serviceWorker" in navigator) {
        navigator.serviceWorker.ready.then(function(registration) {
            registration.update();
        })
    }
}

async function checkForAndUpdateStaticCache() {
    let version = await localforage.getItem('cacheVersion')
    if (version === null) {
        await localforage.setItem("cacheVersion", "0");
        version = "0";
    }
    console.debug("[Cache Updater DEBUG] cache version " + version)
    fetch('/static-cache/version/')
        .then(
            function (response) {
                if (response.status !== 200) {
                    console.error('[Cache Updater ERROR] Server error while checking for updates, status code ' + response.status);
                    return;
                }

                // Examine the text in the response
                response.json().then(function (data) {
                    let serverVersion = data.version.substring(0, 16);
                    console.debug("[Cache Updater DEBUG] Server cache version " + serverVersion)
                    if (serverVersion !== version) {
                        updateStaticCache();
                        updateServiceWorker();
                        console.info("[Cache Updater INFO] Update successful")
                        localforage.setItem("cacheVersion", serverVersion);
                        localforage.getItem("notifications").then(notificationsAllowed => {
                            if (notificationsAllowed) {
                                notifyUpdate();
                            }
                        })
                    }
                });
            }
        )
        .catch(function (err) {
            console.error('[Cache Updater ERROR] Fetch error while checking for updates', err);
        });
}

checkForAndUpdateStaticCache();

localforage.getItem('checkForUpdatesTimeout').then(timeout => {
    if (timeout === null) {
        localforage.setItem("checkForUpdatesTimeout", 120000);
        timeout = 120000;
    }

    setInterval(checkForAndUpdateStaticCache, timeout);
});