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


localforage.getItem('notifications').then(notificationsAllowed => {
    if (notificationsAllowed === null) {
        localforage.setItem("notifications", false);
    }
})

localforage.getItem('askNotifications').then(askNotifications => {
    if (askNotifications === null) {
        localforage.setItem("askNotifications", true);
    }
})


function notifications() {
    let askNotifications = localforage.getItem('askNotifications');
    if (Notification.permission === "granted") {
        localforage.setItem("notifications", true)
    }
    if (Notification.permission !== "granted" && askNotifications) {
        Notification.requestPermission().then(r => {
            if (Notification.permission !== "granted") {
                localforage.setItem("askNotifications", false);
            }
            else {
                localforage.setItem("notifications", true)
            }
        });
    }
}

notifications();
