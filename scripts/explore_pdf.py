"""Print what pdfplumber extracts from a PDF. For local exploration only."""

import sys

import pdfplumber


def main() -> None:
    path = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else None

    with pdfplumber.open(path, password=password) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for table in page.extract_tables():
                if not table or len(table[0]) != 7:
                    continue
                first, last = table[0], table[-1]
                print(
                    f"page {page_number}: {len(table)} rows | "
                    f"first: {first[0]!r} {first[5]} | "
                    f"last: {last[0]!r} {last[5]}"
                )


if __name__ == "__main__":
    main()
