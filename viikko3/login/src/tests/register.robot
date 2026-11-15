*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***
Register With Valid Username And Password
    Set Username  kalle2
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Submit Credentials
    Register Should Succeed

Register Accepts Password With Numbers
    Set Username  kalle3
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Submit Credentials
    Register Should Succeed

Register Accepts Password With Symbol And Letters
    Set Username  kalle4
    Set Password  kalle#abc
    Set Password Confirmation  kalle#abc
    Submit Credentials
    Register Should Succeed

Register Rejects Password With Only Lowercase Letters
    Set Username  kalle5
    Set Password  kallekalle
    Set Password Confirmation  kallekalle
    Submit Credentials
    Register Should Fail With Message  Password must include non-letter characters

Register Rejects Password With Only Uppercase And Lowercase Letters
    Set Username  kalle6
    Set Password  KalleKalle
    Set Password Confirmation  KalleKalle
    Submit Credentials
    Register Should Fail With Message  Password must include non-letter characters

Register With Too Short Username And Valid Password
    Set Username  ka
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Submit Credentials
    Register Should Fail With Message  Username is too short

Register With Valid Username And Too Short Password
    Set Username  kalle2
    Set Password  short
    Set Password Confirmation  short
    Submit Credentials
    Register Should Fail With Message  Password is too short

Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Submit Credentials
    Register Should Fail With Message  Username is already in use


Passwords And Confirmation Must Match Success
    Set Username  testmatch1
    Set Password  matchpass123
    Set Password Confirmation  matchpass123
    Submit Credentials
    Register Should Succeed
    

Passwords And Confirmation Must Match Failure
    Set Username  testmatch2
    Set Password  matchpass123
    Set Password Confirmation  wrongpass123
    Submit Credentials
    Register Should Fail With Message  Password and confirmation do not match

*** Keywords ***
Register Should Succeed
    Welcome Page Should Be Open

Register Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Get Text  body  *=  ${message}

Set Password Confirmation
    [Arguments]  ${password}
    Fill Secret  id=password_confirmation  $password

Submit Credentials
    Click  button >> text=Register

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page
