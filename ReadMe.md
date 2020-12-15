## This project was inspired by [ielashi's eltetris](https://github.com/ielashi/eltetris)

[The detailed introduction of the original project can be seen here](https://imake.ninja/el-tetris-an-improvement-on-pierre-dellacheries-algorithm/)

### This is a version implemented using python
```shell
# Run the AI
# Linux
python3 ExampleTetris/Game.py
# Windows
python ExampleTetris/Game.py
```

### Requirement 
#### pygame

### Develop Environment
[Pop-os 20.10](https://system76.com/pop)

[Pycharm](https://www.jetbrains.com/pycharm/) with Python3.8

### Test Environment
#### Linux: Pass
#### Windows: Pass

## issues
If it is not run in the IDE (mine is Pycharm), it may become unresponsive or even crash
(it is reasonable, because we don't have to monitor any time, just simple while True)

## future

```text
1.A set of universal conversion proxy interface, 
so that any implementation of Tetris can be converted into an AI-recognizable form
2.Allow AI to operate games built in any form.
3.The game built by other language?
```

### Note

```text
USE THE TYPEs IN AI/StandardType TO PARSE YOUR DATA TO AI
```
