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

localforage.getItem('settingsPage').then(page => {
    if (page === null) {
        localforage.setItem("settingsPage", "general")
        page = "general"
    }
    switchTab(page);
})


function switchTab(tabName) {
    if (tabName === null) {
        tabName = "general";
    }
    localforage.getItem('settingsPage').then(currentPage => {
        $("#"+currentPage).hide();
    });

    try {
        $("#"+tabName).show();
        localforage.setItem("settingsPage", tabName);
    }
    catch (error) {
        console.error("Switch page error", error)
    }
}