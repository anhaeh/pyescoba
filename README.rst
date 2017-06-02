========
PyEscoba
========

Clásico juego de naipes "Escoba de 15" desarrollado en Python. El mismo es totalmente funcional
y puede jugarse desde consola o desde su interface gráfica implementada en PyGame.

Se implementa IA de selección de jugada optima. La misma calcula la mejor jugada en base
a todas las cartas disponibles.


Screenshot: https://cloud.githubusercontent.com/assets/26558799/26708890/ff75854c-4724-11e7-9149-19a24f1ea7b3.png

Si quieres simular una jugada entre 2 IA's, solo tienes que agregar 2 CpuPlayer
(en app.py o en app_pygame.py) y ver como juegan entre ellas!

Ejecución
---------
1. Por terminal:

    $python app.py

2. PYGAME Engine. Instalar las dependencias en requirements.txt y ejecutar app_pygame.py:

    $pip install -r requirements.txt

    $python app_pygame.py