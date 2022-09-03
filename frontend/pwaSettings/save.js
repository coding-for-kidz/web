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


 localforage.getItem("checkForUpdatesTimeout").then(timeout => {
     $("#checkForUpdatesTimeout").val(timeout/1000)
 });


$("#checkForUpdatesTimeout").on("change", function() {
    localforage.setItem("checkForUpdatesTimeout", $("#checkForUpdatesTimeout").val());
});
