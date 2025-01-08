from gesetze_crawler import wayback_machine_crawler as wmc

def test_get_wayback_web_address():
    input_address = "https://www.gesetze-im-internet.de/gg/index.html"
    input_timestamp = "2007"
    expected_wayback_address = "https://web.archive.org/web/20070212121108/https://www.gesetze-im-internet.de/gg/index.html"
    wayback_address = wmc.get_wayback_web_address(input_address, input_timestamp)
    assert wayback_address == expected_wayback_address

def test_get_wayback_web_addresses():
    input_address = "https://www.gesetze-im-internet.de/gg/index.html"
    input_timestamp = "2007"
    expected_first_wayback_addresses = [
        "https://web.archive.org/web/20070212121108/https://www.gesetze-im-internet.de/gg/index.html",
        "https://web.archive.org/web/20101225011202/https://www.gesetze-im-internet.de/gg/index.html",
        "https://web.archive.org/web/20110503222102/https://www.gesetze-im-internet.de/gg/index.html"
    ]
    wayback_addresses = wmc.get_wayback_web_addresses(input_address, input_timestamp)
    assert len(wayback_addresses) >= 3
    for i in range(3):
        assert wayback_addresses[i] == expected_first_wayback_addresses[i]
    