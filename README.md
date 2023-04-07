# LastFMTools

This is repo of pythons scripts, i created over the past year or so that utilize
lastfm scrobbling feature, and public lastfm api to create visualizations of user listening history.

### Tools:

##### GIF-Mosaic
![alt text](https://github.com/Heroesluk/azure2/blob/main/static/movie2readme.gif)

## Okay but what is LastFM in the first place?

Last.fm is a music streaming and recommendation service that allows users to create personalized music profiles, discover new music, and connect with other music enthusiasts.

The scrobbling feature of Last.fm tracks the music you listen to on various platforms and records it on your profile. This data is used to analyze your music taste and listening history.

## Can i test those scripts without having LastFM account, or even without running them by myself? 

Yeah, all of the scripts i've created are available at [LastFMTools.app](https://sea-lion-app-rlgof.ondigitalocean.app) to freely use by anyone. 
There's also *random* feature for every tool, that lets you use script without providing your
LastFM nickname. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install LastFMTools
```

## Direct usage

```python
import LastFMTools

bubble_chart = BubbleChart("album", 50, "bubble.png", "MyNickname")


gif_mosaic = GifMosaic("10-11-2022", "month", 5, "File.gif", "MyNickName")


color_mosaic = ColorMosaic(COLOR.YELLOW, 4, "Yellow.png")

```
## Contribution

If you think there's anything to improve in those scripts,
 then feel free to create issues and pull-requests, 



## License

[MIT](https://choosealicense.com/licenses/mit/)
