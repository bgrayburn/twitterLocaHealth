docker kill twitterSearch
docker rm twitterSearch
docker run -p 80:80 --name="twitterSearch" -it twittersearch /bin/bash
