import pymupdf
import os

PDF = "pmc_water/water_report.pdf"

doc = pymupdf.open(PDF)

print("Pages:", len(doc))
print()

for i, page in enumerate(doc):
    text = page.get_text("text").strip()
    images = page.get_images(full=True)

    print(
        f"Page {i+1:3} | "
        f"text chars: {len(text):5} | "
        f"images: {len(images):2}"
    )

    if text:
        print("   TEXT:", repr(text[:150]))

doc.close()