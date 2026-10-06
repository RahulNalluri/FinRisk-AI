let selectedTxType = 'UPI';

// Transaction type limits (in Rupees) - realistic limits in India
const txLimits = {
  'UPI': { max: 100000, warning: 50000, label: 'UPI max: ₹1,00,000/transaction' },
  'Card': { max: 500000, warning: 300000, label: 'Card limit depends on issuer' },
  'ATM': { max: 20000, warning: 10000, label: 'ATM max: ₹20,000/transaction' },
  'Wire': { max: 10000000, warning: 5000000, label: 'Wire transfers are usually for large amounts' },
  'Ecom': { max: 500000, warning: 300000, label: 'E-commerce limit depends on merchant' },
  'NEFT': { max: 10000000, warning: 5000000, label: 'NEFT transfers usually for large amounts' }
};

function selectTxType(type, el) {
  selectedTxType = type;
  document.querySelectorAll('.tx-btn').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
}

// ✅ NEW: Validate transaction amount based on type
function validateTransactionAmount() {
  const amount = parseFloat(document.getElementById('amount').value);
  const limits = txLimits[selectedTxType] || { max: 500000, warning: 300000 };
  
  if (amount > limits.max) {
    return {
      valid: false,
      error: `❌ ${selectedTxType} has a maximum limit of ₹${limits.max.toLocaleString('en-IN')} per transaction. Amount ${amount.toLocaleString('en-IN')} exceeds limit.`
    };
  }
  
  if (amount > limits.warning) {
    return {
      valid: true,
      warning: `⚠️ Warning: ₹${amount.toLocaleString('en-IN')} is unusually high for ${selectedTxType}. (Typical limit: ₹${limits.warning.toLocaleString('en-IN')})`
    };
  }
  
  return { valid: true, warning: null };
}

function showLoading(prefix) {
  document.getElementById(prefix + 'Empty').style.display = 'none';
  document.getElementById(prefix + 'Blocked').classList.remove('visible');
  document.getElementById(prefix + 'Loading').classList.add('active');
  document.getElementById(prefix + 'Result').classList.remove('visible');
}

function showResult(prefix) {
  document.getElementById(prefix + 'Loading').classList.remove('active');
  document.getElementById(prefix + 'Result').classList.add('visible');
  document.getElementById(prefix + 'Result').classList.add('fade-up');
}

function showBlocked(prefix, message) {
  document.getElementById(prefix + 'Loading').classList.remove('active');
  document.getElementById(prefix + 'Result').classList.remove('visible');
  const el = document.getElementById(prefix + 'Blocked');
  el.classList.add('visible');
  document.getElementById(prefix + 'BlockedMsg').textContent = message;
}

function renderReasons(listId, reasons) {
  const ul = document.getElementById(listId);
  ul.innerHTML = '';
  reasons.forEach(r => {
    const li = document.createElement('li');
    li.innerHTML = `<span class="reason-dot"></span>${r}`;
    ul.appendChild(li);
  });
}

async function renderCustomerBg(custId) {
  const custBg = document.getElementById('custBg');
  const custIdClean = (custId || '').trim();
  if (!custIdClean) { custBg.style.display = 'none'; return; }

  custBg.style.display = 'block';
  custBg.innerHTML = `
    <div class="customer-bg-title">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
      </svg>
      Customer Background
    </div>
    <p style="font-family:var(--mono);font-size:12px;color:var(--muted);text-align:center;padding:16px 0">
      Looking up customer ${custIdClean}...
    </p>`;

  try {
    const res = await fetch('/get_customer/' + custIdClean);
    const cust = await res.json();

    if (!cust.found) {
      custBg.innerHTML = `
        <div class="customer-bg-title">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
          </svg>
          Customer Background
        </div>
        <p style="font-family:var(--mono);font-size:12px;color:var(--red);text-align:center;padding:16px 0">
          ✕ ${cust.message}
        </p>`;
      return;
    }

    const riskColor = cust.risk_profile === 'High'   ? 'var(--red)'    :
                      cust.risk_profile === 'Medium' ? 'var(--yellow)' : 'var(--green)';

    custBg.innerHTML = `
      <div class="customer-bg-title">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
        </svg>
        Customer Background
      </div>
      <div class="cust-grid">
        <div class="cust-field"><div class="cf-label">Customer ID</div><div class="cf-value" style="color:var(--orange)">${cust.customer_id}</div></div>
        <div class="cust-field"><div class="cf-label">Age</div><div class="cf-value">${cust.customer_age}</div></div>
        <div class="cust-field"><div class="cf-label">Location</div><div class="cf-value">${cust.city}</div></div>
        <div class="cust-field"><div class="cf-label">Card Types</div><div class="cf-value">${cust.card_types.join(', ')}</div></div>
        <div class="cust-field"><div class="cf-label">Total Transactions</div><div class="cf-value">${cust.total_tx}</div></div>
        <div class="cust-field"><div class="cf-label">Avg. Amount</div><div class="cf-value">${cust.avg_amount}</div></div>
        <div class="cust-field">
          <div class="cf-label">Flagged Transactions</div>
          <div class="cf-value" style="color:${cust.flagged_tx > 0 ? 'var(--red)' : 'var(--green)'}">
            ${cust.flagged_tx} time${cust.flagged_tx !== 1 ? 's' : ''}
          </div>
        </div>
        <div class="cust-field">
          <div class="cf-label">Risk Profile</div>
          <div class="cf-value" style="color:${riskColor}">${cust.risk_profile}</div>
        </div>
      </div>
      <div class="tx-history">
        <div class="tx-history-title">RECENT TRANSACTION HISTORY</div>
        ${cust.history.map(tx => `
          <div class="tx-hist-row">
            <span class="th-type">${tx.type}</span>
            <span class="th-amt">${tx.amount}</span>
            <span style="color:var(--muted);font-size:11px;flex:1;text-align:center">${tx.location}</span>
            <span class="th-status ${tx.status}">${tx.status.toUpperCase()}</span>
          </div>`).join('')}
      </div>`;

  } catch (err) {
    custBg.innerHTML = `
      <div class="customer-bg-title">Customer Background</div>
      <p style="font-family:var(--mono);font-size:12px;color:var(--muted);text-align:center;padding:16px 0">
        Could not fetch customer data — is Flask running?
      </p>`;
  }
}

