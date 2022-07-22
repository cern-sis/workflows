import csv

from inspire_utils.record import get_value


def get_authors(dict):
    return dict["authors"]


def get_primary_category(hit):
    return get_value(hit, "arxiv_eprints.categories[0][0]", default="no category")


def get_affiliations(authors):
    affiliations_per_author = [
        (get_value(author, "affiliations", default=[{"country": "UNKNOWN"}]))
        for author in authors
    ]
    countries_per_author = []
    for affiliation in affiliations_per_author:
        countries_per_author.append(
            [
                get_value(countries, "country", default="UNKNOWN") or ["UNKNOWN"]
                for countries in affiliation
            ]
        )

    for countries in countries_per_author:
        for country in countries:
            if "Palestine" == country:
                index = countries.index("Palestine")
                countries[index] = "West Bank and Gaza"
            elif "HUMAN CHECK" == country:
                index = countries.index("HUMAN CHECK")
                countries[index] = "UNKNOWN"
            elif "United Kingdom" == country:
                index = countries.index("United Kingdom")
                countries[index] = "UK"
            elif "Yemen" == country:
                index = countries.index("Yemen")
                countries[index] = "Yemen, Rep."
            elif "México" == country:
                index = countries.index("México")
                countries[index] = "Mexico"
            elif "Bahamas" == country:
                index = countries.index("Bahamas")
                countries[index] = "The Bahamas"
            elif "United States of America" == country:
                index = countries.index("United States of America")
                countries[index] = "USA"
        if len(countries) == 0:
            countries = ["UNKNOWN"]
    return countries_per_author


def get_country_with_highest_gdp(countries, gdps):
    values = [(country, gdps[country]) for country in countries]
    return max(values, key=lambda t: t[1])[0]


def get_most_important_country(countries, gdps):
    hep_institutes = {
        "KEK": "Japan",
        "SLAC": "USA",
        "DESY": "Germany",
        "FERMILAB": "USA",
        "JINR": "Russia",
    }
    if len(countries) == 1:
        return countries[0]
    if "CERN" in countries:
        return "CERN"
    if len(present_hep := set(hep_institutes.keys()).intersection(set(countries))) > 0:
        if len(present_hep) == 1:
            return hep_institutes[present_hep.pop()]
        countries_of_hep_insitutions = [
            hep_institutes[hep_instition] for hep_instition in present_hep
        ]
        return get_country_with_highest_gdp(countries_of_hep_insitutions, gdps)
    return get_country_with_highest_gdp(countries, gdps)


def get_gdp_from_file():
    with open("gdp.csv", "r") as file:
        reader = csv.reader(file)
        ret_dict = {}
        for row in reader:
            value = row[3]
            ret_dict[row[0]] = float(value) if value else 0
        ret_dict["Taiwan"] = ret_dict["China"]
        return ret_dict


def build_countries_list_values(countries, all_countries_list):
    ret_dict = {country: 0 for country in all_countries_list}
    for country in countries:
        if country not in ret_dict:
            ret_dict["UNKNOWN"] += 1 
        else:
            ret_dict[country] += 1
    ret_list = [value for value in ret_dict.items()]
    return [(amount * 100 / len(countries)) for _, amount in ret_list]
