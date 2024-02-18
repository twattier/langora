MIN_IMG_SIZE = 300

default_list_click = [
    "//button[contains(@id, 'accept')]",
    "//button[contains(., 'ccept')]",
    "//button[contains(., 'onsent')]",
    "//a[contains(., 'ccept')]",        
]

default_list_content = [
    "article",
    "div/class=article",
    "div/class=container",
    "div/id=content",
    "div/class=content",
    "body"
]

web_scrapper = {    
    "hbr.org": {"content" : "div/class=standard--container"},
    "www.bcg.com": {"content" : "div/class=content-inner-wrapper"},
    "www.linkedin.com": {
        "click" : "//button[contains(@aria-label, 'Ignore')]",
        "content" : "div/data-test-id=article-content-blocks"
    },
    "www.gartner.com": {"content" : "div/class=emt-container-inner"},
    "www.eweek.com" : {"click" : "//button[contains(., 'AGREE')]"}}