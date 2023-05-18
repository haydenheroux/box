#!/usr/bin/python3
from typing import List, NamedTuple

def get_lines(filename: str) -> List[str]:
    lines = list()
    with open(filename, "r") as file:
        for line in file:
            lines.append(line)
    return lines

class Doc(NamedTuple):
    name: str
    return_type: str
    parameters: List[str]
    documentation: str


def fmt_doc(doc: Doc) -> str:
    return f"{doc.return_type} {doc.name} {doc.documentation} {'_'.join(doc.parameters)}"

def parse_chunk(chunk: List[str]) -> Doc:
    for index, line in enumerate(chunk):
        if not line.startswith("//"):
            info = ''.join(chunk[:index]).replace("// ", "")
            if "struct" in line:
                name = docs[-1][2:-1]
                parameters = [x.replace(";", ", ") for x in chunk[index+1:-2]]
                return Doc(name, "struct", parameters, info)
            else:
                signature = ''.join(chunk[index+1:])
                delim = signature.find('(')
                name = signature[:delim]
                parameters = signature[delim+1:-1].split(',')
                return Doc(name, line, parameters, info)
    return Doc("", "", list(), "")


if __name__ == "__main__":
    lines = get_lines("box.c")
    in_doc = False
    start_docs = list()
    end_docs = list()
    for i in range(len(lines)):
        if lines[i].startswith("//"):
            start_docs.append(i)
            in_doc = True
        if (lines[i].startswith("{") or lines[i].startswith("\n")) and in_doc:
            end_docs.append(i)
            in_doc = False

    if len(start_docs) != len(end_docs):
        print("fail")

    for i in range(len(start_docs)):
        docs = [x.strip() for x in lines[start_docs[i]:end_docs[i]]]
        print(fmt_doc(parse_chunk(docs)))
