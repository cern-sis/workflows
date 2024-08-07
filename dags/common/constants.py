import re
from collections import OrderedDict

ARXIV_EXTRACTION_PATTERN = re.compile(r"(arxiv:|v[0-9]$)", flags=re.I)
NODE_ATTRIBUTE_NOT_FOUND_ERRORS = (AttributeError, TypeError)
COUNTRY_PARSING_PATTERN = re.compile(r"\b[A-Z]*[a-z]*$")
ORGANIZATION_PARSING_PATTERN = re.compile(r",\s\b[A-Z]*[a-z]*$")
REMOVE_SPECIAL_CHARS = re.compile(r"[^A-Za-z0-9\s\,\.]+")
LICENSE_PATTERN = re.compile(r"([A-Za-z]+)\/([0-9]+\.[0-9]+)")
LICENSE_VERSION_PATTERN = re.compile(r"\d{1,}\.\d{1}")
CREATIVE_COMMONS_PATTERN = re.compile(r".*(creative\s{0,}commons).*", flags=re.I)
BY_PATTERN = re.compile(r".*(attribution).*", flags=re.I)
WHITE_SPACES = re.compile(r"[\n\t]{1,}" + r"\s{2,}")
CDATA_PATTERN = re.compile(r"<\?CDATA(.*)\?>")
FN_REGEX = re.compile(r"<fn.*<\/fn>")

JOURNAL_MAPPING = {"PLB": "Physics Letters B", "NUPHB": "Nuclear Physics B"}

PARTNERS = [
    "Australia",
    "Austria",
    "Belgium",
    "Canada",
    "CERN",
    "China",
    "Czech Republic",
    "Denmark",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hong-Kong",
    "Hungary",
    "Iceland",
    "Israel",
    "Italy",
    "Japan",
    "JINR",
    "Mexico",
    "Netherlands",
    "Norway",
    "Poland",
    "Portugal",
    "Slovak Republic",
    "South Africa",
    "South Korea",
    "Spain",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Turkey",
    "United Kingdom",
    "United States",
]

