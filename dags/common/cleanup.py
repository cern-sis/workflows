def clean_whitespace_characters(input):
    return " ".join(input.split())

def convert_html_subsripts_to_latex(input):
    from re import sub

    input = sub("<sub>(.*?)</sub>", r"$_{\1}$", input)
    input = sub("<inf>(.*?)</inf>", r"$_{\1}$", input)
    input = sub("<sup>(.*?)</sup>", r"$^{\1}$", input)   

    return input
