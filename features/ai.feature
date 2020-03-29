Feature: AI generate available command list
    Scenario: Unit stand
        Given Unit stand
        Then return one of commands
            |command|
            |"moveOrAttack"|
            |"retreatOrStorm"|
            |"stopOrDefense"|