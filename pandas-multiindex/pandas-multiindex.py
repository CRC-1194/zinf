import pandas as pd
import numpy as np

def processFrame(dFrame):
    """Reduces a pandas.DataFrame into pandas.Series by processing columns."""
    return pd.Series((np.average(dFrame["CFL"]), np.max(dFrame["E_v"]), np.max(dFrame["E_b"]), 
                     dFrame.iloc[-1]["E_g"], np.average(dFrame['t'])), index=indexD.split(" "))



# Prescribed column names, usually read from the data file.  
indexD = "CFL E_v E_b E_g t"

# Random generation of data. D1, D2, D3, mimick individual experiments / simulations.
D1 = pd.DataFrame(np.random.randn(10,5), columns=indexD.split(" "))
D2 = pd.DataFrame(np.random.randn(10,5), columns=indexD.split(" "))
D3 = pd.DataFrame(np.random.randn(10,5), columns=indexD.split(" "))
D4 = pd.DataFrame(np.random.randn(10,5), columns=indexD.split(" "))

# Series generated from data frames (tables).
E1 = processFrame(D1)
E2 = processFrame(D2)
E3 = processFrame(D3)
E4 = processFrame(D4)

# Parameters, usually read from the data file (metadata).
N = [32, 64]
CFL = [0.25,0.75]

# Cartesian parameter product. 
parameterIndex = pd.MultiIndex.from_product([N, CFL], names=["N", "CFL"])

# Build a data frame from error series Ei
errors = pd.DataFrame([E1,E2,E3,E4],index=parameterIndex)

# Print the errors 
print(errors)

# Print the errors in LaTex format for direct inclusion in the document.
print(errors.to_latex())

# Print the maximal E_v error
print(errors["E_v"].max())