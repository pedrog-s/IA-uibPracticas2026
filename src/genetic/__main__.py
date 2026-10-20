from genetic import agent, joc


def main():
    genetic = joc.Genetic(
        [agent.Genetic()]
    )

    genetic.comencar()

if __name__ == "__main__":
    main()
