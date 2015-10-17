import csv

def parse_authors(f):
    authors = []
    with open(f, "r") as af:
        author_parser = csv.reader(af)
        for row in author_parser:
            institution = row[0]
            last_name = row[4]
            initials = row[5]
            authors.append((institution, last_name, initials))

    return authors

def main():
    author_file = "data/Staff.csv"
    authors = parse_authors(author_file)
    for (uni, sn, i) in authors:
        print uni, sn, i

if __name__ == "__main__":
    main()