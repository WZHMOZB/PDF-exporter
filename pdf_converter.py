import pdfplumber
import pandas as pd
import os

def extract_units_from_pdf(pdf_path):
    data = []
    current_org_unit = None
    current_b1_b2_unit = None

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    if 'Organisation number:' in line:
                        current_org_unit = line.split('Organisation number:')[1].strip()
                        print(f"Found Organisation unit on page {page_number}: {current_org_unit}")
                    elif 'B-1 Unit' in line:
                        current_b1_b2_unit = line.split('B-1 Unit')[1].strip()
                        print(f"Found B-1 unit on page {page_number}: {current_b1_b2_unit}")
                    elif 'B-2 Unit' in line:
                        current_b1_b2_unit = line.split('B-2 Unit')[1].strip()
                        print(f"Found B-2 unit on page {page_number}: {current_b1_b2_unit}")
                    
                    if current_org_unit and current_b1_b2_unit:
                        formatted_row = f"RBI {current_org_unit} {current_b1_b2_unit}"
                        data.append({'RBI Unit': formatted_row})
                        current_org_unit = None
                        current_b1_b2_unit = None
            else:
                print(f"No text found on page {page_number}")
    
    return data

def save_to_csv(data, csv_path):
    if not data:
        print("No units found to save.")
        return
    
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}")

def main():
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    pdf_path = os.path.join(desktop_path, 'January2025.pdf')
    csv_path = os.path.join(desktop_path, 'output.csv')
    
    data = extract_units_from_pdf(pdf_path)
    save_to_csv(data, csv_path)

if __name__ == "__main__":
    main()
