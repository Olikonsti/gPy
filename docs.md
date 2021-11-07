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
py <indentation level> {
    # python code
}
````

<details>
  <summary>variable declaration</summary>

allowes to give a variable a value

args:
- variable/value/calculation

return:
- value declared by args

examples:
``var1 = 1``
``var2 = 3 + var1``
</details>

# STD functions


<details>
  <summary>print</summary>

prints text to the console

args:
- variable/value

examples:
``print "test message"``
``print defined_var``
</details>


<details>
  <summary>input</summary>

asks the user for input by offering him a text

args:
- variable/value # type: string - used for the input asking text

return:
- user input # string

examples:
``out = input "> "``
``print defined_var``
</details>


<details>
  <summary>thread</summary>

starts a new thread of a function specified by a function pointer

args:
- function pointer

examples:
``thread *testaction``
</details>


<details>
  <summary>delay</summary>

waits for the specified time in seconds

args:
- variable/value # float for delay in seconds

examples:
``delay 3.8``
``delay var2``
</details>


<details>
  <summary>get_type</summary>

prints name and type of a variable pointer

args:
- variable pointer

examples:
``get_type *age``
</details>


<details>
  <summary>stradd</summary>

adds two strings

args:
- variable/value # string1
- variable/value # string2

return:
- string

examples:
``stradd name1 name2``
</details>


<details>
  <summary>value</summary>

returns value of a variable pointer

args:
- variable pointer

return:
- value of variable

examples:
``value *name``
</details>


<details>
  <summary>return</summary>

sets return variable to first arg

args:
- variable/value

return:
- value

examples:
``return 321``
</details>


<details>
  <summary>genuuid</summary>

returns a uuid used for objects etc.

return:
- value # float

examples:
``genuuid``
</details>


<details>
  <summary>user_confirm_exit</summary>

waits for user to press enter before exiting
</details>

# using classtools


dog.gpc
```
@action dog.init {

    # create object
    self = obj *dog
    
    
    name = "knecht"
    # adding attribute to object
    attr self *name

    name = "ne"

    return self
}

@action dog.print_info {
    @classaction
    print name
}
```

script.gpy
```
@import examples/dog.gpc

@action main {
    f = dog.init
    dog.print_info f
}
```


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
