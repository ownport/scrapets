

def fetch_by_url(url, path):

    filename = os.path.join(path, sha256url(url))
    resp = requests.get(url, stream=True)
    if resp.status_code == 200:
        with open(filename, 'wb') as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)
        return {
                'url': url,
                'sha256/url': sha256url(url),
                'sha256/file': sha256file(filename),
                'pairtree/url': pairtree(sha256url(url)),
                'pairtree/file': pairtree(sha256file(filename))
            }
    else:
        return {}


def fetch_by_urls(urls, path):

    with open(urls, 'r') as source:
        for url in source:
            url = url.strip()
            if not url:
                continue
            yield json.dumps(fetch_by_url(url, path))
