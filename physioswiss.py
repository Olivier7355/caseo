"""
Scrape physioswiss.ch from 'start_id' to 'end_id' and save the result in 'therapist_data.csv'
Usage: python physioswiss.py
"""

import requests
import csv
from bs4 import BeautifulSoup
import re

class PhysioSwissScraper:

    def __init__(self, page_number):
        self.page_number = page_number
        self.base_url = 'https://www.physioswiss.ch'
        self.main_url = f"https://www.physioswiss.ch/fr/practices?page={page_number}"
        self.csv_filename = "therapists_data.csv"
    
    def scrape(self):
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
        
            try:
                response = requests.get(self.main_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    practice_list = soup.find_all('a', class_='result-preview practice')
                    for practice in practice_list:
                        link = self.base_url + practice['href']
                        print(f"url: {link}")
                        response_link = requests.get(link)
                        if response_link.status_code == 200:
                            soup_link = BeautifulSoup(response_link.content, 'html.parser')
                            display_full_name = soup_link.find('h1').text.strip()
                            first_name = link.split('/')[-1].split('-')[0].capitalize()
                            last_name = link.split('/')[-1].split('-')[1].capitalize()

                            fine_print = soup_link.find_all('p', class_='fine-print')
                            Adresse = fine_print[-1].text.strip().split('  ')
                            filtered_Adresse = [item for item in Adresse if item.strip()]

                            if len(filtered_Adresse) > 3 :
                                zip_city = filtered_Adresse[-1].strip()
                                address_2 = filtered_Adresse[-2].strip()
                                address_1 = filtered_Adresse[-3].strip()
                                before_address = filtered_Adresse[0].strip()

                            else :
                                zip_city = filtered_Adresse[-1].strip()
                                address_2 = ''
                                address_1 = filtered_Adresse[-2].strip()
                                before_address = filtered_Adresse[0].strip()

                            contact_details = soup_link.find('p', class_='fine-print contact-details').text.strip().split('\n')
                            filtered_contact_details = [item.strip() for item in contact_details if item.strip()]

                            email = 'None'
                            website = 'None'
                            mobile_phone = 'None'
                            landline_phone = 'None'

                            for i in range(len(filtered_contact_details)):
                                if "Téléphone:" in filtered_contact_details[i]:
                                    phone_number = filtered_contact_details[i + 1]
                                    if "075 " in phone_number[:4] :
                                        mobile_phone = "+41 75" + phone_number[3:]
                                    elif "076 " in phone_number[:4] :
                                        mobile_phone = "+41 76" + phone_number[3:]
                                    elif "077 " in phone_number[:4] :
                                        mobile_phone = "+41 77" + phone_number[3:]
                                    elif "078 " in phone_number[:4] :
                                        mobile_phone = "+41 78" + phone_number[3:]
                                    elif "079 " in phone_number[:4] :
                                        mobile_phone = "+41 79" + phone_number[3:]
                                    else :
                                        landline_phone = "+41 " + phone_number[1:]

                                elif "Adresse e-mail:" in filtered_contact_details[i]:
                                    email = filtered_contact_details[i + 1]

                                elif "Site Web:" in filtered_contact_details[i]:
                                    website = filtered_contact_details[i + 1]

                            practice_id = link.split('/')[-2]
                            type_therapeute = (soup_link.find('h4').text.strip()).split(' ')[-1].strip()
                            
                            details = soup_link.find('table', class_='details').text.strip().split('  ')
                            filtered_details = [item.strip() for item in details if item.strip()]

                            for i in range(len(filtered_details)):
                                if "Numéro RCC:" in filtered_details[i]:
                                    try :
                                        rcc = filtered_details[i + 1]
                                    except :
                                        rcc = 'None'

                                elif "Numéro GLN:" in filtered_details[i]:
                                    try :
                                        gln = filtered_details[i + 1]
                                    except :
                                        gln = 'None'
                           
                            
                            body = str(soup_link.find('table', class_='details'))
                            pattern = r'<span>Intitulé:</span>(.*?)</td>'
                            matches = re.findall(pattern, body, re.DOTALL)
                            if matches:
                                extracted_text = matches[0].strip().split(',')
                                extracted_text = [element.strip() for element in extracted_text]
                                lang_1 = extracted_text[0] if len(extracted_text) > 0 else 'None'
                                lang_2 = extracted_text[1] if len(extracted_text) > 1 else 'None'
                                lang_3 = extracted_text[2] if len(extracted_text) > 2 else 'None'
                                lang_4 = extracted_text[3] if len(extracted_text) > 3 else 'None'
                                lang_5 = extracted_text[4] if len(extracted_text) > 4 else 'None'

                            serv_1 = serv_2 = serv_3 = serv_4 = serv_5 = 'None'
                            pattern = r'<span>Services spécifiques:</span>(.*?)</td>'
                            matches = re.findall(pattern, body, re.DOTALL)
                            if matches:
                                extracted_text = matches[0].strip().split(',')
                                extracted_text = [element.strip() for element in extracted_text]
                                serv_1 = extracted_text[0] if len(extracted_text) > 0 else 'None'
                                serv_2 = extracted_text[1] if len(extracted_text) > 1 else 'None'
                                serv_3 = extracted_text[2] if len(extracted_text) > 2 else 'None'
                                serv_4 = extracted_text[3] if len(extracted_text) > 3 else 'None'
                                serv_5 = extracted_text[4] if len(extracted_text) > 4 else 'None'

                            description = 'None'
                            body = str(soup_link.find('div', class_='g-s-main wide-right content'))
                            pattern = r'<h3>Description</h3>(.*?)</div>'
                            matches = re.findall(pattern, body, re.DOTALL)
                            if matches:
                                description = matches[0].strip().replace('</p>', '').replace('<p>', '')

                            specification = 'None'
                            spec_1 = spec_2 = spec_3 = spec_4 = spec_5 = 'None'
                            body = str(soup_link.find('div', class_='g-s-right wide details-meta'))
                            
                            pattern = r'</h5>(.*?)<p class="fine-print contact-details">'
                            matches = re.findall(pattern, body, re.DOTALL)
                            if matches:
                                specification = matches[0].strip()
                            
                            pattern = r'<span class="c-grey">(.*?)</span>'
                            matches = re.findall(pattern, specification, re.DOTALL)
                            if matches:
                                spec_1 = matches[0] if len(matches) > 0 else 'None'
                                spec_2 = matches[1] if len(matches) > 1 else 'None'
                                spec_3 = matches[2] if len(matches) > 2 else 'None'
                                spec_4 = matches[3] if len(matches) > 3 else 'None'
                                spec_5 = matches[4] if len(matches) > 4 else 'None'   

                            linkedin = facebook = instagram = title = 'None'
                            row = [link, title, display_full_name, first_name, last_name, before_address, address_1, address_2,
                                   zip_city, mobile_phone, landline_phone, email, website, linkedin, facebook, instagram,
                                   "", practice_id, type_therapeute, rcc, gln, description, lang_1, lang_2, lang_3, lang_4, lang_5,
                                   spec_1, spec_2, spec_3, spec_4, spec_5, serv_1, serv_2, serv_3, serv_4, serv_5]
                            writer.writerow(row)
                        
                        else:
                            print(f"Failed to retrieve profile {link}. Status code: {response_link.status_code}")

                else:
                    print(f"Failed to retrieve page. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error scraping: {str(e)}")


if __name__ == "__main__":
    start_id = 1 
    end_id = 233

    for x in range(start_id, end_id) :
        scraper = PhysioSwissScraper(x)
        scraper.scrape()


