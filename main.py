import random
from math import sqrt

from matplotlib import pyplot as plt
from matplotlib.cm import get_cmap
from matplotlib.pyplot import scatter
from matplotlib.pyplot import show
from matplotlib.pyplot import savefig


def man_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def pyt_dist(p1, p2):
    return int(sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2))


def get_centroid(cluster):
    x_sum = 0
    y_sum = 0
    for p in cluster:
        x_sum += p[0]
        y_sum += p[1]
    return [x_sum // len(cluster), y_sum // len(cluster)]


def get_medoid(cluster):
    min = 0
    min_index = -1
    for p1 in range(len(cluster)):
        dist = 0
        for p2 in range(len(cluster)):
            if p1 == p2:
                continue
            dist += man_dist(cluster[p1], cluster[p2])
        if min_index == -1:
            min = dist
            min_index = 0
        if dist < min:
            min_index = p1
            min = dist
    return cluster[min_index]


def get_dist(full_cluster):
    points = full_cluster[0]
    distance = 0
    for p in points:
        distance += man_dist(full_cluster[1], p)
    return distance


def draw(data, title):
    print("Vykreslujem...")
    successful = 0
    x_array = []
    y_array = []
    cmap = get_cmap("hsv", 20)
    for i in range(len(data)):
        x_array.clear()
        y_array.clear()
        for item in data[i][0]:
            x_array.append(item[0])
            y_array.append(item[1])
        if data[i][2] < 500:
            successful += 1
        scatter(x_array, y_array, s=1, color=cmap(i))
        scatter(data[i][1][0], data[i][1][1], s=50, color='black', marker="$\u25EF$")
    title1 = title + ", uspesnost: " + str(int((successful/len(data))*100))+"%"
    plt.title(title1)
    savefig("C:\\Users\\jakub\\Desktop\\UI4\\testy\\"+title)
    show()


def k_means_centroid(k, points, toggle_print):
    centroids = []
    clusters = []
    iteration = 0
    while len(centroids) != k:
        ch = random.choice(points)
        if ch not in centroids:
            centroids.append(ch)
    prev_centroids = []
    for c in centroids:
        clusters.append([[c], c])
    while prev_centroids != centroids:
        for p in range(len(points)):
            min = 20000
            index_c = 0
            for c in range(k):
                if clusters[c][1] != []:
                    dist = man_dist(points[p], clusters[c][1])
                    if dist < min:
                        min = dist
                        index_c = c
            clusters[index_c][0].append(points[p])
        prev_centroids = centroids[:]
        iteration += 1
        for m in range(k):
            if len(clusters[m][0]) != 0:
                new = get_centroid(clusters[m][0])
                centroids[m] = new
                clusters[m][1] = new
                clusters[m][0] = []
            else:
                clusters[m][1] = []
        match = 0
        for g in range(k):
            if centroids[g] == prev_centroids[g]:
                match += 1
        if toggle_print:
            print("Stav je " + (str(int((match / k) * 100))) + "%")
    else:
        for p in range(len(points)):
            min = 20000
            index_c = 0
            for c in range(k):
                if clusters[c][1] != []:
                    dist = man_dist(points[p], clusters[c][1])
                    if dist < min:
                        min = dist
                        index_c = c
            clusters[index_c][0].append(points[p])
        for c in clusters:
            if len(c[0]) != 0:
                c.append(get_dist(c) // len(c[0]))
    return clusters


def k_means_medoid(k, points):
    medoids = []
    clusters = []
    iteration = 0
    while len(medoids) != k:
        ch = random.choice(points)
        if ch not in medoids:
            medoids.append(ch)
    prev_medoids = []
    for c in medoids:
        clusters.append([[c], c])
    while prev_medoids != medoids:
        for p in range(len(points)):
            min = 20000
            index_c = 0
            for c in range(k):
                if clusters[c][1] != []:
                    dist = man_dist(points[p], clusters[c][1])
                    if dist < min:
                        min = dist
                        index_c = c
            clusters[index_c][0].append(points[p])
        prev_medoids = medoids[:]
        iteration += 1
        for m in range(k):
            if len(clusters[m][0]) != 0:
                new = get_medoid(clusters[m][0])
                medoids[m] = new
                clusters[m][1] = new
                clusters[m][0] = []
            else:
                clusters[m][1] = []
        match = 0
        for g in range(k):
            if medoids[g] == prev_medoids[g]:
                match += 1

        print("Stav je " + (str(int((match / k) * 100))) + "%")
    else:
        for p in range(len(points)):
            min = 20000
            index_c = 0
            for c in range(k):
                if clusters[c][1] != []:
                    dist = man_dist(points[p], clusters[c][1])
                    if dist < min:
                        min = dist
                        index_c = c
            clusters[index_c][0].append(points[p])
        for c in clusters:
            c.append(get_dist(c) // len(c[0]))
    return clusters


def divisive(k, points: list):
    n = 1
    clusters = k_means_centroid(2, points, False)
    n += 1
    while n != k:
        max = clusters[0][2]
        index_max = 0
        for c in clusters:
            next = c[2]
            index = clusters.index(c)
            if next > max:
                max = next
                index_max = index

        new_clusters = k_means_centroid(2, clusters[index_max][0], False)
        clusters.pop(index_max)
        clusters.append(new_clusters[0])
        clusters.append(new_clusters[1])
        n += 1
        new_clusters.clear()
    return clusters


def agglomerative(k, points):
    return


if __name__ == '__main__':
    table = []
    n = 20000
    k = 20
    for i in range(20):
        x = random.randint(-4900, 4901)
        y = random.randint(-4900, 4901)
        while [x, y] in table:
            x = random.randint(-4900, 4901)
            y = random.randint(-4900, 4901)
        table.append([x, y])
    for i in range(n):
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        picked = random.choice(table)
        while [picked[0] + x_offset, picked[1] + y_offset] in table:
            x_offset = random.randint(-100, 101)
            y_offset = random.randint(-100, 101)
            picked = random.choice(table)
        table.append([picked[0] + x_offset, picked[1] + y_offset])
    print("Centroid:")
    draw(k_means_centroid(k, table, True), "k = " + str(k) + ",n = " + str(n) + ", centroid")
    print("Medoid:")
    draw(k_means_medoid(k, table), "k = " + str(k) + ",n = " + str(n) + ", medoid")
    print("Divisive: ")
    draw(divisive(k, table), "k = " + str(k) + ",n = " + str(n) + ", divisive")
    #print("Agglomerative:")
    #draw(agglomerative(k, table), "k = " + str(k) + ",n = " + str(n) + ", divisive")
