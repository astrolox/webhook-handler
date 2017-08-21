
# Webhook Handler

Lightweight but comprehensive application which receives and handles webhooks.

## Configuration

You will require a configuration file similar to this example. In this example the webhook URL of `http://0.0.0.0/url-slug-for-hook?token=63fa31f8-47b6-4c21-bf23-122ead338eb9` is defined. When this URL is accessed via POST the defined behaviour is triggered.

The configuration file needs to be placed in the `instance` directory. The default name for the file is `config.json`.

**Ensure that the token is kept secret.**

```json
{
  "WEBHOOKS": {
    "url-slug-for-hook": {
      "token": "63fa31f8-47b6-4c21-bf23-122ead338eb9",
      "behaviour": "shell",
      "cmd": "uptime"
    }
  }
}
```

## Run

You have several options for running this web service.

I recommend using docker. 
e.g. `docker run --volume=/usr/src/app/instance/ astrolox/webhook-handler`

If you have installed python 3 you can install the dependencies using pip.
e.g. `pip install -r requirements.txt`

Once you have all the required python 3 packages intalled you can then either run the application directly or use the flask cli tool. Please note that when running directly you can specify arguments on the command line.
e.g. `./webhook-handler.py --help` or `FLASK_APP=webhook-handler.py flask run`

## Environment

The following environment variables are honoured:
 * `CONFIG` = Name of the configuration file
 * `HOST` = IP to bind to when listening for inbound connection
 * `PORT` = TCP port to bind to when listening for inbound connection

Additionally standard [Flask](http://flask.pocoo.org/docs/0.12/) environment variables are honoured. e.g. `FLASK_DEBUG=1`
