from common.parsing.parser import IParser
from common.parsing.xml_extractors import (
    CustomExtractor,
)
from structlog import get_logger
import re


class APSParserXML(IParser):
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.logger = get_logger().bind(class_name=type(self).__name__)
        self.dois = None

        extractors = [
            CustomExtractor("authors", self._get_authors),
        ]
        super().__init__(extractors)

    def _get_affiliations(self, article, contrib):
        affiliations = []
        
        xref_elements = contrib.findall(".//xref[@ref-type='aff']")
        
        if not xref_elements:
            self.logger.msg("No affiliations found for this author.")
            return affiliations
        
        for xref in xref_elements:
            ref_id = xref.get("rid")
            
            if ref_id:
                affiliation_node = article.find(f".//aff[@id='{ref_id}']")
                
                if affiliation_node is not None:
                    full_text_parts = []
                    ror = None
                    
                    for child in affiliation_node.iter():
                        if child.tag == "institution-id" and child.get("institution-id-type") == "ror":
                            ror = child.text
                        elif child.tag not in ["label", "sup", "institution-id"]:
                            if child.text:
                                full_text_parts.append(child.text.strip())
                        if child.tail:
                            full_text_parts.append(child.tail.strip())
                    
                    raw_aff_text = " ".join(filter(None, full_text_parts))
                    aff_text = re.sub(r'\s*,\s*,*', ', ', raw_aff_text)
                    aff_text = re.sub(r'\s+', ' ', aff_text).strip()
                    
                    affiliations.append({"value": aff_text, "ror": ror})
                else:
                    self.logger.msg(f"Affiliation with id '{ref_id}' not found.")
        
        return affiliations


    def _get_authors(self, article):
        authors = []
        
        contrib_group = article.find("./front/article-meta/contrib-group")
        if contrib_group is None:
            return authors

        for contrib in contrib_group.findall("./contrib[@contrib-type='author']"):
            author = {}
            
            name = contrib.find("./name")
            if name is not None:
                given_names = name.find("given-names")
                surname = name.find("surname")
                author["given_names"] = given_names.text if given_names is not None else ""
                author["surname"] = surname.text if surname is not None else ""
                author["full_name"] = f"{author['given_names']} {author['surname']}".strip()
            
            orcid = contrib.find("./contrib-id[@contrib-id-type='orcid']")
            if orcid is not None:
                author["orcid"] = orcid.text
            
            author["affiliations"] = self._get_affiliations(article, contrib)
            
            authors.append(author)
        
        return authors

