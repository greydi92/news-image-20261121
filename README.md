[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/greydi92/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/greydi92/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — Saturday 21 November 2026

Built for the [make.fun "Sum up 21 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261121).

One image that sums up the world's news of Saturday 21 November 2026: a front-page infographic with six stories from that day, across regions and fields — Russian missiles landing in Poland during a huge overnight barrage on Ukraine, Wall Street sliding into correction as the AI sell-off deepens, the World Court finding Myanmar guilty of Rohingya genocide, hackers hitting JPMorgan, Visa and Mastercard through third-party vendors, Britain and the EU signing new food, carbon and youth-mobility deals, and Israel's president asking Gadi Eisenkot to form the next government. Every story was verified as happening, or first reported, on 21 November 2026.

Sources: AP / Reuters (missiles in Poland), Reuters / CNN / New York Post (Wall Street sell-off), UN News / Le Monde / CNN (ICJ Myanmar verdict), Reuters / Cybersecurity Dive (bank vendor breach), BBC (UK–EU deals), The Paris Eye (Eisenkot).

`main.py` (Python 3.13, standard library only) copies `entry.png` to the output directory. The image was rendered at build time by `gen_image.py` (Pillow, DejaVu fonts). No network, no timestamps, no randomness — two runs write byte-identical output.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024, ~120 KB).

---

<sub>Entered on [make.fun](https://make.fun/?ref=qgn48q27&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
