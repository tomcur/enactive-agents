import abc
import os
import cPickle
import settings
import model.world
import model.structure
import model.agent
import model.perceptionhandler

class Experiment(object):

    controller = None
    world = None

    def parse_world(self, world_repr, mapper=None):
        """
        Parse a representation of a world to a world.
        :param world_repr: A list of strings that represent a world.
        :param map: A function that maps symbols to objects.
        :return: The world.
        :rtype: model.world.World
        """
        if mapper is None:
            mapper = self.mapper

        world = model.world.World()

        max_y = 0
        max_x = 0
        y = 0
        for line in world_repr:
            x = 0
            for symbol in line:
                obj = mapper(symbol)
                if not obj is None:
                    obj.set_position((x,y))
                    world.add_entity(obj)
                x += 1
                max_x = max(max_x, x)
            y += 1
            max_y = max(max_y, y)

        world.set_width(max_x)
        world.set_height(max_y)

        return world

    def mapper(self, symbol):
        """
        Parse a symbol to a world entity.
        :param symbol: The symbol to parse to an entity.
        :return: The entity to be placed in the world.
        :rtype: model.world.Entity
        """
        if symbol == "w":
            return model.structure.Wall()
        elif symbol == "b":
            return model.structure.Block()
        elif symbol == "a":
            return model.agent.ConstructiveAgent()
        elif symbol == "h":
            return model.agent.HomeostaticConstructiveAgent()
        elif symbol == "p":
            a = model.agent.ConstructiveAgent()
            a.set_perception_handler(model.perceptionhandler.BasicPerceptionHandler())
            return a
        elif symbol == "u":
            a = model.agent.HumanAgent()
            a.set_perception_handler(model.perceptionhandler.BasicPerceptionHandler())
            return a
        else:
            return None

    def get_world(self):
        """
        Get the world generated by this experiment.
        :return: The world generator by this experiment.
        :rtype: model.world.World
        """
        if self.world == None:
            raise ValueError("self.world should be set by the experiment")
        else:
            return self.world

    def controller(self, event, coords):
        """
        Called to control the simulation.
        :param event: The control event
        :param coords: The world coordinates the mouse is currently at
        """
        pass

    def load_agent(self, file_name):
        """
        Load an agent from file.
        :param file_name: The name of the file to load the agent from (e.g., "20161118T035805 - Agent DZX26I.p").
        :return: The loaded agent.
        """
        file_path = os.path.join(settings.AGENT_DIR, file_name)
        a = cPickle.load(open(file_path, "rb"))
        return a

    def load_world(self, file_name):
        """
        Load a world from file.
        :param file_name: The name of the file to load the world from (e.g., "20161118T035805.p").
        :return: The loaded world.
        """

        try:
            import dill
        except ImportError:
            print "ERROR: Module 'dill' is required to load worlds."
            return None
        else:       
            file_path = os.path.join(settings.WORLD_DIR, file_name)
            w = dill.load(open(file_path, "rb"))
            return w

    @staticmethod
    def load_experiment(file_name):
        """
        Load an experiment from file.
        :param file_name: The name of the file to load the experiment from (e.g., "20161118T035805.p").
        :return: The loaded experiment.
        """

        try:
            import dill
        except ImportError:
            print "ERROR: Module 'dill' is required to load experiments."
            return None
        else:       
            file_path = os.path.join(settings.EXPERIMENT_DIR, file_name)
            e = dill.load(open(file_path, "rb"))
            return e