========
PyEscoba
========

Clásico juego de naipes "Escoba de 15" desarrollado en Python. El mismo es totalmente funcional
y puede jugarse desde consola.

Se implementa un CPU player con IA de selección de jugada optima, teniendo en cuenta todas las cartas,
el valor de cada una, y como dejará el tablero para la siguiente jugada del oponente.

También se incluye una implementación basica en pygame para observar el comportamiento de la IA
y como selecciona las distintas jugadas. (Utilizar click izquierdo para realizar jugadas y
click derecho para descartarlas)

Screenshot: https://cloud.githubusercontent.com/assets/26558799/26315317/2938fb84-3ee7-11e7-8d61-1d233c5b76d7.png

Si quieres simular una jugada entre 2 IA's, solo tienes que agregar 2 CpuPlayer en app.py y ver
como juegan entre ellas!

Ejecución
---------
1. Por terminal:

    $python app.py

2. Utilizando PYGAME Engine. Instalar las dependencias de requirements.txt y ejecutar app_pygame.py:

    $pip install -r requirements.txt
    $python app_pygame.py