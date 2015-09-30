# lastcall

_Tells you your last chance to get home via public transit._

## Documentation

Read the code. It's under 140 lines and heavily annotated.

## Running the current proof-of-concept

### With docker
```bash
# get a google maps directions api key
echo "my api key" > src/apikey.txt

# change source/destination files to suit you
vim -p src/{source,destinations}.txt

# install docker
pacman -S docker

# run the project in a container
./run.sh
```

### Without docker

```bash
# get a google maps directions api key
echo "my api key" > src/apikey.txt

# change source/destination files to suit you
vim -p src/{source,destinations}.txt

# install the latest python3
# package might be 'python3' on your system
pacman -S python

# install google maps library
# command might be 'pip3' on your system
pip install googlemaps

# run it
# command might be 'python3' on your system
python src/lastcall.py
```

## Sample output

Displayed at ten-thirty:
```
 _______________
/               \
| 10:34 - 11:17 |
| 10:41 - 11:24 |
| 10:56 - 11:39 |
| 11:04 - 11:47 |
| 11:11 - 11:54 |
| 11:26 - 12:09 |
\_______________/
```

Displayed at twenty-two hundred:
```
 _______________
/               \
| 22:04 - 22:47 |
| 22:12 - 23:03 |
| 22:35 - 23:22 |
\_______________/
```

Displayed at midnight:
```
 _______________
/               \
|               |
|  No transit!  |
|               |
\_______________/
```
