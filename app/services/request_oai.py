import requests
import xml.etree.ElementTree as ET
from pyramid.request import Request
import re


class RequestOAI:
    def __init__(self, request: Request):
        self.request = request

    def request_oai(self, site_url, abbreviation):
        url = (
            f"{site_url}/oai?verb=ListRecords&metadataPrefix=oai_dc&set={abbreviation}"
        )
        response = requests.get(url)

        if response.status_code == 200:
            xml_data = response.content
            root = ET.fromstring(xml_data)

            records = root.findall(".//{*}record")
            resumption_token_element = root.find(".//{*}resumptionToken")

            parse_results = self.parse_oai(records)
            resumption_results = []

            if resumption_token_element is not None:
                resumption_token = resumption_token_element.text
                resumption_results = self.resumption_parse(resumption_token, site_url)

            combined_results = resumption_results + parse_results
            counts = len(combined_results)

            return {"results": combined_results, "counts": counts}

        else:
            error_message = {"error": "Failed to fetch data"}
            return error_message

    def resumption_parse(self, token, site_url):
        url = f"{site_url}/oai?verb=ListRecords&resumptionToken={token}"
        response = requests.get(url)

        if response.status_code == 200:
            xml_data = response.content
            root = ET.fromstring(xml_data)

            records = root.findall(".//{*}record")
            resumption_token_element = root.find(".//{*}resumptionToken")

            parse_results = self.parse_oai(records)
            resumption_results = []

            if resumption_token_element is not None:
                resumption_token = resumption_token_element.text
                resumption_results = self.resumption_parse(resumption_token, site_url)

            combined_results = resumption_results + parse_results
            return combined_results

        else:
            error_message = {"error": "Failed to fetch data"}
            return error_message

    def parse_oai(self, records):
        results = []

        for record in records:
            header = record.find("{*}header")
            metadata = record.find("{*}metadata")
            dc = metadata.find("{*}dc")

            articleId = header.find("{*}identifier").text.split("/")[-1]
            lastUpdate = header.find("{*}datestamp").text
            title = dc.find("{*}title").text
            creators = dc.findall("{*}creator")
            subjects = dc.findall("{*}subject")
            description = dc.find("{*}description").text
            publisher = dc.find("{*}publisher").text
            publishDate = dc.find("{*}date").text
            doi = dc.findall("{*}identifier")[-1].text
            sources = dc.findall("{*}source")[0].text
            fileView_elements = dc.findall("{*}relation")
            fileView = fileView_elements[0].text if fileView_elements else None

            sources_split = sources.split(";")

            subjectsText = ([subject.text for subject in subjects],)

            subjectsText = subjects[0].text if subjects else ""

            if subjectsText:
                subjectsText = re.split(r", |; |,|;", subjectsText)
                subjectsText = [subject.title() for subject in subjectsText]
            else:
                subjectsText = []

            publishYear = publishDate.split("-")[0]

            results.append(
                {
                    "article_id": articleId,
                    "last_update": lastUpdate,
                    "title": title,
                    "creators": [creator.text for creator in creators],
                    "subjects": subjectsText,
                    "description": description,
                    "publisher": publisher,
                    "publish_at": publishDate,
                    "publish_year": publishYear,
                    "doi": doi,
                    "featured": False,
                    "file_view": fileView,
                    "journal": sources_split[0].strip(),
                    "volume": sources_split[1].strip().split(", ")[0].split(" ")[1],
                    "issue": sources_split[1].strip().split(", ")[1].split(" ")[1],
                    "pages": sources_split[2].strip(),
                }
            )

        return results
