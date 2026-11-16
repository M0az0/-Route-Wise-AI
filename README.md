# 🗺️ Route Wise AI
### Smart City Navigation Using the A* Search Algorithm

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Algorithm](https://img.shields.io/badge/Algorithm-A*-16A085?style=for-the-badge)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

</p>

---

## 📌 Project Overview

**Route Wise AI** is a Python desktop application that demonstrates intelligent route finding using the **A* (A-Star) Search Algorithm**.

The application represents a city as a weighted graph, where locations are nodes and roads are edges with distances measured in kilometers.

Users can select a starting location and a destination, then use A* search to explore the graph and find a route based on actual road distances and estimated remaining distances.

The application provides an interactive visual map, route highlighting, search statistics, and the ability to dynamically add new locations.

## 👥 Project Team

| Role | Name | Student ID |
|---|---|---|
| Student 1 | Moaz Mohamed | 24030257 |
| Student 2 | Yousef Hany | 25030532 |

### 🎓 Academic Information

| Field | Details |
|---|---|
| Course Name | Fundamentals of AI |
| Course Code | CF321 |
| Teaching Assistants | Kaled Tarek & Khalid Walid |

---

## ✨ Main Features

- 📍 **Location Selection:** Choose a starting city and destination from dropdown menus.
- 🧠 **A* Search Algorithm:** Search for a route using the evaluation function \(f(n)=g(n)+h(n)\).
- 🗺️ **Interactive City Map:** Visualize locations and their road connections.
- 🛣️ **Route Highlighting:** Display the selected route using highlighted roads.
- 📏 **Distance Calculation:** Display the total road distance in kilometers.
- 🔍 **Search Statistics:** Show the number of explored nodes and route stops.
- ➕ **Dynamic City Addition:** Add new locations while the application is running.
- 🔗 **Graph Connectivity:** Connect newly added locations to existing cities with weighted edges.
- 🚫 **Position Validation:** Prevent new locations from being placed too close to existing map nodes.
- 🔄 **Reset Function:** Clear the previous search results and restore the initial map display.

---

## 🧠 A* Search Algorithm

The A* algorithm is an informed search algorithm that evaluates possible paths using three main values:

\[
f(n)=g(n)+h(n)
\]

Where:

| Symbol | Description |
|---|---|
| \(g(n)\) | Actual cost from the starting location to the current location. |
| \(h(n)\) | Estimated remaining distance from the current location to the destination. |
| \(f(n)\) | Estimated total path cost through the current location. |

### How It Works

1. Initialize the starting location.
2. Calculate its evaluation function.
3. Select the candidate with the lowest priority from the priority queue.
4. Explore its neighboring locations.
5. Calculate the new path cost.
6. Update the best-known cost when a shorter path is found.
7. Continue until the destination is reached or no possible paths remain.
8. Reconstruct and display the resulting route.

### Heuristic Function

The application uses the Euclidean distance between two locations as its heuristic estimate.

\[
h(n)=\frac{\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}}{45}
\]

The coordinates of each location are used to estimate the straight-line distance to the destination.

---

## 🖥️ Application Interface

The application includes a visual city map and a route information panel.

### Interface Components

| Component | Function |
|---|---|
| Start Location | Select the starting city. |
| Destination | Select the target city. |
| Find Shortest Route | Execute the A* search. |
| Reset | Clear previous search results. |
| Add City | Add a new location to the graph. |
| Route Insights | Display route information and search statistics. |
| City Map | Visualize locations and road connections. |

### Route Visualization

- 🟠 **Orange Roads:** Roads included in the selected route.
- 🟢 **Green Location:** Starting location.
- 🟣 **Purple Location:** Destination.
- 🔵 **Blue Locations:** Other locations.
- 🟠 **Explored Locations:** Locations visited during the search.

---

## 🚀 Installation & Execution

### Requirements

- Python 3.10 or newer.
- Tkinter (included with standard Python installations on Windows).

**No external libraries or additional pip installations are required.**

### 1. Clone the Repository

```bash
git clone YOUR_REPOSITORY_URL
```

### 2. Open the Project Folder

```bash
cd route-wise-ai
```

### 3. Run the Application

```bash
python route_wise_ai.py
```

The desktop application will open automatically.

---

## 🎯 Example Usage

Try the following example using the initial city map:

**Starting Location:** University

**Destination:** Airport

**Expected Route:**

```text
University
    ↓
Park
    ↓
Museum
    ↓
Mall
    ↓
Airport
```

**Route Information:**

| Metric | Result |
|---|---|
| Starting Location | University |
| Destination | Airport |
| Total Distance | 15 km |
| Number of Route Stops | 5 |

The route is calculated using the road weights stored in the graph.

---

## ➕ Adding a New City

Route Wise AI allows users to extend the city graph without modifying the source code.

### Steps

1. Click the **+ Add City** button.
2. Enter the new city name.
3. Select an existing city to connect to.
4. Enter the road distance in kilometers.
5. Click **Choose Location on Map**.
6. Select an available position on the map.
7. Click **Save City**.

### Graph Update

When a new city is added, the application updates the location dictionary and the road connections:

```python
LOCATIONS[new_city] = (x, y)

ROADS[new_city] = {
    connected_city: distance
}

ROADS[connected_city][new_city] = distance
```

The new location immediately becomes available in both selection menus and can be used in subsequent A* searches.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language. |
| Tkinter | Desktop graphical user interface. |
| Heapq | Priority queue implementation. |
| Math | Euclidean distance and coordinate calculations. |
| A* Search | Intelligent route-finding algorithm. |
| Graph Theory | Representing locations and road connections. |

---

## 📁 Project Structure

```text
Route-Wise-AI/
│
├── route_wise_ai.py
│
└── README.md
```

| File | Description |
|---|---|
| `route_wise_ai.py` | Main application containing the graph, A* algorithm, and graphical interface. |
| `README.md` | Project documentation and usage instructions. |

---

## 🎓 Learning Objectives

This project demonstrates practical applications of fundamental Artificial Intelligence concepts:

- Understanding informed search algorithms.
- Implementing the A* search algorithm.
- Applying heuristic functions.
- Representing real-world problems using weighted graphs.
- Using priority queues for efficient search.
- Visualizing search results through a graphical interface.
- Dynamically modifying graph structures.

---

## 📄 License

This project was developed as an academic project for the Fundamentals of AI course (CF321).

