def clean_whitespace_characters(input):
    return " ".join(input.split())


def convert_html_subsripts_to_latex(input):
    from re import sub

    input = sub("<sub>(.*?)</sub>", r"$_{\1}$", input)
    input = sub("<inf>(.*?)</inf>", r"$_{\1}$", input)
    input = sub("<sup>(.*?)</sup>", r"$^{\1}$", input)

    return input


def clean_html(input):
    from lxml.etree import ParserError, XMLSyntaxError
    from lxml.html.clean import Cleaner

    try:
        cleaner = Cleaner(safe_attrs_only=True, remove_unknown_tags=False)
        return cleaner.clean_html(input)
    except (XMLSyntaxError, ParserError):
        return input
