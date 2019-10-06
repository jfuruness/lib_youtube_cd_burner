# lib\_youtube\_cd\_burner
This package contains the functionality to burn a CD with just a playlist (or video) URL. It also contains a flask website for ease of use. 

* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)
* [Description](#package-description)
* [Usage](#forecast-usage)
* [Possible Future Improvements](#forecast-possible-future-improvements)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#licence)
* [Todo and Possible Future Improvements](#todopossible-future-improvements)
* [FAQ](#faq)
## Package Description
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

This package downloads a youtube playlist and burns a CD (or saves to a file) with the songs contained in that playlist. This is done through a series of steps.

1. If the flask app is open, the url is passed into the flask app. It is not validated because you are only supposed to be running this on your own machine, so just don't do anything stupid.
2. This URL is passed into Youtube_Playlist object. This object saves the URL.
3. Then, the Youtube_Playlist objects generate_cds function is called. This is the function that will do all the heavy lifting for CD burning
4. The songs from the playlist are downloaded using youtube_dl. A fix has been made to youtube_dl. Normally it errors for songs of a certain format, some weird format used for Russian songs (which of course people want to use this to download). We do not want it to error out, and instead simply skip those songs.  CD length is customizable, as well as intervals inbetween the songs on the CD. However, these are by default set to 80 minutes and 3 seconds, respectively.
5. The songs are downloaded into a fresh directory (that will be deleted once the parser is done. With each download, the song is formatted. Songs need to be formatted in a very particular manner in order for them to be able to be burned on an audio CD. They need to be WAV, 44100HZ, bidirectional (two channels), and PCM16. In addition, three seconds are added to each song. The functionality exists to remove all silence at the end of songs (in case there is already silence at the end) but this function takes a long time and is not turned on by default. You can find this function in song.py, however, it is not a part of a normal run because I wanted to get this project done and running.
6. Then these songs are added to a CD class. If the save path option is entered, then this step is skipped, and the audio is normalized and copied to the new path. If there are too many songs, then more than one CD is created. Randomization is possible, but turned off by default, since I wanted to minimize features to get this running.
7. After adding all songs to the CD, the CD audio is normalized. This is a process where songs volumes are increased or decreased so that from one song to the next the volume doesn't jump up and down.
8. After this the disk is ejected. It waits until a user inputs a disk. If no disk is input but the disk reader is closed, then the function returns nothing. 
9. After the disk is inserted, the program calls a bash script that uses wodim to burn the CD. The burn is as slow as is allowed to have a more even burn for when playing on crappy car sterios (for which this application was designed).

### Usage
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

NOTE: For this to run, wodim requires you to be a sudo user. All of these must be done with sudo. 

#### In a Script
Initializing the Main module:


| Parameter    | Default                             | Description                                                                                                       |
|--------------|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| url         | some test url     | The url for the playlist that will be downloaded |
| stream_level | ```logging.INFO```                        | Logging level for printing                                                                                        |
| save_path | None                        | Path to save songs to if not burning CD                                                                                        |
> Note that any one of the above attributes can be changed or all of them can be changed in any combination
> Also note that there are many more logging arguments, and different inputs to the youtube_cd burner and each one of it's functions. However, in order to get this module up and running we are not including every potential parameter, because I probably will be the only one that ever uses this application so documenting them would be a waste of time. If you cannot figure it out from the well documented code feel free to contact me at jfuruness@gmail.com with the subject header including the package name.

To run from a script with just the default CD burner:
```python
from lib_youtube_cd_burner import main, app
main(url=<insert url here>)
```
To run with custom logging level:
```python
from logging import DEBUG
from lib_youtube_cd_burner import main, app
main(url=<insert url here>, logger_args={"stream_level": DEBUG})
```
To run and instead of burning save all songs to a path:
```python
from logging import DEBUG
from lib_youtube_cd_burner import main, app
main(url=<insert url here>, save_path=<insert_path_here>)
```

To run and instead of burning save all songs to a path and also make a different format:

```python
from logging import DEBUG
from lib_youtube_cd_burner import main, app
main(url=<insert url here>,
     save_path=<insert_path_here>,
     song_format="mp3")
```

Again, you can create the youtube_playlist class to be able to have much more granularity with it and be able to paramatize functions for more features, but I won't ever do that, so if someone wants to modify this please contact me at jfuruness@gmail.com and I can write more documentation, I just don't want to waste my effort on it.

To run the app 
(NOTE: because you are running this on your host machine, it is not secure. We run this with the debugger because it is not deployed anywhere. Do NOT deploy flask in this way. Also, the flask app is just for usability, it does not add any functionality.)
```python
from lib_youtube_cd_burner import app
app.run(debug=True)
```

Then look on a web browser at localhost:5000

#### From the Command Line

run in a terminal: ```sudo youtube_cd_burner```

This will start the flask application on localhost:5000

### Installation instructions
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

First install wodim:

```sudo apt-get install wodim```

```sudo apt-get install ffmpeg```


Then install the package with:
```pip3 install lib_youtube_cd_burner --upgrade --force```

To install from source and develop:
```
git clone https://github.com/jfuruness/lib_youtube_cd_burner.git
cd lib_youtube_cd_burner
pip3 install wheel --upgrade
pip3 install -r requirements.txt --upgrade
python3 setup.py sdist bdist_wheel
python3 setup.py install
```

NOTE: you cannot use develop arg because of the way flask works. You must reinstall for dev after every change. It sucks, I know, but flask really does not like being inside of a package.

### System Requirements
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

Linux. It needs wodim, I don't know how to burn a CD on windows and I have asked and found no answers.

## Testing
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

Run tests on install by doing:
```pip3 install lib_bgp_data --force --install-option test```
This will install the package, force the command line arguments to be installed, and run the tests
NOTE: You might need sudo to install command line arguments when doing this

You can test the package if in development by moving/cd into the directory where setup.py is located and running:
```python3 setup.py test```

To test a specific submodule, cd into that submodule and run:
```pytest```

Note: I currently have not written any tests, since I have tried the CD's and know that it works. Idk if it's worth it to write since this package is complete so I'll put it off for now


## Development/Contributing
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
6. Email me at jfuruness@gmail.com because idk how to even check those messages

## History
   * [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)
   * 0.1.0 - Burns CDs with flask app, minimal features
   * 0.1.1 - Burn CDs or save songs with custom format
   * 0.1.2 - Fixed bug where songs wouldn't save to existing paths
   * 0.1.3 - Doesn't delete final directory to run multiple queries at once potentially
   * 0.1.4 - Fixed logging to show better info
   * 0.1.5 - Fixed install bug
   * 0.1.5 - Added multi URL functionality for a single folder/cd to allow for normalized audio across multiple playlists

## Credits
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

There where various sites I visited to learn about audio CD's, unfortunately I did not record them as I did them because I didn't plan on making a package. Here are two posts that helped:

https://stackoverflow.com/a/42496373
https://superuser.com/a/1367091

And of course this would not have been possible without youtube_dl and wodim, two very useful packages.

Also, Corey Schafer on youtube had a tutorial on making a flask application that I used.

And the flask tutorial for packages is also useful, code was used from there as well

## License
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

BSD License

## TODO/Possible Future Improvements
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

        * Youtube_dl is slow, use a custom downloader to be faster
        * multiprocess?
        * Make better tests
        * Make it so that it checks if the path will run out of memory
        * Try getting it to work on windows:
            * https://en.wikipedia.org/wiki/Cdrtools
            * https://tweaks.com/windows/48619/how-to-burn-cd-and-dvd-images-iso-files-from-the-command-line/
            * Windows ctypes
            * http://www.intelliadmin.com/index.php/2013/09/burn-a-dvd-or-cd-from-the-command-line/
            * https://superuser.com/questions/584617/how-to-burn-a-cd-files-not-iso-from-the-command-line-in-windows-7
            * https://pytale.wordpress.com/category/python-cddvd-burner/
            * https://www.daniweb.com/programming/software-development/threads/72834/handling-cd-drives-from-python
        * add extra features to the docs such as remove silence, allow user to set burn speed, etc.
            * Again, prob won't do this, because it'll just be me using it

## FAQ
* [lib\_youtube\_cd\_burner](#lib\_youtube\_cd\_burner)

Q: Why does downloading the songs take a while??

A: It's the downloading from Youtube. Youtube updates their site constantly to prevent this sort of thing. There are custom down loaders to get around this, but it's fast enough and I don't care.

Q: Why does the CD not burn fast?

A: Because the CD does not burn well if it burns fast and this is designed for people with old crappy stereos that do not have good error correction

Q: Why does the flask app have to be in the top directory?

A: Because the flask naming scheme sucks, and it literally does not work in any way anywhere else no matter what I do. Or at least I should say, it cannot be dynamically installed and run anywhere if you do that.
