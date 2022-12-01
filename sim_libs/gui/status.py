from collections import defaultdict


class Status:
    def __init__(self,
                 arrivals=defaultdict(lambda: 0),
                 seller_waits=defaultdict(lambda: []),
                 scan_waits=defaultdict(lambda: []),
                 event_log = []
                 ):
        self.arrivals = arrivals
        self.seller_waits = seller_waits
        self.scan_waits = scan_waits
        self.event_log = event_log

    def register_bus_arrival(self, time, bus_id, people_created):
        self.register_arrivals(time, len(people_created))
        print(f"Bus #{bus_id} arrived at {time} with {len(people_created)} people")
        self.event_log.append({
            "event": "BUS_ARRIVAL",
            "time": round(time, 2),
            "busId": bus_id,
            "peopleCreated": people_created
        })

    def register_group_moving_from_bus_to_seller(self, people, walk_begin, walk_end, seller_line, queue_begin, queue_end,
                                                 sale_begin, sale_end):
        wait = queue_end - queue_begin
        service_time = sale_end - sale_begin
        self.register_seller_wait(queue_end, wait)
        print(
            f"Purchasing group of {len(people)} waited {wait} minutes in Line {seller_line}, needed {service_time} minutes to complete")
        self.event_log.append({
            "event": "WALK_TO_SELLER",
            "people": people,
            "sellerLine": seller_line,
            "time": round(walk_begin, 2),
            "duration": round(walk_end - walk_begin, 2)
        })
        self.event_log.append({
            "event": "WAIT_IN_SELLER_LINE",
            "people": people,
            "sellerLine": seller_line,
            "time": round(queue_begin, 2),
            "duration": round(queue_end - queue_begin, 2)
        })
        self.event_log.append({
            "event": "BUY_TICKETS",
            "people": people,
            "sellerLine": seller_line,
            "time": round(sale_begin, 2),
            "duration": round(sale_end - sale_begin, 2)
        })

    def register_visitor_moving_to_scanner(self, person, walk_begin, walk_end, scanner_line, queue_begin, queue_end,
                                           scan_begin, scan_end):
        wait = queue_end - queue_begin
        service_time = scan_end - scan_begin
        self.register_scan_wait(queue_end, wait)
        print(
            f"Scanning customer waited {wait} minutes in Line {scanner_line}, needed {service_time} minutes to complete")
        self.event_log.append({
            "event": "WALK_TO_SCANNER",
            "person": person,
            "scannerLine": scanner_line,
            "time": round(walk_begin, 2),
            "duration": round(walk_end - walk_begin, 2)
        })
        self.event_log.append({
            "event": "WAIT_IN_SCANNER_LINE",
            "person": person,
            "scannerLine": scanner_line,
            "time": round(queue_begin, 2),
            "duration": round(queue_end - queue_begin, 2)
        })
        self.event_log.append({
            "event": "SCAN_TICKETS",
            "person": person,
            "scannerLine": scanner_line,
            "time": round(scan_begin, 2),
            "duration": round(scan_end - scan_begin, 2)
        })

    def register_arrivals(self, time, num):
        self.arrivals[int(time)] += num

    def register_seller_wait(self, time, wait):
        self.seller_waits[int(time)].append(wait)

    def register_scan_wait(self, time, wait):
        self.scan_waits[int(time)].append(wait)
