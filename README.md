# wad_project

### Before Beginning
get python 3.13
then use pip install –r requirements.txt
run like normal django

### Must Use
- python anywhere
- polulation_script.py
- ajax/javascript/jquery (front end)

### Project Description

Our website idea is a social media platform that is for musicians to upload their music and albums to the platform and for music fans to follow artists they like, allowing them to find new artists and easily see when new songs are released. In addition to liking, commenting and downloading songs and album covers, the users should also be able to search for artists, search by different genres of music, stream music and add songs to their playlists. Musicians should be able to upload songs and images, and view how many profile views and downloads each song has.

### Project Specification

**Core Functionality:**

Users must be able to create personal accounts. 

Users will have to use accounts to upload UGC (music) or to interact with UGC (like, comment, follow other users) on the platform.

This can be done through Django, using their user authentication services.

Users must be able to upload music through their accounts, as well as interact with music they discover. This will be through listening, liking, sharing, following artists, and more.

Using SQLite, we can store related data together using related data (for example, posts will have an uploadID, artistID and the time at which it was uploaded stored in an SQL database.

Users must be able to search for music and users, using a search bar.

We may use HTML + CSS along with querying the SQL database

**Total Functionality:**

The app will utilise an algorithm to give music and artist recommendations to users.

We would likely have to use some sort of selection function, that takes into account the user’s favourite genres, followed artists, and popularity of songs, in order to determine what song to next recommend.

The app will feature a creator dashboard. This dashboard will allow artists to review the music they have uploaded on the app, with basic analytics. This may include a like to dislike ratio, a view count and average listen time.

We can use basic CSS to format a simple creator page

Users may upload basic metadata for their account. Things like profile pictures, a bio, and a username.

All we would need to do is validate inputs, to make sure people don’t upload inappropriate / malicious UGC (such as SQL injection or XSRF)


 
