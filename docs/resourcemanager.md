# Работа с ресурсами

Работа с ресурсами производится посредством prg.common.resources.ResourceManager

Пример работы с ресурсами в коде игры:

```python
rm = ResourceManager('tiles', 5)  # Загрузить пакет ресурсов для тайла №5
tex = rm.get_resource('texture')
```
Будет возвращён файловый объект.


# Формат хранения ресурсов

Все ресурсы хранятся в папке res, которая имеет следующую структуру:
```
res
├── tiles
│   └── 1
│       ├── main
│       ├── script.py
│       ├── sounds
│       │   ├── footstep.ogg
│       │   └── open.ogg
│       └── textures
│           ├── open.png
│           └── closed.png
└── foo
...
```
В этом примере есть пакеты ресурсов tiles и foo, в пакете tiles есть только ресурс для тайла под ID 1, содержащий в себе звуки, текстуры и скрипт
При этом файл `main` должен иметь следующий формат:
```json
{
  "resource_version": "rgres1",
  "name": "Door",
  "description": "Simple door",
  "tile_script": "script",
  "res_list": [
    {
      "name": "texture0",
      "type": "image",
      "file": "textures/open.png"
    },
    {
      "name": "texture1",
      "type": "image",
      "file": "textures/closed.png"
    },
    {
      "name": "snd.footstep",
      "type": "sound",
      "file": "sounds/footstep.ogg"
    },
    {
      "name": "snd.footstep",
      "type": "sound",
      "file": "sounds/open.ogg"
    },
    {
      "name": "script",
      "type": "script",
      "file": "script.py"
    },
  ]
}
```

**При этом сам ресурс может быть как директорией, так и ZIP-архивом**
