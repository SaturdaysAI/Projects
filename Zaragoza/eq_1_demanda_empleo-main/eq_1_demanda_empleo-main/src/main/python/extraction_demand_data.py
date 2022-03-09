import re
import pandas as pd
from tika import parser
import main.streamlit.config as config

class ExtractionDemandData:

    # REGEX: https://regexr.com  https://regex-generator.olafneumann.org
    SPECIAL_CHARACTERS = [' ', '/', '(', ')', ',', '.']
    PATTERN_JOB = r'([A-ZÑÁÉÍÓÚ\/\(\)\s\,\.\-]+)+'
    PATTERN_LOCATION = r'(([A-ZÑÁÉÍÓÚ]{1,}[a-zñáéíóú]+(\s?|\-?)|[a-zñáéíóú]+\s)*(\(\s[A-ZÑÁÉÍÓÚ]+\s\)){1})'
    PATTERN_JOB_LOCATION = r'([A-ZÑÁÉÍÓÚ\/\(\)\s\,\.\-]+)(([A-ZÑÁÉÍÓÚ]{1,}[a-zñáéíóú]+(\s?|\-?)|[a-zñáéíóú]+\s)*(\(\s[A-ZÑÁÉÍÓÚ]+\s\)){1})'
    PATTERN_ID_JOB = r'(Oferta:\s{1}\d+)'
    PATTERN_DATE = r'(\d+/\d+/\d+)'
    PATTERN_OFFICE = r'(Oficina:\s[A-ZÑÁÉÍÓÚ]+\-?([A-ZÑÁÉÍÓÚ]+\s?)*)' # r'(Oficina:\s[A-ZÑÁÉÍÓÚ\-]+)'
    PATTERN_FOOTNOTE = r'Ofertas en difusión a fecha\s\d+/\d+/\d+\sPágina\s\d\sde\s\d{1,3}'
            
    def __init__(self):
        self.data_list = list()

    def get_text_list_from_pdf(self, pdf_path):
        text_list = []
        raw = parser.from_file(pdf_path)
        text_list = raw["content"].splitlines()
        return ['||' if text == '' else text for text in text_list] # list(filter(None, text_list)) # text_list

    def get_df_demand(self, text_list):
        # sourcery skip: list-literal, merge-comparisons, simplify-str-len-comparison
        job_info= ''
        sector = None        
        for text in text_list:            
            if 'Sector Profesional:' in text:         
                sector = str(text).replace('Sector Profesional:', '').strip()
                print('sector: ', sector)
                #if sector == 'SEGUROS Y FINANZAS':
                #    print('OK')
                self.preprocessing_job_info(job_info, sector_value)
                job_info = ''        
            if (text != 'OFERTAS DE EMPLEO EN DIFUSIÓN') and ('Sector Profesional:' not in text): # text != '' and 
                job_info += text + ' '
                sector_value = sector
        self.preprocessing_job_info(job_info, sector_value)                
        return pd.DataFrame(self.data_list, columns=['sector', 'id_job', 'date', 'job', 'city', 'province', 'office', 'content', 'description', 'task', 'requirement', 'english_level', 'condition', 'number'])

    def preprocessing_job_info(self, job_info, sector_value):
        # sourcery skip: list-literal, merge-comparisons
        job_info_bad = job_info
        job_info_bad = job_info_bad.replace('||', '').strip()
        if len(job_info_bad) != 0:           
            # Job, Location:
            job_location_match_list = re.findall(config.PATTERN_JOB_LOCATION, job_info)
            # ID Job:
            id_job_match_list = re.findall(config.PATTERN_ID_JOB, job_info)               
            # Date:
            date_office_match_list = re.findall(config.PATTERN_DATE+'\s'+config.PATTERN_OFFICE, job_info) 
            size = self.get_smallest(len(job_location_match_list), len(id_job_match_list), len(date_office_match_list))
                            
            job_info_aux_list = list()     
            for i in range(size):
                job_location = str(job_location_match_list[i][0])+str(job_location_match_list[i][1])
                if job_location[0] == '.' or job_location[0] == ' ':
                    job_location = job_location[1:]
                id_job = str(id_job_match_list[i])
                date_office = str(date_office_match_list[i][0])+' '+str(date_office_match_list[i][1]) # str(' '.join(date_office_match_list[i][0]))
                job_info_aux = job_location.strip()+' '+id_job.strip()+' '+date_office.strip()                        
                print(job_info_aux)
                if job_info_aux in job_info:
                    job_info = str(job_info).replace(job_info_aux, '##')
                else:
                    job_info_aux2 = job_location.strip()+' '+id_job.strip()
                    if job_info_aux2 in job_info:
                        job_info = str(job_info).replace(job_info_aux2, '##')
                job_info_aux_list.append(job_info_aux)
            
            pattern=re.compile(config.PATTERN_FOOTNOTE)
            job_info = re.sub(pattern, '', job_info)
            job_info = job_info.replace('||', '').replace('AGUA ', '').replace('"', '').strip()
            job_info_list = str(job_info).split('##')
            job_info_list = list(filter(None, job_info_list))

            for i in range(len(job_info_list)):    
                # Content:               
                content = job_info_list[i].strip()
                # Description:
                description_value = self.get_description_from_content(content)
                # Task:
                task_value = self.get_task_from_content(content)
                # Requirement:
                requirement_value = self.get_requirement_from_content(content)
                # English level:
                english_level_value = self.get_english_level_from_content(content)
                # Condition:
                condition_value = self.get_condition_from_content(content)
                # Number:
                number_value = self.get_number_from_content(content)

                office_value, date_value, id_job_value, job_value, city_value, province_value = self.get_office_date_id_job(job_info_aux_list[i])                        
                if sector_value and office_value and date_value and id_job_value and job_value and city_value and province_value and content:               
                    self.data_list.append((sector_value, id_job_value, date_value, job_value, city_value, province_value, office_value, content, description_value, task_value, requirement_value, english_level_value, condition_value, number_value))

    def get_office_date_id_job(self, text):        
        # sourcery skip: use-named-expression
        # OFFICE:
        office_match = re.search(config.PATTERN_OFFICE, text)
        if office_match:
            office = office_match[0].replace('Oficina:', '').strip()
            text = text.replace(office_match[0], '').strip()
        # print('office: ', office)

        # DATE --> 27/09/2021         
        date_match = re.search(r'(\d+/\d+/\d+)', text)
        if date_match:
            date = date_match[0]
            text = text.replace(date, '').strip()
        # print('date: ', date)

        # ID_JOB --> Oferta: 022021007166
        id_job_match = re.search(r'Oferta:\s{1}\d+', text)
        if id_job_match:
            id_job = str(id_job_match[0]).replace('Oferta:', '').strip()
            text = text.replace(id_job_match[0], '').strip()
        # print('id_job: ', id_job)

        # JOB --> CONTABLES                        
        job_concated = ''
        for character in text:                 
            if (character.isupper()) or (character in self.SPECIAL_CHARACTERS):
                job_concated += character
            else:
                job = job_concated[:len(job_concated)-1].strip()
                text = text.replace(job, '').strip()
                # print('job: ', job)
                break

        # LOCATION --> Gurrea de Gállego ( HUESCA )
        city = None
        province = None
        if ('(' in text) and (')' in text):
            location_list = text.split('(')
            city = location_list[0].strip()
            province = location_list[1].replace(')', '').strip()                                                
            # print('city: ', city)
            # print('province: ', province)
        return office, date, id_job, job, city, province

    def get_smallest(self, num1, num2, num3):
        if (num1 < num2) and (num1 < num3):
            return num1
        elif (num2 < num1) and (num2 < num3):
            return num2
        else:
            return num3

    def get_description_from_content(self, content):      
        description = None  
        if description := re.search(r'(DESCRIPCIÓN:.*FUNCIONES:)', content):
            description = str(description[0]).replace('DESCRIPCIÓN:', '').replace('FUNCIONES:', '').strip()
        return description

    def get_task_from_content(self, content):
        task_value = None
        if task := re.search(r'(\<b\>TAREAS:\<\/b\>.*\<b\>REQUISITOS)', content):
            task_text = str(task[0]).replace('<b>', '').replace('REQUISITOS', '').strip()
            task_list = task_text.split('</b>')
            task_value = task_list[1].strip()
            if task_value[0] == '.':
                task_value = task_value[1:].strip()
        return task_value
        
    def get_requirement_from_content(self, content):     
        requirement_value = None
        if requirement := re.search(r'(\<b\>REQUISITOS solicitados por la empresa:\<\/b\>.*\<b\>CONDICIONES)', content):
            requirement_text = str(requirement[0]).replace('<b>', '').replace('CONDICIONES', '').strip()
            requirement_list = requirement_text.split('</b>')
            requirement_value = requirement_list[1].strip()
            if requirement_value[0] == '.':
                requirement_value = requirement_value[1:].strip()
        elif requirement := re.search(r'(REQUISITOS:\s\<b\>Finalización de un título en los 5 años anteriores al inicio del contrato\<\/b\>.*\<b\>)', content):
            requirement_text = str(requirement[0]).replace('<b>', '').strip()
            requirement_list = requirement_text.split('</b>')
            requirement_value = requirement_list[1].strip()
            if requirement_value[0] == '.':
                requirement_value = requirement_value[1:].strip()
        return requirement_value

    def get_english_level_from_content(self, content):    
        if english_level := re.search(r'(\<b\>inglés nivel medio-alto\<\/b\>)', content):
            return str(english_level[0]).replace('<b>', '').replace('</b>', '').replace('inglés nivel', '').strip()
        else:
            return None

    def get_condition_from_content(self, content):    
        condition_value = None
        if condition := re.search(r'(\<b\>CONDICIONES:\<\/b\>.*\<b\>)', content):
            condition_text = str(condition[0]).replace('<b>', '').strip()            
            condition_list = condition_text.split('</b>')
            condition_value = condition_list[1].strip()
            if condition_value[0] == '.':
                condition_value = condition_value[1:].strip()
        return condition_value

    def get_number_from_content(self, content):    
        number_value = None
        if number := re.search(r'(\<b\>\d{4}\<\/b\>.*)', content):
            number_text = str(number[0]).strip()            
            number_list = number_text.split('</b>')
            number_value = number_list[1].strip()
            if number_value[0] == '.':
                number_value = number_value[1:].strip()
        return number_value

def main():
    extraction_data = ExtractionDemandData()
    ROOT_PATH = '...'
    pdf_path = ROOT_PATH+'/eq_1_demanda_empleo/actualizado/resources/diarios/S23/S23_14.2.pdf'
    text_list = extraction_data.get_text_list_from_pdf(pdf_path)
    
    df_data = extraction_data.get_df_demand(text_list)
    df_data_path = ROOT_PATH+'/eq_1_demanda_empleo/actualizado/resources/diarios_csv/S23/ofertas_S23_14.2.csv'
    df_data.to_csv(df_data_path, sep=',', encoding='utf-8', index_label='index', index=False)

if __name__ == '__main__':
    main()