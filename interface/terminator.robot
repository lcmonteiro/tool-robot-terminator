*** Settings ***
Documentation     Commander Keywords
Library           Remote    ${terminator_host}    WITH NAME    terminator

*** Keywords ***

Run Mission
    [Documentation]    Execute a Mission By ID
    [Arguments]  @{id}
    [Return]     ${result}
    ${result}=   terminator.execute    @{id}
    