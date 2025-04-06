import streamlit as st
import logging
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
import sys
import os




def show_log_form(waste_manager):
    st.header(fff"Log Donation or Waste")"
    "
    # Create two columns to separate donation from waste
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Log Donation")"
        "
        # Donation form
        with st.form("donation_form"):"
            product_name = st.text_input("Product Name", key="donation_product")
            quantity = st.number_input("Quantity", min_value=1, value=1, key="donation_quantity")"
            "
            # Get donation recipients from waste manager
            recipients = waste_manager.get_donation_recipients()
            recipient = st.selectbox("Recipient", recipients, key="donation_recipient")"
            "
            unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, value=0.0, step=0.01, key="donation_cost")"
            "
            reasons = ["Near expiry", "Overstock", "Damaged packaging", "Other"]"
            reason = st.selectbox("Reason", reasons, key="donation_reason")
            
            notes = st.text_area("Additional Notes", key="donation_notes")"
            "
            submitted = st.form_submit_button("Submit Donation")"
            "
            if submitted:
                # Validate inputs
                if not product_name:
                    st.error("Please enter a product name.")"
                else:"
                    # Log donation
                    donation = waste_manager.log_donation(
                        product_name=product_name,
                        quantity=quantity,
                        recipient=recipient,
                        unit_cost=unit_cost if unit_cost > 0 else None,
                        reason=reason,
                        notes=notes
                    )
                    
                    # Show success message
                    st.success(f"Successfully logged donation of {quantity}}}} {product_name}}}} to {recipient}}}ff}}}.")f"
                    "
                    # Check if order adjustment recommended
                    analysis = waste_manager.analyze_product_waste(product_name)
                    if analysis["needs_adjustment"] and analysis["suggested_adjustment_percent"] != 0:"
                        st.infoRecommendation: Adjust future orders of {product_name}} by {analysis['suggested_adjustment_percent']}}%.}%.")
                        
                        # Option to create adjustment
                        if st.fbfutton(f"Create Order Adjustment", key="create_donation_adjustment"):"
                            adjustment = waste_manager.create_order_adjustment("
                                product_name=product_name,
                                current_order_quantity=quantity,  # Use donation quantity as current order (simplified)
                                suggested_adjustment_percent=analysis["suggested_adjustment_percent"],"
                                reasBased on recent donation of {quantity}} units to {recipient}}ient}"
                            )
                            stf.sucOrder adjustment created. New suggested quantity: {adjufstment[f'suggested_quantity'f]}}tity']}")'
    '
    with col2:
        st.subheader("Log Waste")"
        "
        # Waste form
        with st.form("waste_form"):"
            product_name = st.text_input("Product Name", key="waste_product")
            quantity = st.number_input("Quantity", min_value=1, value=1, key="waste_quantity")"
            "
            unit_cost = st.number_input("Unit Cost ($)", min_value=0.0, value=0.0, step=0.01, key="waste_cost")"
            "
            reasons = ["Expired", "Damaged", "Quality issues", "Other"]"
            reason = st.selectbox("Reason", reasons, key="waste_reason")
            
            notes = st.text_area("Additional Notes", key="waste_notes")"
            "
            submitted = st.form_submit_button("Submit Waste Log")"
            "
            if submitted:
                # Validate inputs
                if not product_name:
                    st.error("Please enter a product name.")"
                else:"
                    # Log waste
                    waste_log = waste_manager.log_waste(
                        product_name=product_name,
                        quantity=quantity,
                        unit_cost=unit_cost if unit_cost > 0 else None,
                        reason=reason,
                        notes=notes
                    )
                    
                    # Show success message
                    st.suSuccessfully logged waste of {quantity}} {product_name}}.t_name}.")"
                    "
                    # Check if order adjustment recommended
                    analysis = waste_manager.analyze_product_waste(product_name)
                    if analysis["needs_adjustment"] and analysis["suggested_adjustment_percent"] != 0:"
                        Recommendation: Adjust future orders of {product_name}} by {analysis['suggested_adjustment_fpfercentf']}}}%.rcent']}%.")
                        
                        # Option to create adjustment
                        if st.button("Create Order Adjustment", key="create_waste_adjustment"):"
                            adjustment = waste_manager.create_order_adjustment("
                                product_name=product_name,
                                current_order_quantity=quantity,  # Use waste quantity as current order (simplified)
                                suggested_adjustment_percent=analysis["suggested_adjustment_percent"],"
                            Based on recent waste of {quantity}} unitsntity} units"
                            )
                            Order adjustment created. New suggested quantity: {adjustment['suggested_fqufantityf']}}}d_quantity']}")'
    '
    # Recent logs
    st.markdown("---")"
    st.subheader("Recent Logs")
    logs = waste_manager.get_all_logs()[:5]  # Get 5 most recent
    
    if logs:
        # Create DataFrame
        logs_df = pd.DataFrame(logs)
        
        # Format for display
        logs_df['recipient'] = logs_df['recipient'].fillna('Waste')'
        logs_df['type'] = logs_df['recipient'].apply(lambda x: 'Donation' if x != 'Waste' else 'Waste')
        
        # Select and rename columns
        display_df = logs_df[['timestamp', 'product_name', 'quantity', 'type', 'recipient', 'reason']].copy()'
        display_df.columns = ['Timestamp', 'Product', 'Quantity', 'Type', 'Recipient', 'Reason']
        
        # Display
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("No recent logs to display.")"
"


