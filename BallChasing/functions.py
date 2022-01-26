import numpy as np

def find_mean(data):
        print(data)
        new_data = []
        data_sort = sorted(data)
        q1_data = data_sort[:len(data_sort)//2]
        q3_data = data_sort[len(data_sort)//2:]
        Q1 = np.median(q1_data)
        Q3 = np.median(q3_data)
        #print("Q1: " +str(Q1))
        #print("Q3: " + str(Q3))

        for d in data:
            d = float(d)
            #print("d: " + str(d))
            #print("d>=Q1: " + str(d>=Q1))
            #print("d<=Q3: " + str(d<=Q3))
            if d >= Q1 and d <= Q3:
                    new_data.append(d)
        print(new_data)
        return np.mean(new_data)

#print(find_mean([25.341863098849544, 9.86958235016359, 16.264869624932143, 5.288193775215941, 5.8037774458629015, 41.66920077672735, 41.66920077672735, 16.078261466156366, 10.667279816506062]))