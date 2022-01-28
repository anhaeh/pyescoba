Feature: test a cpu when it must do a escoba

  Scenario: make a escoba when is the only available move
    Given a IA player is registered in the game
    And has "7" of "ORO" in his hand
    And the table has "4" of "ORO"
    And the table has "4" of "ESPADA"
    When the player "IA" plays
    Then the table is empty
    And the player has "1" escoba

  Scenario: make a escoba when are many moves
    Given a IA player is registered in the game
    And has "7" of "ORO" in his hand
    And has "6" of "BASTO" in his hand
    And the table has "4" of "ORO"
    And the table has "4" of "ESPADA"
    And the table has "1" of "BASTO"
    When the player "IA" plays
    Then the table is empty
    And the player has "1" escoba
