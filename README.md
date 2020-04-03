Note: these instructions are for OSX. It is recommended you use virtualenv. 

1) Make sure you have pytyhon 3.7+ and Homebrew installed. 

2) Install the python libraries 
```pip install -r requirements.txt```

3) Install Redis
```brew install redis```

4) Start Redis
```redis-server /usr/local/etc/redis.conf```

5) Ensure redis is running
```redis-cli ping```

6) Start Flask
```python server.py```

To uninstall redis
```
brew uninstall redis
rm ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
```

