# [Final fields](#final_fields)

| Field                | Processed                                                                                                                          | Subfield       | Subsubfield |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------- | ----------- |
| dois                 | <a href="#generic_parsing">generic_parsing</a> : <a href="#33">[33]</a>                                                            | value          |             |
| arxiv_eprints        | <a href="#enricher">enricher</a> : <a href="#67">[67]</a>                                                                          | value          |             |
|                      |                                                                                                                                    | categories     |             |
| page_nr              | <a href="#parsing">parsing</a> : <a href="#6">[6]</a>                                                                              |                |             |
| authors              | <a href="#parsing">parsing</a> : <a href="#6">[6]</a> <br/><a href="#generic_parsing">generic_parsing</a> : <a href="#22">[22]</a> | surname        |             |
|                      |                                                                                                                                    | given_names    |             |
|                      |                                                                                                                                    | full_name      |             |
|                      |                                                                                                                                    | affiliations   | country     |
|                      |                                                                                                                                    |                | institution |
| collections          | <a href="#parsing">parsing</a> <a href="#12">[12]</a>                                                                              |                |             |
| license              | <a href="#parsing">parsing</a> <a href="#11">[11]</a>                                                                              | url            |             |
|                      |                                                                                                                                    | license        |             |
| publication_info     | <a href="#generic_parsing">generic_parsing</a> : <a href="#40">[40]]</a>                                                           | journal_title  |             |
|                      |                                                                                                                                    | journal_volume |             |
|                      |                                                                                                                                    | year           |             |
| abstracts            | <a href="#enhancer">enhancer</a> : <a href="#46">[46]</a>                                                                          | value          |             |
| acquisition_source   | <a href="#enhancer">enhancer</a> : <a href="#49">[49]</a>                                                                          | source         |             |
|                      |                                                                                                                                    | method         |             |
|                      |                                                                                                                                    | date           |             |
| copyright            | <a href="#enhancer">enhancer</a> : <a href="#50">[50]</a>                                                                          | year           |             |
|                      |                                                                                                                                    | statement      |             |
| imprints             | <a href="#enhancer">enhancer</a> : <a href="#51">[51]</a>                                                                          | date           |             |
|                      |                                                                                                                                    | publisher      |             |
| record_creation_date | <a href="#enhancer">enhancer</a> : <a href="#50">[50]</a>                                                                          |                |             |
| titles               | <a href="#enhancer">enhancer</a> : <a href="#51">[51]</a>                                                                          | title          |             |
|                      |                                                                                                                                    | source         |             |
| $schema              | <a href="#enricher">enricher</a> : <a href="#66">[66]</a>                                                                          |                |             |

# [Enricher](#enricher)

|                                |               |                                                       |
| ------------------------------ | ------------- | ----------------------------------------------------- |
| Reference                      | Field         | Enricher                                              |
| <a id="66" href="#66">[66]</a> | schema        | <a href="#_get_schema">\_get_schema</a>               |
| <a id="67" href="#67">[67]</a> | arxiv_eprints | <a href="#_get_arxiv_eprints">\_get_arxiv_eprints</a> |

### [\_get_schema](#_get_schema)

| Reference | Subfield | Value                                                                            | Default value |
| --------- | -------- | -------------------------------------------------------------------------------- | ------------- |
|           |          | <code>os.getenv("REPO_URL", "http://repo.qa.scoap3.org/schemas/hep.json")</code> |               |

### [\_get_arxiv_eprints](#_get_arxiv_eprints)

| Reference                      | Subfield   | Processing                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------------ | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a id="68" href="#68">[68]</a> | categories | 1. Need to take arxiv id value from arxiv_eprints.value <br/> 2. Make a request to arxiv API: <code>f'https://export.arxiv.org/api/query?search_query=id:{arxiv_eprints.value}'</code>if:{ arxiv_eprints.value}' <br/> 3. From XML response, take the categories by path: arxiv:primary_category and rest of the categories by path: /w3:category. <br/>xml_namespaces = { "arxiv": "http://arxiv.org/schemas/atom", "w3": "http://www.w3.org/2005/Atom", } |
| <a id="69" href="#69">[69]</a> | value      | Cleans blank space                                                                                                                                                                                                                                                                                                                                                                                                                                          |

# [Enhancer](#enhancer)

