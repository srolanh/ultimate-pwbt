# -*- coding=utf-8 -*-

import sys

stopsf = open("stops.txt", 'r')
agencyf = open("agency.txt", 'r')
routesf = open("routes.txt", 'r')
tripsf = open("trips.txt", 'r')
stop_timesf = open("stop_times.txt", 'r')
calendarf = open("calendar.txt", 'r')
calendar_datesf = open("calendar_dates.txt", 'r')

stops = stopsf.readlines()
agency = agencyf.readlines()
routes = routesf.readlines()
trips = tripsf.readlines()
stop_times = stop_timesf.readlines()
calendar = calendarf.readlines()
calendar_dates = calendar_datesf.readlines()

stopsf.close()
agencyf.close()
routesf.close()
tripsf.close()
stop_timesf.close()
calendarf.close()
calendar_datesf.close()

for i in range(0, len(stops)):
    stops[i] = stops[i].split(", ")

for i in range(0, len(agency)):
    agency[i] = agency[i].split(", ")

for i in range(0, len(routes)):
    routes[i] = routes[i].split(", ")

for i in range(0, len(trips)):
    trips[i] = trips[i].split(", ")

for i in range(0, len(stop_times)):
    stop_times[i] = stop_times[i].split(", ")

for i in range(0, len(calendar)):
    calendar[i] = calendar[i].split(", ")

for i in range(0, len(calendar_dates)):
    calendar_dates[i] = calendar_dates[i].split(", ")

def aq(s):
    return "\"" + s + "\""

def sq(s):
    if s == None:
        return ""
    r = ""
    for i in range(0, len(s)):
        if not ((i == 0 or i == len(s)-1) and s[i] == '\"'):
            r += s[i]
    return r

def punct(s):
    if s == None:
        return ""
    r = ""
    for i in range(0, len(s)):
        r += s[i]
        if i == 3 or i == 5:
            r += '.'
    return r

def time_to_int(s):
    h = int(s[0:2])
    m = int(s[3:len(s)])
    return 60*h+m

def stop_id(stop_name):
    ret = list()
    for i in stops:
        if i[2] == stop_name:
            ret.append(i[0])
    return ret

def stop_name(stop_id):
    for i in stops:
        if i[0] == stop_id:
            return i[2]

def stop_code(stop_id):
    for i in stops:
        if i[0] == stop_id:
            return i[1]

def agency_name(agency_id):
    for i in agency:
        if i[0] == agency_id:
            return i[1]

def route_name(route_id):
    for i in routes:
        if i[0] == route_id:
            return i[3]

def route_code(route_id):
    for i in routes:
        if i[0] == route_id:
            return i[2]

def route_agency(route_id):
    for i in routes:
        if i[0] == route_id:
            return i[1]

def code_route_id(route_code):
    for i in routes:
        if i[2] == route_code:
            return i[0]

def trip_route_id(trip_id):
    for i in trips:
        if i[2] == trip_id:
            return i[0]

def trip_service_id(trip_id):
    for i in trips:
        if i[2] == trip_id:
            return i[1]

def stop_time(trip_id, stop_id, stop_seq):
    for i in stop_times:
        if i[0] == trip_id and i[3] == stop_id and i[4] == stop_seq:
            return i[1][0:5]

def stop_dep_time(trip_id, stop_id, stop_seq):
    for i in stop_times:
        if i[0] == trip_id and i[3] == stop_id and i[4] == stop_seq:
            return i[2][0:5]

def trips_stop_at(stop_id):
    r = list()
    for i in stop_times:
        if i[3] == stop_id:
            r.append(tuple((i[0],i[4])))
    return r

def trip_stops(trip_id):
    q = list()
    for i in stop_times:
        if i[0] == trip_id:
            q.append(tuple((i[3],i[4])))
    return q

def route_trips(route_id):
    r = list()
    for i in trips:
        if i[0] == route_id:
            r.append(i[2])
    return r

def service_calendar(service_id):
    r = ""
    for i in calendar:
        if i[0] == service_id:
            if i[1] == "1":
                r += "1"
            else:
                r += "-"
            if i[2] == "1":
                r += "2"
            else:
                r += "-"
            if i[3] == "1":
                r += "3"
            else:
                r += "-"
            if i[4] == "1":
                r += "4"
            else:
                r += "-"
            if i[5] == "1":
                r += "5"
            else:
                r += "-"
            if i[6] == "1":
                r += "6"
            else:
                r += "-"
            if i[7] == "1":
                r += "7"
            else:
                r += "-"
            ret = list()
            ret.append(r)
            ret.append(i[8])
            ret.append(i[9])
            return ret

