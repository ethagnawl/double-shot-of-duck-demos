# Quack - Complex Demo

## Depenencies
- [uv 0.7.20](https://docs.astral.sh/uv/)
- [duckdb 1.5.3](https://duckdb.org/install/?platform=linux&environment=cli)
- [optional] [tmuxinator](https://github.com/tmuxinator/tmuxinator)


## Running samples
### tmuxinator
The simplest option is to use the included tmuxinator project config file via:  `tmuxinator start -p project.yaml`

### Manually
If you'd prefer to use separate terminals, screen, Emacs or whatever else, you can use the commands from the tmuxinator project config file:

```
windows:
  - duck:
      panes:
        - duckdb -init server.sql /tmp/quack-vectors
        - duckdb -init cats.sql /tmp/quack-vectors-cat
        - duckdb -init ducks.sql /tmp/quack-vectors-duck
  - router:
      panes:
        - sleep 5 && uv run router.py # lazy
  - web-front-end:
      panes:
        - uv run fastapi dev web_client/main.py --port 9990
  - cameras:
      panes:
        - uv run camera.py backyard-1 ./frames/pexels-glacika67-11769613.jpg https://double-shot-of-duck-demos.s3.us-east-1.amazonaws.com/ducks/pexels-glacika67-11769613.jpg
        - uv run camera.py backyard-2 ./frames/pexels-helen1-30002405.jpg https://double-shot-of-duck-demos.s3.us-east-1.amazonaws.com/cats/pexels-helen1-30002405.jpg
```
