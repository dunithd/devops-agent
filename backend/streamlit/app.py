import streamlit as st
import psycopg2
import pandas as pd

# Database connection parameters
DB_HOST = 'p-hjctr79xu3-a-rw-external-ea91f117847d15d5.elb.eu-west-2.amazonaws.com'
DB_NAME = 'workshop'
DB_USER = 'edb_admin'
DB_PASS = 'Spr!ng20232025'


# Connect to the PostgreSQL database
def get_messages():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
    query = "SELECT user_id, channel_id, message_text, timestamp FROM slack.messages"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit application
st.title('#operations Slack')

try:
    messages_df = get_messages()
    if not messages_df.empty:
        for index, row in messages_df.iterrows():
            st.write(f"**User:** {row['user_id']} | **Channel:** {row['channel_id']} | **Timestamp:** {row['timestamp']}")
            st.write(f"**Message:** {row['message_text']}")
            st.divider()
    else:
        st.write("No messages found.")
except Exception as e:
    st.error(f"Error fetching messages: {e}")