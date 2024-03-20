"""
Scrape asca.ch from 'start_id' to 'end_id' and save the result in 'therapist_data.csv'
Usage: python asca.py
"""

import requests
import csv
from datetime import datetime


class AscaScraper:
    def __init__(self, start_id, end_id):
        self.start_id = start_id
        self.end_id = end_id
        self.base_url = "https://wp.asca.ch/therapist/details/?id={}&language=fr"
        self.csv_filename = "therapists_data.csv"

    def scrape_and_save(self):
        headers = [
            "API url",
            "salutation",
            "firstName + lastName",
            "firstName",
            "lastName",
            "careOf",
            "street",
            "null",
            "zip + city",
            "null",
            "null",
            "businessEmail",
            "webSite",
            "linkedIn",
            "facebook",
            "instagram",
            "null",
            "id",
            "company",
            "memberFrom",
            "bookOnlineUrl",
            "description"
        ]
        therapies_headers = ["therapies [{}]".format(i) for i in range(20)]
        headers.extend(therapies_headers)

        with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for therapist_id in range(self.start_id, self.end_id + 1):
                api_url = self.base_url.format(therapist_id)
                response = requests.get(api_url)
                if response.status_code == 200:
                    therapist_data = response.json()
                    try :
                        time_since = (datetime.strptime(therapist_data.get("memberFrom", ""), "%Y-%m-%dT%H:%M:%S")).strftime("%d.%m.%Y")

                    except :
                        time_since = (datetime.strptime(therapist_data.get("memberFrom", "").split("T")[0], "%Y-%m-%d")).strftime("%d.%m.%Y")

                    try :
                        adress = therapist_data["address"].get("zip", "") + " " + therapist_data["address"].get("city", ""),
                    except :
                        adress = "N/A"

                    row = [
                        api_url,
                        therapist_data.get("salutation", ""),
                        therapist_data.get("firstName", "") + " " + therapist_data.get("lastName", ""),
                        therapist_data.get("firstName", ""),
                        therapist_data.get("lastName", ""),
                        therapist_data["address"].get("careOf", ""),
                        therapist_data["address"].get("street", ""),
                        "",
                        adress,
                        "",
                        "",
                        therapist_data.get("businessEmail", ""),
                        therapist_data.get("webSite", ""),
                        therapist_data.get("linkedIn", ""),
                        therapist_data.get("facebook", ""),
                        therapist_data.get("instagram", ""),
                        "",
                        therapist_id,
                        therapist_data.get("company", ""),
                        time_since,
                        therapist_data.get("bookOnlineUrl", ""),
                        therapist_data.get("description", "")
                    ]
                    
                    therapies = therapist_data.get("therapies", [])[:20]  
                    row.extend(therapies)
                    
                    writer.writerow(row)
                    print ('id :', therapist_id,' time: ', time_since)
                    
                else:
                    print(f"Failed to fetch data for therapist ID: {therapist_id}")


if __name__ == "__main__":
    start_id = 601323   # enter here the first id to scrape
    end_id = 626536     # enter here the last id to scrape
    scraper = AscaScraper(start_id, end_id)
    scraper.scrape_and_save()



