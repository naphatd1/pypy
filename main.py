import os
import datetime
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from matplotlib import font_manager
from PIL import Image
from utils.data_processing import load_data_fortianalyzer
from utils.plotting import plot_top_bandwidth_users, def_plot_status_table, plot_botnet_victims
from utils.string_utils import get_thai_date_string, prepend_date
from utils.image_processing import fig2img, resize_image, draw_text

def main():
    load_dotenv()

    font_dirs = ['fonts/']
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)

    plt.rcParams['font.family'] = "TH Sarabun New"
    plt.rcParams['font.size'] = 20

    # data_file = 'example.json'
    template_file = 'templates/comnet-stat-onepage-template.png'
    output_directory = os.getenv("DIR_OUTPUT", "./")
    output_filename = prepend_date('onepage.png')

    # report_data = load_data(data_file)
    report_data = load_data_fortianalyzer(
        os.getenv("FORTIANALYZER_HOST"),
        os.getenv("FORTIANALYZER_USERNAME"),
        os.getenv("FORTIANALYZER_PASSWORD"),
        os.getenv("FORTIANALYZER_DEVICE"),
        int(os.getenv("FORTIANALYZER_LAYOUT_ID")),
    )
    top_bandwidth_users = report_data['top_users']
    botnet_victims = report_data['botnet_victims']

    template_image = Image.open(template_file).convert("RGBA")
    
#     thai_months = [
#     "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม",
#     "มิถุนายน", "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม",
#     "พฤศจิกายน", "ธันวาคม"
# ]

    # อัปเดตไฟล์ .env ด้วยวันที่ปัจจุบัน
    # today = datetime.date.today()
    # year_be = today.year + 543
    # month_name = thai_months[today.month - 1]

    # อ่านค่าจาก .env
    # day = int(os.getenv("DAY")) + 1
    # month_name = str(os.getenv("MONTH"))
    # year_be = int(os.getenv("YEAR_BE"))

    # แปลงปี พ.ศ. เป็น ค.ศ. (ปี ค.ศ. = ปี พ.ศ. - 543)
    # year_ad = year_be - 543
    # # สร้างวัตถุ datetime
    # date1 = datetime.date(year_ad, today.month, day)
    # # Draw texts
    # print(f"วันที่ {date1.day} เดือน {month_name} พ.ศ. {year_be}")
    # bb = f"วันที่ {date1.day} {month_name} พ.ศ. {year_be}"


    today = datetime.date.today()
    
    # แปลงเป็นปี พ.ศ.
    thai_year = today.year + 543
    
    # แปลงเป็นชื่อเดือนภาษาไทย
    thai_months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
        "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
        "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    thai_month = thai_months[today.month - 1]
    
    thai_day = today.day
    
    # แสดงวันที่ในรูปแบบ วัน เดือน พ.ศ.
    thai_date = f'วันที่ {thai_day} {thai_month} พ.ศ. {thai_year}'

    if thai_date:
        onepage_date = thai_date
    else:
        onepage_date = get_thai_date_string()
    draw_text(template_image, (707, 315), onepage_date, font_size=80, anchor="ma")
    draw_text(template_image, (274, 560), "จำนวนผู้ลงทะเบียนสุทธิ",font_size=60,anchor="ma")
    draw_text(template_image, (274, 630), os.getenv("USER_REGISTERED_COUNT"), font_size=100, anchor="ma")
    draw_text(template_image, (274, 790), "ผู้ใช้งาน", font_size=60,anchor="ma")
    draw_text(template_image, (274, 850), "1,034", font_size=100, anchor="ma")
    if os.getenv("COMMENT"):
        draw_text(template_image, (128, 1690), "การแก้ไขปัญหาที่พบ", font_size=50)
        draw_text(template_image, (128, 1750), os.getenv("COMMENT"), font="fonts/THSarabunNew.ttf")

    # Plot top bandwidth users
    top_bandwidth_user_fig = plot_top_bandwidth_users(top_bandwidth_users, "", "ปริมาณการใช้งาน", "ผู้ใช้/หมายเลขไอพี")
    plot_image_top_bandwidth_user = fig2img(top_bandwidth_user_fig)
    plot_image_top_bandwidth_user_resized = resize_image(plot_image_top_bandwidth_user, 860, 860)

    # Plot status tables
    status_data = [
        ["เครื่องปรับอากาศเครื่องที่ 1", os.getenv("STATUS_AIR_CONDITIONER_1")],
        ["เครื่องปรับอากาศเครื่องที่ 2", os.getenv("STATUS_AIR_CONDITIONER_2")],
        ["เครื่องสำรองไฟเครื่องที่ 1", os.getenv("STATUS_UPS_1")],
        ["เครื่องสำรองไฟเครื่องที่ 2", os.getenv("STATUS_UPS_2")],
        ["เครื่องตรวจจับน้ำ", os.getenv("STATUS_LEAKAGE_DETECTOR")],
        ["เครื่องจับควัน VESDA", os.getenv("STATUS_SMOKE_DETECTOR")],
        ["เครื่องควบคุมสลับไฟฟ้า", os.getenv("STATUS_ATS")],
        ["เครื่องกำเนิดไฟฟ้า", os.getenv("STATUS_GENERATOR")],
    ]

    status_fig = def_plot_status_table(status_data)
    plot_image_status = fig2img(status_fig)

    # # Plot botnet victims
    botnet_fig = plot_botnet_victims(botnet_victims[:10], "", "จำนวน", "ผู้ใช้/หมายเลขไอพี")
    plot_image_botnet = fig2img(botnet_fig)

    template_image.paste(plot_image_top_bandwidth_user_resized, (530, 520), plot_image_top_bandwidth_user_resized)
    template_image.paste(plot_image_status, (96, 1084), plot_image_status)
    template_image.paste(plot_image_botnet, (96, 1504), plot_image_botnet)
    
    template_image.save(os.path.join(output_directory, output_filename))

    plt.close()

if __name__ == '__main__':
    main()
