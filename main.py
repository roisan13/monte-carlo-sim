import numpy as np
import matplotlib.pyplot as plt


# Parametrii modelului inamicului
head_radius = 0.18  # Cap (raza cercului)
chest_dimensions = (0.6, 0.3)  # Piept (width, height)
arm_dimensions = (0.2, 0.5)  # Maini (width, height)
stomach_dimensions = (0.5, 0.3)  # Stomac (width, height)
leg_dimensions = (0.2, 0.5)  # Picioare (width, height)

# Hitbox damage
damage_values = {
    "head": 135,
    "chest": 35,
    "arm": 35,
    "stomach": 44,
    "leg": 26,
}

shooting_zone = (-1.5, 1.5)


def draw_enemy():
    # Modelul inamicului pe grafic
    fig, ax = plt.subplots(figsize=(8, 8))

    # Cap
    head = plt.Circle((0, 1.28), head_radius, color="red", alpha=0.7, label="Cap")
    ax.add_artist(head)

    # Piept
    chest = plt.Rectangle((-chest_dimensions[0] / 2, 0.8), chest_dimensions[0], chest_dimensions[1],
                           color="blue", alpha=0.7, label="Piept")
    ax.add_artist(chest)

    # Maini
    left_arm = plt.Rectangle((-chest_dimensions[0] / 2 - arm_dimensions[0], 0.6), arm_dimensions[0], arm_dimensions[1],
                              color="green", alpha=0.7, label="Maini")
    right_arm = plt.Rectangle((chest_dimensions[0] / 2, 0.6), arm_dimensions[0], arm_dimensions[1],
                               color="green", alpha=0.7)
    ax.add_artist(left_arm)
    ax.add_artist(right_arm)

    # Stomac
    stomach = plt.Rectangle((-stomach_dimensions[0] / 2, 0.5), stomach_dimensions[0], stomach_dimensions[1],
                             color="orange", alpha=0.7, label="Stomac")
    ax.add_artist(stomach)

    # Picioare
    left_leg = plt.Rectangle((-stomach_dimensions[0] / 2, 0), leg_dimensions[0], leg_dimensions[1],
                              color="purple", alpha=0.7, label="Picior")
    right_leg = plt.Rectangle((stomach_dimensions[0] / 2 - leg_dimensions[0], 0), leg_dimensions[0], leg_dimensions[1],
                               color="purple", alpha=0.7)
    ax.add_artist(left_leg)
    ax.add_artist(right_leg)

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("Modelul inamicului pe plan 2D")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.legend()
    ax.grid()
    plt.show()

def check_hit(glont):
    x, y = glont

    # Cap
    if np.sqrt(x ** 2 + (y - 1.28) ** 2) <= head_radius:
        return "head"

    # Piept
    if -chest_dimensions[0] / 2 <= x <= chest_dimensions[0] / 2 and 0.8 <= y <= 1.1:
        return "chest"

    # Maini
    if (-chest_dimensions[0] / 2 - arm_dimensions[0] <= x <= -chest_dimensions[0] / 2 and 0.6 <= y <= 1.1) or \
       (chest_dimensions[0] / 2 <= x <= chest_dimensions[0] / 2 + arm_dimensions[0] and 0.6 <= y <= 1.1):
        return "arm"

    # Stomac
    if -stomach_dimensions[0] / 2 <= x <= stomach_dimensions[0] / 2 and 0.5 <= y <= 0.8:
        return "stomach"

    # Picioare
    if (-stomach_dimensions[0] / 2 <= x <= -stomach_dimensions[0] / 2 + leg_dimensions[0] and 0 <= y <= 0.5) or \
       (stomach_dimensions[0] / 2 - leg_dimensions[0] <= x <= stomach_dimensions[0] / 2 and 0 <= y <= 0.5):
        return "leg"

    # Miss!
    return None

def monte_carlo_simulation(num_shots, num_simulations):
    success_count = 0
    all_shots = []  # All bullets shot acorss ALL simulations
    damage_per_simulation = []
    hits_per_zone = {zone: 0 for zone in damage_values.keys()}
    probabilities = []

    for i in range(1, num_simulations + 1):
        total_damage = 0
        for _ in range(num_shots):
            glont = (
                np.random.uniform(*shooting_zone),
                np.random.uniform(*shooting_zone)
            )
            hit_zone = check_hit(glont)

            all_shots.append((glont, hit_zone))

            if hit_zone:
                total_damage += damage_values[hit_zone]
                hits_per_zone[hit_zone] += 1

        damage_per_simulation.append(total_damage)
        if total_damage >= 100:
            success_count += 1

        probabilities.append(success_count / i)

    final_probability = success_count / num_simulations
    return final_probability, all_shots, damage_per_simulation, hits_per_zone, probabilities

