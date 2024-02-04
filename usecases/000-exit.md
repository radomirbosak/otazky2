# Task: Can exit program


## After learning
```
> Exit the program.
# program ends
```

## Before learning

```
> Exit the program.
What do you want me to do?  # what is your intent?
> Exit the program.
```
or 

In case "Exit" intent exists and has human description and has associated function.
```
> Exit the program.
Do you want me to exit the program?
> Yes.
# program ends
```

* program will need to eventually create a system/hierarchy of intents.
* for now a list of non-parametrized intents will do

## Concept: builtin answers

* yes
* no
* [Bad answer]
* (?)[Good answer]


## Concept: builtin commands

* add function

* `fn path/to/functionfile.py`

## Concept: builtin question

* > Should I run function ...?
