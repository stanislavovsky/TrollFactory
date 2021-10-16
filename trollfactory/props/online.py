"""Online activity data generation prop for TrollFactory."""

from string import ascii_uppercase, ascii_lowercase, digits
from random import choice, randint
from pkgutil import get_data
from typing import Optional
from json import loads

EMAIL_PROVIDERS = {
    'polish': ['@niepodam.pl'],
    'english_us': ['@armyspy.com', '@cuvox.de', '@dayrep.com', '@einrot.com',
                   '@gustr.com', '@jourrapide.com', '@rhyta.com',
                   '@superrito.com', '@teleworm.us'],
}

EMAIL_URLS = {
    '@niepodam.pl': 'http://niepodam.pl/users/',
    '@armyspy.com': 'http://www.fakemailgenerator.com/#/armyspy.com/',
    '@cuvox.de': 'http://www.fakemailgenerator.com/#/cuvox.de/',
    '@dayrep.com': 'http://www.fakemailgenerator.com/#/dayrep.com/',
    '@einrot.com': 'http://www.fakemailgenerator.com/#/einrot.com/',
    '@gustr.com': 'http://www.fakemailgenerator.com/#/gustr.com/',
    '@jourrapide.com': 'http://www.fakemailgenerator.com/#/jourrapide.com/',
    '@rhyta.com': 'http://www.fakemailgenerator.com/#/rhyta.com/',
    '@superrito.com': 'http://www.fakemailgenerator.com/#/superrito.com/',
    '@teleworm.us': 'http://www.fakemailgenerator.com/#/teleworm.us/',
}

TLDS = ['.pl', '.com', '.com.pl', '.net', '.biz', '.me']


def generate_username(name: str, surname: str) -> str:
    name = name.split(', ')[0] if ', ' in name else name
    return name.lower()[0] + '_' + surname.lower()


def generate_email(username: str, language: str) -> str:
    return username + choice(EMAIL_PROVIDERS[language])


def generate_email_url(email: str, username: str) -> Optional[str]:
    email_provider = '@' + email.split('@')[1]
    if email_provider in EMAIL_URLS:
        return EMAIL_URLS[email_provider] + username
    return None


def generate_domain_name(username: str) -> str:
    return username.replace('_', '') + choice(TLDS)


def generate_password() -> str:
    return ''.join(choice(ascii_uppercase + ascii_lowercase + digits
                          ) for _ in range(16))


def generate_setup(language: str) -> dict:
    return choice(loads(get_data(__package__,
                                 'langs/'+language+'/setups.json')))


def generate_operating_system(setup: dict) -> str:
    return setup['os']


def generate_browser(setup: dict) -> str:
    return setup['browser']


def generate_user_agent(setup: dict) -> str:
    return ' '.join(setup['user_agent'])


def generate_ipv4() -> str:
    return '.'.join(str(randint(0, 255)) for _ in range(4))


def generate_ipv6() -> str:
    return ':'.join('{:x}'.format(randint(0, 2**16 - 1)) for i in range(8))


def generate_mac() -> str:
    return ("02:00:00:%02x:%02x:%02x" % (
            randint(0, 255), randint(0, 255), randint(0, 255))).upper()


class Online:
    def __init__(self, properties: dict) -> None:
        self.properties = properties
        self.unresolved_dependencies = []

        for dependency in ['name', 'language']:
            if dependency not in self.properties:
                self.unresolved_dependencies.append(dependency)

    def generate(self) -> dict:
        # Used properties
        name = self.properties['name']['name']
        surname = self.properties['name']['surname']
        language = self.properties['language']['language']

        # Generate data
        username = generate_username(name, surname)
        email = generate_email(username, language)
        domain_name = generate_domain_name(username)
        password = generate_password()
        setup = generate_setup(language)
        operating_system = generate_operating_system(setup)
        browser = generate_browser(setup)
        user_agent = generate_user_agent(setup)
        ipv4 = generate_ipv4()
        ipv6 = generate_ipv6()
        mac = generate_mac()
        email_url = generate_email_url(email, username)

        return {
            'prop_title': 'Online',
            'username': username,
            'email': email,
            'receive_email': email_url,
            'domain_name': domain_name,
            'password': password,
            'operating_system': operating_system,
            'browser': browser,
            'user_agent': user_agent,
            'ipv4': ipv4,
            'ipv6': ipv6,
            'mac': mac,
        }
