import random
from sim_libs.gui.calculate import Calc as calc
from sim_libs.gui.sim_env import SimEnv as SimEnv


class Customer:
    @staticmethod
    def purchasing_customer(env, stat, config, seller_canvas, scanners_canvas, people_processed, seller_lines, scanner_lines):
        walk_begin = env.now
        yield env.timeout(random.gauss(config.TIME_TO_WALK_TO_SELLERS_MEAN, config.TIME_TO_WALK_TO_SELLERS_STD))
        walk_end = env.now

        queue_begin = env.now
        seller_line = calc.pick_shortest(seller_lines)
        with seller_line[0].request() as req:
            # Wait in line
            seller_canvas.add_to_line(seller_line[1])
            yield req
            seller_canvas.remove_from_line(seller_line[1])
            queue_end = env.now

            # Buy tickets
            sale_begin = env.now
            yield env.timeout(random.gauss(config.SELLER_MEAN, config.SELLER_STD))
            sale_end = env.now

            stat.register_group_moving_from_bus_to_seller(people_processed, walk_begin, walk_end, seller_line[1],
                                                          queue_begin, queue_end, sale_begin, sale_end)

            env.process(Customer.scanning_customer(env, stat, config, scanners_canvas, people_processed, scanner_lines, config.TIME_TO_WALK_TO_SCANNERS_MEAN,
                                          config.TIME_TO_WALK_TO_SCANNERS_STD))

    @staticmethod
    def scanning_customer(env, stat, config, scanners, people_processed, scanner_lines, walk_duration, walk_std):
        # Walk to the seller
        walk_begin = env.now
        yield env.timeout(random.gauss(walk_duration, walk_std))
        walk_end = env.now

        # We assume that the visitor will always pick the shortest line
        queue_begin = env.now
        scanner_line = calc.pick_shortest(scanner_lines)
        with scanner_line[0].request() as req:
            # Wait in line
            for _ in people_processed: scanners.add_to_line(scanner_line[1])
            yield req
            for _ in people_processed: scanners.remove_from_line(scanner_line[1])
            queue_end = env.now

            # Scan each person's tickets
            for person in people_processed:
                scan_begin = env.now
                yield env.timeout(random.gauss(config.SCANNER_MEAN, config.SCANNER_STD))  # Scan their ticket
                scan_end = env.now
                stat.register_visitor_moving_to_scanner(person, walk_begin, walk_end, scanner_line[1], queue_begin,
                                                        queue_end, scan_begin, scan_end)
