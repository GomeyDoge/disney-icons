import requests

def get_set_ids() -> list[str]:
    sets = []
    r = requests.get("https://disney.content.edge.bamgrid.com/svc/content/Collection/StandardCollection/version/6.1/region/US/audience/k-false,l-true/maturity/1830/language/en/contentClass/avatars/slug/avatars")
    for container in r.json()["data"]["Collection"]["containers"]:
        sets.append(container["set"]["refId"])
    return sets

def get_download_urls(setId) -> list[str]:
    urls = []
    r = requests.get(f"https://disney.content.edge.bamgrid.com/svc/content/PersonalizedCuratedSet/version/6.1/region/US/audience/k-false,l-true/maturity/1830/language/en/setId/{setId}/pageSize/24/page/1")
    for data in r.json()["data"]["PersonalizedCuratedSet"]["items"]:
        url = data["image"]["tile"]["1.00"]["avatar"]["default"]["url"]
        name = data["image"]["tile"]["1.00"]["avatar"]["default"]["masterId"] + ".png"
        urls.append((url, name))
    return urls

def main():
    sets = get_set_ids()
    for setId in sets:
        urls = get_download_urls(setId)
        for (url, name) in urls:
            r = requests.get(url)
            with open(name, "wb") as f:
                f.write(r.content)
                f.close()
                print("Wrote " + name)

if __name__ == "__main__":
    main()
