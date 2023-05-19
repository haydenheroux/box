#!/usr/bin/python3

from typing import List, NamedTuple, Optional

"""
Documents a source code object.
"""
class Doc(NamedTuple):
    description: Optional[List[str]]
    name: Optional[str]
    parameters: Optional[List[str]]
    return_type: Optional[str]


"""
Gets each line in the file located at filename.
"""
def get_lines(filename: str) -> List[str]:
    lines = list()
    with open(filename, "r") as file:
        for line in file:
            lines.append(line)
    return lines


"""
Formats a documentation object into a string.
"""
def fmt_doc(doc: Doc) -> str:
    lines = list()
    lines.append(f"## {doc.return_type} {doc.name}")
    lines.append("")
    if doc.description:
        lines.extend(doc.description)
    if doc.parameters:
        lines.append("")
        lines.append("Parameters:")
        lines.extend([f" - `{parameter}`" for parameter in doc.parameters])
    lines.append("\n")
    return '\n'.join(lines)


"""
Finds the index of the first definition line.
"""
def find_definition_start(doc: List[str]) -> int:
    for index, line in enumerate(doc):
        if not line.startswith("//"):
            return index
    return 0

"""
Parses lines of a documentation string into a documentation object.
"""
def parse_doc(doc: List[str]) -> Doc:
    name = None
    parameters = None
    return_type = None

    # Separate each part of the documentation
    definition_start = find_definition_start(doc)
    description = doc[:definition_start]
    definition = doc[definition_start:]

    # Transform each line of the description
    description = [description_line.replace("//", "").strip() for description_line in description]

    return_type = definition[0]

    if "struct" in return_type:
        return_type = "struct"
        # Last word of the last line, after deleting semicolon
        name = definition[-1].split(' ')[-1].replace(';', '')
        # Each line of the middle part of the definition, after deleting semicolon
        parameters = [parameter.replace(';', '') for parameter in definition[1:-1]]
    else:
        # Create a string from each line in the signature 
        signature = ''.join(definition[1:])
        # Split the signature into name and parameter parts
        name_index = signature.find('(')
        # Name part precedes the parameters
        name = signature[:name_index]
        # Individually format each parameter
        parameters = [paramter.strip() for paramter in signature[name_index:][1:-1].split(',')]
    return Doc(description=description, name=name, parameters=parameters, return_type=return_type)


"""
Gets the documentation strings in the lines of a file.
"""
def get_docs(lines: List[str]) -> List[List[str]]:
    in_doc = False
    start_indexes = list()
    end_indexes = list()

    for index, line in enumerate(lines):
        at_start_of_doc = line.startswith("//")
        at_end_of_doc = line.startswith("{") or len(line.strip()) == 0
        if in_doc and at_end_of_doc:
            end_indexes.append(index)
            in_doc = False
        elif not in_doc and at_start_of_doc:
            start_indexes.append(index)
            in_doc = True

    docs = list()

    indexes = zip(start_indexes, end_indexes)
    for start_index, end_index in indexes:
        docs.append([line.strip() for line in lines[start_index:end_index]])

    return docs


if __name__ == "__main__":
    lines = get_lines("box.c")
    doc_lines = [fmt_doc(parse_doc(doc)) for doc in get_docs(lines)]
    with open("README.md", "w") as file:
        file.write('\n'.join(doc_lines))

