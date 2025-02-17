// Fungsi untuk memperbarui waktu setiap detik
function updateTime() {
    const timeElement = document.getElementById("time");

    // Dapatkan waktu saat ini
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // Menambahkan leading zero
    const day = now.getDate().toString().padStart(2, '0'); // Menambahkan leading zero
    const hours = now.getHours().toString().padStart(2, '0'); // Menambahkan leading zero
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');

    // Gabungkan waktu menjadi string dengan format HH:MM:SS
    const currentTime = '' + year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds;
    
    // Update elemen dengan waktu yang baru
    timeElement.textContent = currentTime;
}

// Panggil fungsi updateTime setiap detik (1000 ms = 1 detik)
setInterval(updateTime, 1000);
