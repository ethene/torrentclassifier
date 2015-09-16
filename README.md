#Torrent classifier POC

using http://www.libtorrent.org/
with python 
(tested with 2.7 but v.3 should be OK)

>just play with this shit
>to get the idea and improve

__requires:__

* python >=2.7, pip
* (sudo) pip install python-libtorrent
* ffmpeg

__usage:__

*python pytorrent.py [file.magnet|file.torrent]*

starts sequential file download + provides .avi ffmpeg metadata output


