# Flask Bower Server

Flask version of Twitter's [bower server](https://github.com/twitter/bower-server)

## Installation

    virtualenv env
    source env/bin/activate
    pip install -r requirements.txt
    python server.py

## Create package

    curl http://127.0.0.1:5000/packages -v -F 'name=jquery' -F 'url=git://github.com/jquery/jquery.git'

## Find package

    curl http://127.0.0.1:5000/packages/jquery
      {"name":"jquery","url":"git://github.com/jquery/jquery.git"}

## License

Licensed under the MIT License
