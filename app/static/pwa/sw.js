self.addEventListener('install', async e => {
   return self.skipWaiting();
});

self.addEventListener('fetch', (e) => {
  e.respondWith(fetch(e.request));
});