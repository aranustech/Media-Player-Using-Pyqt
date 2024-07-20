# Media Player Menggunakan PyQT

Aplikasi Media Player yang dibangun menggunakan PyQt6 dan OpenCV. 
Aplikasi ini memiliki antarmuka (UI) yang ramah pengguna yang dirancang dengan QtDesigner.

## # Requirements

Untuk menjalankan proyek ini, Anda perlu menginstal paket Python berikut:

- PyQt6 
- opencv-python

## # Instalasi

### 1. Clone repository ini
```bash
git clone https://github.com/aranustech/media-player-using-pyqt.git
cd media-player-using-pyqt
```

### 2. Buat dan aktifkan lingkungan virtual (opsional tapi disarankan):
```bash
python -m venv venv
source venv/bin/activate   # Di Windows, gunakan `venv\Scripts\activate`
```

### 3. Instal library python yang dibutuhkan:
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi
```bash
python main.py
```
Ketika Anda menjalankan dan memilih file video, tampilan akan muncul seperti yang terlihat pada gambar di bawah ini.
![image](icon\result.png)

## # Mendesain UI

Proyek ini menggunakan QtDesigner untuk merancang antarmuka pengguna (UI). QtDesigner adalah alat yang memungkinkan Anda membangun UI grafis dengan cepat menggunakan widget dari kerangka kerja Qt GUI melalui antarmuka drag-and-drop. Berikut adalah langkah-langkah untuk menginstal QtDesigner dan mengonversi file *.ui* ke *.py*.

### 1. Instalasi QtDesigner
Unduh dan instal QtDesigner dari [fman build system](https://build-system.fman.io/qt-designer-download). 
Buka terminal dan jalankan perintah berikut (Pada Sistem Operasi Linux (Debian/Ubuntu)):
```bash
sudo apt-get install qttools5-dev-tools
```

### 2. Mendesain UI Anda

Setelah QtDesigner terinstal, Anda dapat mulai mendesain UI dengan langkah-langkah berikut:
- Buka QtDesigner.
- Buat proyek baru atau buka file .ui yang sudah ada.
- Gunakan alat-alat yang tersedia di QtDesigner untuk merancang antarmuka pengguna sesuai kebutuhan proyek Anda.
- Simpan desain Anda dalam format file .ui.

### 3. Mengonversi File .ui ke .py

Setelah selesai mendesain UI Anda, langkah selanjutnya adalah mengonversi file .ui menjadi file Python (.py). Berikut adalah langkah-langkahnya:
- Buka terminal atau command prompt.
- Navigasikan ke direktori tempat file .ui disimpan.
- Jalankan perintah berikut untuk mengonversi file .ui menjadi .py:
```bash
pyuic6 -x ui_main.ui -o ui_main.py
```
 
## # Contribution
Jika Anda ingin berkontribusi pada proyek ini, silakan fork repositori ini dan buat pull request dengan perubahan Anda.

## # License
Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file [LICENSE](LICENSE) untuk detail lebih lanjut.

## # Acknowledgements
- [PyQt6 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [OpenCV Documentation - Getting started with videos](https://docs.opencv.org/3.4/dd/d43/tutorial_py_video_display.html) 
- [QtDesigner Documentation](https://doc.qt.io/qt-6/qtdesigner-manual.html)

Temukan informasi lainya dari chanel Aranus Technology

[![Website Article](https://img.shields.io/badge/Website--blue)](https://aranustech.co.id/news)
[![Discord Channel](https://img.shields.io/badge/Discord-Channel-blue?logo=discord&logoColor=white)](https://discord.gg/qneXR8u9)
[![Linkedin pages](https://img.shields.io/badge/Likedin-page-blue)](https://www.linkedin.com/company/aranus-technology)
