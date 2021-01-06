# ntc-pjapronto
ntc-pjapronto is an example python http server using Japronto  

## Install Japronto
```shell script
pip3 install https://github.com/squeaky-pl/japronto/archive/master.zip
```

## Start
```shell script
python3 main.py
```

## Call API Tag
### Add New Tag
```bash
curl -X POST -i 'http://127.0.0.1:8080/tag' \
  -H "Content-Type: application/json" \
  --data '{
    "name": "tag1"
  }'
```

### Update Tag
```bash
curl -X PUT -i 'http://127.0.0.1:8080/tag' \
  -H "Content-Type: application/json" \
  --data '{
    "id": "5ff379a2669ad8ac6d1addc1",
    "name": "tag1 update"
  }'
```

### Get Tag
```bash
# Get a tag
curl -X GET -H 'Content-Type: application/json' \
  -i 'http://127.0.0.1:8080/tag/5ff379a2669ad8ac6d1addc1'

# Get slide tags
curl -X GET -H 'Content-Type: application/json' \
  -i 'http://127.0.0.1:8080/tags?page=1'
```

### Delete Tag
```bash
curl -X DELETE -H 'Content-Type: application/json' \
  -i 'http://127.0.0.1:8080/tag/5ff37b2a669ad8ac6d1addda'
```


## License
This code is under the [Apache License v2](https://www.apache.org/licenses/LICENSE-2.0).  
