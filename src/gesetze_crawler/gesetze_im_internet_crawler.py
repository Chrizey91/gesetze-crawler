import requests
from bs4 import BeautifulSoup
import os
import zipfile
from pathlib import Path
from urllib.parse import urljoin

GESETZE_IM_INTERNET_BASE_URL = "https://www.gesetze-im-internet.de/"
GESETZE_IM_INTERNET_AKTUELL_URL = "https://www.gesetze-im-internet.de/aktuell.html"

def get_law_text_file_address(web_address: str, file_type: str) -> str:
    response = requests.get(web_address)
    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a")
    file_path = ""
    for link in links:
        if link.abbr and link.abbr.contents[0] == file_type:
            base_path = os.path.split(web_address)[0]
            file_path = base_path + "/" + link.get("href")
        
    if not file_path:    
        raise FileNotFoundError("The web-address " + web_address + " does not offer " + file_type + "-file downloads.")
    
    return file_path

def get_law_text_web_address(law_text_abbr: str) -> str:
    response = requests.get(GESETZE_IM_INTERNET_AKTUELL_URL)
    soup = BeautifulSoup(response.content, "html.parser")

    teillisten = soup.find_all("a", class_="alphabet")
    for link in teillisten:
        tl_request = requests.get(GESETZE_IM_INTERNET_BASE_URL + link.get("href"))
        tl_soup = BeautifulSoup(tl_request.content, "html.parser")

        law_links = tl_soup.find_all("a")
        for ll in law_links:
            if ll.abbr and ll.abbr.contents[0] != "PDF":
                if str(ll.abbr.contents[0]).strip() == law_text_abbr:
                    return urljoin(GESETZE_IM_INTERNET_BASE_URL, ll.get("href"))
    

def download_law_text_xml(web_address: str, output_dir: str):
    raise FileNotFoundError("The web-address " + web_address + " does not offer xml-file downloads.")

def download_law_text_html(html_path: str, output_dir: str):
    response = requests.get(html_path)
    if not response.ok:
        raise FileNotFoundError("The web-address " + html_path + " does not exist.")
    soup = BeautifulSoup(response.text, "html.parser")
    law_section = soup.find("div", attrs={"id": "container"})

    raw_output_dir = os.path.join(output_dir, "html")

    Path(raw_output_dir).mkdir(parents=True, exist_ok=True)

    law_text = ""
    for s in law_section.strings:
        law_text += s + "\n"
    
    with open(os.path.join(raw_output_dir, "law_text.md"), "w", encoding="utf-8") as f:
        f.writelines(law_text)

    
def download_law_text(web_address: str, output_dir):
    try:
        download_law_text_xml(web_address, output_dir)
    except FileNotFoundError:
        download_law_text_html(web_address, output_dir)

def crawl_gesetze_im_internet(law_text_abbr: str, output_dir: str):
    law_text_web_address = get_law_text_web_address(law_text_abbr)
    law_text_file_address = get_law_text_file_address(law_text_web_address, "HTML")
    download_law_text(law_text_file_address, output_dir)

def download_law_text_zip(link: str):
    print("Path obtained: " + link)
    base_path = os.path.split(link)[0]
    zip_path = base_path + "/xml.zip"
    print("New path: " + zip_path)
    download_path = "test-dir"
    download_and_extract_zip(zip_path, download_path)
    file_counter = 0
    for file in os.listdir(download_path):
        if file.endswith(".xml"):
            file_counter += 1
            if file_counter > 1:
                raise FileExistsError("More than one XML-file")
            write_law_text(os.path.join(download_path, file), download_path)

def write_law_text(link_to_xml_file: str, output_dir: str):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    law_text = ""

    with open(link_to_xml_file, "r") as f:
        soup = BeautifulSoup(f, features="xml")
        for s in soup.strings:
            law_text += s + "\n"
    
    with open(os.path.join(output_dir, "law_text.md"), "w") as f:
        f.writelines(law_text)


def download_and_extract_zip(zip_url: str, output_dir: str):
    """
    Downloads a .zip file from a given URL, extracts its contents, and stores them in a specified directory.

    :param zip_url: URL of the .zip file to download.
    :param output_dir: Directory where the extracted contents should be stored.
    :return: None
    """
    try:
        # Ensure the output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Download the zip file
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()  # Raise an error for failed requests

        # Define the temporary file path for the zip file
        zip_path = os.path.join(output_dir, "temp_download.zip")

        # Write the content to the temporary file
        with open(zip_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)

        # Remove the temporary zip file
        os.remove(zip_path)

        print(f"Contents extracted successfully to {output_dir}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the zip file: {e}")
    except zipfile.BadZipFile as e:
        print(f"Failed to extract the zip file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

