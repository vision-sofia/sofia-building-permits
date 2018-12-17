import requests
import json
import csv
import os.path

saved_fields = [
    "Number", "Hash", "DocumentTypeName", "Status", "TakeEffect", "Issuer",
    "Employer", "Object", "Region", "Terrain", "RegulationNeighbourhood",
    "Upi", "Identifier", "Address", "Polygon"
]

deleted_fields = [
    "TakeEffectFilter"
]

permits = {}
permits_csv = "permits.csv"

if os.path.isfile(permits_csv):
    with open(permits_csv, "r") as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=saved_fields)
        for row in reader:
            permits[row["Hash"]] = row

output_file = open(permits_csv, "a")
writer = csv.DictWriter(output_file, fieldnames=saved_fields)
if len(permits) == 0:
    writer.writeheader()

def get_polygon(permit_hash):
    resp = requests.get("https://www.sofia-agk.com/Map/GetObjectGeometryByIdAndType/?url=%s&type=7&group=4" % permit_hash)
    if resp.status_code == 200:
        print("polygon obtain for permit %s", permit_hash)
        return resp.content.decode("utf-8")
    else:
        print("failed to obtain polygon for permit %s", permit_hash)
        return ""

for i in range(1, 1000):
    with open("resp-%d.json" % i, "r") as f:
        file_contents = json.load(f)

        for item in file_contents["Data"]:
            if item["Hash"] in permits:
                continue
                
            for f in deleted_fields:
                del item[f]

            item["TakeEffect"] = item["TakeEffect"]["DateTime"]
            item["Polygon"] = get_polygon(item["Hash"])
        
            writer.writerow(item)