async function analyzeTransaction() {
  const amount = document.getElementById('amount').value;
  const custId = document.getElementById('customer_id').value.trim();

  if (!amount) { alert('Please enter a transaction amount.'); return; }
  if (!custId) { alert('Please enter a Customer ID.'); return; }

  // ✅ NEW: Validate transaction amount against payment type limits
  const validation = validateTransactionAmount();
  if (!validation.valid) {
    alert(validation.error);
    return;
  }
  
  // Show warning if applicable
  if (validation.warning) {
    alert(validation.warning + '\n\nContinuing with analysis...');
  }

  showLoading('fraud');

  try {
    const response = await fetch('/predict_payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ amount, customer_id: custId, tx_type: selectedTxType })
    });
    const data = await response.json();

    if (data.blocked) {
      showBlocked('fraud', data.message);
      renderCustomerBg(custId);
      return;
    }

    const vEl = document.getElementById('fraudVerdict');
    if (data.label === 'FRAUD') {
      vEl.className = 'verdict fraud'; vEl.textContent = '✕ FRAUD DETECTED';
    } else if (parseFloat(data.score) > 50) {
      vEl.className = 'verdict warn'; vEl.textContent = '⚠ SUSPICIOUS';
    } else {
      vEl.className = 'verdict safe'; vEl.textContent = '✔ SAFE';
    }

    document.getElementById('scoreVal').textContent  = data.score + '%';
    document.getElementById('confVal').textContent   = data.confidence + '%';
    document.getElementById('riskPct').textContent   = data.score + '%';
    document.getElementById('riskMeter').style.width = Math.min(data.score, 100) + '%';

    // ✅ NEW: Display transaction type and amount in result
    document.getElementById('txTypeDisplay').textContent = selectedTxType;
    document.getElementById('amountDisplay').textContent = '₹' + parseFloat(amount).toLocaleString('en-IN');

    // Display fraud type if available
    const fraudTypeDisplay = document.getElementById('fraudTypeDisplay');
    if (data.fraud_type && data.label === 'FRAUD') {
      fraudTypeDisplay.style.display = 'block';
      document.getElementById('fraudTypeValue').textContent = data.fraud_type;
    } else {
      fraudTypeDisplay.style.display = 'none';
    }

    renderReasons('fraudReasons', data.reasons);
    showResult('fraud');
    renderCustomerBg(custId);

  } catch (err) {
    alert('Could not connect to Flask backend. Make sure app.py is running.');
  }
}

async function predictLoan() {
  const income  = document.getElementById('income').value;
  const loanAmt = document.getElementById('loan_amount').value;
  const purpose = document.getElementById('purpose').value;

  if (!income || !loanAmt) { alert('Please fill in all loan fields.'); return; }

  showLoading('loan');

  try {
    const response = await fetch('/predict_loan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ income, loan_amount: loanAmt, purpose })
    });
    const data = await response.json();

    const vEl = document.getElementById('loanVerdict');
    vEl.className   = data.label === 'APPROVED' ? 'verdict approved' : 'verdict rejected';
    vEl.textContent = data.label === 'APPROVED' ? '✔ APPROVED' : '✕ REJECTED';

    document.getElementById('loanScore').textContent     = data.score + '%';
    document.getElementById('loanApproval').textContent  = data.approval + '%';
    document.getElementById('approvalPct').textContent   = data.approval + '%';
    document.getElementById('defaultPct').textContent    = data.score + '%';
    document.getElementById('approvalMeter').style.width = Math.min(data.approval, 100) + '%';
    document.getElementById('defaultMeter').style.width  = Math.min(data.score, 100) + '%';

    renderReasons('loanReasons', data.reasons);
    showResult('loan');

  } catch (err) {
    alert('Could not connect to Flask backend. Make sure app.py is running.');
  }
}