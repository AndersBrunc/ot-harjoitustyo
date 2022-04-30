# **BudgetApp**

This app can be used to create a budget and keep track of purchases.

## Documentation

- [Specification of Requirements](budgetapp/documentation/vaatimusmaarittely.md)

- [Architecture](budgetapp/documentation/arkkitehtuuri.md)

- [Work accounting](budgetapp/documentation/tuntikirjanpito.md)

- [Changelog](budgetapp/documentation/changelog.md)

- [Release](https://github.com/NaND3R5/ot-harjoitustyo/releases/tag/viikko5)

## Installation

1. Install dependencies using the command:

```bash
poetry install
```

2. Initialize prerequisites with the command:

```bash
poetry run invoke build
```

3. Start the application with the command:

```bash
poetry run invoke start
```

## Commands

### Run the program

Run the program using:

```bash
poetry run invoke start
```

### Testing
Run tests using:

```bash
poetry run invoke test
```

### Test Coverage

Create a test coverage report to the _htmlcov_-folder using:

```bash
poetry run invoke coverage-report
```

### Pylint

Execute a pylint-inspection based on the requirements specified in the [.pylintrc](./budgetapp/.pylintrc) -file:

```bash
poetry run invoke pylint
```
