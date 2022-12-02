# 02223 Model-Based Systems Engineering Fall 22: Drones vs. Bikes food delivery
## Prerequisites

- Python 3.10 or above.

## How to get started
Assuming `python -V` yields a version >= 3.10, then one should be able to proceed with no further ado. If not, then one might have to explicitly do:

`python3.10 ...`

Note, the above will obviously only work if it is already installed.

It is always recommended to initialize a virtual environment to avoid dependency issues and pollution of the global pip:

`python -m venv myvenv`

Activate the virtual environment:

`source myvenv/bin/activate`

Then install requirements from the `requirements.txt` file:

`pip install -r requirements.txt`

Now it should be possible to run the simulation.
To see an complete overview of available arguments, do:

`python main.py -h`

To run the simulator with default parameters shown in the help page:

`python main.py`

If you want to see the plots but get an error like

`UserWarning: Matplotlib is currently using agg, which is a non-GUI backend, so cannot show the figure.`

You can fix it by:

Windows - you need to run the Python installer and modify the installation to install tkinter. 

Ubuntu - you can just run sudo apt-get install python3-tk.