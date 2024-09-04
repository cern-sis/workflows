
![elsevier_dags_process](./Elsevier_doc_diagram.png)

# Practical information
Parsing Elsevier content involves a unique two-phase process, distinct from other publishers.

Phase 1: The initial phase involves parsing the dataset.xml file, which contains all the records and some mandatory fields. This file serves as the foundation for gathering essential data across the dataset.

Phase 2: In the second phase, the main.xml file is parsed for each individual record. The paths to the main.xml file, as well as any associated PDF and PDF/A files, are provided in the dataset.xml file parsed during Phase 1. This ensures that all necessary files and data are correctly linked and processed.

# [Final fields](#final_fields)

| Field                | Processed                                                                                                                          | Subfield       | Subsubfield |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------- | ----------- |
| dois                 | <a href="#generic_parsing">generic_parsing</a> : <a href="#45">[45]</a>                                                            | value          |             |
| arxiv_eprints        | <a href="#enricher">enricher</a> : <a href="#62">[62]</a>                                                                          | value          |             |
|                      |                                                                                                                                    | categories     |             |
| page_nr              | <a href="#parsing">parsing</a> : <a href="#36">[36]</a>                                                                            |                |             |
| authors              | <a href="#parsing">parsing</a> : <a href="#37">[37]</a> <br/><a href="#generic_parsing">generic_parsing</a> : <a href="#33">[33]</a> | surname        |             |
|                      |                                                                                                                                    | given_names    |             |
|                      |                                                                                                                                    | full_name      |             |
|                      |                                                                                                                                    | affiliations   | country     |
|                      |                                                                                                                                    |                | institution |
| collaborations       | <a href="#generic_parsing">generic_parsing</a> : <a href="#35">[35]</a>                                                            | value          |             |
| license              | <a href="#parsing">parsing</a> : <a href="#38">[38]</a>                                                                            | url            |             |
|                      |                                                                                                                                    | license        |             |
| publication_info     | <a href="#generic_parsing">generic_parsing</a> : <a href="#52">[52]</a>                                                            | journal_title  |             |
|                      |                                                                                                                                    | journal_volume |             |
|                      |                                                                                                                                    | year           |             |
|                      |                                                                                                                                    | artid          |             |
|                      |                                                                                                                                    | material       |             |
| abstracts            | <a href="#enhancer">enhancer</a> : <a href="#53">[53]</a>                                                                          | value          |             |
| acquisition_source   | <a href="#enhancer">enhancer</a> : <a href="#54">[54]</a>                                                                          | source         |             |
|                      |                                                                                                                                    | method         |             |
|                      |                                                                                                                                    | date           |             |
| copyright            | <a href="#enhancer">enhancer</a> : <a href="#55">[55]</a>                                                                          | year           |             |
|                      |                                                                                                                                    | statement      |             |
| imprints             | <a href="#enhancer">enhancer</a> : <a href="#56">[56]</a>                                                                          | date           |             |
|                      |                                                                                                                                    | publisher      |             |
| record_creation_date | <a href="#enhancer">enhancer</a> : <a href="#57">[57]</a>                                                                          |                |             |
| titles               | <a href="#enhancer">enhancer</a> : <a href="#58">[58]</a>                                                                          | title          |             |
|                      |                                                                                                                                    | source         |             |
| $schema              | <a href="#enricher">enricher</a> : <a href="#60">[60]</a>                                                                          |                |             |                                                                         |                |             |



# [Enhancer](#enhancer)

| Reference                      | Field                | Enhancer                                                                           |
| ------------------------------ | -------------------- | ---------------------------------------------------------------------------------- |
| <a id="53" href="#53">[53]</a> | abstracts            | <a href="#__construct_abstracts">\_\_construct_abstracts</a>                       |
| <a id="54" href="#54">[54]</a> | acquisition_source   | <a href="#__construct_acquisition_source">\_\_construct_acquisition_source</a>     |
| <a id="55" href="#55">[55]</a> | copyright            | <a href="#__construct_copyright">\_\_construct_copyright</a>                       |
| <a id="56" href="#56">[56]</a> | imprints             | <a href="#__construct_imprints">\_\_construct_imprints</a>                         |
| <a id="57" href="#57">[57]</a> | record_creation_date | <a href="#__construct_record_creation_date">\_\_construct_record_creation_date</a> |
| <a id="58" href="#58">[58]</a> | titles               | <a href="#__construct_titles">\_\_construct_titles</a>                             |
| <a id="59" href="#59">[59]</a> |                      | <a href="#__remove_country">\_\_remove_country</a>                                 |

