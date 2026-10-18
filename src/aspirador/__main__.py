from aspirador import joc_gui, agent


agents = [agent.AspiradorMemoria()]

hab = joc_gui.Aspirador(agents)
hab.comencar()