/* 双语翻译 Service Worker：缓存应用外壳，离线也能打开界面（翻译本身要联网） */
const CACHE = "shuangyu-v1";
const ASSETS = ["./", "./index.html", "./manifest.json", "./icon.svg", "./apple-touch-icon.png"];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  // 只缓存本站的静态资源；翻译接口和外部抓取一律走网络
  if (url.origin === self.location.origin) {
    e.respondWith(
      caches.match(e.request).then((hit) => hit || fetch(e.request))
    );
  }
});
