Feature: test a cpu when it must throw cards

  Scenario: throw 2 of "espada" when the table has lower than 4
    Given a IA player is registered in the game
      And has "1" of "ORO" in his hand
      And has "2" of "ESPADA" in his hand
      And has "6" of "COPA" in his hand
      And the table has "1" of "BASTO"
      When the player "IA" plays
      Then the table has "2" of "ESPADA"

  Scenario: throw the worst card when the table has not cards
    Given a IA player is registered in the game
      And has "1" of "ORO" in his hand
      And has "2" of "ORO" in his hand
      And has "4" of "ESPADA" in his hand
      When the player "IA" plays
      Then the table has "4" of "ESPADA"

  Scenario: throw the worst seven card
    Given a IA player is registered in the game
      And has "7" of "ORO" in his hand
      And has "7" of "COPA" in his hand
      When the player "IA" plays
      Then the table has "7" of "COPA"

  Scenario: throw a GOLD card for exceed 15
    Given a IA player is registered in the game
      And has "1" of "COPA" in his hand
      And has "3" of "ORO" in his hand
      And the table has "7" of "BASTO"
      And the table has "6" of "COPA"
      When the player "IA" plays
      Then the table has "3" of "ORO"