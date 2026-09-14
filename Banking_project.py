import streamlit as st
import pandas as pd

st.set_page_config(page_title="PNB Banking Dashboard",layout="wide")

# SESSION STATE
if "balance" not in st.session_state:
    st.session_state.balance = 0
if "transactions" not in st.session_state:
    st.session_state.transactions = []
if "kyc_documents" not in st.session_state:
    st.session_state.kyc_documents = {}

# SIDEBAR
st.sidebar.title("PNB BANK")
st.sidebar.divider()

st.sidebar.subheader("Navigation")
page = st.sidebar.radio("Go to",
    ["Dashboard",
    "Deposit",
    "Withdraw",
    "KYC Management",
    "Transactions",
    "Account Details"])

st.sidebar.divider()

st.sidebar.subheader("Account Information")
st.sidebar.write("**Account Holder:**")
st.sidebar.write("Tarun Kaushal")
st.sidebar.write("**Account Type:**")
st.sidebar.write("Savings Account")
st.sidebar.write("**Account Status:**")
st.sidebar.success("Active")

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Account"):
    st.session_state.balance = 0
    st.session_state.transactions = []
    st.session_state.kyc_documents = {}
    st.rerun()

# HEADER
st.title("Punjab National Bank")
st.caption("Digital Banking & Account Management System")
st.divider()

# CALCULATE TRANSACTION TOTALS
total_deposits = sum(t["Amount"] for t in st.session_state.transactions if t["Type"] == "Deposit")
total_withdrawals = sum(t["Amount"] for t in st.session_state.transactions if t["Type"] == "Withdrawal")
total_transactions = len(st.session_state.transactions)

# 1. DASHBOARD
if page == "Dashboard":
    st.header("Account Dashboard")
    # KPI CARDS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Current Balance", f"₹ {st.session_state.balance:,}")
    with col2:
        st.metric("Total Deposits", f"₹ {total_deposits:,}")
    with col3:
        st.metric("Total Withdrawals", f"₹ {total_withdrawals:,}")
    with col4:
        st.metric("Transactions",total_transactions)
    st.divider()

    # ACCOUNT DETAILS
    st.subheader("Account Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
            **Account Holder:** Tarun Kaushal

            **Account Type:** Savings Account
   
            **Account Status:** Active""")
    with col2:
        if st.session_state.kyc_documents:
            st.success(f"KYC Status: Completed\n\n"
                f"Documents: {len(st.session_state.kyc_documents)}")
        else:
            st.warning("KYC Status: Not Completed")
    st.divider()

# 2. DEPOSIT
elif page == "Deposit":
    st.header("Deposit Money")
    st.write("Add money to your PNB savings account.")
    deposit_amount = st.number_input("Enter amount to deposit",min_value=0,step=100,key="deposit_amount")
    if st.button("Deposit Money",key="deposit_button"):
        if deposit_amount > 0:
            st.session_state.balance += deposit_amount
            st.session_state.transactions.append({"Type": "Deposit","Amount": deposit_amount,"Balance": st.session_state.balance})
            st.success(f"₹ {deposit_amount:,} deposited successfully.")
            st.info(f"New Balance: " f"₹ {st.session_state.balance:,}")
        else:
            st.error("Cannot deposit zero or negative amount.")

# 3. WITHDRAW
elif page == "Withdraw":
    st.header("Withdraw Money")
    st.write("Withdraw money from your PNB savings account.")
    withdraw_amount = st.number_input("Enter amount to withdraw", min_value=0, step=100, key="withdraw_amount")
    if st.button("Withdraw Money",key="withdraw_button"):
        if withdraw_amount <= 0:
            st.error("Cannot withdraw zero or negative amount.")
        elif withdraw_amount > st.session_state.balance:
            st.error("Insufficient balance.")
        else:
            st.session_state.balance -= withdraw_amount
            st.session_state.transactions.append({"Type": "Withdrawal", "Amount": withdraw_amount, "Balance": st.session_state.balance})
            st.success(f"₹ {withdraw_amount:,} withdrawn successfully.")
            st.info(f"Remaining Balance: " f"₹ {st.session_state.balance:,}")

# 4. KYC MANAGEMENT
elif page == "KYC Management":
    st.header("KYC Management")
    st.write("Manage your Know Your Customer documents.")
    col1, col2 = st.columns(2)
    with col1:
        document_type = st.selectbox("Document Type",
            ["Aadhaar",
            "PAN",
            "Passport",
            "Driving License"])
    with col2:
        document_number = st.text_input("Document Number")
    if st.button("Update KYC",key="kyc_button"):
        if document_number.strip():
            st.session_state.kyc_documents[document_type] = document_number.strip()
            st.success("KYC updated successfully.")
        else:
            st.error("Please enter document number.")
    st.divider()
    st.subheader("Submitted Documents")
    if st.session_state.kyc_documents:
        kyc_data = []
        for document, number in (st.session_state.kyc_documents.items()):
            kyc_data.append({"Document Type": document, "Document Number": number})
        kyc_df = pd.DataFrame(kyc_data)
        st.dataframe(kyc_df,use_container_width=True,hide_index=True)
    else:
        st.info("No KYC documents submitted.")

# 5. TRANSACTIONS
elif page == "Transactions":
    st.header("Transaction History")
    if st.session_state.transactions:
        df = pd.DataFrame(st.session_state.transactions)

        # FILTER
        transaction_filter = st.selectbox("Filter Transactions",
            ["All",
            "Deposit",
            "Withdrawal"])
        if transaction_filter != "All":
            filtered_df = df[df["Type"] == transaction_filter]
        else:
            filtered_df = df
        st.dataframe(filtered_df,use_container_width=True, hide_index=True)
    else:
        st.info("No transactions available.")

# 6. ACCOUNT DETAILS
elif page == "Account Details":
    st.header("Account Details")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Personal Information")
        st.write("**Account Holder:** Tarun Kaushal")
        st.write("**Account Type:** Savings Account")
        st.write("**Bank:** Punjab National Bank")
        st.write("**Account Status:** Active")
    with col2:
        st.subheader("Financial Information")
        st.write(f"**Current Balance:** "  f"₹ {st.session_state.balance:,.2f}")
        st.write(f"**Total Deposits:** "  f"₹ {total_deposits:,.2f}")
        st.write(f"**Total Withdrawals:** "  f"₹ {total_withdrawals:,.2f}")
        st.write(f"**Total Transactions:** "  f"{total_transactions}")

    st.divider()
    st.subheader("KYC Status")
    if st.session_state.kyc_documents:
        st.success("KYC Completed")
        for document, number in (st.session_state.kyc_documents.items()):
            st.write(f"**{document}:** {number}")
    else:
        st.warning("KYC has not been completed.")