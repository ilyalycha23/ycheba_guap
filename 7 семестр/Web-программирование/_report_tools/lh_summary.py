import glob
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
d = r"D:\ycheba_guap\7 семестр\Web-программирование\lab4\report_assets\lighthouse"
res = {}
for f in sorted(glob.glob(os.path.join(d, "*.report.json"))):
    j = json.load(open(f, encoding="utf-8"))
    c = j["categories"]
    a = j["audits"]
    name = os.path.basename(f).split(".")[0]
    row = {k: round(c[k]["score"] * 100) for k in ("performance", "accessibility", "best-practices", "seo")}
    row.update(
        LCP=round(a["largest-contentful-paint"]["numericValue"]),
        TBT=round(a["total-blocking-time"]["numericValue"]),
        CLS=round(a["cumulative-layout-shift"]["numericValue"], 3),
    )
    row["failed"] = [
        k
        for k, v in a.items()
        if v.get("score") is not None
        and v["score"] < 0.9
        and v.get("scoreDisplayMode") in ("binary", "numeric", "metricSavings")
    ]
    row["ua"] = j["environment"]["hostUserAgent"]
    row["form"] = j["configSettings"]["formFactor"]
    row["throttling"] = j["configSettings"]["throttlingMethod"]
    row["time"] = j["fetchTime"]
    row["lh"] = j["lighthouseVersion"]
    res[name] = row
    print(name, {k: v for k, v in row.items() if k != "ua"})
json.dump(res, open(os.path.join(d, "summary.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