COUNTRIES_DEFAULT_MAPPING = OrderedDict(
    [
        ("INFN", "Italy"),
        ("Democratic People's Republic of Korea", "North Korea"),
        ("DPR Korea", "North Korea"),
        ("DPR. Korea", "North Korea"),
        ("CERN", "CERN"),
        ("European Organization for Nuclear Research", "CERN"),
        ("KEK", "Japan"),
        ("DESY", "Germany"),
        ("FERMILAB", "USA"),
        ("FNAL", "USA"),
        ("SLACK", "USA"),
        ("Stanford Linear Accelerator Center", "USA"),
        ("Joint Institute for Nuclear Research", "JINR"),
        ("JINR", "JINR"),
        ("Northern Cyprus", "Turkey"),
        ("North Cyprus", "Turkey"),
        ("New Mexico", "USA"),
        ("South China Normal University", "China"),
        ("Hong Kong China", "Hong Kong"),
        ("Hong-Kong China", "Hong Kong"),
        ("Hong Kong, China", "Hong Kong"),
        ("Hong Kong", "Hong Kong"),
        ("Hong-Kong", "Hong Kong"),
        ("Algeria", "Algeria"),
        ("Argentina", "Argentina"),
        ("Armenia", "Armenia"),
        ("Australia", "Australia"),
        ("Austria", "Austria"),
        ("Azerbaijan", "Azerbaijan"),
        ("Belarus", "Belarus"),
        ("Belgium", "Belgium"),
        ("Belgique", "Belgium"),
        ("Bangladesh", "Bangladesh"),
        ("Brazil", "Brazil"),
        ("Brasil", "Brazil"),
        ("Benin", "Benin"),
        (u"Bénin", "Benin"),
        ("Bulgaria", "Bulgaria"),
        ("Bosnia and Herzegovina", "Bosnia and Herzegovina"),
        ("Canada", "Canada"),
        ("Chile", "Chile"),
        ("ROC", "Taiwan"),
        ("R.O.C", "Taiwan"),
        ("Republic of China", "Taiwan"),
        ("China (PRC)", "China"),
        ("PR China", "China"),
        ("China", "China"),
        ("People's Republic of China", "China"),
        ("Republic of China", "China"),
        ("Colombia", "Colombia"),
        ("Costa Rica", "Costa Rica"),
        ("Cuba", "Cuba"),
        ("Croatia", "Croatia"),
        ("Cyprus", "Cyprus"),
        ("Czech Republic", "Czech Republic"),
        ("Czech", "Czech Republic"),
        ("Czechia", "Czech Republic"),
        ("Denmark", "Denmark"),
        ("Egypt", "Egypt"),
        ("Estonia", "Estonia"),
        ("Ecuador", "Ecuador"),
        ("Finland", "Finland"),
        ("France", "France"),
        ("Germany", "Germany"),
        ("Deutschland", "Germany"),
        ("Greece", "Greece"),
        ("Hungary", "Hungary"),
        ("Iceland", "Iceland"),
        ("India", "India"),
        ("Indonesia", "Indonesia"),
        ("Iran", "Iran"),
        ("Ireland", "Ireland"),
        ("Israel", "Israel"),
        ("Italy", "Italy"),
        ("Italia", "Italy"),
        ("Japan", "Japan"),
        ("Jamaica", "Jamaica"),
        ("Korea", "South Korea"),
        ("Republic of Korea", "South Korea"),
        ("South Korea", "South Korea"),
        ("Latvia", "Latvia"),
        ("Lebanon", "Lebanon"),
        ("Lithuania", "Lithuania"),
        ("Luxembourg", "Luxembourg"),
        ("Macedonia", "Macedonia"),
        ("Mexico", "Mexico"),
        (u"México", "Mexico"),
        ("Monaco", "Monaco"),
        ("Montenegro", "Montenegro"),
        ("Morocco", "Morocco"),
        ("Niger", "Niger"),
        ("Nigeria", "Nigeria"),
        ("Netherlands", "Netherlands"),
        ("The Netherlands", "Netherlands"),
        ("New Zealand", "New Zealand"),
        ("Zealand", "New Zealand"),
        ("Norway", "Norway"),
        ("Oman", "Oman"),
        ("Sultanate of Oman", "Oman"),
        ("Pakistan", "Pakistan"),
        ("Panama", "Panama"),
        ("Philipines", "Philipines"),
        ("Poland", "Poland"),
        ("Portugalo", "Portugal"),
        ("Portugal", "Portugal"),
        ("P.R.China", "China"),
        (u"People’s Republic of China", "China"),
        ("Republic of Belarus", "Belarus"),
        ("Republic of Benin", "Benin"),
        ("Republic of Korea", "South Korea"),
        ("Republic of San Marino", "San Marino"),
        ("Republic of South Africa", "South Africa"),
        ("Romania", "Romania"),
        ("Russia", "Russia"),
        ("Russian Federation", "Russia"),
        ("Saudi Arabia", "Saudi Arabia"),
        ("Kingdom of Saudi Arabia", "Saudi Arabia"),
        ("Arabia", "Saudi Arabia"),
        ("Serbia", "Serbia"),
        ("Singapore", "Singapore"),
        ("Slovak Republic", "Slovakia"),
        ("Slovak", "Slovakia"),
        ("Slovakia", "Slovakia"),
        ("Slovenia", "Slovenia"),
        ("South Africa", "South Africa"),
        ("Africa", "South Africa"),
        (u"España", "Spain"),
        ("Spain", "Spain"),
        ("Sudan", "Sudan"),
        ("Sweden", "Sweden"),
        ("Switzerland", "Switzerland"),
        ("Syria", "Syria"),
        ("Taiwan", "Taiwan"),
        ("Thailand", "Thailand"),
        ("Tunisia", "Tunisia"),
        ("Turkey", "Turkey"),
        ("Ukraine", "Ukraine"),
        ("United Kingdom", "UK"),
        ("Kingdom", "UK"),
        ("United Kingdom of Great Britain and Northern Ireland", "UK"),
        ("UK", "UK"),
        ("England", "UK"),
        ("Scotland", "UK"),
        ("Wales", "UK"),
        ("New South Wales", "Australia"),
        ("U.K", "UK"),
        ("United States of America", "USA"),
        ("United States", "USA"),
        ("USA", "USA"),
        ("U.S.A", "USA"),
        ("U.S.A.", "USA"),
        ("America", "USA"),
        ("Uruguay", "Uruguay"),
        ("Uzbekistan", "Uzbekistan"),
        ("Venezuela", "Venezuela"),
        ("Vietnam", "Vietnam"),
        ("Viet Nam", "Vietnam"),
        ("Yemen", "Yemen"),
        ("Peru", "Peru"),
        ("Kuwait", "Kuwait"),
        ("Sri Lanka", "Sri Lanka"),
        ("Lanka", "Sri Lanka"),
        ("Kazakhstan", "Kazakhstan"),
        ("Mongolia", "Mongolia"),
        ("United Arab Emirates", "United Arab Emirates"),
        ("Emirates", "United Arab Emirates"),
        ("Malaysia", "Malaysia"),
        ("Qatar", "Qatar"),
        ("Kyrgyz Republic", "Kyrgyz Republic"),
        ("Jordan", "Jordan"),
        ("Belgrade", "Serbia"),
        ("Istanbul", "Turkey"),
        ("Ankara", "Turkey"),
        ("Rome", "Italy"),
        ("Georgia", "Georgia"),
    ]
)

INSTITUTIONS_AND_COUNTRIES_MAPPING = OrderedDict([
    ("INFN", "Italy"),
    ("European Organization for Nuclear Research", "CERN"),
    ("Conseil Européen pour la Recherche Nucléaire", "CERN"),
    ("CERN", "CERN"),
    ("KEK", "Japan"),
    ("DESY", "Germany"),
    ("FERMILAB", "USA"),
    ("FNAL", "USA"),
    ("SLACK", "USA"),
    ("Stanford Linear Accelerator Center", "USA"),
    ("Joint Institute for Nuclear Research", "JINR"),
    ("JINR", "JINR"),
    ("ROC", "Taiwan"),
    ("R.O.C", "Taiwan"),
])
