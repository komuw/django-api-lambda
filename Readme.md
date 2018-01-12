
# ussd lambda

A simple example showing how to run a ussd app (or any django[1] app really) in AwS lambda using up[2].

## Deploy

```
$ up
```

## development
> `virtualenv -p python3 .venv`                             
> `source .venv/bin/activate`                            
> `pip3 install -r dev_requirements.txt`                        
> `python app.py collectstatic && python app.py migrate`             
> `up start`                  
> `autopep8 --experimental --in-place -r -aaaaaa .`                          
> `flake8 .`                        
```
curl -X POST -H "Content-Type: application/json" \
    -d '{"phonessionId": "10p5","text":"1", "serviceCode": "312"}' \
    "http://localhost:$PORT/ussd"
```

## Links

1. [Django](https://www.djangoproject.com/)
2. [up](https://github.com/apex/up)
