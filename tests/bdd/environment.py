from entities.game_controller import GameController


def before_scenario(context, scenario):
    context.game = GameController()
    context.player = None


# Available hooks before|after + all|step|scenario|feature
