import os
import shutil
import subprocess
import time
import csv
import sqlite3

# Constants
TEMP_DIR = "temp5"
TEMP_DIR2 = ""
WORK_CSV = os.path.join(TEMP_DIR, "work.csv")
WORK3_CSV = os.path.join(TEMP_DIR, "work3.csv")
RESULTS_TXT = os.path.join(TEMP_DIR, "results.txt")
RESULTS_PAC_CSV = os.path.join(TEMP_DIR, "results_pac.csv")
DB_FILE = "PTCodes.db"

# Helper functions
def run_command(command):
    """Runs a shell command and prints the output."""
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running command: {command}\n{result.stderr.decode()}")
    return result.stdout.decode()

def create_directory(dir_name):
    """Creates a directory if it doesn't exist."""
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def format_csv():
    """Formats the CSV file as per the original script."""
    print("Formatting work.csv to initialize code.")
    
    # Remove the first line (header) and extract the first 8 characters of each row
    with open(WORK_CSV, 'r') as infile, open(WORK3_CSV, 'w') as outfile:
        reader = csv.reader(infile)
        next(reader)  # Skip header
        for row in reader:
            outfile.write(row[0][:8] + "\n")

def download_database():
    """Downloads and prepares the geonames database."""
    print("DOWNLOADING DATABASE")
    #time.sleep(10)
    run_command(f"wget -P {TEMP_DIR} http://download.geonames.org/export/zip/PT.zip")
    run_command(f"unzip {os.path.join(TEMP_DIR, 'PT.zip')} -d {TEMP_DIR}")
    
    # Clean up
    os.remove(os.path.join(TEMP_DIR, "readme.txt"))
    os.remove(os.path.join(TEMP_DIR, "PT.zip"))

def initialize_search_script():
    """Simulates running the search script."""
    print("INICIALIZANDO O SCRIPT")
    #time.sleep(10)
    
    # Run the geoprocessing script (replace 'gp' with subprocess for actual use)
    run_command(f"gp -q {os.path.join(TEMP_DIR2, 'sc4.gp')}")

    # Process results.txt into results_pac.csv
    with open(RESULTS_TXT, 'r') as infile, open(RESULTS_PAC_CSV, 'w') as outfile:
        for line in infile:
            fields = line.split("\t")
            outfile.write(f"{fields[1]},{fields[2]},{fields[3]}\n")

def convert_to_sqlite():
    """Converts the CSV data into an SQLite database."""
    print("CONVERTING TO DATABASE")
    #time.sleep(10)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create table
    cursor.execute("CREATE TABLE IF NOT EXISTS Results (codigo_postal TEXT, concelho TEXT, distrito TEXT);")
    
    # Import CSV into SQLite
    with open(RESULTS_PAC_CSV, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            cursor.execute("INSERT INTO Results (codigo_postal, concelho, distrito) VALUES (?, ?, ?)", row)
    
    conn.commit()
    conn.close()

def check_files():
    """Check if the required files exist."""
    print("CHECKING FILES")
    
    # Check PT.txt
    pt_txt = os.path.join(TEMP_DIR, "PT.txt")
    if os.path.exists(pt_txt):
        print(f"{pt_txt} Checked!! File exists.")
        run_command(f"wc -l {pt_txt}")
    else:
        print(f"{pt_txt} File does not exist.")
    
    # Check results.txt
    if os.path.exists(RESULTS_TXT):
        print(f"{RESULTS_TXT} Checked!! File exists.")
        run_command(f"wc -l {RESULTS_TXT}")
    else:
        print(f"{RESULTS_TXT} File does not exist.")
    
    # Check results_pac.csv
    if os.path.exists(RESULTS_PAC_CSV):
        print(f"{RESULTS_PAC_CSV} Checked!! File exists.")
        run_command(f"wc -l {RESULTS_PAC_CSV}")
    else:
        print(f"{RESULTS_PAC_CSV} File does not exist.")

def database_stats():
    """Print SQLite database statistics."""
    print("DATABASE STATS")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA page_count;")
    print(f"Page count: {cursor.fetchone()[0]}")
    
    cursor.execute("PRAGMA page_size;")
    print(f"Page size: {cursor.fetchone()[0]}")
    
    cursor.execute("SELECT sqlite_version();")
    print(f"SQLite version: {cursor.fetchone()[0]}")
    
    conn.close()

def convert_to_pdf():
    """Convert output.txt to PDF using LibreOffice."""
    print("Converting output.txt to PDF")
    run_command("libreoffice --headless --convert-to pdf output.txt")

# Main script
if __name__ == "__main__":
    print("PTCodes Super-Search Script !!!")
    
    # Create temp directory
    create_directory(TEMP_DIR)
    
    # Copy codigos_postais.csv to work.csv
    shutil.copy("codigos_postais.csv", WORK_CSV)
    
    # Set permissions (optional in Python, unless needed)
    os.chmod(WORK_CSV, 0o777)
    
    # Format the CSV
    format_csv()
    
    # Download and prepare the database
    download_database()
    
    # Run the geoprocessing script and prepare results
    initialize_search_script()
    
    # Convert results to SQLite
    convert_to_sqlite()
    
    # Check the important files
    check_files()
    
    # Print database statistics
    database_stats()
    
    # Convert output to PDF
    convert_to_pdf()
