# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
# Initialize FastAPI app
app = FastAPI()

# Pydantic model for request body
class VerifyRequest(BaseModel):
    name: str
    account_number: str

# Pydantic model for request body
class RequestName(BaseModel):
    name: str

# Pydantic model for response
class CustomerInfo(BaseModel):
    name: str
    account_number: str
    deductible_amount: float

# Sample insurance data
database = {
    "john doe": {
        "policy_number": "CAR123456",
        "contract_details": "This contract covers collision, comprehensive, and liability insurance. Roadside assistance is included. Deductible: $500. Coverage limit: $50,000 per accident.",
        "open_claims": [
            {
                "status": "In Progress",
                "date": date(2025, 3, 1),
                "repair_shop": "AutoFix Garage"
            },
            {
                "status": "Pending Approval",
                "date": date(2025, 2, 15),
                "repair_shop": "Speedy Repairs"
            }
        ]
    },
    "jane smith": {
        "policy_number": "CAR987654",
        "contract_details": "This contract covers liability and uninsured motorist protection. No collision or comprehensive coverage. Deductible: $1,000. Coverage limit: $25,000 per accident.",
        "open_claims": [
            {
                "status": "Under Review",
                "date": date(2025, 1, 28),
                "repair_shop": "Elite Auto Body"
            }
        ]
    },
    "robert brown": {
        "policy_number": "CAR567890",
        "contract_details": "Full coverage plan including collision, comprehensive, liability, and rental reimbursement. Deductible: $250. Coverage limit: $75,000 per accident.",
        "open_claims": []
    }
}
# Dummy data
class Customer:
    def __init__(self, name, account_number, deductible_amount):
        self.name = name
        self.account_number = account_number
        self.deductible_amount = deductible_amount

# Static data structure
customers = [
    Customer("john doe", "123456789", 500.0),
    Customer("jane doe", "987654321", 1000.0),
    Customer("bob smith", "111111111", 2000.0),
]


# Endpoint for verification
@app.post("/verify", response_model=CustomerInfo)
async def verify_customer(request: VerifyRequest):
    """
    Verify a customer by name and account number.

    Args:
    - request (VerifyRequest): Request body containing name and account number.

    Returns:
    - CustomerInfo: Customer information if verified, otherwise raises an exception.
    """
    req_name = request.name.lower()
    for customer in customers:
        if customer.name == req_name and customer.account_number == request.account_number:
            return CustomerInfo(
                name=customer.name,
                account_number=customer.account_number,
                deductible_amount=customer.deductible_amount,
            )
    raise HTTPException(status_code=404, detail="Customer not found")

@app.post("/customers")
async def get_customer_info(request: RequestName):
    print("printing")
    req_name = request.name.lower()
    person = database.get(req_name)
    if person:
        return {"name": req_name, "policy_number": person["policy_number"], "contract_details": person["contract_details"], "open_claims": person["open_claims"]}
    
    raise HTTPException(status_code=404, detail="Customer not found")



# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
