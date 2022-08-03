# Compete with your NEAT AI racing driver

---

## General

This is a demonstration and game of NEAT where each registered player is responsible for training an AI racing driver, which they can use to compete with other players.

## Setup

Ensure you have the required python libraries by installing from [requirements.txt](./requirements.txt).

```bash
pip install -r requirements.txt
```

## Usage

The script provided in this directory is meant to be used from the command line, using the script `main.py`:

```bash
usage: AI-NEAT-racing [-h] [-m {1,2,3,4,5}] [-t] [--generations [GENERATIONS]] [-p PLAY [PLAY ...]] [--show_opponents] [-v] name

Train an AI to race around maps

positional arguments:
  name                  Name of the trainer.

options:
  -h, --help            show this help message and exit
  -m {1,2,3,4,5}, --map {1,2,3,4,5}
                        Select which map by integer (1 - 5) what map to use.
  -t, --train           Starts training a model to the user with specified number of generations using flag: --generations.
  --generations [GENERATIONS]
                        Number of generations model will train to.
  -p PLAY [PLAY ...], --play PLAY [PLAY ...]
                        Who to play against
  --show_opponents      Shows other possible opponents to play agains.
  -v, --verbose         Verbose mode
```

### Training
To use the script a database of player´s models is first needed, therefore start by training your model with the command,

```bash
./main.py user -m 2 -t --generations 12
```

This will start a `pygame` window with the different (non-interactive) models trying to learn the game map.

When `generations` criteria has been met, the script stores the model to the `user`.

### Other players

To play against other opponents first ensure there are other opponents to play. This can be done using:

```bash
./main.py user --show_opponents
```

```bash
[info] Showing registered users:
       user
       another_user
       another_user2
```

### Playing

We are now ready to compete against other users ai´s.

```bash
./main.py user -m 2 -p another_user
```

This will launch a competition between `user` and `another_user`.

### Multiple players

You can also play against multiple users at the same time.

```bash
./main.py user -m 2 -p another_user another_user2
```