def get_theoretical_probability(num_shots):
    probabilities = {
        5: 0.05,
        10: 0.13,
        15: 0.22,
        20: 0.33,
        25: 0.45,
        30: 0.53
    }
    return probabilities.get(num_shots, 0)
def analyze_errors(probability, num_simulations, theoretical_probability):
    error_absolute = abs(probability - theoretical_probability)
    error_relative = error_absolute / theoretical_probability
    error_standard = np.sqrt((theoretical_probability * (1 - theoretical_probability)) / num_simulations)
    confidence_interval = (probability - 1.96 * error_standard, probability + 1.96 * error_standard)

    print("\n=== Analiza erorilor ===")
    print(f"Probabilitate estimata: {probability:.4f}")
    print(f"Probabilitate teoretica: {theoretical_probability:.4f}")
    print(f"Eroare absoluta: {error_absolute:.4f}")
    print(f"Eroare relativa: {error_relative:.2%}")
    print(f"Eroare standard: {error_standard:.4f}")
    print(f"Interval de incredere 95%: {confidence_interval[0]}, {confidence_interval[1]}")

# Grafic: Damage per simulare
def plot_damage_distribution(damage_per_simulation):
    plt.figure(figsize=(10, 6))
    plt.hist(damage_per_simulation, bins=20, color="skyblue", edgecolor="black")
    plt.axvline(100, color="red", linestyle="dashed", linewidth=2, label="100 damage = KILL")
    plt.title("Distributia damage-ului total per simulare")
    plt.xlabel("Damage total")
    plt.ylabel("Frecventa")
    plt.legend()
    plt.grid()
    plt.show()

# Grafic: Repartizarea loviturilor pe zone
def plot_hits_per_zone(hits_per_zone):
    zones = list(hits_per_zone.keys())
    hits = list(hits_per_zone.values())

    plt.figure(figsize=(10, 6))
    plt.bar(zones, hits, color=["red", "blue", "green", "orange", "purple"], edgecolor="black")
    plt.title("Repartizarea loviturilor pe zone")
    plt.xlabel("Zonă")
    plt.ylabel("Număr de lovituri")
    plt.grid(axis="y")
    plt.show()

# Grafic: Heatmap al loviturilor
def plot_heatmap(all_shots):
    x_hits = [glont[0][0] for glont in all_shots if glont[1] is not None]
    y_hits = [glont[0][1] for glont in all_shots if glont[1] is not None]

    plt.figure(figsize=(10, 6))
    plt.hist2d(x_hits, y_hits, bins=50, cmap="hot")
    plt.colorbar(label="Densitatea loviturilor")
    plt.title("Heatmap al loviturilor pe modelul tintei")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid()
    plt.show()

# Grafic: Performanta cu 5, 10, .. 25 focuri
def plot_performance_by_shots(num_simulations):
    shot_counts = [5, 10, 15, 20, 25]
    probabilities = []

    for shots in shot_counts:
        probability, _, _, _, _ = monte_carlo_simulation(shots, num_simulations)
        probabilities.append(probability)

    plt.figure(figsize=(10, 6))
    plt.plot(shot_counts, probabilities, marker="o", color="blue")
    plt.title("Performanta în functie de numarul de gloante")
    plt.xlabel("Numar de gloante")
    plt.ylabel("Probabilitatea de a omori tinta")
    plt.grid()
    plt.show()

# Grafic: Convergenta probabilitatii
def plot_probability_convergence(probabilities):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(probabilities) + 1), probabilities, color="blue")
    plt.axhline(probabilities[-1], color="red", linestyle="dashed", label="Probabilitate finala")
    plt.title("Convergenta probabilitatii estimarii")
    plt.xlabel("Numar de simulari")
    plt.ylabel("Probabilitate estimata")
    plt.legend()
    plt.grid()
    plt.show()


num_shots = int(input("Introduceți numărul de focuri trase (5/10/15/20/25) \n"))

draw_enemy()
num_simulations = 10000
probability, all_shots, damage_per_simulation, hits_per_zone, probabilities = monte_carlo_simulation(num_shots, num_simulations)
print(f"Probabilitatea de a elimina inamicul cu {num_shots} focuri: {probability:.4f}")


# Analiza erorilor, chiar daca theoretical_probability este o estimare luata din ... mai multe simulari
th_prb = get_theoretical_probability(num_shots)
analyze_errors(probability, num_simulations, theoretical_probability=th_prb)


# Grafice
plot_probability_convergence(probabilities)
plot_damage_distribution(damage_per_simulation)
plot_hits_per_zone(hits_per_zone)
plot_heatmap(all_shots)
plot_performance_by_shots(num_simulations)

