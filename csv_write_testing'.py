import csv
from operator import methodcaller

a = '''Exercise Date/time Elapsed time (minutes) Exercises Exercises per minute Correct Errors Score
Interval Ear Training 2021-10-12 18:22:00 7.97 26 3.3 11 15 42
Interval Ear Training 2021-10-12 23:19:00 11.98 36 3 12 24 33
Interval Ear Training 2021-10-13 13:21:00 8.22 22 2.7 10 12 45
Interval Ear Training 2021-10-13 20:01:00 8.8 2 0.2 1 1 50
Interval Ear Training 2021-10-13 20:29:00 0.05 0 0 0 0 0
Interval Ear Training 2021-10-13 21:48:00 3.47 24 6.9 6 18 25
Interval Ear Training 2021-10-14 00:53:00 2.88 21 7.3 9 12 43
Interval Ear Training 2021-10-14 09:14:00 5.68 34 6 17 17 50
Interval Ear Training 2021-10-14 11:20:00 2.23 14 6.3 5 9 36
Interval Ear Training 2021-10-14 15:33:00 5.33 23 4.3 7 16 30
Interval Ear Training 2021-10-15 01:09:00 4.87 21 4.3 9 12 43
Interval Ear Training 2021-10-15 11:05:00 6.95 39 5.6 13 26 33'''
print(a)

a_lines = a.split('\n')
a_lines = list(map(methodcaller("split", " "), a_lines))

with open('./stats.csv', 'w') as f:
    # create the csv writer
    writer = csv.writer(f)

    # write a row to the csv file
    writer.writerows(a_lines)