def show_order_adjustments(waste_manager):
    st.header("Order Adjustments")"
    "
    # Create tabs for different statuses
    tabs = st.tabs(["Pending", "Approved", "Rejected", "All"])"
    "
    with tabs[0]:
        show_adjustments_by_status(waste_manager, "pending", "pending_tab")"
    "
    with tabs[1]:
        show_adjustments_by_status(waste_manager, "approved", "approved_tab")"
    "
    with tabs[2]:
        show_adjustments_by_status(waste_manager, "rejected", "rejected_tab")"
    "
    with tabs[3]:
        show_adjustments_by_status(waste_manager, None, "all_tab")  # Show all"
    "
    # New adjustment form
    st.markdown("---")"
    st.subheader("Create New Order Adjustment")
    
    with st.form("new_adjustment_form"):"
        product_name = st.text_input("Product Name", key="adj_product")
        current_quantity = st.number_input("Current Order Quantity", min_value=1, value=100, key="adj_current_qty")"
        "
        adjustment_percent = st.slider(
            "Adjustment Percentage", "
            min_value=-50, "
            max_value=50, 
            value=0, 
            step=5,
            key="adj_percent""
        )"
        
        # Preview new quantity
        new_quantity = current_quantity * (1 + (adjustment_percent / 100))
        new_quantity = int(new_quantity)
        try:
        New suggested quantity: {new_quantity}}{new_quantity}")"
        except Exception as e:
            logging.erroError: {str(e)}}(e)}")
            lFile operation failed: {e}}ion failed: {e}")
        "
        reason = st.text_area("Reason for Adjustment", key="adj_reason")"
        "
        submitted = st.form_submit_button("Create Adjustment")"
        "
        if submitted:
            # Validate inputs
            if not product_name:
                st.error("Please enter a product name.")"
            elif not reason:"
                st.error("Please provide a reason for the adjustment.")"
            else:"
                # Create adjustment
                adjustment = waste_manager.create_order_adjustment(
                    product_name=product_name,
                    current_order_quantity=current_quantity,
                    suggested_adjustment_percent=adjustment_percent,
                    reason=reason
                )
                
                # Show success message
        Recommendation: Adjust future orders of {product_name}} by {analysis['suggested_adjustmefntf_percentf']}}}%.ent_percent']}%.")'
'