while True:
    msg = """
1) Maršruta nosaukums no koda
2) Maršruti starp divām pieturām
3) Reisa pieturas un laiki
4) Visi maršruta reisi
5) Reisi caur pieturu
x) Iziet
? """
    n = input(msg)
    if n == "1":
        c = input("Kods: ")
        print(sq(route_name(code_route_id(c))))
    elif n == "2":
        s1 = aq(input("Pietura A: "))
        s2 = aq(input("Pietura B: "))
        print()
        l1 = stop_id(s1)
        l2 = stop_id(s2)
        l = list()
        for i in l1:
            for j in l2:
                q1 = trips_stop_at(i)
                q2 = trips_stop_at(j)
                for k in q1:
                    for m in q2:
                        if k[0] == m[0] and time_to_int(stop_time(m[0], j, m[1])) > time_to_int(stop_time(k[0], i, k[1])):
                            atb = "" + sq(route_name(trip_route_id(k[0])))
                            atb += " "
                            atb += '(' + route_code(trip_route_id(k[0])) + ')'
                            atb += " "
                            atb += stop_dep_time(k[0], i, k[1]) + " – " + stop_time(m[0], j, m[1])
                            atb += " "
                            atb += sq(agency_name(route_agency(trip_route_id(k[0]))))
                            atb += " "
                            atb += "[reiss " + k[0] + "]"
                            c = service_calendar(trip_service_id(k[0]))
                            atb += " " + c[0]
                            atb += " " + punct(c[1]) + "–" + punct(c[2])[0:len(punct(c[2]))-1]
                            l.append(tuple((time_to_int(stop_dep_time(k[0],i,k[1])), atb)))
        l.sort(key= lambda i : i[0])
        for i in l:
            print(i[1])
    elif n == "3":
        r = input("Reisa nr.: ")
        print()
        s = trip_stops(r)
        for i in s:
            atb = sq(stop_name(i[0])) + " "
            if stop_time(r,i[0],i[1]) == stop_dep_time(r,i[0],i[1]):
                atb += stop_time(r,i[0],i[1])
            else:
                atb += stop_time(r,i[0],i[1]) + "-" + stop_dep_time(r,i[0],i[1])
            print(atb)
    elif n == "4":
        m = input("Maršruta nr.: ")
        print()
        mi = code_route_id(m)
        t = route_trips(mi)
        for i in t:
            s = trip_stops(i)
            c = service_calendar(trip_service_id(i))
            atb = sq(stop_name(s[0][0])) + " " + stop_time(i,s[0][0],s[0][1]) + " – " + sq(stop_name(s[-1][0])) + " " + stop_time(i,s[-1][0],s[-1][1]);
            atb += " [reiss " + i + "] "
            atb += c[0] + " " + punct(c[1]) + "–" + punct(c[2])[0:len(punct(c[2]))-1]
            print(atb)
    elif n == "5":
        p = stop_id(aq(input("Pietura: ")))
        print()
        l = list()
        for j in p:
            t = trips_stop_at(j)
            for i in t:
                atb = "" + sq(route_name(trip_route_id(i[0]))) + " (" + route_code(trip_route_id(i[0])) + ") "
                if stop_time(i[0], j, i[1]) == stop_dep_time(i[0], j, i[1]):
                    atb += stop_time(i[0], j, i[1])
                else:
                    atb += stop_time(i[0], j, i[1]) + "-" + stop_dep_time(i[0], j, i[1])
                atb += " uz: " + sq(stop_name(trip_stops(i[0])[-1][0]))
                atb += " [reiss " + i[0] + "] "
                c = service_calendar(trip_service_id(i[0]))
                atb += c[0] + " " + punct(c[1]) + "-" + punct(c[2])[0:len(punct(c[2]))-1]
                l.append(tuple((time_to_int(stop_time(i[0], j, i[1])), atb)))
        l.sort(key= lambda i : i[0])
        for i in l:
            print(i[1])
    elif n == "x":
        break