# How to create a gpy class and use it

```
@action dog.init {
    name = arg[0]
    self = obj *dog.init

    attr self *name

    return self
}

@action dog.print_info {
    @classaction
    print name
    name = 3
    attr self *name
}

@action dog.change_name {
    @classaction
    name = arg[1]
    attr self *name
}
```

every action in a class apart from the constructor should have a @classaction keyword before anything else can be done;

In classactions, the first argument is the object itself (the self) so the first real parameter would be arg[1]

the obj keyword in the constructor creates the object and then saves a uuid to the variable self which is later getting returned by the constructor

the attr keyword takes a uuid (self) and a variable pointer and adds the variable value to the objects attributes with the name of the variable
