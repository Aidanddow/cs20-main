// Option1 = Enable Preview
enable_footnotes = document.getElementById("enable_footnotes");
force_reprocess = document.getElementById("force_reprocess");

enable_footnotes.addEventListener("click", save_enable_footnotes);
force_reprocess.addEventListener("click", save_force_reprocess);

function save_enable_footnotes() {
  if (enable_footnotes.checked) {
    chrome.storage.local.set({ enable_footnotes: "1" }, function () {});
  } else {
    chrome.storage.local.set({ enable_footnotes: "0" }, function () {});
  }
}

function save_force_reprocess() {
  if (force_reprocess.checked) {
    chrome.storage.local.set({ force_reprocess: "1" }, function () {});
  } else {
    chrome.storage.local.set({ force_reprocess: "0" }, function () {});
  }
}

function loadOptions() {
  chrome.storage.local.get(
    ["enable_footnotes", "force_reprocess"],
    function (data) {
      if (data.enable_footnotes == 0) {
        enable_footnotes.checked = false;
      } else {
        enable_footnotes.checked = true;
      }

      if (data.force_reprocess == 0) {
        force_reprocess.checked = false;
      } else {
        force_reprocess.checked = true;
      }
    }
  );
}

loadOptions();
