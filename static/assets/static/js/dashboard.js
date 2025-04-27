// Fungsi untuk memperbarui waktu setiap detik
function updateTime() {
    const timeElement = document.getElementById("time");

    if (!timeElement) return; // Pastikan elemen ada

    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    // Format waktu HH:MM:SS
    const currentTime = `${hours}:${minutes}:${seconds}`;
    
    // Update elemen dengan waktu yang baru
    timeElement.textContent = currentTime;
}

// Panggil fungsi updateTime setiap detik
setInterval(updateTime, 1000);

// Fungsi untuk memperbarui tanggal sekali saat halaman dimuat
function updateDate() {
    const dateElement = document.getElementById("date");

    if (!dateElement) return; // Pastikan elemen ada

    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const day = now.getDate().toString().padStart(2, '0');

    // Format tanggal YYYY-MM-DD
    const currentDate = `${year}-${month}-${day}`;
    
    // Update elemen dengan tanggal yang baru
    dateElement.textContent = currentDate;
}

// Jalankan fungsi saat halaman dimuat
document.addEventListener("DOMContentLoaded", function() {
    updateDate();
    updateTime(); // Jalankan sekali agar waktu tidak kosong sebelum `setInterval`
});
