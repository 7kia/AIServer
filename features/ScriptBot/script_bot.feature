Feature: ScriptBot generate random command
    Scenario: ScriptBot return command is JSON
        Given Unit list, unit parameters, map bounds
        Then return one of commands
            |command|
            |"moveOrAttack"|
            |"retreatOrStorm"|
            |"stopOrDefense"|