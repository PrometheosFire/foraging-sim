import numpy as np
from collections import defaultdict

PRECOMPUTED_OFFSETS = {
    0: [[(0, 0)]],
    1: [
        [(0, 0)],
        [(-1, 0), (1, 0), (0, -1), (0, 1),
         (-1, -1), (-1, 1), (1, -1), (1, 1)]
    ],
    2: [
        [(0, 0)],
        [(-1, 0), (1, 0), (0, -1), (0, 1),
         (-1, -1), (-1, 1), (1, -1), (1, 1)],
        [(-2, 0), (2, 0), (0, -2), (0, 2),
         (-2, -1), (-2, 1), (2, -1), (2, 1),
         (-1, -2), (1, -2), (-1, 2), (1, 2),
         (-2, -2), (-2, 2), (2, -2), (2, 2)]
    ],
    3: [
        [(0, 0)],
        [(-1, 0), (1, 0), (0, -1), (0, 1),
         (-1, -1), (-1, 1), (1, -1), (1, 1)],
        [(-2, 0), (2, 0), (0, -2), (0, 2),
         (-2, -1), (-2, 1), (2, -1), (2, 1),
         (-1, -2), (1, -2), (-1, 2), (1, 2),
         (-2, -2), (-2, 2), (2, -2), (2, 2)],
        [(-3, 0), (3, 0), (0, -3), (0, 3),
         (-3, -1), (-3, 1), (3, -1), (3, 1),
         (-1, -3), (1, -3), (-1, 3), (1, 3),
         (-2, -3), (2, -3), (-2, 3), (2, 3),
         (-3, -2), (-3, 2), (3, -2), (3, 2),
         (-3, -3), (-3, 3), (3, -3), (3, 3)]
    ]
}


class SpatialGrid:
    def __init__(self, domain_size=1.0, cell_size=0.08):
        self.domain_size = domain_size
        self.cell_size = cell_size
        self.grid = defaultdict(list)
        self.grid_width = int(self.domain_size / self.cell_size)

    def _cell_index(self, pos):
        """Convert position to wrapped grid cell index"""
        x = pos[0] #% self.domain_size
        y = pos[1] #% self.domain_size
        return (int(x / self.cell_size), int(y / self.cell_size))

    def _periodic_distance(self, p1, p2):
        """Toroidal distance between p1 and p2 in a periodic domain"""
        d = np.abs(p1 - p2)
        d = np.where(d > self.domain_size / 2, self.domain_size - d, d)
        return np.linalg.norm(d)

    def clear(self):
        """Clear all stored resources"""
        self.grid.clear()

    def remove(self, pos):
        """Remove a resource at position pos from the grid"""
        cell = self._cell_index(pos)
        #if cell in self.grid:
        #    try:
        self.grid[cell].remove(pos)
        #if not self.grid[cell]:
        #    del self.grid[cell]  # clean up empty cells
        #    except ValueError:
        #        pass  # resource not found in that cell

    def insert(self, pos):
        """Insert a resource at position pos (2D)"""
        cell = self._cell_index(pos)
        self.grid[cell].append(pos)

    def insert_many(self, positions):
        """
        Insert multiple resource positions (Nx2 NumPy array)
        """
        for pos in positions:
            self.insert(tuple(pos))

    def _generate_circle_offsets(self, range_cells):
        """Generate cell offsets by ring level (level 0 first, then 1, 2...)"""
        seen = set()
        levels = []
        for r in range(range_cells + 1):
            level = []
            for dx in range(-r, r + 1):
                for dy in range(-r, r + 1):
                    if max(abs(dx), abs(dy)) == r and (dx, dy) not in seen:
                        seen.add((dx, dy))
                        level.append((dx, dy))
            levels.append(level)
        return levels

    def nearby(self, pos, radius):
        """Return all resource positions within radius of pos"""
        cx, cy = self._cell_index(pos)

        range_cells = int(np.ceil(radius / self.cell_size))
        offset_levels = PRECOMPUTED_OFFSETS.get(range_cells)
        
        if offset_levels is None:
            offset_levels = self._generate_circle_offsets(range_cells)

        nearby_resources = []
        for level in offset_levels:
            for dx, dy in level:
                nx = (cx + dx) % self.grid_width
                ny = (cy + dy) % self.grid_width
                cell = (nx, ny)

                nearby_resources += self.grid.get(cell, [])

            if nearby_resources:
                return nearby_resources

        return nearby_resources
    
    def all_resources(self):
        """Return a flat list of all resource positions in the grid"""
        return [res for cell in self.grid.values() for res in cell]
