"""从 Crossref 取得已人工核实论文的结构化书目，保留核查快照。"""
import json
import pathlib
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOIS = [
    "10.26599/TST.2019.9010074",
    "10.26599/TST.2019.9010075",
    "10.26599/TST.2018.9010107",
    "10.1016/j.cpc.2016.07.010",
    "10.1016/j.future.2017.03.019",
    "10.1016/j.future.2016.01.021",
    "10.1109/TST.2015.7128935",
]

def main():
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({
        "https": "http://127.0.0.1:7892"
    }))
    records = []
    for doi in DOIS:
        request = urllib.request.Request(
            "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/"),
            headers={"User-Agent": "USTB-Lab-Local-Research/1.0"},
        )
        with opener.open(request, timeout=40) as response:
            item = json.load(response)["message"]
        records.append({key: item.get(key) for key in [
            "DOI", "title", "author", "container-title", "published", "published-print",
            "published-online", "volume", "issue", "page", "URL"
        ]})
        print(doi)
    output = ROOT / "docs" / "crossref-verified.json"
    output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
