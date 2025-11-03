const container = document.getElementById("qr-container");
const loader = document.getElementById("loader");
let loading = false;

async function loadMoreQRCodes() {
    if (loading) return;
    loading = true;
    loader.textContent = "Loading more QR codes...";
    try {
        const res = await fetch('/generate');
        const data = await res.json();
        data.qrcodes.forEach(b64 => {
            const img = document.createElement("img");
            img.src = "data:image/png;base64," + b64;
            img.className = "qr";
            container.appendChild(img);
        });
    } catch (err) {
        console.error("Error loading QR codes:", err);
        loader.textContent = "Failed to load QR codes.";
    } finally {
        loading = false;
        loader.textContent = "Scroll down to load more QR codes...";
    }
}

window.addEventListener("scroll", () => {
    const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 100;
    if (nearBottom && !loading) {
        loadMoreQRCodes();
    }
});

window.onload = loadMoreQRCodes;