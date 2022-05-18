from passenger import *


class Passengers:
    def __init__(self):
        # Store the center positions of the objects
        self.passengers = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0
        self.entered
        self.exited
        self.count
        
    def setArea(self, area):
        self.area = area
        
    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, passenger in self.passengers.items():
                dist = math.hypot(cx - passenger.cx, cy - passenger.cy)
                if passenger.cy > cy:
                    direction = 'In'
                else:
                    direction = 'Out'

                # print(dist)
                if dist < 100:
                    self.passengers[id].cx = cx
                    self.passengers[id].cy = cy
                    self.passengers[id].ttl = 30

                    objects_bbs_ids.append([x, y, w, h, id, direction])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.passengers[self.id_count] = Passenger(self.id_count, rect)
                objects_bbs_ids.append([x, y, w, h, self.id_count, None])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        self.__update_ttl()

        new_center_points = {}

        for id, p in self.passengers.items():
            new_center_points[id] = (p.cx, p.cy)

        return objects_bbs_ids

    def __update_ttl(self):
        to_remove = []
        for id, p in self.passengers.items():
            if self.passengers[p.id].ttl == 0:
                to_remove.append(p.id)
            else:
                self.passengers[p.id].ttl -= 1

        for pid in to_remove:
            if self.passengers[pid].direction != 0 and self.passengers[p.id].cy > self.area[1]:
                self.exited += 1
            elif self.passengers[pid].direction != 0 and self.passengers[p.id].cy > self.area[1]:
                self.entered += 1
                
            self.count = self.entered - self.exited
            del self.passengers[pid]

    def get_counter(self):
        return self.id_count
    
    def get_count(self):
        return (self.entered, self.exited, self.count)
