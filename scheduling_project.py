import pandas as pd
import numpy as np
import time

start_time = time.time()
my_dataframe = pd.read_csv("scheduling.csv", header=None)
# Reads job durations from a CSV file into the DataFrame "my_dataframe".

def johnson(K):
    machine_1 = []
    machine_2 = []
    a1 = []
    a2 = []
    for i in range(K):
        if my_dataframe.iloc[i][0] <= my_dataframe.iloc[i][2]:
            machine_1.append(my_dataframe.iloc[i][0])
            #pj değeri ekler
            a1.append(i)
            #indis ekler
        else:
            machine_2.append(my_dataframe.iloc[i][2])
            print(machine_2)
            a2.append(i)
            print(a2)
            
    # Selects the smaller of the durations on the 1st and 3rd machines and adds their indices to lists.
    machine_1 = sorted(machine_1)
    # Sorts jobs in ascending order based on processing times on machine 1.
    a1_sorted = sorted(a1, key=lambda x: my_dataframe.iloc[x][0])
    # Sorts indices based on the processing times of jobs in ascending order.
    machine_2 = sorted(machine_2, reverse=True)
    machine_2.sort(reverse=True)
    list_d = machine_1 + machine_2
    print(list_d)
    a2_sorted = sorted(a2, key=lambda x: my_dataframe.iloc[x][2], reverse=True)
    # Performs the same operations in reverse order.
    list_sort = a1_sorted + a2_sorted
    # Merges indices into a common list.

    return machine_1, machine_2, list_sort, list_d

def johnson2(K):
    machine_3 = []
    machine_4 = []
    a3 = []
    a4 = []
    for i in range(K):
        if my_dataframe.iloc[i][0] + my_dataframe.iloc[i][1] <= my_dataframe.iloc[i][1] + my_dataframe.iloc[i][2]:
            machine_3.append(my_dataframe.iloc[i][0])
            a3.append(i)
        else:
            machine_4.append(my_dataframe.iloc[i][2])
            a4.append(i)
        # Selects the smaller of the sums of durations on the 1st and 2nd, and 2nd and 3rd machines, and adds their indices to lists.
    machine_3.sort()
    a3_sorted = sorted(a3, key=lambda x: my_dataframe.iloc[x][0] + my_dataframe.iloc[x][1])
    machine_4.sort(reverse=True)
    a4_sorted = sorted(a4, key=lambda x: my_dataframe.iloc[x][1] + my_dataframe.iloc[x][2], reverse=True)
    list_sort2 = a3_sorted + a4_sorted
    return machine_3, machine_4,list_sort2

K = int(input("Enter the number of jobs to work with (between 1 and 60): "))
# Select the number of jobs to work with. Exp: 5, 15, 45, 60

machine_1, machine_2, list_sort,list_d = johnson(K)
machine_3,machine_4,list_sort2 = johnson2(K)

selected_rows = my_dataframe.iloc[list_sort].values.tolist()
print(selected_rows)
selected_rows2 = my_dataframe.iloc[list_sort2].values.tolist()
# Retrieves jobs based on indices.

list_abc = []
list_abc2 = []

for i in range (K):
    for j in range(3):
        list_abc.append(selected_rows[i][j])
print(list_abc)
# Rid of paranthesese
for i in range (K):
    for j in range(3):
        list_abc2.append(selected_rows2[i][j])

# Flattens the selected_rows into a single list since we can't use the current format with the graph method.

np_mya = np.array(list_abc)

np_mya = np_mya.reshape(K,3).transpose()



# Converts the list, takes its transpose, and arranges it in the desired format.

cmax = np_mya[0][0]
for i in range (len(np_mya[0])-1):
    np_mya[0][i+1] = np_mya[0][i] + np_mya[0][i+1]
for i in range (len(np_mya)-1):
    np_mya[i+1][0] = np_mya[i][0] + np_mya[i+1][0]

for i in range (1,len(np_mya[0])):
    if np_mya[0][i] < np_mya[1][i-1]: 
        np_mya[1][i] += np_mya[1][i-1]
    else:
        np_mya[1][i] += np_mya[0][i]

for i in range(2,len(np_mya[0])+1):
    if np_mya[1][i-1] < np_mya[2][i-1]:
        np_mya[2][i-1] += np_mya[2][i-2]
    else:
        np_mya[2][i-1] += np_mya[1][i-1]

# Calculates Cmax using the graph method. (For machines 1 and 3)

print(np_mya)
cmax1= np_mya[(len(np_mya)-1)][(len(np_mya[0])-1)]
print(f"Solution for S1: {cmax1}")

np_mya = np.array(list_abc2)
np_mya = np_mya.reshape(K,3).transpose()


for i in range (len(np_mya[0])-1):
    np_mya[0][i+1] = np_mya[0][i] + np_mya[0][i+1]
for i in range (len(np_mya)-1):
    np_mya[i+1][0] = np_mya[i][0] + np_mya[i+1][0]

for i in range (1,len(np_mya[0])):
    if np_mya[0][i] < np_mya[1][i-1]: 
        np_mya[1][i] += np_mya[1][i-1]
    else:
        np_mya[1][i] += np_mya[0][i]

for i in range(2,len(np_mya[0])+1):
    if np_mya[1][i-1] < np_mya[2][i-1]:
        np_mya[2][i-1] += np_mya[2][i-2]
    else:
        np_mya[2][i-1] += np_mya[1][i-1]

# Calculates Cmax using the graph method. (For machines 1+2 and 2+3)

cmax2= np_mya[(len(np_mya)-1)][(len(np_mya[0])-1)]
print(np_mya)
print(f"Solution for S2: {cmax2}")

s=0
if cmax1<=cmax2:
    s= cmax1
    print(f"The solution found for S1 is better than the S2 solution. Answer: {cmax1}")
else:
    s=cmax2
    print(f"The solution found for S2 is better than the S1 solution. Answer: {cmax2}")

# Prints the smaller makespan.

end_time = time.time()
elapsed_time = end_time - start_time
print(f"{K} makine icin gecen zaman ,{elapsed_time}")
# Calculates the elapsed
