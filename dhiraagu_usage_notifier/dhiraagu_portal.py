from email import header
import requests
from bs4 import BeautifulSoup
import prettytable as pt

LOGIN_URL = "https://portal.dhivehinet.net.mv/adsls/login_api"
HOME_URL = "https://portal.dhivehinet.net.mv/home"


def login_and_return_html(username, password):
    payload = {
        'data[adsl][username]': username,
        'data[adsl][password]': password
    }

    session = requests.Session()
    login_request = session.post(LOGIN_URL, data=payload)

    # If login credentials are correct
    if login_request.status_code == 200:
        home_page = session.get(HOME_URL)
        return home_page.text  # return html
    else:
        return False


def get_usage_data(home_page):
    soup = BeautifulSoup(home_page, 'html.parser')

    # plan_allowance = soup.find_all('td', {"colspan": "2"})[-1]

    # Convert data type into bytes as an int
    plan_allowance = convert_size_to_bytes(soup.select_one(
        'th:-soup-contains("Plan Allowance")').find_next('td').text)

    # Get the percentage remaining as a string with only the number
    percentage_remaining_as_string = soup.find(
        'div', {"class": "progress-bar-allowance"}).text.replace('% Left', '')
    percentage_remaining = float(percentage_remaining_as_string)

    data_remaining = (percentage_remaining / 100) * plan_allowance
    data_used = plan_allowance - data_remaining

    # Pretty Table
    table = pt.PrettyTable(['Name', 'Value'], header=False, padding_width=2)

    # Customize
    table.title = 'Usage Data'
    table.align['Name'] = 'l'
    table.align['Value'] = 'r'

    # Populate data
    table.add_row(['Allowance', sizeof_fmt(plan_allowance)])
    table.add_row(['Remaining', sizeof_fmt(data_remaining)])
    table.add_row(['Used', sizeof_fmt(data_used)])

    # Markdown (V2) 'pre-formatted fixed-width code block'
    output = f'```{table}```'

    return output


def convert_size_to_bytes(size_str):
    """Convert human filesizes to bytes.

    Special cases:
     - singular units, e.g., "1 byte"
     - byte vs b
     - yottabytes, zetabytes, etc.
     - with & without spaces between & around units.
     - floats ("5.2 mb")

    To reverse this, see hurry.filesize or the Django filesizeformat template
    filter.

    :param size_str: A human-readable string representing a file size, e.g.,
    "22 megabytes".
    :return: The number of bytes represented by the string.
    """
    multipliers = {
        'kilobyte':  1024,
        'megabyte':  1024 ** 2,
        'gigabyte':  1024 ** 3,
        'terabyte':  1024 ** 4,
        'petabyte':  1024 ** 5,
        'exabyte':   1024 ** 6,
        'zetabyte':  1024 ** 7,
        'yottabyte': 1024 ** 8,
        'kb': 1024,
        'mb': 1024**2,
        'gb': 1024**3,
        'tb': 1024**4,
        'pb': 1024**5,
        'eb': 1024**6,
        'zb': 1024**7,
        'yb': 1024**8,
    }

    for suffix in multipliers:
        size_str = size_str.lower().strip().strip('s')
        if size_str.lower().endswith(suffix):
            return int(float(size_str[0:-len(suffix)]) * multipliers[suffix])
    else:
        if size_str.endswith('b'):
            size_str = size_str[0:-1]
        elif size_str.endswith('byte'):
            size_str = size_str[0:-4]
    return int(size_str)


# Convert bytes in int into human readable file sizes
def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.00:
            return f"{num:3.2f}{unit}{suffix}"
        num /= 1024.00
    return f"{num:.2f}Yi{suffix}"