### [\_\_construct_abstracts](#__construct_abstracts)

| Reference                      | Subfield | Value                                                                          |
| ------------------------------ | -------- | ------------------------------------------------------------------------------ |
| <a id="60" href="#60">[60]</a> | value    | Take value from <a href="#parsing">parsing</a> abstract <a href="#2">[2]</a>   |
| <a id="61" href="#61">[61]</a> | source   | Constant: Elsevier                                                             |

### [\_\_construct_acquisition_source](#__construct_acquisition_source)

| Reference                      | Subfield | Value                                            |
| ------------------------------ | -------- | ------------------------------------------------ |
| <a id="62" href="#62">[62]</a> | source   | Constant: Elsevier                               |
| <a id="63" href="#63">[63]</a> | method   | Constant: Elsevier                               |
| <a id="64" href="#64">[64]</a> | date     | <code>datetime.datetime.now().isoformat()</code> |

### [\_\_construct_copyright](#__construct_copyright)

| Reference                      | Subfield  | Value                                                                                     |
| ------------------------------ | --------- | ----------------------------------------------------------------------------------------- |
| <a id="65" href="#65">[65]</a> | year      | Take value from <a href="#parsing">parsing</a> copyright_year <a href="#7">[7]</a>        |
| <a id="66" href="#66">[66]</a> | statement | Take value from <a href="#parsing">parsing</a> copyright_statement <a href="#8">[8]</a>   |

### [\_\_construct_imprints](#__construct_imprints)

| Reference                      | Subfield  | Value                                                                                                |
| ------------------------------ | --------- | ---------------------------------------------------------------------------------------------------- |
| <a id="67" href="#67">[67]</a> | date      | Take value from <a href="#generic_parsing">generic_parsing</a> date_published <a href="#41">[41]</a> |
| <a id="68" href="#68">[68]</a> | publisher | Constant: Elsevier                                                                                   |

### [\_\_construct_record_creation_date](#__construct_record_creation_date)

| Reference                      | Subfield | Value                                            |
| ------------------------------ | -------- | ------------------------------------------------ |
| <a id="69" href="#69">[69]</a> |          | <code>datetime.datetime.now().isoformat()</code> |

### [\_\_construct_titles](#__construct_titles)

| Reference                      | Subfield | Value                                                                                                |
| ------------------------------ | -------- | ---------------------------------------------------------------------------------------------------- |
| <a id="70" href="#70">[70]</a> | title    | Removed fn tags. `FN_REGEX = re.compile(r"")`<br/> `FN_REGEX.sub("", item.pop("title", "")).strip()` |
| <a id="71" href="#71">[71]</a> | source   | Constant: Elsevier                                                                                   |

### [\_\_remove_country](#__remove_country)

| Reference                      | Field                                                                                    | Value | Processing                                   |
| ------------------------------ | ---------------------------------------------------------------------------------------- | ----- | -------------------------------------------- |
| <a id="72" href="#72">[72]</a> | From <a href="#parsing">parsed</a> JSON value: affiliations <a href="#17">[17]</a>.country |       | From parsed JSON value: affiliations.country |


# [generic_parsing](#generic_parsing)

