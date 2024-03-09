def generate_bibtex_citation(pandas):
    bibtex_entry = """
@Manual{,
    title = {Nome do Pacote: Uma breve descrição},
    author = {Nome do Autor},
    year = {Ano},
    note = {Versão do pacote},
    url = {URL do pacote}
}
"""
    return bibtex_entry

# Imprimir a entrada BibTeX
print(generate_bibtex_citation())
