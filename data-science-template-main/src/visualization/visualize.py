import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display
# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df = df[df["set"] == 1]
plt.plot(set_df["acc_y"].reset_index(drop=True))

# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
#creating a loop and looping over the unique subsetssets
for lable in df["lable"].unique():
    subset = df[df["lable"] == lable]
    fig, ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop=True), label=lable)
    plt.legend()
    plt.show()

for lable in df["lable"].unique():
    subset = df[df["lable"] == lable]
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=lable)
    plt.legend()
    plt.show()



# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20,5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
category_df = df.query("lable == 'squat'").query("participant == 'A'").reset_index()

fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------
#also done sorting because if sorting is not done the data will be messed up and mixed graph will be generated
participant_df = df.query("lable == 'bench'").sort_values("participant").reset_index()

fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
lable = "squat"
participant = "A"

all_axis_df = df.query(f"lable == '{lable}'").query(f"participant =='{participant}'").reset_index()

fig, ax = plt.subplots()
all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
labels = df["lable"].unique()
participants = df["participant"].unique()
for lable in labels:
    for participant in participants:
        all_axis_df = (
            df.query(f"lable == '{lable}'")
            .query(f"participant =='{participant}'")
            .reset_index()
        )
        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
            ax.set_ylabel("acc_y")
            ax.set_xlabel("samples")
            plt.title(f"{lable} ({participant})".title())
            plt.legend()

for lable in labels:
    for participant in participants:
        all_axis_df = (
            df.query(f"lable == '{lable}'")
            .query(f"participant =='{participant}'")
            .reset_index()
        )
        if len(all_axis_df) > 0:
            fig, ax = plt.subplots()
            all_axis_df[["gyro_x","gyro_y","gyro_z"]].plot(ax=ax)
            ax.set_ylabel("gyro_y")
            ax.set_xlabel("samples")
            plt.title(f"{lable} ({participant})".title())
            plt.legend()
# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
lable = "row"
participant = "A"
combiine_plot_df =( 
    df.query(f"lable == '{lable}'")
    .query(f"participant =='{participant}'")
    .reset_index(drop=True)
)

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20,10))
combiine_plot_df[["acc_x","acc_y","acc_z"]].plot(ax=ax[0])
combiine_plot_df[["gyro_x","gyro_y","gyro_z"]].plot(ax=ax[1])
ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox =True, shadow =True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox =True, shadow =True)
ax[1].set_xlabel("Samples")



# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
labels = df["lable"].unique()
participants = df["participant"].unique()
for lable in labels:
    for participant in participants:
        combiine_plot_df = (
            df.query(f"lable == '{lable}'")
            .query(f"participant =='{participant}'")
            .reset_index()
        )
        if len(combiine_plot_df) > 0:
            fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20,10))
            combiine_plot_df[["acc_x","acc_y","acc_z"]].plot(ax=ax[0])
            combiine_plot_df[["gyro_x","gyro_y","gyro_z"]].plot(ax=ax[1])
            ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox =True, shadow =True)
            ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox =True, shadow =True)
            ax[1].set_xlabel("Samples")
            plt.savefig(f"../../reports/figures/{lable.title()} ({participant}).png")
            plt.show()
        