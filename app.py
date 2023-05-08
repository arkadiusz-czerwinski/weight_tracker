
import streamlit as st
import time
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def delete_all_weights():
    session.query(Weight).delete()
    session.commit()



# Create the SQLAlchemy engine and session
engine = create_engine('sqlite:///weight-tracker.db')
Session = sessionmaker(bind=engine)
session = Session()

# Define the SQLAlchemy model for the weights table
Base = declarative_base()
class Weight(Base):
    __tablename__ = 'weights'

    id = Column(Integer, primary_key=True)
    weight = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)

# Create the weights table if it doesn't exist
Base.metadata.create_all(engine)

# Define the Streamlit app
st.title('Weight Tracker')

if st.button('Delete all weights'):
    delete_all_weights()
    st.write('All weight records have been deleted.')


weight = st.number_input('Enter your weight in kg:')
if st.button('Save'):
    timestamp = int(time.time())
    weight_record = Weight(weight=weight, timestamp=timestamp)
    session.add(weight_record)
    session.commit()
    st.success('Weight record saved!')

weights = session.query(Weight).all()
if weights:
    df = pd.DataFrame([(datetime.fromtimestamp(weight.timestamp), weight.weight) for weight in weights],
                      columns=['timestamp', 'weight'])
    fig = go.Figure(data=go.Scatter(x=df['timestamp'], y=df['weight']))
    fig.update_layout(
        title='Weight over time',
        xaxis_title='Date',
        yaxis_title='Weight (kg)',
        width=800,
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write('No weight records found.')
