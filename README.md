# Physics Engine

A standalone application to exploring how different forces can affect an object. This project focuses on physics simulations / interpreting ecuations into code 

## Features

### Support needed

The software requirements to run must be the following :

- Linux OS 
- C++ 11 or above
- SFML library installed


## Setup work


### Install SFML

SFML can be installed dirrectly from the website by following the instructions or cloned from the [repository](https://github.com/SeptimiuPop/2D-Game-Engine/tree/main/External/SFML).

If the latter is chosen, all directories except `include` and `lib` in the SFML folder can be removed. In order to compile the code properly the `Makefile` file should include the following changes :

```
$(CC) -c $(SRC) $(INCLUDES) <SFML/include Path>
$(CC) *.o -o $(EXE_PATH) $(LIBS) -L <SFML/lib Path> 
```

Where `<SFML/include Path>` and `<SFML/lib Path>` are replaced by the path of the include and lib directories in the cloned SFML folder

---

### Prepare the commands

In order to successfully build and run the application you must create a folder named bin where the build files will go. To do this use the following command from the terminal :

```properties
mkdir bin
```

Other names can also be used for the directory but the 'BIN_PATH' in the Makefile should be changed accordingly

---

### Launch the Application

From the terminal use the following command to build and launch the application :

` make run `  

### Build the application
From the terminal use the following command to compile the code in the bin folder created previously, and run it :

`make build`

### Clear the previous build for the application

From the terminal use the following command to clear the build :

` make clear `
