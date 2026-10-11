#!/usr/bin/env python3
"""Generator Surat Penawaran Kerjasama BSV (PDF).
Usage: python3 buat_surat.py data.json
data.json: {"nomor": str, "tanggal": str, "kepada": str, "output": str}
"""
import json, sys, os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                Table, TableStyle, Image as RLImage, HRFlowable)

BASE = os.path.dirname(os.path.abspath(__file__))
LOGO = os.path.join(BASE, "assets", "logo_emblem.jpg")
WM = os.path.join(BASE, "assets", "watermark.jpg")
DARK = HexColor("#1a1a1a")
GREY = HexColor("#555555")
GREEN = HexColor("#234d2c")

def kop(canvas, doc):
    canvas.saveState()
    W, H = A4
    # watermark emblem samar di tengah halaman
    ww, wh = 380, 380
    canvas.drawImage(WM, (W - ww) / 2, (H - wh) / 2 + 20, width=ww, height=wh,
                     preserveAspectRatio=True, mask="auto")
    # logo
    canvas.drawImage(LOGO, 40, H - 100, width=72, height=72,
                     preserveAspectRatio=True, mask="auto")
    canvas.setFillColor(DARK)
    canvas.setFont("Times-BoldItalic", 26)
    canvas.drawString(128, H - 62, "Bantir Skyview")
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(GREY)
    canvas.drawString(128, H - 78,
        "Jl. Sumowono - Boja, Bantir, Losari, Kec. Sumowono, Kab. Semarang")
    canvas.drawString(128, H - 91, "Telp: 0851-1364-3717")
    canvas.setStrokeColor(DARK); canvas.setLineWidth(1.4)
    canvas.line(40, H - 112, W - 40, H - 112)
    canvas.setLineWidth(0.5)
    canvas.line(40, H - 116, W - 40, H - 116)
    # aksen hijau tua tipis di tepi bawah halaman
    canvas.setFillColor(GREEN)
    canvas.rect(0, 0, W, 10, stroke=0, fill=1)
    canvas.restoreState()

def buat_surat(data):
    out = data.get("output") or os.path.join(BASE, "surat.pdf")
    doc = SimpleDocTemplate(out, pagesize=A4,
                            leftMargin=45, rightMargin=45,
                            topMargin=125, bottomMargin=45)
    normal = ParagraphStyle("n", fontName="Helvetica", fontSize=11,
                            leading=16.5, alignment=TA_JUSTIFY,
                            spaceAfter=7, textColor=DARK)
    hdr = ParagraphStyle("h", parent=normal, alignment=TA_LEFT, spaceAfter=2)
    center = ParagraphStyle("c", parent=normal, alignment=TA_CENTER)
    right = ParagraphStyle("r", parent=normal, alignment=TA_RIGHT)
    bold = ParagraphStyle("b", parent=normal, fontName="Helvetica-Bold")

    S = []
    S.append(Paragraph("Nomor &nbsp;&nbsp;&nbsp;&nbsp;: %s" % data.get("nomor",""), hdr))
    S.append(Paragraph("Lampiran &nbsp;: -", hdr))
    S.append(Paragraph("Perihal &nbsp;&nbsp;&nbsp;&nbsp;: <b>Penawaran Kerjasama Kegiatan Sekolah</b>", hdr))
    S.append(Spacer(1, 14))
    S.append(Paragraph("Kepada Yth.<br/><b>%s</b><br/>di Tempat" % data.get("kepada",""), hdr))
    S.append(Spacer(1, 12))
    S.append(Paragraph("Dengan hormat,", normal))
    S.append(Paragraph(
        "Perkenalkan, kami dari <b>Bantir Skyview (BSV)</b>, destinasi wisata keluarga "
        "yang berlokasi di Bantir, Losari, Kecamatan Sumowono, Kabupaten Semarang. "
        "Melalui surat ini, kami menawarkan <b>kerjasama kegiatan sekolah</b> berupa "
        "paket kunjungan edukasi dan rekreasi (<i>outing class / field trip</i>) bagi "
        "para siswa Sekolah Dasar.", normal))
    S.append(Paragraph(
        "Adapun fasilitas yang kami sediakan dalam paket kegiatan ini meliputi:", normal))
    for i, f in enumerate([
        "<b>Tiket masuk</b> kawasan Bantir Skyview;",
        "<b>Kolam renang</b> anak yang aman dan bersih;",
        "<b><i>Children playground</i></b> untuk bermain dan beraktivitas;",
        "<b>Area <i>outbound</i></b> yang luas, asri, dan cocok untuk kegiatan "
        "kelompok serta permainan edukatif."], 1):
        S.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;%d. %s" % (i, f), normal))
    S.append(Paragraph(
        "Biaya paket kegiatan ini sangat terjangkau, yaitu:", normal))
    S.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; <b>Rp5.000,-/peserta</b> untuk SD di wilayah "
        "<b>Bantir &ndash; Losari</b>;", normal))
    S.append(Paragraph(
        "&nbsp;&nbsp;&nbsp;&nbsp;&bull; <b>Rp7.000,-/peserta</b> untuk SD di wilayah "
        "<b>Sumowono</b>.", normal))
    S.append(Paragraph(
        "Kami berharap penawaran ini dapat menjadi alternatif kegiatan pembelajaran "
        "di luar kelas yang menyenangkan, aman, dan bermanfaat bagi para siswa. "
        "Untuk informasi lebih lanjut atau penjadwalan kunjungan, Bapak/Ibu dapat "
        "menghubungi kami di nomor <b>0851-1364-3717</b>.", normal))
    S.append(Paragraph(
        "Demikian surat penawaran ini kami sampaikan. Atas perhatian dan kerja sama "
        "Bapak/Ibu, kami mengucapkan terima kasih.", normal))
    S.append(Spacer(1, 8))
    S.append(Paragraph("Hormat kami,", right))
    S.append(Paragraph("Bantir, %s" % data.get("tanggal",""), right))
    S.append(Spacer(1, 44))
    S.append(Paragraph("<b>Tri Widadi</b>", ParagraphStyle("s", parent=right, fontName="Helvetica-Bold")))
    S.append(Paragraph("Supervisor BSV", right))

    doc.build(S, onFirstPage=kop, onLaterPages=kop)
    print("OK:", out)
    return out

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        data = json.load(f)
    buat_surat(data)