| Reference                      | Field                  | Subfield  | Processing                                                                                                                                                                      | Default value |
| ------------------------------ | ---------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- |
| <a id="33" href="#33">[33]</a> | authors                | full_name | Joins <a href="#parsing">parsed</a> surname <a href="#10">[10]</a> and <a href="#parsing">parsed</a> given_names <a href="#11">[11]</a>: "{0}, {1}".format(surname, given_names) |               |
| <a id="34" href="#34">[34]</a> | abstract               |           | Cleans blank space characters                                                                                                                                                   |               |
| <a id="35" href="#35">[35]</a> | collaborations         | value     | Puts the collaboration value into the array of dicts: <code>[{"value": collaboration}]</code>                                                                                   |               |
| <a id="36" href="#36">[36]</a> | collections            | primary   | Puts the collections value into the array of dicts: <code>[{"value": collections}]</code>                                                                                       |               |
| <a id="37" href="#37">[37]</a> | title                  |           | Cleans blank space characters                                                                                                                                                   |               |
| <a id="38" href="#38">[38]</a> | subtitle               |           | Cleans blank space characters, takes the first value. PS. HAVE NEVER SEEN IT                                                                                                    |               |
| <a id="39" href="#39">[39]</a> | journal_year           |           | Takes <a href="#parsing">parsed</a> journal_year <a href="#22">[22]</a>                                                                                                         |               |
| <a id="40" href="#40">[40]</a> | preprint_date          |           | NO SUCH FIELD IN ELSEVIER                                                                                                                                                       |               |
| <a id="41" href="#41">[41]</a> | date_published         |           | Takes <a href="#parsing">parsed</a> date_published <a href="#21">[21]</a>                                                                                                       |               |
| <a id="42" href="#42">[42]</a> | related_article_doi    |           | Puts the related_article_doi value into the array of dicts: <code>[{"value": related_article_doi}]</code>. PS. HAVE NEVER SEEN IT                                               |               |
| <a id="43" href="#43">[43]</a> | free_keywords          |           | Cleans blank space characters. ELSEVIER DOESN'T HAVE THIS FIELD                                                                                                                 |               |
| <a id="44" href="#44">[44]</a> | classification_numbers |           | NO SUCH FIELD IN ELSEVIER                                                                                                                                                       |               |
| <a id="45" href="#45">[45]</a> | dois                   |           | Puts the doi value into the array of dicts: <code>[{"value": doi}]</code>                                                                                                       |               |
| <a id="46" href="#46">[46]</a> | thesis_supervisor      |           | NO SUCH FIELD IN ELSEVIER!!! Should take parsed thesis_supervisor and parse with generic parser in the same way as authors <a href="#33">[33]</a>                               |               |
| <a id="47" href="#47">[47]</a> | thesis                 |           | NO SUCH FIELD IN ELSEVIER!!! Should take parsed thesis value.                                                                                                                   |               |
| <a id="48" href="#48">[48]</a> | urls                   |           | NO SUCH FIELD IN ELSEVIER!!! Should take parsed urls value.                                                                                                                     |               |
| <a id="49" href="#49">[49]</a> | local_files            |           | NO SUCH FIELD IN ELSEVIER!!! Should take parsed local_files value.                                                                                                              |               |
| <a id="50" href="#50">[50]</a> | record_creation_date   |           | NO SUCH FIELD IN ELSEVIER!!! Should take parsed record_creation_date value.                                                                                                     |               |
| <a id="51" href="#51">[51]</a> | control_field          |           | NO SUCH FIELD IN ELSEVIER!!! Should take parsed control_field value.                                                                                                            |               |
| <a id="52" href="#52">[52]</a> | publication_info       |           | <a href="#_generic_parsing_publication_info">\_generic_parsing_publication_info</a>                                                                                             |               |
|                                | journal_title          |           | REMOVED                                                                                                                                                                         |
|                                | journal_volume         |           | REMOVED                                                                                                                                                                         |
|                                | journal_year           |           | REMOVED                                                                                                                                                                         |
|                                | journal_issue          |           | REMOVED                                                                                                                                                                         |
|                                | journal_doctype        |           | REMOVED                                                                                                                                                                         |

### [\_generic_parsing_publication_info](#_generic_parsing_publication_info)

| Reference                      | Subfield         | Value                                                                     | Default value |
| ------------------------------ | ---------------- | ------------------------------------------------------------------------- | ------------- |
| <a id="27" href="#27">[27]</a> | journal_title    | Takes <a href="#parsing">parsed</a> journal_title <a href="#19">[19]</a>  | ""            |
| <a id="28" href="#28">[28]</a> | journal_volume   | Takes <a href="#parsing">parsed</a> journal_volume <a href="#26">[26]</a> | ""            |
| <a id="29" href="#29">[29]</a> | year             | Takes <a href="#parsing">parsed</a> journal_year <a href="#22">[22]</a>   | ""            |
| <a id="30" href="#30">[30]</a> | artid            | Takes <a href="#parsing">parsed</a> journal_artid <a href="#20">[20]</a>  | ""            |
| <a id="31" href="#31">[31]</a> | material         | NO SUCH FIELD IN ELSEVIER                                                 | ""            |
| <a id="32" href="#32">[32]</a> | pubinfo_freetext | NO SUCH FIELD IN ELSEVIER                                                 | ""            |


# [metadata parsing](#metadataparsing)
Parses data.xml file

