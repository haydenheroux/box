#!/usr/bin/python3
from typing import List, NamedTuple, Optional

def get_lines(filename: str) -> List[str]:
    lines = list()
    with open(filename, "r") as file:
        for line in file:
            lines.append(line)
    return lines

class Doc(NamedTuple):
    description: Optional[List[str]]
    name: Optional[str]
    parameters: Optional[List[str]]
    return_type: Optional[str]


def fmt_doc(doc: Doc) -> str:
    return f"{doc.return_type} {doc.name} {doc.description} {doc.parameters}"

def parse_doc(doc: List[str]) -> Doc:
    description = None
    name = None
    parameters = None
    return_type = None

    definition = None

    for index, line in enumerate(doc):
        at_end_of_description = not line.startswith("//")
        if at_end_of_description:
            description = doc[:index]
            definition = doc[index:]
            break

    if description is None:
        return Doc(description=description, name=name, parameters=parameters, return_type=return_type)

    if definition is None:
        return Doc(description=description, name=name, parameters=parameters, return_type=return_type)

    description = [description_line.replace("//", "").strip() for description_line in description]

    return_type_line = definition[0]
    return_type_is_struct = "struct" in return_type_line

    if return_type_is_struct:
        return_type = "struct"
        final_line = definition[-1]
        name = final_line.split(' ')[-1].replace(';', '')
        parameters = [parameter.replace(';', '') for parameter in definition[1:-1]]
    else:
        return_type = return_type_line
        signature = ''.join(definition[1:])
        name_index = signature.find('(')
        name = signature[:name_index]
        parameters = signature[name_index:][1:-1].split(", ")
    return Doc(description=description, name=name, parameters=parameters, return_type=return_type)


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
    for doc in get_docs(lines):
        print(fmt_doc(parse_doc(doc)))
