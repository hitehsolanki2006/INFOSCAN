# report.py
import os
from datetime import datetime
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "INFOSCAN - System Audit Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_metadata(self, metadata):
        self.set_font("Arial", "", 12)
        for k, v in metadata.items():
            self.cell(0, 10, f"{k}: {v}", ln=True)
        self.ln(5)

    def add_section(self, title, content):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, title, ln=True)
        self.set_text_color(0, 0, 0)

        self.set_font("Arial", "", 12)
        for key, val in content.items():
            if isinstance(val, list):
                val = ', '.join(str(i) for i in val)
            elif isinstance(val, dict):
                val = str(val)
            self.multi_cell(0, 8, f"{key}: {val}")
        self.ln(5)

def save_pdf_report(data, output_dir="reports"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"INFOSCAN_Report_{timestamp.replace(':', '-').replace(' ', '_')}.pdf"
    filepath = os.path.join(output_dir, filename)

    pdf = PDFReport()
    pdf.add_page()

    metadata = {
        "Tool": "INFOSCAN - Cybersecurity Audit Tool",
        "Generated On": timestamp,
        "Author": "Hitesh Solanki"
    }

    pdf.add_metadata(metadata)

    for section, content in data.items():
        pdf.add_section(section, content)

    pdf.output(filepath)
    return filepath
