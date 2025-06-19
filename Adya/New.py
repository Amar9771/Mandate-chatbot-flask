from fpdf import FPDF

class PDF(FPDF):
    pass

def generate_pdf(data):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Company Name: {data['Company Name']}", ln=1)
    pdf.cell(0, 10, f"Rating Date: {data['Rating Date']}", ln=1)
    pdf.cell(0, 10, f"Rating Agency: {data['Rating Agency']}", ln=1)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Facilities:", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.cell(60, 8, "Facility Name", border=1, align="C")
    pdf.cell(40, 8, "Amount (Rs. Cr)", border=1, align="C")
    pdf.cell(40, 8, "Rating", border=1, align="C")
    pdf.ln()

    for facility in data["Facilities"]:
        pdf.cell(60, 8, str(facility["Facility Name"]), border=1)
        pdf.cell(40, 8, str(facility["Amount"]), border=1, align="R")
        pdf.cell(40, 8, str(facility["Rating"]), border=1, align="C")
        pdf.ln()

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 10, "Rating Rationale:", ln=1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 8, data["Rationale"])

    # Return the PDF as bytearray (no encode)
    pdf_bytes = pdf.output(dest='S')
    return pdf_bytes

if __name__ == "__main__":
    # Sample data dictionary
    data = {
        "Company Name": "Company Name",
        "Rating Date": "2025/06/02",
        "Rating Agency": "Rating Agency",
        "Facilities": [
            {
                "Facility Name": "Facility Name 1",
                "Amount": "1",
                "Rating": "Rating 1"
            }
        ],
        "Rationale": "This is the rating rationale text that explains the basis for the rating."
    }

    pdf_bytes = generate_pdf(data)

    # Save the PDF bytes to a file
    with open("rating_rationale.pdf", "wb") as f:
        f.write(pdf_bytes)

    print("PDF generated and saved as rating_rationale.pdf")
c