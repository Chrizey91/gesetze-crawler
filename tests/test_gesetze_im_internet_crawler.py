import os
from gesetze_crawler import gesetze_im_internet_crawler as gii

def test_get_law_text_web_address():
    law_text_abbr = "GG"
    law_text_web_address = gii.get_law_text_web_address(law_text_abbr)
    assert law_text_web_address == "https://www.gesetze-im-internet.de/gg/index.html"

def test_download_law_text_html_wayback(test_dir):
    wayback_address = "https://web.archive.org/web/20160209224728/https://www.gesetze-im-internet.de/gg/BJNR000010949.html"
    assert not os.path.exists(os.path.join(test_dir, "html", "law_text.md"))
    gii.download_law_text_html(wayback_address, test_dir)
    assert os.path.exists(os.path.join(test_dir, "html", "law_text.md"))

def test_download_law_text_html_gii(test_dir):
    wayback_address = "https://www.gesetze-im-internet.de/gg/BJNR000010949.html"
    assert not os.path.exists(os.path.join(test_dir, "html", "law_text.md"))
    gii.download_law_text_html(wayback_address, test_dir)
    assert os.path.exists(os.path.join(test_dir, "html", "law_text.md"))

def test_get_law_text_file_address():
    law_text_address = "https://www.gesetze-im-internet.de/gg/index.html"
    expected_law_text_file_address = "https://www.gesetze-im-internet.de/gg/BJNR000010949.html"
    law_text_file_address = gii.get_law_text_file_address(law_text_address, "HTML")
    assert law_text_file_address == expected_law_text_file_address

def test_crawl_gesetze_im_internet_wayback():
    pass
