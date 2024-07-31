import xml.etree.ElementTree as ET

def clean_xml_data(xml_string):
    """
    Clean the XML data by removing everything after "</FortiAnalyzer_Report>\r\n".

    Args:
        xml_string: The string containing the XML data.

    Returns:
        The cleaned XML string.
    """

    closing_tag_index = xml_string.find("</FortiAnalyzer_Report>\r\n")
    if closing_tag_index > 0:
        return xml_string[:closing_tag_index + len("</FortiAnalyzer_Report>\r\n")]
    else:
        return xml_string

def extract_data(id_element):
    """
    Extracts data from an "id" element in the XML report.

    Args:
        id_element: An ElementTree object representing the "id" element.

    Returns:
        A dictionary containing the extracted data.
    """

    data = {}
    data['value'] = id_element.attrib['value']
    for child in id_element:
        data[child.tag] = child.text.strip()  # Remove leading/trailing whitespace
    return data

def parse_report(xml_string):
    """
    Parses the cleaned XML data and extracts data from specific tables.

    Args:
        xml_string: The cleaned XML string.

    Returns:
        A dictionary containing extracted data from "Botnet Victims" and "Top 20 Users by Bandwidth" tables.
    """

    try:
        root = ET.fromstring(xml_string)

        botnet_victims = []
        for id_element in root.find('table[@name="Botnet Victims"]').findall('id'):
            botnet_victims.append(extract_data(id_element))

        top_users = []
        for id_element in root.find('table[@name="Top 20 Users by Bandwidth (exclude servers)"]').findall('id'):
            top_users.append(extract_data(id_element))

        return {'botnet_victims': botnet_victims, 'top_users': top_users}

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
