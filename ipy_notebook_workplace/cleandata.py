import pandas as pd
import os
import re

# Hard-coded mapping for Chinese to English translations
translation_map = {
    "车辆类别": "Vehicle_Category",
    "行政区域": "Administrative_Region",
    "车辆类型": "Vehicle_Type",
    "最大电压电池包序号": "Max_Voltage_Battery_Pack_Index",
    "最大电压电池序号": "Max_Voltage_Battery_Index",
    "最大电压值": "Max_Voltage_Value_V",  # Include unit in header
    "最小电压电池包序号": "Min_Voltage_Battery_Pack_Index",
    "最小电压电池序号": "Min_Voltage_Battery_Index",
    "最小电压值": "Min_Voltage_Value_V",  # Include unit in header
    "总电压": "Total_Voltage_V",  # Include unit in header
    "最大温度电池包序号": "Max_Temperature_Battery_Pack_Index",
    "最大温度探针序号": "Max_Temperature_Probe_Index",
    "最大温度值": "Max_Temperature_Value_DegreeC",  # Replace °C with DegreeC
    "最小温度电池包序号": "Min_Temperature_Battery_Pack_Index",
    "最小温度探针序号": "Min_Temperature_Probe_Index",
    "最小温度值": "Min_Temperature_Value_DegreeC",  # Replace °C with DegreeC
    "SOC": "State_Of_Charge_%",  # Include unit in header
    "总电流": "Total_Current_A",  # Include unit in header
    "绝缘电阻": "Insulation_Resistance_MegaOhm",  # Replace MΩ with MegaOhm
    "剩余电量": "Remaining_Energy_kWh",  # Replace KW•h with kWh
    "有效性": "Validity",
    "上传日期": "Upload_Date",
    "上传时间": "Upload_Time",
    "通州区": "Tongzhou_District",
    "无效": "Invalid",
    "电动出租车": "Electric_Taxi",
    "E200EV电动出租车": "E200EV_Electric_Taxi"  # Added translation for "E200EV电动出租车"
}

# Function to sanitize headers
def sanitize_header(header):
    # Replace specific units in headers
    header = header.replace("KW•h", "kWh").replace("MΩ", "MegaOhm").replace("°C", "DegreeC")
    # Remove special characters and replace spaces with underscores
    sanitized = re.sub(r'[^\x00-\x7F]+', '', header)  # Remove non-ASCII characters
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', sanitized)  # Replace special characters with underscores
    sanitized = re.sub(r'_+', '_', sanitized)  # Replace multiple underscores with a single one
    return sanitized.strip('_')

# Function to translate headers to English
def translate_headers(headers):
    return [sanitize_header(translation_map.get(header, header)) for header in headers]

# Function to sanitize data values (remove units from cell values)
def sanitize_data(df):
    def sanitize_cell(cell):
        if isinstance(cell, str):  # Only process string values
            # Translate specific terms using the translation map
            cell = translation_map.get(cell, cell)
            
            # If the cell contains numeric values with units, remove the units
            if any(char.isdigit() for char in cell):  # Check if the cell contains numbers
                # Remove specific units but preserve numeric values
                cell = cell.replace("KW•h", "kWh").replace("MΩ", "MegaOhm").replace("°C", "DegreeC")
                cell = re.sub(r'[kWhMegaOhmDegreeCVAM%]', '', cell)  # Remove units
                cell = re.sub(r'[^0-9.-]', '', cell)  # Keep only numeric values
            
            # Return the translated or original cell value
            return cell
        return cell  # Return unchanged if not a string
    
    # Apply sanitization to all cells
    return df.applymap(sanitize_cell)

# Function to process an .xls file and convert it to .csv
def process_xls_to_csv(input_file, output_dir):
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Translate and sanitize headers
    df.columns = translate_headers(df.columns)
    
    # Sanitize data entries (remove units from cell values)
    df = sanitize_data(df)
    
    # Construct output file path
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}.csv")
    
    # Save as CSV
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Processed: {input_file} -> {output_file}")

# Main function to process all .xls files in a directory
def process_all_xls_files(input_dir, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all .xls files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xls"):
            input_file = os.path.join(input_dir, file_name)
            process_xls_to_csv(input_file, output_dir)

# Example usage
if __name__ == "__main__":
    input_directory = "data"  # Replace with your input directory
    output_directory = "data"  # Replace with your output directory
    process_all_xls_files(input_directory, output_directory)