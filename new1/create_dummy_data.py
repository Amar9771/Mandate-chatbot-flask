from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Company, BWRClientData

engine = create_engine('sqlite:///company_data.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Add dummy company
company1 = Company(
    CompanyName='Acme Corporation',
    Address='123 Acme St, Metropolis',
    Email='info@acmecorp.com',
    Phone='+1234567890',
    Brief='A leading manufacturer of anvils and dynamite.'
)

# Add dummy BWR client data
bwr1 = BWRClientData(
    CompanyName='Acme Corporation',
    Escalation='No escalations reported.',
    Alerts='No alerts.',
    Issues='None',
    RationaleLink='http://example.com/rationale/acme',
    WDRequests='No withdrawal requests.',
    RatingHistory='AA stable for 5 years.'
)

session.add(company1)
session.add(bwr1)
session.commit()
print("Dummy data added!")
