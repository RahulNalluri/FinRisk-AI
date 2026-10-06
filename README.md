# Financial Fraud Risk System (FinRisk AI)

A Python/Flask demo for inspecting customer transaction history, flagging payment
risk, and estimating loan default risk. The web interface includes a transaction
scanner, loan assessment form, analytics dashboard, and customer profiles.

The application reads local CSV data and serialized scikit-learn artifacts. It
does not connect to a bank, process payments, or persist submitted transactions.

## Current behavior

- **Payment screening:** requires a numeric customer ID present in the scam
  dataset. After checking the selected transaction limit, any prior fraudulent
  record produces `FRAUD` with a fixed score of `85` and confidence of `95`.
  Customers with no flagged history receive `SAFE`, score `12`, and confidence
  `93`. The fraud type comes from the first available historical type.
  This endpoint currently uses history rules, not model inference, even though
  some interface labels describe model-based scoring.
- **Loan assessment:** monthly income below INR 60,000 is rejected immediately.
  Otherwise, a saved scaler and Gradient Boosting classifier estimate default
  risk. Class `0` maps to `APPROVED`; class `1` maps to `REJECTED`.
  The displayed approval value is `100 - default risk`.
- **Dashboard:** summarizes all records loaded from the scam CSV, including
  fraud counts, fraud types, and locations. The browser refreshes every 30 seconds,
  but the CSV is loaded only at server startup; restart after changing it.
- **Customer profiles:** show historical fraud rates, recommendations, and up to
  20 records in CSV order. The scanner's customer lookup shows up to six records.

The payment limits below are hardcoded application rules, not a statement of
banking or regulatory limits. Amounts above the limit are blocked; equal amounts
are allowed. Unknown transaction type strings currently bypass this limit check.

| Transaction type | Maximum amount (INR) |
| --- | ---: |
| UPI | 100,000 |
| CARD | 500,000 |
| ATM | 20,000 |
| WIRE | 10,000,000 |
| ECOM | 500,000 |
| NEFT | 10,000,000 |

## Project layout

```text
src/
  app.py                       Flask entry point and JSON endpoints
  train_scam_model.py           Random Forest scam classifier
  train_fraud_type_model.py     Random Forest fraud-type classifier
  train_loan_model.py           Gradient Boosting loan classifier and scaler
  train_payment_model.py        Optional online-payment classifier
  train_creditcard_model.py     Optional credit-card classifier
templates/                     Home, dashboard, and customer-profile pages
static/                        CSS and browser JavaScript
notebooks/                     Exploratory analysis notebooks
data/                          Local CSV datasets (ignored by Git)
models/                        Trained artifacts (ignored by Git)
requirements.txt/txt           Python dependency file
check_dataset.py               Dataset inspection script
test_predictions.py            Standalone scam-model diagnostic script
create_powerpoint.py           Presentation generator
docs/                          Reports, presentations, and duplicate app files
```

Use the root `src`, `templates`, and `static` folders to run the app. The copies
under `docs/` are not used by `src/app.py`.

## Setup and run

Run these commands from the project root with Python 3 available. The existing
dependency list is unpinned; use compatible scikit-learn versions for training
and loading saved artifacts, or regenerate them in your environment.

### 1. Install dependencies

