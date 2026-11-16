
import heapq
import math
import tkinter as tk
from tkinter import ttk, messagebox


LOCATIONS = {
    "University": (80, 300), "Library": (205, 155), "Hospital": (345, 110),
    "Mall": (480, 175), "Airport": (650, 105), "Park": (245, 390),
    "Museum": (390, 305), "Stadium": (535, 370), "Station": (665, 315),
}

ROADS = {
    "University": {"Library": 4, "Park": 3},
    "Library": {"University": 4, "Hospital": 3, "Park": 5, "Museum": 6},
    "Hospital": {"Library": 3, "Mall": 4, "Museum": 5},
    "Mall": {"Hospital": 4, "Airport": 5, "Museum": 3, "Stadium": 5},
    "Airport": {"Mall": 5, "Station": 4},
    "Park": {"University": 3, "Library": 5, "Museum": 4, "Stadium": 6},
    "Museum": {"Library": 6, "Hospital": 5, "Mall": 3, "Park": 4, "Stadium": 3},
    "Stadium": {"Mall": 5, "Park": 6, "Museum": 3, "Station": 3},
    "Station": {"Airport": 4, "Stadium": 3},
}


def heuristic(city, goal):
    x1, y1 = LOCATIONS[city]
    x2, y2 = LOCATIONS[goal]
    return math.hypot(x2 - x1, y2 - y1) / 45


def a_star(graph, start, goal):
    frontier = [(heuristic(start, goal), 0, start)]
    came_from = {start: None}
    best_cost = {start: 0}
    explored = []

    while frontier:
        _, current_cost, current = heapq.heappop(frontier)

        if current_cost != best_cost[current]:
            continue

        explored.append(current)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1], current_cost, explored

        for neighbor, road_cost in graph[current].items():
            new_cost = current_cost + road_cost

            if neighbor not in best_cost or new_cost < best_cost[neighbor]:
                best_cost[neighbor] = new_cost
                came_from[neighbor] = current
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, new_cost, neighbor))

    return None, 0, explored


class RouteWiseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Route Wise AI | A* City Navigator")
        self.geometry("1120x690")
        self.minsize(980, 620)
        self.configure(bg="#f4f7fb")

        self.path, self.explored = [], []
        self.new_city_position = None
        self.add_city_dialog = None
        self.position_label = None
        self.start_var = tk.StringVar(value="University")
        self.goal_var = tk.StringVar(value="Airport")

        self._build_ui()
        self.draw_map()

    def _build_ui(self):
        header = tk.Frame(self, bg="#13233f", height=92)
        header.pack(fill="x")

        tk.Label(header, text="ROUTE WISE AI", font=("Segoe UI", 22, "bold"),
                 bg="#13233f", fg="white").place(x=30, y=18)

        tk.Label(header, text="Smart city navigation powered by A* Search",
                 font=("Segoe UI", 10), bg="#13233f", fg="#b9c8e8").place(x=32, y=55)

        tk.Label(header, text="f(n) = g(n) + h(n)", font=("Consolas", 16, "bold"),
                 bg="#13233f", fg="#65d6c3").place(relx=1.0, x=-36, y=32, anchor="e")

        controls = tk.Frame(self, bg="#ffffff", padx=22, pady=18)
        controls.pack(fill="x", padx=22, pady=(18, 8))

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox", padding=7, font=("Segoe UI", 10))

        tk.Label(controls, text="Start location", bg="white", fg="#42526b",
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")

        self.start_box = ttk.Combobox(
            controls, textvariable=self.start_var,
            values=list(LOCATIONS), state="readonly", width=18
        )
        self.start_box.grid(row=1, column=0, padx=(0, 18), pady=(5, 0))

        tk.Label(controls, text="Destination", bg="white", fg="#42526b",
                 font=("Segoe UI", 10, "bold")).grid(row=0, column=1, sticky="w")

        self.goal_box = ttk.Combobox(
            controls, textvariable=self.goal_var,
            values=list(LOCATIONS), state="readonly", width=18
        )
        self.goal_box.grid(row=1, column=1, padx=(0, 22), pady=(5, 0))

        tk.Button(
            controls, text="Find shortest route", command=self.find_route,
            bg="#176b87", fg="white", activebackground="#11536b",
            activeforeground="white", relief="flat", cursor="hand2",
            font=("Segoe UI", 10, "bold"), padx=20, pady=8
        ).grid(row=1, column=2)

        tk.Button(
            controls, text="Reset", command=self.reset,
            bg="#e9eef5", fg="#23344f", relief="flat",
            cursor="hand2", font=("Segoe UI", 10), padx=15, pady=8
        ).grid(row=1, column=3, padx=10)

        tk.Button(
            controls, text="+ Add city", command=self.open_add_city,
            bg="#dcf7ef", fg="#0b6b5b", relief="flat",
            cursor="hand2", font=("Segoe UI", 10, "bold"),
            padx=15, pady=8
        ).grid(row=1, column=4)

        body = tk.Frame(self, bg="#f4f7fb")
        body.pack(fill="both", expand=True, padx=22, pady=(8, 22))

        self.canvas = tk.Canvas(body, bg="white", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.choose_city_position)

        panel = tk.Frame(body, bg="white", width=272, padx=20, pady=20)
        panel.pack(side="right", fill="y", padx=(12, 0))
        panel.pack_propagate(False)

        tk.Label(
            panel, text="ROUTE INSIGHTS", bg="white", fg="#13233f",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        self.status = tk.Label(
            panel, text="Choose two places, then search.",
            wraplength=225, justify="left", bg="white",
            fg="#5d6b82", font=("Segoe UI", 10)
        )
        self.status.pack(anchor="w", pady=(8, 22))

        self.metric_labels = {}

        for title, key in [
            ("TOTAL DISTANCE", "distance"),
            ("NODES EXPLORED", "explored"),
            ("ROUTE STOPS", "stops")
        ]:
            box = tk.Frame(panel, bg="#f4f7fb", padx=12, pady=10)
            box.pack(fill="x", pady=5)

            tk.Label(
                box, text=title, bg="#f4f7fb", fg="#73819a",
                font=("Segoe UI", 8, "bold")
            ).pack(anchor="w")

            label = tk.Label(
                box, text="—", bg="#f4f7fb", fg="#176b87",
                font=("Segoe UI", 16, "bold")
            )
            label.pack(anchor="w")
            self.metric_labels[key] = label

        tk.Label(
            panel, text="HOW A* CHOOSES", bg="white",
            fg="#13233f", font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(25, 5))

        tk.Label(
            panel,
            text="g(n): road cost already travelled\nh(n): straight-line estimate\nf(n): g(n) + h(n)",
            justify="left", bg="white", fg="#5d6b82",
            font=("Segoe UI", 9)
        ).pack(anchor="w")

    def draw_map(self):
        self.canvas.delete("all")
        drawn = set()

        for city, neighbors in ROADS.items():
            x1, y1 = LOCATIONS[city]

            for neighbor, distance in neighbors.items():
                edge = tuple(sorted((city, neighbor)))

                if edge in drawn:
                    continue

                drawn.add(edge)
                x2, y2 = LOCATIONS[neighbor]

                color, width = ("#d8e0ec", 2)

                if self._is_path_edge(city, neighbor):
                    color, width = ("#f4a261", 5)

                self.canvas.create_line(
                    x1, y1, x2, y2, fill=color, width=width
                )

                mx, my = (x1 + x2) / 2, (y1 + y2) / 2

                self.canvas.create_text(
                    mx, my - 12, text=f"{distance} km",
                    fill="#73819a", font=("Segoe UI", 8, "bold")
                )

        for city, (x, y) in LOCATIONS.items():
            fill = "#fff4e6" if city in self.explored else "#eaf2fb"
            outline, text = "#f4a261", "#243b5a"

            if city == self.start_var.get():
                fill, outline, text = "#dcf7ef", "#16a085", "#0b6b5b"

            if city == self.goal_var.get():
                fill, outline, text = "#e9e4ff", "#7059c8", "#513aa2"

            self.canvas.create_oval(
                x - 28, y - 28, x + 28, y + 28,
                fill=fill, outline=outline, width=3
            )

            self.canvas.create_text(
                x, y, text=city[:3].upper(),
                fill=text, font=("Segoe UI", 9, "bold")
            )

            self.canvas.create_text(
                x, y + 42, text=city,
                fill="#42526b", font=("Segoe UI", 9, "bold")
            )

    def _is_path_edge(self, a, b):
        return any(
            {a, b} == {self.path[i], self.path[i + 1]}
            for i in range(len(self.path) - 1)
        )

    def find_route(self):
        start, goal = self.start_var.get(), self.goal_var.get()

        if start == goal:
            messagebox.showwarning(
                "Choose different locations",
                "Start and destination must be different."
            )
            return

        self.path, distance, self.explored = a_star(ROADS, start, goal)

        self.metric_labels["distance"].config(text=f"{distance:.1f} km")
        self.metric_labels["explored"].config(text=str(len(self.explored)))
        self.metric_labels["stops"].config(text=str(len(self.path)))

        self.status.config(
            text=" → ".join(self.path),
            fg="#176b87",
            font=("Segoe UI", 10, "bold")
        )

        self.draw_map()

    def reset(self):
        self.path, self.explored = [], []

        self.status.config(
            text="Choose two places, then search.",
            fg="#5d6b82", font=("Segoe UI", 10)
        )

        for label in self.metric_labels.values():
            label.config(text="—")

        self.draw_map()

    def open_add_city(self):
        if self.add_city_dialog and self.add_city_dialog.winfo_exists():
            self.add_city_dialog.focus_set()
            return

        self.new_city_position = None

        dialog = tk.Toplevel(self)
        self.add_city_dialog = dialog
        dialog.title("Add a city to the graph")
        dialog.configure(bg="white")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        frame = tk.Frame(dialog, bg="white", padx=24, pady=22)
        frame.pack()

        tk.Label(
            frame, text="Add a city", bg="white", fg="#13233f",
            font=("Segoe UI", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        tk.Label(
            frame, text="The city will be connected to one existing city.",
            bg="white", fg="#5d6b82", font=("Segoe UI", 9)
        ).grid(row=1, column=0, columnspan=2, sticky="w", pady=(3, 16))

        tk.Label(
            frame, text="City name", bg="white", fg="#42526b",
            font=("Segoe UI", 9, "bold")
        ).grid(row=2, column=0, sticky="w")

        self.city_name_entry = tk.Entry(frame, width=26, font=("Segoe UI", 10))
        self.city_name_entry.grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=(4, 12)
        )

        tk.Label(
            frame, text="Connect to", bg="white", fg="#42526b",
            font=("Segoe UI", 9, "bold")
        ).grid(row=4, column=0, sticky="w")

        self.connect_var = tk.StringVar(value=list(LOCATIONS)[0])

        self.connect_box = ttk.Combobox(
            frame, textvariable=self.connect_var,
            values=list(LOCATIONS), state="readonly", width=23
        )
        self.connect_box.grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(4, 12)
        )

        tk.Label(
            frame, text="Road distance in km", bg="white",
            fg="#42526b", font=("Segoe UI", 9, "bold")
        ).grid(row=6, column=0, sticky="w")

        self.distance_entry = tk.Entry(frame, width=26, font=("Segoe UI", 10))
        self.distance_entry.grid(
            row=7, column=0, columnspan=2, sticky="ew", pady=(4, 12)
        )

        self.position_label = tk.Label(
            frame, text="Location: not selected",
            bg="white", fg="#b35c00", font=("Segoe UI", 9)
        )
        self.position_label.grid(row=8, column=0, sticky="w")

        tk.Button(
            frame, text="Choose location on map",
            command=self.start_position_pick,
            bg="#e9eef5", fg="#23344f", relief="flat",
            cursor="hand2", padx=10, pady=6
        ).grid(row=8, column=1, sticky="e")

        tk.Button(
            frame, text="Save city", command=self.save_city,
            bg="#176b87", fg="white", relief="flat",
            cursor="hand2", font=("Segoe UI", 10, "bold"),
            padx=18, pady=7
        ).grid(row=9, column=0, columnspan=2, pady=(18, 0))

        self.city_name_entry.focus_set()

    def start_position_pick(self):
        self.add_city_dialog.grab_release()
        self.add_city_dialog.withdraw()

        self.status.config(
            text="Click a free location on the map for the new city.",
            fg="#b35c00", font=("Segoe UI", 10, "bold")
        )

    def choose_city_position(self, event):
        if not self.add_city_dialog or not self.add_city_dialog.winfo_exists():
            return

        nearest_city, nearest_distance = min(
            (
                (city, math.dist((event.x, event.y), position))
                for city, position in LOCATIONS.items()
            ),
            key=lambda item: item[1],
        )

        if nearest_distance < 82:
            self.add_city_dialog.deiconify()
            self.add_city_dialog.lift()
            self.add_city_dialog.grab_set()

            messagebox.showwarning(
                "Choose a free map area",
                f"This point is too close to {nearest_city}. Choose a location at least one node-width away.",
                parent=self.add_city_dialog,
            )
            return

        self.new_city_position = (event.x, event.y)

        self.position_label.config(
            text=f"Location: ({event.x}, {event.y}) selected",
            fg="#0b6b5b"
        )

        self.add_city_dialog.deiconify()
        self.add_city_dialog.lift()
        self.add_city_dialog.grab_set()
        self.add_city_dialog.focus_set()

    def save_city(self):
        name = self.city_name_entry.get().strip()
        connected_city = self.connect_var.get()

        try:
            distance = float(self.distance_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid distance",
                "Enter a positive number for the road distance.",
                parent=self.add_city_dialog
            )
            return

        if not name:
            messagebox.showerror(
                "Missing city name",
                "Enter a name for the new city.",
                parent=self.add_city_dialog
            )
            return

        if name in LOCATIONS:
            messagebox.showerror(
                "City already exists",
                "Choose a different city name.",
                parent=self.add_city_dialog
            )
            return

        if distance <= 0:
            messagebox.showerror(
                "Invalid distance",
                "Road distance must be greater than zero.",
                parent=self.add_city_dialog
            )
            return

        if self.new_city_position is None:
            messagebox.showerror(
                "Choose a map location",
                "Click 'Choose location on map', then click the map.",
                parent=self.add_city_dialog
            )
            return

        LOCATIONS[name] = self.new_city_position
        ROADS[name] = {connected_city: distance}
        ROADS[connected_city][name] = distance

        self.refresh_location_lists()

        self.path, self.explored = [], []

        self.status.config(
            text=f"{name} was added and connected to {connected_city} ({distance:g} km).",
            fg="#0b6b5b", font=("Segoe UI", 10, "bold")
        )

        self.add_city_dialog.destroy()
        self.add_city_dialog = None
        self.draw_map()

    def refresh_location_lists(self):
        cities = list(LOCATIONS)
        self.start_box["values"] = cities
        self.goal_box["values"] = cities


if __name__ == "__main__":
    RouteWiseApp().mainloop()
