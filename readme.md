# Cek Validasi Data KPU Pemilu 2024

Tested di python 3.11.7

## Detail Program

- `api.py`
  - Mengambil data dari api kpu
- `api_kawalpemilu.py`
  - Mengambil data dari api kawalpemilu
- `scrapping_validation.py`
  - Program untuk membandingkan antara jumlah suara paslon dan suara sah yang diambil dari [KPU Pemilu 2024](https://pemilu2024.kpu.go.id/)
  - Output merupakan 2 file csv di folder result dengan format:
    - `result-[nama_file_json]-[timestamp].csv`
    - `error_result-[nama_file_json]-[timestamp].csv`
- `scrapping_to_spreadsheet.py`
  - Program untuk mengambil data dari [KPU Pemilu 2024](https://pemilu2024.kpu.go.id/) dan [Kawal Pemilu](https://kawalpemilu.org/)
  - Output berupa file csv di folder result dengan format:
    - `result-[nama_kota/kabupaten]-[date].csv`
  - File csv akan di upload ke google spreadsheet
- `app.py`
  - Program ini menggunakan flask untuk membuat api yang menyediakan endpoint untuk trigger scrapping_to_spreadsheet.py
  - Menggunakan Celery untuk menjalankan job secara async/background
  - Endpoint yang tersedia:
    - `/scrap-all`
      - untuk scrapping semua data
    - `/scrap/[kode_provinsi]`
      - untuk scrapping data berdasarkan kode provinsi
    - `/scrap/[kode_provinsi]/[kode_kabupaten]`
      - untuk scrapping data berdasarkan kode kabupaten

## Cara Penggunaan

- Clone repository
  - `git clone https://github.com/rfaturriza/kpu2024`
- Pastikan python sudah terinstall, sebaiknya menggunakan python 3.11.7
- Pindah directory ke folder kpu2024
  - `cd kpu2024`
- Install requirements
  - `pip3 install -r requirements.txt`
- Untuk menjalankan scrapping_validation.py
  - `python3 scrapping_validation.py`
- Untuk menjalankan scrapping_to_spreadsheet.py
  - `python3 scrapping_to_spreadsheet.py`
- Untuk menjalankan `app.py`
  - Install redis
    - Website: [redis.io](https://redis.io/)
    - Mac OS: [Redis Mac OS](https://redis.io/docs/install/install-redis/install-redis-on-mac-os/)
    - Windows: [Redis WIN](https://redis.io/docs/install/install-redis/install-redis-on-windows/)
    - Linux: [Redis Linux](https://redis.io/docs/install/install-redis/install-redis-on-linux/)
  - `flask run` - di terminal 1
  - `celery -A app.celery worker --loglevel=info` - di terminal 2
  - Biasanya program akan jalan di port 5000. Buka browser dan akses `http://localhost:5000/`
