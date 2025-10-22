Feature: Test autocomplete
  A basic test of the autocomplete functionality

  Scenario Outline: Autocomplete verification

    Given the train times page

    When I enter <chars> into the search box

    Then <suggestions> stations are suggested

    Examples:
      | chars  | suggestions                                              |
      | glasg  | Glasgow Central,Glasgow Queen Street                     |
      | Southa | Southall,Southampton Airport Parkway,Southampton Central |
      | cardi  | Cardiff Bay,Cardiff Central,Cardiff Queen Street         |


  Scenario: Search results by button click

    Given the train times page

    When I enter partick into the search box

    And I click the search button

    Then the partick departures page is displayed
