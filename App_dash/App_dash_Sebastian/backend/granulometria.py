import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d 
malla = [#para las mallas
    "11/2" , #Tamiz 11/2
    "1",
    "3/4",
    "3/8",
    "No 4",
    "No 10",
    "No 20",
    "No 40",
    "No 60",
    "No 100",
    "No 200",
    "fondo"
    ]

abertura=[
    37.5, #Para Tamiz 11/2
    25,
    19,
    9.5,
    4.75,
    2,
    0.85,
    0.425,
    0.250,
    0.15,
    0.075,
    0
]
retenido=[
    1, #Para Tamiz 11/2
    1,
    130,
    150,
    120,
    60,
    100,
    100,
    205,
    50,
    200,
    35
]
granulometria=pd.DataFrame({
    "Malla":malla,
    "Abertura":abertura,
    "Retenido":retenido
})

granulometria["Retenido_acum"]=granulometria["Retenido"].cumsum()
granulometria["Pasa"] = granulometria["Retenido"].sum()-granulometria["Retenido_acum"]
granulometria["Por_Pasa"]= round(granulometria["Pasa"]*100/granulometria["Retenido"].sum(),2)
granulometria["Por_Pasa"]= round((granulometria["Pasa"] * 100 / granulometria["Retenido"].sum()) if granulometria["Retenido"].sum() != 0 else 0, 2)
