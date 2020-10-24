Operations
===

### Full operation:
```
-o 
FULL 
-in
http://isaiminihits.net/site_arrahman_instrument.xhtml
-out
/root/gerrit/karaoke/ar-instrumental
```

## Creator:

```

-o 
CREATOR 
-in
/media/sf_gerrit/karaoke/kaviya-thalivan
-out
/media/sf_gerrit/karaoke/kaviya-thalivan
```


Scrap single page

-o 
SCRAP_PAGE 
-in
https://www.tamilmusix.in/gana_songs_collections.html
-out
/root/gerrit/karaoke/gana-songs

Scrap all the pages..

-o 
SCRAP_ALL_PAGE 
-in
http://isaiminihits.net/site_arrahman_instrument.xhtml
-out
/root/gerrit/karaoke/ar-instrumental




Download from url

-o 
DOWNLOAD 
-in
http://tnhits.xyz/Download.php?file=VGFtaWwgQS1aIFNvbmdzL08tUCBIaXRzIENvbGxlY3Rpb25zL1BhbGxpa29vZGFtLzkgTWFuaWtrdSA5IE1hbmlra3UubXAz
-out
/root/gerrit/karaoke/gana-songs


Download from file
-o 
DOWNLOAD_LIST
-in
/root/gerrit/karaoke/melody-songs/song_urls.txt
-out
/root/gerrit/karaoke/melody-songs


Split single file
-o 
SPLEETER
-in
/root/gerrit/karaoke/melody-songs/download/_Aadiyile_Sedhi_.mp3
-out
/root/gerrit/karaoke/melody-songs


Split list
-o 
SPLEETER_LIST
-in
/root/gerrit/karaoke/melody-songs/download
-out
/root/gerrit/karaoke/melody-songs


Convert single file:

-o 
CONVERT
-in
/root/gerrit/karaoke/melody-songs/accompaniment/_Aadiyile_Sedhi_.mp3
-out
/root/gerrit/karaoke/melody-songs

Convert list
-o 
CONVERT_LIST
-in
/root/gerrit/karaoke/ar-instrumental/accompaniment
-out
/root/gerrit/karaoke/ar-instrumental

upload
-o 
UPLOAD_LIST
-in
/root/gerrit/karaoke/melody-songs/video-converted
-out
/root/gerrit/karaoke/melody-songs


