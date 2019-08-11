# phones_crawler
This module designed to crawl web pages and parse them to find phone numbers.

### installation
```
$ pip install -r requirements.txt
```

### tests
Requirements: 

```
$ pip install -r requirements.txt -r requirements.dev.txt
```

Run tests:
```
$ pytest tests/
```

### example
```bash
$ python example.py 
```
### caveats
- as long as we consider any 7-digits long sequence to be a Moscow city phone number we doomed to have a low precision rate. 