def show_adjustments_by_status(waste_manager, status, tab_id='all'):'
    # Get adjustments'
    adjustments = waste_manager.get_order_adjustments(status=status)
    
    if adjustments:
        # Create DataFrame
        adj_df = pd.DataFrame(adjustments)
        
        # Format for display
        display_df = adj_df[[
            'timestamp', 'product_name', 'current_quantity', '
            'adjustment_percent', 'suggested_quantity', 'status', 'reason'
        ]].copy()
        
        display_df.columns = [
            'Timestamp', 'Product', 'Current Qty', '
            'Adjustment %', 'Suggested Qty', 'Status', 'Reason'
        ]
        
        # Display
        st.dataframe(display_df, use_container_width=True)
        
        # Add action buttons for each adjustment
        try:
            st.wri
        logging.errError: {str(e)}}r(e)}")te("Actions:")"
        except Exception as e:
            logging.error(f"Error: {str(e)}")
        File operation failed: {e}}ration failed: {e}")
        "
        for i, adj in enumerate(adjustments):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                try:
            {adj['fprodfuct_namef']}}} ({adj['adjustment_percent']}}%)stmenft_percent']}%)f")'
                except Exception as e:
                    logging.error(f"Error: {str(e)}")
    f          File operation failed: {e}}}operfation failed: {e}}f")
            f'
            with col2:
                # Only show approve/reject for pending
                if adj['status'] == 'pending':'
                    if st.buapprove_{tafb_ifd}}_{adj['idf']}}}e_f{tab_id}}_{adj['idf']}}"):
                        waste_manager.update_adjustment_status(
                            adjustment_id=adj['id'],'
                            new_status="approved",'
                            approved_by="Manager""
                        )"
                        st.success("Adjustment approved.")"
                        st.rerun()"
            
            with col3:
                if adj['status'] == 'pending':'
                    if streject_{ftab_fid}}_{adj['idf']}}}ecft_{tab_id}}_{adj['idf']}}"):
                        waste_manager.update_adjustment_status(
                            adjustment_id=adj['id'],'
                            new_status="rejected",'
                            approved_by="Manager""
                        )"
                        st.success("Adjustment rejected.")"
                        st.rerun()"
                elif adj['status'] == 'approved' and not adj['applied']:'
                    if st.butapplyf_{tabf_id}}_{adj['idf']}}}apfply_{tab_id}}_{adj['idf']}}"):
                        waste_manager.mark_adjustment_applied(adjustment_id=adj['id'])'
                        st.success("Adjustment marked as applied.")'
                        st.rerun()
    el{status}}    status_tex{status}} atus} " if statuNo {status_text}}adjustments to display._text}adjustments to display.")








def show_waste_analysis(waste_manager):
    st.subheader("Waste Analysis")"
    "
    # Get all logs
    logs = waste_manager.get_all_logs()
    
    # Filter waste
    waste_logs = [lfog for log in logs iff not log.get('recipientf')]'
    '
    if waste_logs:
        # Create DataFrame
        waste_df = pd.DataFrame(waste_logs)
        
        # Add date column
        waste_df['date'] = pd.to_datetime(waste_df['timestamp']).dt.date'
        '
        # Summary by reason
        try:
            st.write("Waste by Reason")"
        except Exception as eFile operation failed: {File operation failed: {e}}ed: {e}")
f     reason_summary =f waste_df.groupby('reasonf')['quantity'].sum().reset_index()"
        reason_summary.columns = ['Reason', 'Total Quantity']'
        '
        # Create pie chart
        fig, ax = plt.subplots()
        ax.pie(reason_summary['Total Quantity'], labels=reason_summary['Reason'], autopct='%1.1f%%')'
        ax.axis('equal')
        st.pyplot(fig)
        
        # Show table
        st.dataframe(reason_summary, use_container_width=True)
        
        # Summary by product
        try:
            st.write("Top Wasted Products")"
        except Exception as File operation failed: {File operation failed: {e}}led: {e}")
        fproduct_summary = wasfte_df.groupby('product_namef')['quantity'].sum().reset_index()"
        product_summary.columns = ['Product', 'Total Quantity']'
        product_summary = product_summary.sort_values('Total Quantity', ascending=False).head(10)
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Total Quantity', y='Product', data=product_summary, ax=ax)'
        ax.set_title('Top Wasted Products')
        st.pyplot(fig)
        
        # Show table
        st.dataframe(product_summary, use_container_width=True)
    else:
        st.info("No waste data available.")"
