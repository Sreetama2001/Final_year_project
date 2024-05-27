import pdfkit
import csv
from hrv import *

def generate_html_report(name, gender, age, email, hr, bloodvolume, stress_level, rmssd):
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Patient Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Patient Report</h1>
        <table>
            <tr>
                <th>Name</th>
                <td>{name}</td>
            </tr>
            <tr>
                <th>Gender</th>
                <td>{gender}</td>
            </tr>
            <tr>
                <th>Age</th>
                <td>{age}</td>
            </tr>
            <tr>
                <th>Contact</th>
                <td>{email}</td>
            </tr>
            <tr>
                <th>Heart Rate (HR)</th>
                <td>{hr}</td>
            </tr>
            <tr>
                <th>Blood Volume</th>
                <td>{bloodvolume}</td>
            </tr>
            <tr>
                <th>Stress</th>
                <td>{stress_level}</td>
            </tr>
            <tr>
                <th>HRV</th>
                <td>{rmssd}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
def generate_pdf(html, output_file):
    pdfkit.from_string(html, output_file,configuration=config)

if __name__ == "__main__":
    with open('vitalsReport.csv',mode = 'r') as file:
        reader =csv.reader(file)
        data = list(reader)
    name = data[len(data)-1][0]
    gender =data[len(data)-1][1]
    age = data[len(data)-1][2]
    email = data[len(data)-1][3]
    hr = data[len(data)-1][4]
    bloodvolume= data[len(data)-1][5]

    bvp_data = np.load('pulse.npy')  # BVP measurements
    time_data = np.load('hrs.npy')  # Time measurements
    hrv_calculator = HRVCalculator(bvp_data, time_data)
    rmssd = hrv_calculator.calculate_rmssd()
    stress_level = hrv_calculator.determine_stress()
    # terminal
    print(name, gender, age, email, hr, bloodvolume, stress_level, rmssd) 
    # report generation 
    html = generate_html_report(name, gender, age, email, hr, bloodvolume, stress_level,rmssd)
    output_file = "patient_report"
    generate_pdf(html, output_file)
    print(f"Patient report saved as {output_file}")


# Specify the path to wkhtmltopdf executable
# pdfkit.from_url('http://google.com', 'out.pdf', configuration=pdfkit.configuration(wkhtmltopdf= r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"))