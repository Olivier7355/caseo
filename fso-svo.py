"""
Scrape fso-svo.ch from 'start_id' to 'end_id' and save the result in 'osteopath_data.csv'
Usage: python fso-svo.py
"""

import requests
import csv

class Fso:

    def __init__(self, json_url):
        self.json_url = json_url
        self.data = []

    def fetch_data(self):
        response = requests.get(self.json_url)
        if response.status_code == 200:
            self.data = response.json()

    def extract_info(self):
        extracted_info = []
        for entry in self.data:
            source = "https://www.fso-svo.ch/fr/trouver-une-osteopathe?pin=" + str(entry['i'])
            before_address = entry['n']
            address_1 = entry['s']
            zip_city = entry['z'] + " " + entry['c']
            
            phone = entry['p']
            phone = str(phone)
            if "." in phone :
                phone = phone.replace('.', '')

            if " " in phone :
                phone = phone.replace(' ', '')

            if "/" in phone :
                phone = phone.replace('/', '')

            if phone and phone[0] == "0" :
                phone = phone[1:]

            if "+41" in phone[:3] :
                phone = phone[3:]
        
            if "41" in phone[:2] :
                phone = phone[2:]
            
            if "75" in phone[:3] :
                mobile_phone = "+4175" + str(phone[-7:])
                landline_phone = "None"
            elif "76" in phone[:3] :
                mobile_phone = "+4176" + str(phone[-7:])
                landline_phone = "None"
            elif "77" in phone[:3] :
                mobile_phone = "+4177" + str(phone[-7:])
                landline_phone = "None"
            elif "78" in phone[:3] :
                mobile_phone = "+4178" + str(phone[-7:])
                landline_phone = "None"
            elif "79" in phone[:3] :
                mobile_phone = "+4179" + str(phone[-7:])
                landline_phone = "None"
            elif phone.upper() == "FALSE" :
                landline_phone = "None"
                mobile_phone = "None"
            elif not phone :
                landline_phone = "None"
                mobile_phone = "None"
            else :
                landline_phone = "+41" + phone
                mobile_phone = "None"
            
            email = entry['e']
            website = entry['w']
            display_full_name = []
            if len(entry['t']) == 1 :
                display_full_name.append(entry['t'][0]['n'])
            
            else :
                for name in range(0, len(entry['t'])) :
                    display_full_name.append(entry['t'][name]['n'])
                print(display_full_name)

            for i in range(0, len(entry['t'])) :
                extracted_info.append({
                    "source": source,
                    "title": '',
                    "display_full_name": str(display_full_name[i]),
                    "first_name": str(display_full_name[i]).split(' ')[-1],
                    "last_name": (' ').join(str(display_full_name[i]).split(' ')[:-1]),
                    "before_address": before_address,
                    "address_1": address_1,
                    "address_2": '',
                    "zip_city": zip_city,
                    "mobile_phone": mobile_phone,
                    "landline_phone": landline_phone,
                    "email": email,
                    "website": website,
                    
                })
        return extracted_info
    
    def save_to_csv(self, filename):
        extracted_info = self.extract_info()
        if extracted_info:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                fieldnames = extracted_info[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for row in extracted_info:
                    writer.writerow(row)
            print(f"Data saved to {filename}")


if __name__ == "__main__":
    extractor = Fso("https://www.fso-svo.ch/fileadmin/osteosearch/locations/data.json")
    extractor.fetch_data()
    extractor.save_to_csv("osteopath_data.csv")