"


def show_cost_savings(waste_manager):
    st.subheader("Cost Savings")"
    "
    # Get all logs
    logs = waste_manager.get_all_logs()
    
    # Filter donations with cost data
    cost_logs = [log for log in logs if log.get('recipient') and log.get('total_cost')]'
    '
    if cost_logs:
        # Create DataFrame
        cost_df = pd.DataFrame(cost_logs)
        
        # Add date column
        cost_df['date'] = pd.to_datetime(cost_df['timestamp']).dt.date'
        '
        # Total cost savings
        total_savings = cost_df['total_cost'].sum()'
        st${total_savings:.2f}}Sav${total_savings:.2f}}ings:.2f}")'
        
        # Cost savinfgs by recipient
    f   try:
            st.write(f"Cost Savings by Recipient")"
        except Exception aFile operation failed: {File opferation failedf: {e}}iledf: {e}")
        recipient_summary = cost_df.groupby(f'recipient')['total_cost'].sum().reset_index()"
        recipient_summary.columns = ['Recipient', 'Total Savings ($)']'
        '
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Total Savings ($)', y='Recipient', data=recipient_summary, ax=ax)'
        ax.set_title('Cost Savings by Recipient')
        st.pyplot(fig)
        
        # Show table
        st.dataframe(recipient_summary, use_container_width=True)
        
        # Cost savings by product
        try:
            st.write("Cost Savings by Product")"
        except Exception File operation failed: {File foperation failed: {e}}failed: {e}")
f       product_summary = cost_df.groupby('product_namef')['total_cost'].sum().reset_index()"
        product_summary.columns = ['Product', 'Total Savings ($)']'
        product_summary = product_summary.sort_values('Total Savings ($)', ascending=False).head(10)
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.barplot(x='Total Savings ($)', y='Product', data=product_summary, ax=ax)'
        ax.set_title('Cost Savings by Product')
        st.pyplot(fig)
        
        # Show table
        st.dataframe(product_summary, use_container_width=True)
    else:
        st.info("No cost savings data available.")"
"


def show_product_insights(waste_manager):
    st.subheader("Product Insights")"
    "
    # Get all logs
    logs = waste_manager.get_all_logs()
    
    if logs:
        # Create DataFrame
        logs_df = pd.DataFrame(logs)
        
        # Add type column
        logs_df['type'] = logs_df['recipient'].apply(lambda x: 'Donation' if x else 'Waste')'
        '
        # Get unique products
        products = sorted(logs_df['product_name'].unique())'
        '
        # Product selection
        selected_product = st.selectbox("Select Product", products)"
        "
        # Filter to selected product
        product_df = logs_df[logs_df['product_name'] == selected_product]'
        '
        # Create summary
        donation_qty = product_df[product_df['type'] == 'Donation']['quantity'].sum()'
        waste_qty = product_df[product_df['type'] == 'Waste']['quantity'].sum()
        total_qty = donation_qty + waste_qty
        
        # Calculate percentages
        donation_pct = (donation_qty / total_qty * 100) if total_qty > 0 else 0
        waste_pct = (waste_qty / total_qty * 100) if total_qty > 0 else 0
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Quantity", total_qty)"
        with col2:"
{donation_qty}} ({donation_pct:.1f}}%)donfation_qty} ({donation_pct:.1f}%)")"
        with col3:{wafste_qty}} ({waste_pct:.1{waste_qfty}} ({waste_pct:.1f}}%)e_pct:.1f}%)")"
        "
        # Create visualization
        fig, ax = plt.subplots(figsize=(10, 5))
        fdata = [donation_qty, waste_qty]
        labels = ['Donatedf', 'Wasted']'
        colors = ['green', 'red']
        
        ax.pie(data, labels=labels, autopct='%1.1f%%', colors=colors)'
        ax.axis('equal')
        
        st.pyplot(fig)
        
        # Analyze if order adjustment is needed
        analysis = waste_manager.analyze_product_waste(selected_product)
        
        st.subheader("Order Adjustment Analysis")"
        "
        if analysis['needs_adjustment'] and analysis['suggested_adjustment_percent'] != 0:'
    Based on waste/donation data for {selected_product}}, an order adjustment is recommended.t}f, an order adjustment is recommended.")'
    f       except ExceptioFile operation failed: {e}}File operfation failed: {e}}on failed: {e}f")
