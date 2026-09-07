import sqlite3, re, os, io

BASE = os.path.dirname(__file__)
con = sqlite3.connect(os.path.join(BASE, "..", "db", "northwind.db"))
con.text_factory = lambda b: b.decode("utf-8", errors="replace")
cur = con.cursor()

sql = open(os.path.join(BASE, "queries.sql"), encoding="utf-8").read()
chunks = re.split(r"\n(?=-- \d+\. )", sql)
chunks = [c.strip() for c in chunks if re.match(r"^-- \d+\. ", c.strip())]

out = io.open(os.path.join(BASE, "..", "results", "sample_output.txt"), "w", encoding="utf-8")

for chunk in chunks:
    header = chunk.splitlines()[0].lstrip("- ").strip()
    query = chunk
    try:
        cur.execute(query)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchmany(6)
        out.write(f"\n=== {header} ===\n")
        out.write(" | ".join(cols) + "\n")
        for r in rows:
            out.write(" | ".join(str(x) for x in r) + "\n")
    except Exception as e:
        out.write(f"\n=== {header} ===\n")
        out.write(f"ERROR: {e}\n")

out.close()
print("done")
