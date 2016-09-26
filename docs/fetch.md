# fetch operations

```sh
./bin/scrapets fetch --help
Usage: scrapets fetch [OPTIONS] [URL]...

  fetch operations

Options:
  --urls FILENAME             fetch files by the list of urls
  --index FILENAME            index file for storing metadata
  --path PATH                 the target directory, default:
                              /media/data1/svc/github/scrapets
  --user-agent TEXT           User agent, default: Mozilla/5.0 (X11; Ubuntu;
                              Linux x86_64; rv:44.0) Gecko/20100101
                              Firefox/44.0
  --pairtree / --no-pairtree  create pairtree structure in the target
                              directory, default: turn off
  --meta TEXT                 format or metadata. Possible values: short,
                              detail. Default: short
  --help                      Show this message and exit.
```
