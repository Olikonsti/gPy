# gPy

# Keywords

````
if <var1> == <var2> {
    code
}
````
````
while <var1> != <var2> {
    code
}
````
````
py <indentation> {
    # python code
}
````

# Build in functions


## print
prints text to the console

args:
- variable/value

examples:
``print "test message"``
``print defined_var``

## input
asks the user for input by offering him a text

args:
- variable/value # type: string - used for the input asking text

return:
- user input # string

examples:
``out = input "> "``
``print defined_var``

## variable declaration
allowes to give a valuable a value

args:
- variable/value/calculation # variable to declare value to

return:
- value declared by args # string

examples:
``var1 = 1``
``var2 = 3 + var1``

## delay
waits for the specified amount in seconds

args:
- variable/value # float for delay in seconds

examples:
``delay 3.8``
``delay var2``

## windisplay
displays a variable amount in a window (only works in exec_mode 0)

args:
- pointer # variable to always display in a window

examples:
``windisplay *log``
``windisplay *var2``

# Access gPy variables in 'py' block
````
py 2 {
    print(stack["<var>"])
}
````

# Run gPy actions in 'py' block
````
py 2 {
    self.action("<action_name>", [arg1, arg2, ...])
}
````
