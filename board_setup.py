import json
import os
from entities.space import LinkedSpaceList, Space
from properties import Property

def generate_spaces(space_json, property_json, screen_width, screen_height, scene):
    screen_size = min(screen_width, screen_height)
    with open(space_json, 'r') as file:
        space_data = json.load(file)

    num_spaces = len(space_data)
    assert num_spaces % 4 == 0  # The total number of spaces needs to be divisible by 4 (one space for each side)
    num_each_side = (num_spaces // 4) + 1

    # Setup sizes
    board_margin = 35
    board_width = screen_size - 2 * board_margin
    s = board_width // num_each_side

    # Directions, assuming clockwise orientation
    directions = [
        (-1,0),
        (0,-1),
        (1,0),
        (0,1)
    ]

    # Space generation
    space_list = LinkedSpaceList()

    def create_space(scene, x1, y1, info):
        new_space = Space(scene, x1, y1, s, info["space_type"], info["pass_reward"], info["name"], info["icon"], info["color"])
        
        # If a property, set up the appropriate property info
        if info["space_type"] == "PROPERTY":
            with open(property_json, 'r') as file:
                property_info = json.load(file)
            new_space.property = Property(new_space.text, property_info[new_space.text]["value"], property_info[new_space.text]["base_tax"])
        
        # Determine quadrant
        x, y = new_space.rect.x, new_space.rect.y
        c_x, c_y = screen_width // 2, screen_height // 2
        if x >= c_x and y >= c_y:
            new_space.quadrant_idx = 1
        elif x < c_x and y >= c_y:
            new_space.quadrant_idx = 2
        elif x < c_x and y < c_y:
            new_space.quadrant_idx = 3
        elif x >= c_x and y < c_y:
            new_space.quadrant_idx = 4

        return new_space

    # Start with bottom right
    x1, y1 = screen_size - board_margin - s, screen_size - board_margin - s
    curr_space = create_space(scene, x1, y1, space_data[0])
    space_list.set_head_space(curr_space)

    d_idx = 0
    for i in range(1, num_spaces):
        d = directions[d_idx % 4]
        dx = d[0] * (s + 1) # +1 for some padding between spaces
        dy = d[1] * (s + 1)
        x1, y1 = x1 + dx, y1 + dy
        new_space = create_space(scene, x1, y1, space_data[i])
        curr_space.set_next_space(new_space)
        curr_space = new_space
        if i % (num_each_side - 1) == 0:
            d_idx += 1

    curr_space.set_next_space(space_list.get_head_space())
    
    return space_list

def load_test_board(screen_width, screen_height, scene):
    """For testing purposes only"""
    space_json = os.path.join("space_data.json")
    property_json = os.path.join("property_data.json")
    return generate_spaces(space_json, property_json, screen_width, screen_height, scene)

def load_real_board(screen_width, screen_height):
    """The real deal"""
    pass