| Reference                      | Field                | Enhancer                                                                           |
| ------------------------------ | -------------------- | ---------------------------------------------------------------------------------- |
| <a id="46" href="#46">[46]</a> | abstracts            | <a href="#__construct_abstracts">\_\_construct_abstracts</a>                       |
| <a id="47" href="#47">[47]</a> | acquisition_source   | <a href="#__construct_acquisition_source">\_\_construct_acquisition_source</a>     |
| <a id="48" href="#48">[48]</a> | copyright            | <a href="#__construct_copyright">\_\_construct_copyright</a>                       |
| <a id="49" href="#49">[49]</a> | imprints             | <a href="#__construct_imprints">\_\_construct_imprints</a>                         |
| <a id="50" href="#50">[50]</a> | record_creation_date | <a href="#__construct_record_creation_date">\_\_construct_record_creation_date</a> |
| <a id="51" href="#51">[51]</a> | titles               | <a href="#__construct_titles">\_\_construct_titles</a>                             |
| <a id="52" href="#52">[52]</a> |                      | <a href="#__remove_country">\_\_remove_country</a>                                 |

### [\_\_construct_abstracts](#__construct_abstracts)

| Reference                      | Subfield | Value                                                                                          |
| ------------------------------ | -------- | ---------------------------------------------------------------------------------------------- |
| <a id="53" href="#53">[53]</a> | value    | Take value from <a href="#generic_parsing">generic parsing</a> abstract <a href="#23">[23]</a> |
| <a id="54" href="#54">[54]</a> | source   | Constant: Hindawi                                                                              |

### [\_\_construct_acquisition_source](#__construct_acquisition_source)

| Reference                      | Subfield | Value                                            |
| ------------------------------ | -------- | ------------------------------------------------ |
| <a id="55" href="#55">[55]</a> | source   | Constant: Hindawi                                |
| <a id="56" href="#56">[56]</a> | method   | Constant: Hindawi                                |
| <a id="57" href="#57">[57]</a> | date     | <code>datetime.datetime.now().isoformat()</code> |

### [\_\_construct_copyright](#__construct_copyright)

| Reference                      | Subfield  | Value                                                                                   |
| ------------------------------ | --------- | --------------------------------------------------------------------------------------- |
| <a id="58" href="#58">[58]</a> | year      | Take value from <a href="#parsing">parsing</a> copyright_year <a href="#10">[10]</a>    |
| <a id="59" href="#59">[59]</a> | statement | Take value from <a href="#parsing">parsing</a> copyright_statement <a href="#9">[9]</a> |

### [\_\_construct_imprints](#__construct_imprints)

| Reference                      | Subfield  | Value                                                                                                |
| ------------------------------ | --------- | ---------------------------------------------------------------------------------------------------- |
| <a id="60" href="#60">[60]</a> | date      | Take value from <a href="#generic_parsing">generic_parsing</a> date_published <a href="#29">[29]</a> |
| <a id="61" href="#61">[61]</a> | publisher | constant: IOP                                                                                        |

### [\_\_construct_record_creation_date](#__construct_record_creation_date)

| Reference                      | Subfield | Value                                            |
| ------------------------------ | -------- | ------------------------------------------------ |
| <a id="62" href="#62">[62]</a> |          | <code>datetime.datetime.now().isoformat()</code> |

### [\_\_construct_titles](#__construct_titles)

| Reference                      | Subfield | Value                                                                                                |
| ------------------------------ | -------- | ---------------------------------------------------------------------------------------------------- |
| <a id="63" href="#63">[63]</a> | title    | removed fn tags. `FN_REGEX = re.compile(r"")`<br/> `FN_REGEX.sub("", item.pop("title", "")).strip()` |
| <a id="64" href="#64">[64]</a> | source   | constant: IOP                                                                                        |

### [\_\_remove_country](#__remove_country)

|                                |                                                                               |       |                                  |
| ------------------------------ | ----------------------------------------------------------------------------- | ----- | -------------------------------- |
| Reference                      | Field                                                                         | Value | Processing                       |
| <a id="65" href="#65">[65]</a> | from <a href="#parsing">parsed</a> affiliation <a href="#55">country [55]</a> |       | removes county if the value has: |

# [Generic parsing](#generic_parsing)

