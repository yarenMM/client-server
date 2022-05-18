from passenger import *
import const
import socket

class Passengers:
    def __init__(self, area, distance, ttl):
        # Store the center positions of the objects
        self.passengers = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.area = area
        self.entered = 0
        self.exited = 0
        self.count = 0
        self.distance = distance
        self.ttl = ttl
        self.max_ttl = ttl

        self.ClientSocket = socket.socket()
        #self.host = '127.0.0.1'
        self.host = '192.168.186.20'
        self.port = 1234

        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))

    def update(self, objects_rect):
     

        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + w) // 2
            cy = (y + h) // 2
            #print(cy)
            # Find out if that object was detected already
            same_object_detected = False
            for id, passenger in self.passengers.items():
                dist = math.hypot(cx - passenger.cx, cy - passenger.cy)
                print('(', self.passengers[id].cx, ',', self.passengers[id].cy, ',' , id ,',',self.passengers[id].ttl,'),')
                if passenger.init_coord_y < self.area[0]:
                    if passenger.cy > self.area[0]:
                        passenger.passed_upper = True
                    if passenger.cy > self.area[1]:
                        passenger.passed_lower = True
                elif passenger.init_coord_y > self.area[1]:
                    if passenger.cy < self.area[0]:
                        passenger.passed_upper = True
                    if passenger.cy < self.area[1]:
                        passenger.passed_lower = True

                # print(dist)
                if dist < self.distance:
                    if passenger.cy > cy and cy > self.area[0]:
                        passenger.direction += 1
                    elif passenger.cy < cy and cy < self.area[1]:
                        passenger.direction -= 1

                    self.passengers[id].cx = cx
                    self.passengers[id].cy = cy
                    self.passengers[id].ttl = self.ttl

                    objects_bbs_ids.append([x, y, w, h, id, passenger.direction])
                    
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.passengers[self.id_count] = Passenger(self.id_count, rect, self.ttl)
                objects_bbs_ids.append([x, y, w, h, self.id_count, 0])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        self.__update_ttl(self.ClientSocket)

        new_center_points = {}

        for id, p in self.passengers.items():
            new_center_points[id] = (p.cx, p.cy)


        #ClientSocket.close()
        return objects_bbs_ids



    def __update_ttl(self,ClientSocket):
        to_remove = []

        for id, p in self.passengers.items():
            if self.passengers[p.id].ttl <= 0:
                to_remove.append(p.id)
                print('appended')
                
            if self.area[0] <= self.passengers[id].init_coord_y <= self.area[1] and self.passengers[id].ttl < (self.max_ttl - 5):
                to_remove.append(p.id)

        self.remove(to_remove,ClientSocket)

        to_remove = []

        for id, p in self.passengers.items():
            if self.passengers[p.id].ttl <= 0 and self.passed_both(p.id):
                to_remove.append(p.id)
                print('appended lower')
                #print(id, p, self.area, self.passengers[p.id].cy)
            else:
                self.passengers[p.id].ttl -= 1
                print(self.passed_both(p.id), '(', self.passengers[id].cx, ',', self.passengers[id].cy, ',' , id ,',',self.passengers[id].ttl,'),')
                
        self.remove(to_remove,ClientSocket)
        
    def remove(self, to_remove,ClientSocket):
        for pid in to_remove:
            #print(self.passengers[pid].direction, self.passengers[p.id].cy, p.id, pid, self.area[0])
            if self.passengers[pid].direction < 0 and self.passengers[pid].cy > self.area[1] and self.passengers[pid].init_coord_y < self.area[0]:
                self.exited += 1
                info = "0"
                ClientSocket.send(str.encode(info))
            elif self.passengers[pid].direction > 0 and self.passengers[pid].cy < self.area[0] and self.passengers[pid].init_coord_y > self.area[1]:
                self.entered += 1
                info = "1"
                ClientSocket.send(str.encode(info))

            self.count = self.entered - self.exited
            print(int(self.entered), int(self.exited))
            del self.passengers[pid]

    def get_counter(self):
        return self.id_count

    def get_count(self):
        return (self.entered, self.exited, self.count)

    def passed_both(self, pid):
        return self.passengers[pid].passed_upper and self.passengers[pid].passed_lower
