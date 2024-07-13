# How to run the simulation:

## Prerequisites

First of all, running the simulation requires having python and pip (python package manager) installed.
If you have a python version newer than Python 3.4, pip should already be installed by default. If you're not sure if you have it installed or not, you can type:

```bash
pip --version
```

in your terminal, to see what version you have.

## Setting up a virtual environment

Although this step is not strictly necessary, it is highly recommended, and only takes a minute to do.
A Python virtual environment is an isolated environment that allows you to manage dependencies for your Python projects independently from the system-wide Python installation. This isolation ensures that each project can have its own dependencies and versions, preventing conflicts between projects.

### Creating the virtual environment

When in the root directory, you can create a virtual environment by using the following command:

```bash
python3 -m venv myenv
```

This will create a virtual environment that is called "myenv". You will only have to do this once.

### Entering the virtual environment

Now that you have created the virtual environment, you have to enter it, and this is done by either of the following commands, depending on what operating system you are using.

For macOS/Linux:

```bash
source myenv/bin/activate
```

For Windows:

```bash
myenv\Scripts\activate.bat
```

or:

```bash
myenv\Scripts\Activate.ps1
```

### Deactivating the virtual environment

When you no longer want to run the simulations, you can deactivate the virtual environment by simply typing:

```bash
deactivate
```

in your terminal

## Installing required dependencies

When you have entered the virtual environment, you need to install the packages required to run the simulations.
To do this, type the following command while being located in the root directory:

```bash
pip3 install -r requirements.txt
```

This will install all the packages in you environment, and not globally, which is a big advantage. This makes sure you don't get possible conflicts if you try to install packages that you might already have.

## Running the simulation

To run the simulation of the Dutch electoral system, locate the folder "LeggiElettorali", and inside this, locate the folder "Dutch", and run the file called "**main**.py". This will simulate the distribution of mandates, and plot the results.