| Reference                      | Field                  | Subfield             | Processing                                                                                                                                   | Default value |
| ------------------------------ | ---------------------- | -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| <a href="#22" id="22">[22]</a> | authors                | surname, given_names | takes <a href="#2">authors [2]</a> and splits raw_name: if there is a comma, it means that the surname and given_name are in the second part |               |
| <a href="#23" id="23">[23]</a> | abstract               |                      | takes <a href="#3">abstract [3]</a> and cleans white space characters                                                                        |               |
| <a href="#24" id="24">[24]</a> | collaborations         |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#25" id="25">[25]</a> | title                  |                      | takes <a href="#4">title [4]</a> and cleans white space characters                                                                           |               |
| <a href="#26" id="26">[26]</a> | subtitle               |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#27" id="27">[27]</a> | journal_year           |                      |                                                                                                                                              |               |
| <a href="#28" id="28">[28]</a> | preprint_date          |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#29" id="29">[29]</a> | date_published         |                      | takes <a href="#5">date_published [5]</a> and forms it <code> f"{tmp_date.year:04d}-{tmp_date.month:02d}-{tmp_date.day:02d}"</code>          |               |
| <a href="#30" id="30">[30]</a> | related_article_doi    |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#31" id="31">[31]</a> | free_keywords          |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#32" id="32">[32]</a> | classification_numbers |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#33" id="33">[33]</a> | dois                   |                      | takes <a href="#1">dois</a>                                                                                                                  |               |
| <a href="#34" id="34">[34]</a> | thesis_supervisor      |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#35" id="35">[35]</a> | thesis                 |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#36" id="36">[36]</a> | urls                   |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#37" id="37">[37]</a> | local_files            |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#38" id="38">[38]</a> | record_creation_date   |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#39" id="39">[39]</a> | control_field          |                      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#40" id="40">[40]</a> | publication_info       |                      |                                                                                                                                              |               |
| <a href="#41" id="41">[41]</a> |                        | journal_title        | takes <a href="#16">journal title [16]</a>                                                                                                   |               |
| <a href="#42" id="42">[42]</a> |                        | journal_volume       | takes <a href="#17">journal volume [17]</a>                                                                                                  |               |
| <a href="#43" id="43">[43]</a> |                        | journal_year         | takes <a href="#18">journal year [18]</a>                                                                                                    |               |
| <a href="#44" id="44">[44]</a> |                        | journal_issue        | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |
| <a href="#45" id="45">[45]</a> |                        | journal_doctype      | NO SUCH A FIELD IN HINDAWI                                                                                                                   |               |

# [Parsing](#parsing)

| Reference                      | Field               | Source                                                                      | Parsing                                                     |
| ------------------------------ | ------------------- | --------------------------------------------------------------------------- | ----------------------------------------------------------- |
| <a href="#1" id="1">[1]</a>    | dois                | ns0:metadata/ns1:record/ns0:datafield/[@tag='024']/ns0:subfield/[@code='a'] | <code>lambda x: [x]</code>                                  |
| <a href="#2" id="2">[2]</a>    | authors             |                                                                             | <a href="#authors_parsing">authors_parsing</a>              |
| <a href="#3" id="3">[3]</a>    | abstract            | ns0:metadata/ns1:record/ns0:datafield/[@tag='520']/ns0:subfield/[@code='a'] | <code>lambda x: " ".join(x.split())</code>                  |
| <a href="#4" id="4">[4]</a>    | title               | ns0:metadata/ns1:record/ns0:datafield/[@tag='245']/ns0:subfield/[@code='a'] | <code>lambda x: x</code>                                    |
| <a href="#5" id="5">[5]</a>    | date_published      | ns0:metadata/ns1:record/ns0:datafield/[@tag='260']/ns0:subfield/[@code='c'] | <code>lambda x: x</code>                                    |
| <a href="#6" id="6">[6]</a>    | page_nr             | ns0:metadata/ns1:record/ns0:datafield/[@tag='300']/ns0:subfield/[@code='a'] | <code>lambda x: [int(x)]</code>                             |
| <a href="#7" id="7">[7]</a>    | publication_info    |                                                                             | <a href="#_get_publication_info">\_get_publication_info</a> |
| <a href="#8" id="8">[8]</a>    | arxiv_eprints       |                                                                             | <a href="#_get_arxiv">\_get_arxiv</a>                       |
| <a href="#9" id="9">[9]</a>    | copyright_statement | ns0:metadata/ns1:record/ns0:datafield/[@tag='542']/ns0:subfield/[@code='f'] |                                                             |
| <a href="#10" id="10">[10]</a> | copyright_year      | ns0:metadata/ns1:record/ns0:datafield/[@tag='542']/ns0:subfield/            | <code> re.search(r"[0-9]{4}", value).group(0)</code>        |
| <a href="#11" id="11">[11]</a> | license             |                                                                             | <a href="#_get_license">\_get_license</a>                   |
| <a href="#12" id="12">[12]</a> | collections         |                                                                             | constant: "Advances in High Energy Physics"                 |