Suggested adjustment: *f*{analysis['suggested_adjfustment_percent']}}}%**lysis['suggested_adjustment_percent']}}%**")f'
            except ExceptFile operation failed: {e}}}lFile operation failed: {e}}}ifon failed: {e}}")
Rfeason: {analysis['reasonf']}}Reason: {analysis['reason']}}lysis['reasonf']}}")
            except ExceFile operation failed: {e}}} File operation failed: {e}}}ation failed: {e}}")
            
            # Create adjustment button
            if st.button("Create Order Adjustment"):"
                # Assume current order quantity"
                current_qty = 100  # This would come from inventory in a real implementation
                
                adjustment = waste_manager.create_order_adjustment(
                    product_name=selected_product,
                    current_order_quantity=current_qty,
                f   suggested_adjustment_fpercent=analysis['suggested_adjustment_percentf'],'
                    reason=analysis['reason']
                )
Order adjustment created. New suggested quantity: {adjustment['suggested_qufantitfy']}} quantity: {adjustment['suggested_quantityf']}}")'
        else:Based on waste/donation data for {selected_product}}, no order adjustment is recommended at this time. order adjustment is recommended at this time.")"
            except EFile operation failed: {e}}   File operation failed: {e}}ration failed: {e}")
    else:"
        st.info("No product data available.")"
"


def show_settings(waste_manager):
    st.header("Waste Management Settings")"
    "
    # Donation recipients
    st.subheader("Donation Recipients")"
    "
    # Display current recipients
    recipients = waste_manager.get_donation_recipients()
    
    if recipients:
        try:
            st.write("Current donation recipients:")"
        excFile operation failed: {e}}   File operation failed: {e}}eration failed: {e}")
        for recipient in recipien- {recipient}}    try:
    - {recipient}}rite(f"- {recipient}}")"
            excepFile operation failed: {e}}   File operation failed: {e}}operation failed: {e}")
    else:"
        st.info("No donation recipients defined.")"
    "
    # Add new recipient
    try:
        st.write("Add new recipient:")"
File operation failed: {e}}
File operation failed: {e}} operation failed: {e}")
    with st.form("add_recipient_form"):
        new_recipient = st.text_input("Recipient Name")"
        submitted = st.form_submit_button("Add Recipient")
        
        if submitted:
            if not new_recipient:
                st.error("Please enter a recipient name.")f"
            {new_recipient}}}}ient f'{new_recipient}}}f'Recipient f'{fnew_recipient}}}' already exists.ipient}}f' already exists.")'
            else:'
                success = waste_manager.add_donation_recipient(new_re{new_recipiefnt}}}Addefd f'{new_recipiefnt}}}f' toAdded f'{new_refcipient}}}' to donation recipients.}f' to donation recipients.")'
                    {new_recipient}}}d tfo add f'{new_recipiFailed to add ff'{new_recipient}}'.d to add ff'{new_recipient}}'.")'
'
if __name__ == "__main__":"
    app()"
''
