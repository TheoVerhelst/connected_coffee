# connected_coffee

#### *Make coffee right from your laptop*

The idea is to connect a Raspberry to your coffee machine, in order to command it while providing a web interface to make it fancy.

For now though there is only the web interface, no chip programming yet.

Inspiring page:

http://senseowithpi.blogspot.com/

It works with this kind of machine:

![Senseo machine](https://s1.euronics.ee/UserFiles/Products/Images/137704-philips-hd7829-60.png)

The next step would be to also implement a server for MQTT messages so that you can command you coffee machine with your voice through Snips (https://docs.snips.ai/). That's another Raspberry to buy though, and a bigger one this time.

## What's working so far

* A mock simulation of a coffee machine is running on the backend. It heats up and brew a cup in 4 seconds. Top tier.
* The React frontend connects to the backend using Websockets so it's realtime and stuff.

## What's not working

* The state "no_water" is not handled yet.
* The whole project hasn't been tested IRL.

## Running the damn thing

### Backend

The backend is written with Flask.io. Go in the backend directory, and install the needed stuff with

```
virtualenv ve
source ve/bin/activate
pip install -r requirements.txt
```
And run the beast with
#### `python3 backend/server.py`

### Frontend

The frontend is written with in HTML React. So you just need to serve the static
files with a web server, for example `lighttpd`. Just install `lighttpd` and run

#### `sudo bash deploy.sh`
