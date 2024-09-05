import collections


def breadth_first_search(start, end, obstacles, grid_size, width, height):
    def is_valid_position(pos):
        x, y = pos
        return (
            0 <= x < width // grid_size
            and 0 <= y < height // grid_size
            and pos not in visited
            and pos not in obstacle_positions
        )

    def get_adjacent_positions(pos):
        x, y = pos
        adjacent = [
            (x, y + 1),
            (x + 1, y),
            (x, y - 1),
            (x - 1, y),
        ]  # Up, Right, Down, Left
        return [pos for pos in adjacent if is_valid_position(pos)]

    def to_pixel_coordinates(path):
        return [(x * grid_size, y * grid_size) for x, y in path]

    queue = collections.deque([[start]])
    visited = set([start])
    obstacle_positions = {
        (obs.rect.x // grid_size, obs.rect.y // grid_size) for obs in obstacles
    }

    while queue:
        path = queue.popleft()
        current_pos = path[-1]

        if current_pos == end:
            return to_pixel_coordinates(path)

        for next_pos in get_adjacent_positions(current_pos):
            new_path = path + [next_pos]
            queue.append(new_path)
            visited.add(next_pos)

    return []  # No path found
