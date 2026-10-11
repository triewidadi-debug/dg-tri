# DG TRI

Arsip dokumen dan template kerja.

## Isi

- `templates/surat-penawaran/` — Generator Surat Penawaran Kerjasama BSV (PDF)
  - `buat_surat.py` — script generator surat (Python, butuh library `reportlab`)
  - `assets/` — logo & watermark untuk kop surat
  - Cara pakai: `python3 buat_surat.py data.json`
  - Format `data.json`: `{"nomor": "...", "tanggal": "...", "kepada": "...", "output": "..."}`
