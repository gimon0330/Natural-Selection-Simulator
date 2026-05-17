"""Natural Selection Simulator

A small Pygame simulation for visualizing natural selection.

The model is intentionally simple:
- Black circles are prey.
- Red circles are predators.
- During daytime, both move around the field.
- Predators eat prey on collision.
- At the end of each day, surviving prey reproduce.
- Offspring inherit speed and size with small random mutations.
- Traits that help prey survive become more common over generations.

Run:
    python main.py

Controls:
    SPACE  pause / resume
    R      reset simulation
    ESC    quit
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from statistics import mean
from typing import List, Tuple

import pygame


WIDTH = 1080
HEIGHT = 720
FPS = 60
DAY_SECONDS = 8.0
BACKGROUND = (248, 248, 245)
TEXT = (34, 34, 34)
PREY_COLOR = (30, 42, 56)
PREDATOR_COLOR = (226, 77, 77)
ACCENT = (78, 122, 199)


@dataclass
class SimulationConfig:
    initial_prey: int = 120
    initial_predators: int = 6
    prey_base_energy_cost: float = 0.0007
    prey_mutation_rate: float = 0.08
    prey_mutation_strength: float = 0.16
    prey_max_population: int = 420
    predator_starvation_threshold: int = 4
    predator_reproduction_threshold: int = 12
    predator_max_population: int = 18


@dataclass
class Stats:
    day: int = 1
    elapsed_in_day: float = 0.0
    history: List[Tuple[int, int, float, float]] = field(default_factory=list)

    def record(self, prey: List["Prey"], predators: List["Predator"]) -> None:
        if prey:
            avg_speed = mean(p.speed for p in prey)
            avg_size = mean(p.radius for p in prey)
        else:
            avg_speed = 0.0
            avg_size = 0.0
        self.history.append((len(prey), len(predators), avg_speed, avg_size))
        self.history = self.history[-160:]


class Creature:
    def __init__(self, x: float, y: float, speed: float, radius: float, color: Tuple[int, int, int]):
        self.pos = pygame.Vector2(x, y)
        self.angle = random.uniform(0, math.tau)
        self.speed = speed
        self.radius = radius
        self.color = color

    @property
    def velocity(self) -> pygame.Vector2:
        return pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * self.speed

    def random_walk(self, dt: float, turn_strength: float) -> None:
        self.angle += random.gauss(0, turn_strength) * dt
        self.pos += self.velocity * dt
        self._bounce()

    def _bounce(self) -> None:
        if self.pos.x < self.radius:
            self.pos.x = self.radius
            self.angle = math.pi - self.angle
        elif self.pos.x > WIDTH - self.radius:
            self.pos.x = WIDTH - self.radius
            self.angle = math.pi - self.angle

        if self.pos.y < self.radius:
            self.pos.y = self.radius
            self.angle = -self.angle
        elif self.pos.y > HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.angle = -self.angle

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, self.color, self.pos, int(self.radius))


class Prey(Creature):
    def __init__(self, x: float, y: float, speed: float | None = None, radius: float | None = None):
        super().__init__(
            x=x,
            y=y,
            speed=speed if speed is not None else random.uniform(70, 185),
            radius=radius if radius is not None else random.uniform(4, 13),
            color=PREY_COLOR,
        )

    def update(self, dt: float, predators: List["Predator"]) -> None:
        nearest = self._nearest_predator(predators)
        if nearest is not None:
            distance = self.pos.distance_to(nearest.pos)
            if distance < 110:
                away = self.pos - nearest.pos
                if away.length_squared() > 0:
                    self.angle = math.atan2(away.y, away.x)
                    self.pos += away.normalize() * self.speed * 0.55 * dt

        self.random_walk(dt, turn_strength=2.4)

    def reproduce(self, config: SimulationConfig) -> "Prey":
        radius = self._mutate(self.radius, 3.5, 16.0, config)
        speed = self._mutate(self.speed, 55.0, 215.0, config)
        offset = pygame.Vector2(random.uniform(-10, 10), random.uniform(-10, 10))
        child_pos = self.pos + offset
        child_pos.x = max(radius, min(WIDTH - radius, child_pos.x))
        child_pos.y = max(radius, min(HEIGHT - radius, child_pos.y))
        return Prey(child_pos.x, child_pos.y, speed=speed, radius=radius)

    def survival_cost(self, config: SimulationConfig) -> float:
        # Larger and faster prey are visually easier to hit and cost more energy.
        # This gives the simulation a trade-off instead of simply selecting max speed.
        return (self.speed * 0.003 + self.radius * 0.045) * config.prey_base_energy_cost

    def _mutate(self, value: float, low: float, high: float, config: SimulationConfig) -> float:
        if random.random() < config.prey_mutation_rate:
            strength = config.prey_mutation_strength * 2.6
        else:
            strength = config.prey_mutation_strength
        value *= random.uniform(1 - strength, 1 + strength)
        return max(low, min(high, value))

    def _nearest_predator(self, predators: List["Predator"]) -> "Predator" | None:
        if not predators:
            return None
        return min(predators, key=lambda predator: self.pos.distance_squared_to(predator.pos))


class Predator(Creature):
    def __init__(self, x: float, y: float):
        super().__init__(x=x, y=y, speed=random.uniform(95, 145), radius=15, color=PREDATOR_COLOR)
        self.eaten_today = 0

    def update(self, dt: float, prey: List[Prey]) -> None:
        target = self._nearest_prey(prey)
        if target is not None:
            direction = target.pos - self.pos
            if direction.length_squared() > 0:
                desired_angle = math.atan2(direction.y, direction.x)
                self.angle = self._turn_towards(self.angle, desired_angle, max_turn=2.0 * dt)

        self.random_walk(dt, turn_strength=1.0)

    def _nearest_prey(self, prey: List[Prey]) -> Prey | None:
        if not prey:
            return None
        return min(prey, key=lambda item: self.pos.distance_squared_to(item.pos))

    def _turn_towards(self, current: float, target: float, max_turn: float) -> float:
        diff = (target - current + math.pi) % math.tau - math.pi
        diff = max(-max_turn, min(max_turn, diff))
        return current + diff


class Simulation:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.stats = Stats()
        self.prey: List[Prey] = []
        self.predators: List[Predator] = []
        self.paused = False
        self.reset()

    def reset(self) -> None:
        self.stats = Stats()
        self.prey = [Prey(random.uniform(80, WIDTH * 0.45), random.uniform(80, HEIGHT - 80)) for _ in range(self.config.initial_prey)]
        self.predators = [Predator(random.uniform(WIDTH * 0.58, WIDTH - 80), random.uniform(80, HEIGHT - 80)) for _ in range(self.config.initial_predators)]
        self.stats.record(self.prey, self.predators)

    def update(self, dt: float) -> None:
        if self.paused:
            return

        self.stats.elapsed_in_day += dt
        for predator in self.predators:
            predator.update(dt, self.prey)
        for prey in self.prey:
            prey.update(dt, self.predators)

        self._handle_collisions()

        if self.stats.elapsed_in_day >= DAY_SECONDS:
            self._end_day()

    def _handle_collisions(self) -> None:
        survivors: List[Prey] = []
        for prey in self.prey:
            eaten = False
            for predator in self.predators:
                if prey.pos.distance_to(predator.pos) < prey.radius + predator.radius:
                    predator.eaten_today += 1
                    eaten = True
                    break
            if not eaten:
                survivors.append(prey)
        self.prey = survivors

    def _end_day(self) -> None:
        self.stats.day += 1
        self.stats.elapsed_in_day = 0.0

        next_generation: List[Prey] = []
        for prey in self.prey:
            if random.random() > prey.survival_cost(self.config):
                next_generation.append(prey)
                if len(next_generation) < self.config.prey_max_population:
                    next_generation.append(prey.reproduce(self.config))
        self.prey = next_generation[: self.config.prey_max_population]

        next_predators: List[Predator] = []
        for predator in self.predators:
            if predator.eaten_today >= self.config.predator_starvation_threshold:
                predator.eaten_today = 0
                next_predators.append(predator)
                if (
                    len(next_predators) < self.config.predator_max_population
                    and random.random() < 0.35
                ):
                    child = Predator(predator.pos.x + random.uniform(-14, 14), predator.pos.y + random.uniform(-14, 14))
                    next_predators.append(child)
        self.predators = next_predators or [Predator(WIDTH - 120, HEIGHT - 120)]

        if not self.prey:
            self.prey = [Prey(random.uniform(80, WIDTH * 0.45), random.uniform(80, HEIGHT - 80)) for _ in range(30)]

        self.stats.record(self.prey, self.predators)

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        screen.fill(BACKGROUND)
        self._draw_field(screen)
        for prey in self.prey:
            prey.draw(screen)
        for predator in self.predators:
            predator.draw(screen)
        self._draw_overlay(screen, font)
        self._draw_history(screen)

    def _draw_field(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, (230, 230, 224), pygame.Rect(20, 20, WIDTH - 40, HEIGHT - 40), width=1, border_radius=10)

    def _draw_overlay(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        avg_speed = mean(p.speed for p in self.prey) if self.prey else 0
        avg_size = mean(p.radius for p in self.prey) if self.prey else 0
        lines = [
            f"Day {self.stats.day}  |  {self.stats.elapsed_in_day:0.1f}/{DAY_SECONDS:0.0f}s",
            f"Prey {len(self.prey)}  Predators {len(self.predators)}",
            f"Avg speed {avg_speed:0.1f}  Avg size {avg_size:0.1f}",
            "SPACE pause   R reset   ESC quit",
        ]
        x, y = 34, 32
        for line in lines:
            surface = font.render(line, True, TEXT)
            screen.blit(surface, (x, y))
            y += 22

    def _draw_history(self, screen: pygame.Surface) -> None:
        if len(self.stats.history) < 2:
            return
        chart = pygame.Rect(WIDTH - 300, 34, 250, 92)
        pygame.draw.rect(screen, (255, 255, 255), chart, border_radius=8)
        pygame.draw.rect(screen, (225, 225, 220), chart, width=1, border_radius=8)

        prey_counts = [item[0] for item in self.stats.history]
        max_count = max(max(prey_counts), 1)
        points = []
        for index, count in enumerate(prey_counts):
            t = index / max(1, len(prey_counts) - 1)
            x = chart.left + 10 + t * (chart.width - 20)
            y = chart.bottom - 10 - (count / max_count) * (chart.height - 20)
            points.append((x, y))
        if len(points) >= 2:
            pygame.draw.lines(screen, ACCENT, False, points, 2)


def run() -> None:
    pygame.init()
    pygame.display.set_caption("Natural Selection Simulator")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 16)
    simulation = Simulation(SimulationConfig())

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    simulation.paused = not simulation.paused
                elif event.key == pygame.K_r:
                    simulation.reset()

        simulation.update(dt)
        simulation.draw(screen, font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
