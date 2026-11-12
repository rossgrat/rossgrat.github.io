# Personal website

Ross Grattafiori's portfolio and blog, built with Hugo and custom styling.
Visit [ross.grattafiori.dev](https://ross.grattafiori.dev).

## Develop

Use Hugo 0.122.0 and uv 0.12.19.
uv supplies Python 3.12.14 and PyYAML 6.0.3 for publication dates.

```sh
make local
make build
make test
```

`make local` previews drafts; `make build` excludes them from the public site.
Set `HUGO=/path/to/hugo` to select another executable.
Use these Make targets so publication dates are generated from Git history.

Read the [publishing guide](docs/publishing.md) for Pages CMS, images, and dates.
CMS saves commit to this public repository, including drafts.
Production builds use Umami; local previews omit tracking.
To exclude a browser, open the [analytics toggle](https://ross.grattafiori.dev/#toggle-analytics) and confirm that tracking is disabled.
Repeat per browser and device. Opening the link again enables tracking.

[Potatoserver](https://github.com/rossgrat/potatoserver) documents CMS and analytics hosting.