| Reference | Field          | Method | Source                                                                                                                                                   | Parsing                                                                                                                                                                                                                                                                           |
|-----------|----------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href="#18">[18]</a>      | dois           | find   | journal-item-unique-ids/doi                                                                                                                              | [dois]                                                                                                                                                                                                                                                                            |
| <a href="#19">[19]</a>      | journal_title  | find   | journal-item-unique-ids/jid-aid/jid                                                                                                                     |                                                                                                                                                                                                                                                                                   |
| <a href="#20">[20]</a>      | journal_artid  | find   | journal-item-unique-ids/jid-aid/aid                                                                                                                      |                                                                                                                                                                                                                                                                                   |
| <a href="#21">[21]</a>      | date_published | find   | journal-item-properties/online-publication-date                                                                                                          |                                                                                                                                                                                                                                                                                   |
| <a href="#22">[22]</a>      | journal_year   |        |                                                                                                                                                          | get year from <a href="#21">date_published</a>                                                                                                                                                                                                                                    |
| <a href="#23">[23]</a>      | collections    |        |                                                                                                                                                          | same as <a href="#19">journal_title</a>                                                                                                                                                                                                                                           |
| <a href="#24">[24]</a>      | license        |        |                                                                                                                                                          | const: CC-BY-3.0                                                                                                                                                                                                                                                                  |
| <a href="#25">[25]</a>      | files          |        | FOR PDF: files-info/web-pdf/pathname                                                                                                                     | `{           "pdf": pdf_file_path,            "pdfa": os.path.join(os.path.split(pdf_file_path)[0], "main_a-2b.pdf"),            "xml": os.path.join(                files_dir_base, article.find("files-info/ml/pathname").text<br>            ),        }` |
| <a href="#26">[26]</a>      | journal_volume | find   | vol_first=journal-issue/journal-issue-properties/volume-issue-number/vol-first \n suppl=journal-issue/journal-issue-properties/volume-issue-number/suppl | `f"{vol_first} {suppl}"`                                                                                                                                                                                                                                                            |


# [parsing](#parsing)

| Reference | Field               | Required | Method | Source                                 | Parsing                                                                  |
|-----------|---------------------|----------|--------|----------------------------------------|--------------------------------------------------------------------------|
| <a href="#1">[1]</a>       | dois                | True     | find   | item-info/doi                          | doi value is pushed to the array: [doi]                                  |
| <a href="#2">[2]</a>       | abstract            | True     | find   | head/abstract/abstract-sec/simple-para |                                                                          |
| <a href="#3">[3]</a>       | title               | True     | find   | head/title                             |                                                                          |
| <a href="#4">[4]</a>       | authors             | True     | find   |                                        | <a href="#_get_authors">_get_authors</a>                                 |
| <a href="#5">[5]</a>       | collaboration       | False    | find   | author-group/collaboration/text/       |                                                                          |
| <a href="#6">[6]</a>       | copyright_holder    | True     | find   | item-info/copyright                    |                                                                          |
| <a href="#7">[7]</a>       | copyright_year      | False    | find   | item-info/copyrigh                     | get attribute value "year"                                               |
| <a href="#8">[8]</a>       | copyright_statement | True     | find   | item-info/copyright                    |                                                                          |
| <a href="#9">[9]</a>       | journal_doctype     | False    | find   | .                                      | get attribute value of "docsubctype" and map it with article_type_mapping |

### [_get_authors](#_get_authors)

| Reference | Field | Method | Source                                       | Processing                         |
|-----------|-------|--------|----------------------------------------------|------------------------------------|
|           |       | find   | head/author-group                            | used to parse <a href="#_get_authors_details">_get_authors_details</a> |
|           |       | find   | head/author-group/collaboration/author-group | used to parse <a href="#_get_authors_details">_get_authors_details</a> |


### [_get_authors_details](#_get_authors_details)
| Reference | Field        | Method                   | Source     | Processing        |
|-----------|--------------|--------------------------|------------|-------------------|
| <a href="#10">[10]</a>      | surname      | iterated findall results | surname    |                   |
| <a href="#11">[11]</a>      | given_names  | iterated findall results | given-name |                   |
| <a href="#12">[12]</a>      | affiliations | iterated findall results |            | <a href="#_get_affiliations">_get_affiliations</a> |
| <a href="#13">[13]</a>      | email        | iterated findall results | e-address  |                   |
| <a href="#14">[14]</a>      | orcid        | iterated findall results | orcid      |                   |


### [_get_affiliations](#_get_affiliations)
| Reference              | Field        | Method | Source                                                                                                               | Processing                                  |
|------------------------|--------------|--------|----------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| additional information | ref_id_value | find   | affiliation/[@id='{ref_id}'], and ref_if comes from `[cross.get("refid") for cross in author.findall("cross-ref")]`  | THIS FIELD IS NOT PRESENT IN THE FINAL JSON |
| <a href="#15">[15]</a>                   | value        | find   | {ref_id_value}textfn                                                                                                 |                                             |
| <a href="#16">[16]</a>                   | organization | find   | {ref_id_value}affiliation/organization                                                                               |                                             |
| <a href="#17">[17]</a>                   | country      | find   | {ref_id_value}affiliation/country                                                                                    |                            |


