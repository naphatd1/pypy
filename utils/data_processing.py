import json
import time
from utils.xml_parser import clean_xml_data, parse_report
from utils.fortianalyzer import FortiAnalyzer

def load_data(file_path):
    """Load JSON data from a file and clean the XML data."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f, strict=False)
    xml_string = data['result']['data']
    cleaned_xml = clean_xml_data(xml_string)
    return parse_report(cleaned_xml)

def load_data_fortianalyzer(host, username, password, device, layout_id):
    fa = FortiAnalyzer(host)
    if not fa.login(username, password):
        return None
    task_id = fa.generate_report(device, layout_id)
    if not task_id:
        return None
    # Wait for report
    print("\n")
    while True:
        progress = fa.get_report_state(task_id)
        if progress is None:
            return None  # Error occurred during get_report_state
        elif progress == 100:
            break
        else:
            print(f"\rReport generation in progress: {progress}% complete")
            time.sleep(3)
    report_xml = fa.download_report(task_id)
    report_xml_cleaned = clean_xml_data(report_xml)
    fa.delete_report(task_id)
    return parse_report(report_xml_cleaned)
