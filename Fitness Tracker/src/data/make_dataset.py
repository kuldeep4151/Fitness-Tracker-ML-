import pandas as pd
from glob import glob
print(pd.__version__)
# --------------------------------------------------------------
# Read single CSV file
# --------------------------------------------------------------
single_file_acc=pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv")
single_file_gyro = pd.read_csv("../../data/raw/MetaMotion/A-bench-heavy2-rpe8_MetaWear_2019-01-11T16.10.08.270_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv")

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------
files = glob("../../data/raw/MetaMotion/*.csv")
# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------
data_path = "../../data/raw/MetaMotion/"
f = files[0]

participant = f.split("-")[0].replace(data_path, "")
lable = f.split("-")[1]
category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

df = pd.read_csv(f)
df["participant"] = participant
df["lable"] = lable
df["category"] = category

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
#Create two empty dataframe and then append data in them using for loop

acc_df = pd.DataFrame()
gyro_df = pd.DataFrame()

acc_set = 1
gyro_set = 1

for f in files:
    participant = f.split("-")[0].replace(data_path, "")
    lable = f.split("-")[1]
    category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
    
    df = pd.read_csv(f)
    
    df["participant"] = participant
    df["lable"] = lable
    df["category"] = category

    if "Accelerometer" in f:
        df["set"] = acc_set
        acc_set += 1
        acc_df=pd.concat([acc_df, df])
    if "Gyroscope" in f:
        df["set"] = gyro_set
        gyro_set += 1
        gyro_df=pd.concat([gyro_df, df])


# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------

acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms") 
gyro_df.index = pd.to_datetime(gyro_df["epoch (ms)"], unit="ms")

del(acc_df["epoch (ms)"])
del(acc_df["time (01:00)"])
del(acc_df["elapsed (s)"])

del(gyro_df["epoch (ms)"])
del(gyro_df["time (01:00)"])
del(gyro_df["elapsed (s)"])


# --------------------------------------------------------------
# Turn into function
#it is a good practice to turn the code into function
# --------------------------------------------------------------
files = glob("../../data/raw/MetaMotion/*.csv")

def read_data_from_files(files):
    data_path = "../../data/raw/MetaMotion/"
    f = files[0]
    acc_df = pd.DataFrame()
    gyro_df = pd.DataFrame()

    acc_set = 1
    gyro_set = 1

    for f in files:
        participant = f.split("-")[0].replace(data_path, "")
        lable = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")
        
        df = pd.read_csv(f)
        
        df["participant"] = participant
        df["lable"] = lable
        df["category"] = category

        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df=pd.concat([acc_df, df])
        if "Gyroscope" in f:
            df["set"] = gyro_set
            gyro_set += 1
            gyro_df=pd.concat([gyro_df, df])

    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms") 
    gyro_df.index = pd.to_datetime(gyro_df["epoch (ms)"], unit="ms")

    del(acc_df["epoch (ms)"])
    del(acc_df["time (01:00)"])
    del(acc_df["elapsed (s)"])

    del(gyro_df["epoch (ms)"])
    del(gyro_df["time (01:00)"])
    del(gyro_df["elapsed (s)"])

    return acc_df, gyro_df
acc_df, gyro_df = read_data_from_files(files)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------
data_merge = pd.concat([acc_df.iloc[:,:3],gyro_df], axis=1)
#renaming column
data_merge.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "participant",
    "lable",
    "category",
    "set"
]


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------
sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyro_x": "mean",
    "gyro_y": "mean",
    "gyro_z": "mean",
    "participant": "last",
    "lable": "last",
    "category": "last",
    "set": "last",
}
# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz
data_merge[:1000].resample(rule="200ms").apply(sampling)
#split by day
days = [g for n, g in data_merge.groupby(pd.Grouper(freq="D"))]

data_resample = pd.concat([df.resample(rule="200 ms").apply(sampling).dropna() for df in days])

print(data_resample)
# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
#pickle will make sure that we don't have to do conversion again 
#pickle is better option when we deal with timestamps 

data_resample.to_pickle("../../data/interim/01_data_processed.pkl")
