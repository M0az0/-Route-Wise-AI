# Route Wise AI – Algorithm Diagrams

## 1. Graph Representation

```text
LOCATIONS: city -> (x, y) coordinates

ROADS: city -> {connected_city: distance_in_km}
```

## 2. A* Search Algorithm

```text
f(n) = g(n) + h(n)

g(n): Known road distance from start to n.

h(n): Straight-line estimate from n to destination.
```

## 3. Dynamic City Addition

```python
LOCATIONS[new_city] = (x, y)

ROADS[new_city] = {connected_city: distance}

ROADS[connected_city][new_city] = distance
```
