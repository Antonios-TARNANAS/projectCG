```racing_game/
│
├── main.py              ← entry point, game loop
├── settings.py          ← colors, screen size, FPS, constants
│
├── entities/
│   ├── car.py           ← Car class (position, speed, input handling)
│   └── player.py        ← Player wrapper (links a car + controls)
│
├── maps/
│   ├── map_base.py      ← base Map class (draw road, walls, finish line)
│   ├── map_01.py        ← first track (you give me the layout, I code it)
│   └── map_02.py        ← future maps follow same pattern
|
├── ui/
│   ├── car select.py    
│   ├── hud.py        
│   └── menu.py        
│
└── data/
    ├── cars.py          ← list of car configs (speed, handling, acceleration)
    └── maps_registry.py ← list of available maps
```


Interpreter python 3.12

```
python -m pip install --upgrade pip
```

```
pip install pygame
```

```
python main.py # defaults to zqsd
```

```
python main.py -zqsd    # explicit zqsd
```

```
python main.py -wasd    # explicit wasd
```
