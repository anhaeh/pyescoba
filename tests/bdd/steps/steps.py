from behave import *

from entities.card import Card


@given('a IA player is registered in the game')
def step_add_cpu(context):
    context.game.add_cpu_player('CPU')
    context.player = context.game.players[0]


@given('has "{card_number}" of "{card_type}" in his hand')
def step_add_card(context, card_number, card_type):
    card = Card(card_number, card_type)
    context.player.add_card_to_hand(card)


@given('the table has "{card_number}" of "{card_type}"')
def step_add_card_to_table(context, card_number, card_type):
    card = Card(card_number, card_type)
    context.game.table.append(card)


@when('the player "{player_name}" plays')
def step_player_plays(context, player_name):
    context.player.play()


@then('the table is empty')
def step_table_empty(context):
    assert len(context.game.table) == 0


@then('the player has "{count}" escoba')
def step_table_empty(context, count):
    assert len(context.player.escobas) == int(count)


@then('the table has "{card_number}" of "{card_type}"')
def step_table_has(context, card_number, card_type):
    results = filter(lambda x: x.number == int(card_number) and x.card_type == card_type, context.game.table)
    assert len(results) == 1