Windows PowerShell (no environment activation required):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt/txt
```

On macOS/Linux, use `.venv/bin/python` instead of
`.\.venv\Scripts\python.exe` in these commands.

`requirements.txt` is currently a **directory** containing a file named `txt`.
Use the full path above, rather than `pip install -r requirements.txt`.

### 2. Supply local datasets

Create `data/` if needed and supply the following CSV files. Datasets and trained
models are intentionally excluded from Git, so a fresh checkout needs local
copies. There is no automatic dataset downloader.

| Dataset | Used for |
| --- | --- |
| `data/Indian_Online_Scam_Dataset.csv` | Required at runtime; scam and fraud-type training |
| `data/loan_risk_dataset.csv` | Required to train the loan model |
| `data/online_payment_dataset.csv` | Optional payment-model training |
| `data/creditcard.csv` | Optional credit-card-model training |

Expected CSV columns:

- **Scam:** `transaction_id`, `customer_id`, `merchant_id`, `amount`,
  `transaction_time`, `is_fraudulent`, `card_type`, `location`,
  `purchase_category`, `customer_age`, `fraud_type`.
- **Loan:** `person_age`, `person_income`, `person_home_ownership`,
  `person_emp_length`, `loan_intent`, `loan_grade`, `loan_amnt`, `loan_int_rate`,
  `loan_status`, `loan_percent_income`, `cb_person_default_on_file`,
  `cb_person_cred_hist_length`.
- **Online payment:** `step`, `type`, `amount`, `nameOrig`, `oldbalanceOrg`,
  `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest`, `isFraud`,
  `isFlaggedFraud`.
- **Credit card:** `Time`, `V1` through `V28`, `Amount`, `Class`.

Use numeric customer IDs and binary fraud/default labels (`0` or `1`). Training
needs enough labeled examples for a train/test split, including fraudulent
records with nonempty fraud types. The runtime CSV is not cleaned in the same way
as the training data; incomplete records can cause errors.

### 3. Train the required models

If compatible artifacts are already present in `models/`, skip this step.
Training writes or overwrites artifacts in that directory.

```powershell
.\.venv\Scripts\python.exe src/train_scam_model.py
.\.venv\Scripts\python.exe src/train_fraud_type_model.py
.\.venv\Scripts\python.exe src/train_loan_model.py
```

The app loads all eight files below at startup, including the scam and fraud-type
artifacts that the current payment endpoint does not use for inference:

```text
scam_model.pkl             scam_features.pkl
fraud_type_model.pkl       fraud_type_features.pkl       fraud_type_encoder.pkl
loan_risk_model.pkl        loan_features.pkl             loan_scaler.pkl
```

Scam training also creates `scam_threshold.pkl`; the web app does not load it.
Optional training scripts are `src/train_payment_model.py` and
`src/train_creditcard_model.py`. Their outputs are not used by the current app.
All training scripts use an 80/20 split with `random_state=42` and print evaluation
results to the terminal.

### 4. Start Flask

```powershell
.\.venv\Scripts\python.exe src/app.py
```

Open [the local app](http://127.0.0.1:5000). Dashboard and customer profiles are
available from its navigation. The app starts in Flask debug mode.
Fonts and dashboard charts use external Google Fonts and Chart.js CDN resources.

No environment variables or credentials are currently required, so an
`.env.example` is unnecessary. Request examples are included below.

## Routes and request examples

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/` | Transaction scanner and loan form |
| GET | `/dashboard` | Analytics page |
| GET | `/customer-profile` | Customer profile page |
| GET | `/get_customer/<customer_id>` | Customer summary and six historical records |
| POST | `/predict_payment` | History-based payment verdict |
| POST | `/predict_loan` | Loan assessment |
| GET | `/api/dashboard-data` | Dataset-wide analytics |
| GET | `/api/customer-profile/<customer_id>` | Detailed customer risk and history |

Send JSON with `Content-Type: application/json`. For payment screening, replace
the placeholder with a numeric ID from your local CSV:

```json
{
  "customer_id": "REPLACE_WITH_DATASET_CUSTOMER_ID",
  "amount": 15000,
  "tx_type": "UPI"
}
```

Loan request (`POST /predict_loan`):

```json
{
  "income": 75000,
  "loan_amount": 500000,
  "purpose": "PERSONAL"
}
```

Supported loan purposes are `HOME`, `EDUCATION`, `VEHICLE`, `MEDICAL`, `BUSINESS`,
and `PERSONAL`. Payment validation failures return `blocked: true`, usually with
HTTP 200; customer lookup failures return `found: false`. The detailed profile
API uses HTTP 400 for an invalid ID and 404 for an unknown customer.

## Diagnostics and limitations

```powershell
.\.venv\Scripts\python.exe check_dataset.py
.\.venv\Scripts\python.exe test_predictions.py
```

These scripts print diagnostics; they are not an automated assertion-based test
suite. `test_predictions.py` evaluates the scam model directly and therefore
does not test the history rules in `/predict_payment`.

The project is a local demonstration. Displayed accuracy figures and several
homepage metrics are hardcoded, and confidence values are fixed or heuristic.
They are not live evaluation results. Loan inputs use fixed defaults for age,
employment, home ownership, grade, and credit history. The UI treats income as
monthly, while the backend passes it directly to `person_income` and annualizes
it only for the loan-to-income ratio; verify dataset units before interpreting
results. Input validation is limited, and no authentication is implemented.

`create_powerpoint.py` additionally requires `python-pptx` and writes
`presentation.pptx` in the root. Notebook tooling is also separate from the listed
application dependencies.

## Git ignore policy

`.gitignore` excludes directories named `data/` and `models/` at any depth,
including `docs/data/` and `docs/models/`. It also excludes serialized model
files, virtual environments, Python/notebook caches, local environment files,
generated logs and root diagnostic outputs, and editor/OS files. Source code,
notebooks, existing documentation, and sanitized `.env.example` files remain
eligible for version control.

Ignore rules do not remove files already tracked by Git. This folder did not
contain Git metadata when the README and ignore file were added.
