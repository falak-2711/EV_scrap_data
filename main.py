
import requests
import json
import csv
from bs4 import BeautifulSoup

gov_table_response = requests.get(
    "https://fame2.heavyindustries.gov.in/ModelUnderFame.aspx"
)

soup = BeautifulSoup(gov_table_response.content, "html.parser")

data_table_html = soup.find("table", id="mainContent_gvCustomers").find_all("tr")

vehicle_overall_data = []
field_names = [
    "Manufacturer",
    "xEV Model Name",
    "Variant Name",
    "Vehicle Type & Segment",
    "Vehicle CMVR Category",
    "Incentive Amount (In INR)",
    "Status",
    "Links",
]

for entries in data_table_html:

    outer = entries.find("td")
    if outer != None:  # the outer table of manufacturer
        heading = outer.find("itemtemplate")

        manufacturer = ""

        if heading != None:  # heading of the manufacturer
            i = 0
            for lines in heading:
                if i == 2:
                    pass
                    manufacturer = lines.text.strip().split("\n")[0]
                i += 1
        all_row_entries = outer.find_all("tr")

        for entry in all_row_entries:
            # The data entry of each vehicle
            data_object = {
                "Manufacturer": manufacturer,
                "xEV Model Name": "",
                "Variant Name": "",
                "Vehicle Type & Segment": "",
                "Vehicle CMVR Category": "",
                "Incentive Amount (In INR)": "",
                "Status": "",
                "Links": "",
            }
            all_sub_entries = entry.find_all("td")
            if len(all_sub_entries) != 0:  # to seperate the column headings from data

                data_object["xEV Model Name"] = all_sub_entries[1].text.strip()
                data_object["Variant Name"] = all_sub_entries[2].text.strip()
                data_object["Vehicle Type & Segment"] = all_sub_entries[3].text.strip()
                data_object["Vehicle CMVR Category"] = all_sub_entries[4].text.strip()
                data_object["Incentive Amount (In INR)"] = all_sub_entries[
                    5
                ].text.strip()

                data_object["Status"] = all_sub_entries[6].text.strip()

                # the json data from each links in the data entry
                json_link_object_vehicle = {
                    "Range (Km)": "",
                    "Max. Speed (Km/Hr)": "",
                    "Acceleration (m/s2)": "",
                    "Warranty (In Years)": "",
                    "Electric Energy consumption (KWh per 100KM)": "",
                    "Battery Technology": "",
                    "Battery Capacity (kWh)": "",
                    "Battery Density (Wh/Kg)": "",
                    "Battery cycle (No. of Cycles)": "",
                }

                vehicle_sub_link = all_sub_entries[7].find("a")["href"]

                vehicle_link = (
                    f"https://fame2.heavyindustries.gov.in/{vehicle_sub_link}"
                )

                vehicle_data_response = requests.get(vehicle_link)
                vehicle_soup = BeautifulSoup(
                    vehicle_data_response.content, "html.parser"
                )

                json_link_object_vehicle["Range (Km)"] = vehicle_soup.find(
                    "span", id="lblRange"
                ).text
                json_link_object_vehicle["Max. Speed (Km/Hr)"] = vehicle_soup.find(
                    "span", id="lblSpeed"
                ).text
                json_link_object_vehicle["Acceleration (m/s2)"] = vehicle_soup.find(
                    "span", id="lblAcceleration"
                ).text
                json_link_object_vehicle["Warranty (In Years)"] = vehicle_soup.find(
                    "span", id="lblWarantty"
                ).text
                json_link_object_vehicle[
                    "Electric Energy consumption (KWh per 100KM)"
                ] = vehicle_soup.find("span", id="lblEnergyConsumption").text
                json_link_object_vehicle["Battery Technology"] = vehicle_soup.find(
                    "span", id="lblBatteryTechnology"
                ).text
                json_link_object_vehicle["Battery Capacity (kWh)"] = vehicle_soup.find(
                    "span", id="lblBatteryCapacity"
                ).text
                json_link_object_vehicle["Battery Density (Wh/Kg)"] = vehicle_soup.find(
                    "span", id="lblBatteryDensity"
                ).text
                json_link_object_vehicle[
                    "Battery cycle (No. of Cycles)"
                ] = vehicle_soup.find("span", id="lblBatteryLifeCycle").text

                data_object["Links"] = json.dumps(json_link_object_vehicle)

                vehicle_overall_data.append(data_object)
                print(data_object)

with open("output_scraped_data.csv", "w") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(vehicle_overall_data)
