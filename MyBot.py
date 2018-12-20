import hlt
from hlt import constants
from hlt.positionals import Direction
import random
import logging

game = hlt.Game()

# As soon as you call "ready" function below, the 2 second per turn timer will start.
game.ready("test_bot001")

logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))

ship_status = {}


while True:
    game.update_frame()

    me = game.me
    game_map = game.game_map
    #logging.info(game_map)

    command_queue = []

    direction_order = [Direction.North, Direction.South, Direction.East, Direction.West, Direction.Still]
    logging.info(direction_order)
    for ship in me.get_ships():
        position_options = ship.position.get_surrounding_cardinals() + [ship.position]
        
        #logging.info(position_options)

        # {(0,-1): (16,22)}
        position_dict = {}

        # {(0,-1): 200}
        halite_dict = {}

        for n, direction in enumerate(direction_order):
            position_dict[direction] = position_options[n]
            #logging.info(position_dict)

        for direction in position_dict:
            position = position_dict[direction]
            halite_amount = game_map[position].halite_amount
            halite_dict[direction] = halite_amount
            #logging.info(halite_dict)


        if ship.id not in ship_status:
            ship_status[ship.id] = 'moving'
        
        #logging.info(ship_status[ship.id])
        #logging.info(game_map[ship.position].halite_amount)
        #logging.info(ship.halite_amount)

        #logging.info(command_queue)

        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 and ship.is_full != True and ship_status[ship.id] != 'returning': #or ship.is_full:
            move=max(halite_dict, key=halite_dict.get)
            #logging.info(move)
            command_queue.append(ship.move(move))
                    #random.choice([ Direction.North, Direction.South, Direction.East, Direction.West ])))
            ship_status[ship.id] = 'moving'
            #logging.info('moving')

        elif ship.is_full != True and ship_status[ship.id] != 'returning':
            command_queue.append(ship.stay_still())
            ship_status[ship.id] = 'staying_still'

        elif ship.position != me.shipyard.position:
            move = game_map.naive_navigate(ship, me.shipyard.position)
            command_queue.append(ship.move(move))
            #command_queue.append(ship.move(game_map.naive_navigate(ship, me.shipyard.position)))
            ship_status[ship.id] = 'returning'
            #logging.info(game_map.get_unsafe_moves(ship.position, me.shipyard.position))
            #logging.info(move)
            #logging.info(ship.position)
            #logging.info(me.shipyard.position)
            #logging.info('normalize')
            #logging.info(game_map.normalize(ship.position))
            #logging.info(game_map.normalize(me.shipyard.position))


        else:
            ship_status[ship.id] = 'moving'
            command_queue.append(
                ship.move(max(halite_dict, key=halite_dict.get)))

        #logging.info(ship_status)
        #logging.info(command_queue)
    
        #logging.info(game_map[me.shipyard])
        #logging.info(game_map[me.shipyard.position])
        #logging.info(me.shipyard)
        #logging.info(me.shipyard.position)
        #logging.info(game_map.naive_navigate(ship, me.shipyard.position))
        #logging.info(me.halite_amount)


    if game.turn_number <= 1 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(game.me.shipyard.spawn())

    if game.turn_number >= 199 and me.halite_amount >= constants.SHIP_COST \
    and not game_map[me.shipyard].is_occupied and len(me.get_ships()) < 2:
        command_queue.append(game.me.shipyard.spawn())

    #if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied: 
    #    command_queue.append(me.shipyard.spawn())

    #logging.info(me.get_ships())
    game.end_turn(command_queue)