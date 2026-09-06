chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sirr-review-selection",
    title: "Analyze selection with DIKWP SIRR",
    contexts: ["selection"]
  });
});
chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId !== "sirr-review-selection") return;
  const text = encodeURIComponent((info.selectionText || "").slice(0, 12000));
  chrome.tabs.create({url: chrome.runtime.getURL(`review.html?text=${text}`)});
});
