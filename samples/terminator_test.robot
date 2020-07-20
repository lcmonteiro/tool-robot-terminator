*** Settings ***
Documentation     Execute Commands By Identified 
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.

Resource    terminator.robot

*** Test Cases ***

Commader Example
    [Documentation]    Execute a test Mission
    ${result}=  Run Mission  test
    Log To Console  ${result}
