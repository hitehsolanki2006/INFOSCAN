# report.py
import os
from datetime import datetime
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(0, 70, 140)
        self.cell(0, 10, "INFOSCAN - System Audit Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_metadata(self, metadata):
        self.set_font("Arial", "I", 12)
        self.set_text_color(60, 60, 60)
        for k, v in metadata.items():
            self.cell(0, 10, f"{k}: {v}", ln=True)
        self.ln(5)

    def add_section(self, title, content):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 128)
        self.cell(0, 10, f"[{title}]", ln=True)
        self.set_text_color(0, 0, 0)

        self.set_font("Arial", "", 12)

        # Special formatting for "Network Info"
        if title == "Network Info" and isinstance(content, dict):
            for key, val in content.items():
                if isinstance(val, dict):
                    self.cell(0, 8, f"{key}:", ln=True)
                    for subk, subv in val.items():
                        if isinstance(subv, dict):
                            self.cell(10, 8, f" - {subk}:", ln=True)
                            for ssk, ssv in subv.items():
                                self.cell(20, 8, f"   - {ssk}: {ssv}", ln=True)
                        else:
                            self.cell(10, 8, f"   {subk}: {subv}", ln=True)
                elif isinstance(val, list):
                    self.cell(0, 8, f"{key}:", ln=True)
                    for item in val:
                        self.cell(10, 8, f" - {item}", ln=True)
                else:
                    self.multi_cell(0, 8, f"{key}: {val}")
            self.ln(5)
        else:
            # Default formatting for other sections
            for key, val in content.items():
                if isinstance(val, list):
                    self.cell(0, 8, f"{key}:", ln=True)
                    for item in val:
                        self.cell(10, 8, f" - {item}", ln=True)
                elif isinstance(val, dict):
                    self.cell(0, 8, f"{key}:", ln=True)
                    for subk, subv in val.items():
                        self.cell(10, 8, f" - {subk}: {subv}", ln=True)
                else:
                    self.multi_cell(0, 8, f"{key}: {val}")
            self.ln(5)

def save_pdf_report(data, output_dir="reports"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"INFOSCAN_Report_{timestamp.replace(':', '-').replace(' ', '_')}.pdf"
    filepath = os.path.join(output_dir, filename)

    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    metadata = {
        "Tool": "INFOSCAN - Cybersecurity Audit Tool",
        "Generated On": timestamp,
        "Author": "Hunter"
    }

    pdf.add_metadata(metadata)

    for section, content in data.items():
        pdf.add_section(section, content)

    pdf.output(filepath)
    return filepath
