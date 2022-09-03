import * as localforage from "localforage";

// Using config()
localforage.config({
  driver: [
    localforage.INDEXEDDB,
    localforage.LOCALSTORAGE,
    localforage.WEBSQL,
  ],
  name: 'cfk'
});



self.addEventListener('install', (e) => {
    localforage.setItem("pwa", true);
});

self.addEventListener('activate', (e) => {
    self.clients.claim();
});

self.addEventListener( "fetch", event => {
    let request = event.request;

    try {
        event.respondWith(
            // Check the cache first to see if the asset exists, and if it does,
            // return the cached asset.
            caches.match( request, {ignoreSearch: true})
                  .then( cached_result => {
                if ( cached_result ) {
                    console.debug('[Service Worker DEBUG] Using cache');
                    return cached_result;
                }
                else {
                    console.debug('[Service Worker DEBUG] Using Network');
                    // If the asset isn't in the cache, fall back to a network request
                    // for the asset, and proceed to cache the result.
                    return fetch(request).then( response => {
                        return response;
                    })
                    // If the network is unavailable to make a request, pull the offline
                    // page out of the cache.
                    .catch(() => caches.match( "/offline" ));
                }

            })
        ); // end respondWith
    }
    catch (e) {
        console.error("[Service Worker ERROR] " + e.toString())
    }
});


self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    if (event.action === 'viewreleasenotes') {
    var promise = new Promise(function(resolve) {
            setTimeout(resolve, 10);
        }).then(function() {
            // return the promise returned by openWindow, just in case.
            // Opening any origin only works in Chrome 43+.
            return clients.openWindow('/release-notes');
        });

        // Now wait for the promise to keep the permission alive.
        event.waitUntil(promise);
    }
}, false);