### [authors_parsing](#authors_parsing)

| Reference                      | Field        | Source                                          | Parsing                                             |
| ------------------------------ | ------------ | ----------------------------------------------- | --------------------------------------------------- |
| <a href="#13" id="13">[13]</a> | raw_name     | ns0:subfield[@code='a']                         | <code>lambda x: [x]</code>                          |
| <a href="#14" id="14">[14]</a> | affiliations |                                                 | <a href="#_get_affiliations">\_get_affiliations</a> |
| <a href="#15" id="15">[15]</a> | orcid        | ns0:subfield[@code='a']/ns0:subfield[@code='j'] | <code>lambda x: " ".join(x.split())</code>          |

### [\_get_publication_info](#_get_publication_info)

| Reference                      | Field          | Source                                                                      | Parsing |
| ------------------------------ | -------------- | --------------------------------------------------------------------------- | ------- |
| <a href="#16" id="16">[16]</a> | journal_title  | ns0:metadata/ns1:record/ns0:datafield/[@tag='773']/ns0:subfield/[@code='p'] |         |
| <a href="#17" id="17">[17]</a> | journal_volume | ns0:metadata/ns1:record/ns0:datafield/[@tag='773']/ns0:subfield/[@code='v'] |         |
| <a href="#18" id="18">[18]</a> | journal_year   | ns0:metadata/ns1:record/ns0:datafield/[@tag='773']/ns0:subfield/[@code='y'] |         |

### [\_get_arxiv](#_get_arxiv)

| Reference                      | Field | Source                                                                                                                                                                                                                 | Parsing                                          |
| ------------------------------ | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <a href="#19" id="19">[19]</a> | value | "ns0:metadata/ns1:record/ns0:datafield/[@tag='037']/ns0:subfield/[@code='a']" <br/> if the field above == 'arxiv' <br/> field above: <br/> ns0:metadata/ns1:record/ns0:datafield/[@tag='037']/ns0:subfield/[@code='9'] | Removing "arxiv" from value, leaving just digits |

### [\_get_license](#_get_arxiv)

| Reference                      | Field   | Source                                                                                      | Parsing                                                                                                                                                                                                                    |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <a href="#20" id="20">[20]</a> | url     | License urls: "ns0:metadata/ns1:record/ns0:datafield/[@tag='540']/ns0:subfield/[@code='u']" |                                                                                                                                                                                                                            |
| <a href="#21" id="21">[21]</a> | license | license text = ns0:metadata/ns1:record/ns0:datafield/[@tag='540']/ns0:subfield/[@code='a']  | <code>url_parts = license_url.text.split("/")<br/> clean_url_parts = list(filter(bool, url_parts))<br/> version = clean_url_parts.pop()<br/>license_type = clean_url_parts.pop()<br/>f"CC-{license_type}-{version}"</code> |

### [\_get_affiliations](#_get_affiliations)

| Reference                      | Field        | Source                                                                                                                                                                     | Parsing                                                               |
| ------------------------------ | ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| <a href="#53" id="53">[53]</a> | value        | ns0:metadata/ns1:record/ns0:datafield/[@tag='100']/ns0:subfield[@code='u'] <br/> ns0:metadata/ns1:record/ns0:datafield/[@tag='700']/ns0:subfield[@code='u']                |                                                                       |
| <a href="#54" id="54">[54]</a> | organization | same as value: ns0:metadata/ns1:record/ns0:datafield/[@tag='100']/ns0:subfield[@code='u'] <br/> ns0:metadata/ns1:record/ns0:datafield/[@tag='700']/ns0:subfield[@code='u'] | takes the string before the last comma                                |
| <a href="#55" id="55">[55]</a> | country      | same as value: ns0:metadata/ns1:record/ns0:datafield/[@tag='100']/ns0:subfield[@code='u'] <br/> ns0:metadata/ns1:record/ns0:datafield/[@tag='700']/ns0:subfield[@code='u'] | takes the last string after comma, which starts with a capital letter |
