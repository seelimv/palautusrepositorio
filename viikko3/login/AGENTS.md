Repository-specific notes for automated agents

- uv: this repo uses uv for invoking commands. You can run repo commands with `uv run`.
  Example: start the app with
    uv run python src/index.py

- How the app is started and port
  - Primary entrypoint: src/index.py (invokes app.run).
  - Default bind: 0.0.0.0:5001 (Robot tests expect localhost:5001).

- Running Robot Framework tests
  - The application MUST be running before tests. Start it (see above) then run:
    uv run robot src/tests
  - You can also run a single suite/file:
    uv run robot src/tests/login.robot
  - To run a single test by name:
    uv run robot --test "Login With Correct Credentials" src/tests/login.robot

- Username/password validation
  - Validation and auth logic are in src/services/user_service.py
    - UserService.validate enforces username/password rules (length, uniqueness).
    - UserService.check_credentials enforces login checks and raises AuthenticationError on failure.

Sources: pyproject.toml, src/index.py, src/tests/*, src/AppLibrary.py, src/services/user_service.py
