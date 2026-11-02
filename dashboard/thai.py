"""Thai display helpers. Underlying data values and identifiers are never changed."""
from __future__ import annotations

import pandas as pd

MONTHS = ["", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]

# Thai display translations shown ALONGSIDE the original source labels.
DOMAIN_TH = {
    "Malicious Actors & Misuse": "ผู้ประสงค์ร้ายและการนำไปใช้ในทางที่ผิด",
    "AI system safety, failures, and limitations": "ความปลอดภัย ความล้มเหลว และข้อจำกัดของระบบ AI",
    "Discrimination and Toxicity": "การเลือกปฏิบัติและเนื้อหาที่เป็นพิษ",
    "Misinformation": "ข้อมูลที่ผิดพลาดหรือเป็นเท็จ",
    "Privacy & Security": "ความเป็นส่วนตัวและความมั่นคงปลอดภัย",
    "Human-Computer Interaction": "ปฏิสัมพันธ์ระหว่างมนุษย์กับคอมพิวเตอร์",
    "Socioeconomic & Environmental Harms": "ผลเสียต่อสังคม เศรษฐกิจ และสิ่งแวดล้อม",
    "Unclassified": "ยังไม่ได้จัดหมวดหมู่",
}
COUNTRY_TH = {"THA": "ไทย", "KHM": "กัมพูชา", "IDN": "อินโดนีเซีย", "MYS": "มาเลเซีย", "MMR": "เมียนมา",
              "PHL": "ฟิลิปปินส์", "SGP": "สิงคโปร์", "VNM": "เวียดนาม"}


def dom_label(d: str) -> str:
    th = DOMAIN_TH.get(d)
    return f"{d} ({th})" if th else d


def dom_label_br(d: str) -> str:
    th = DOMAIN_TH.get(d)
    return f"{d}<br>{th}" if th else d


def country_label(iso3: str, name: str) -> str:
    th = COUNTRY_TH.get(iso3)
    return f"{name} · {th} ({iso3})" if th else f"{name} ({iso3})"


def fmt_d(d) -> str:
    d = pd.Timestamp(d)
    return f"{d.day:02d} {MONTHS[d.month]} {d.year}"


def fmt_short(d) -> str:
    d = pd.Timestamp(d)
    return f"{d.day:02d} {MONTHS[d.month]}"


def fmt_w(a, b) -> str:
    return f"{fmt_d(a)} – {fmt_d(b)}"
