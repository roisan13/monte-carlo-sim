# Funcție pentru animatie
# nu ruleaza, nu are importurile necesare din matplotlib si nici din main.py
# a fost rulat oricum separat de proiectul principat (a durat 6 ore sa creez un gif)
def generate_animation(total_shots):
    colors = {
        "head": "red",
        "chest": "blue",
        "arm": "green",
        "stomach": "orange",
        "leg": "purple",
        None: "gray",  # Rată
    }

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title("Modelul inamicului pe plan 2D")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid()

    shots_drawn = []

    def update(frame):
        print(frame)
        for _ in range(350):
            glont = (
                np.random.uniform(*shooting_zone),
                np.random.uniform(*shooting_zone)
            )
            hit_zone = check_hit(glont)
            shots_drawn.append((glont, hit_zone))

            color = colors[hit_zone]
            ax.scatter(glont[0], glont[1], color=color, s=5, alpha=0.7)

        return ax

    anim = FuncAnimation(fig, update, frames=total_shots // 10, repeat=False, interval=5)
    anim.save("simulation_faster.gif", writer="pillow")
    plt.close(fig)

generate_animation(total_shots=2000)

