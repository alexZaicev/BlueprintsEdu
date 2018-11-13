
Folder 'base':
    Python base files that are default state of the game. They need to be copied and modified accordingly.
    Modification can be performed by putting special generator familiar tags:

        <list those tags>

    When the game template is created, user from BlueprintApp end can create blueprint logic and query API to
    generate a working copy of python game representation.
    All file fo the generator to touch should be added accordingly to the generator as a new feature.

Folder 'car_simulator':
    Python car simulator template that contains game logic as well as generator specific tags for the API
    code generation. Template file extension: '<name>.py.temp'. Generator will look for these files, analyze the
    and generate the code.

    Folder 'out' in template folder:

        'out' folder contains Python generated game code that can be run from the console (ensure that you have
        'pygame' module installed): python app.py
        