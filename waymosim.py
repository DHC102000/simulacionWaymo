import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import time

class SimpleWaymoEnv:
    def __init__(self, n_agentes=5):
        self.n_agentes = n_agentes
        self.calle_width = 10
        self.calle_length = 100
        self.meta_y = 90
        self.reset()

    def reset(self):
        self.auto = {
            "x": self.calle_width / 2,
            "y": 0,
            "vy": 2.0    
        }

        self.agentes = []
        for _ in range(self.n_agentes):
            self.agentes.append({
                "x": np.random.uniform(0, self.calle_width),
                "y": np.random.uniform(10, self.calle_length),
                "vx": np.random.uniform(-0.3, 0.3),
                "vy": np.random.uniform(-0.3, 0.3)
            })

        return np.array([self.auto["x"], self.auto["y"]])


    def step(self):
        cx = self.auto["x"]
        cy = self.auto["y"]

        parar = False
        distancia = 12   
        side_threshold = 3      

        for a in self.agentes:
            dx = a["x"] - cx
            dy = a["y"] - cy

            if dy <= 0:
                continue

            if abs(dx) > side_threshold:
                continue

            if dy < distancia:
                parar = True
                break

        if not parar:
            self.auto["y"] += self.auto["vy"]

        for a in self.agentes:
            a["x"] += a["vx"]
            a["y"] += a["vy"]

            if a["x"] < 0 or a["x"] > self.calle_width:
                a["vx"] *= -1
            if a["y"] < 0 or a["y"] > self.calle_length:
                a["vy"] *= -1

        done = self.auto["y"] >= self.meta_y
        return np.array([self.auto["x"], self.auto["y"]]), done

    def render(self, ax):
        ax.clear()

        ax.plot([0, self.calle_width, self.calle_width, 0, 0],
                [0, 0, self.calle_length, self.calle_length, 0],
                'k-')

        ax.axhline(self.meta_y, color="green", linestyle="--", label="Meta")

        ax.plot(self.auto["x"], self.auto["y"], "bo", markersize=12, label="Auto")

        xs = [a["x"] for a in self.agentes]
        ys = [a["y"] for a in self.agentes]
        ax.scatter(xs, ys, c="red", label="Agentes Chocadores")

        ax.set_xlim(-2, self.calle_width + 2)
        ax.set_ylim(-2, self.calle_length + 2)
        ax.set_title("Simulación Auto Esquivador")
        ax.legend()

plt.ion()
fig, ax = plt.subplots(figsize=(5, 10))

env = SimpleWaymoEnv()

while True:
    state = env.reset()
    done = False

    while not done:
        state, done = env.step()
        env.render(ax)
        plt.pause(0.05)

    time.sleep(0.5)
