from quiques import agent_amplada, agent_profunditat, joc, agent_informat


def main():
    barca = agent_informat.BarcaGreedy()
    illes = joc.Joc([barca])
    illes.comencar()


if __name__ == "__main__":
    main()
