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

// Register service worker to control making site work offline
if ('serviceWorker' in navigator) {
  navigator.serviceWorker
    .register('/service-worker.js')
    .then(() => { console.info('[Service Worker INFO] Registered'); });
}

window.addEventListener('activate', (e) => {
  document.getElementById("add-button").hidden = true;
  localforage.setItem("installed", true)
})

if (localforage.getItem("installed") === true) {
    document.getElementById("add-button").style.display = "none";
}
